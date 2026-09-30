package com.vertex.documentos;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.auth.oauth2.GoogleCredentials;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class VertexAiService {
    private static final String SYSTEM_PROMPT = "Você é um assistente de contabilidade especialista em extração de dados financeiros de pequenos comércios. Analise a imagem fornecida. Extraia os dados e retorne APENAS um objeto JSON válido (sem blocos de código markdown adicionais como ```json, apenas o texto JSON cru) correspondendo exatamente a estas chaves: fornecedor, valorTotal (numérico), dataVencimento (YYYY-MM-DD), codigoBarras e categoriaSugerida. Se algum campo não estiver legível, retorne null.";
    private static final String CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform";

    private final ObjectMapper objectMapper;
    private final HttpClient httpClient;
    private final String projectId;
    private final String location;
    private final String model;
    private GoogleCredentials credentials;

    public VertexAiService(
            ObjectMapper objectMapper,
            @Value("${google.cloud.project-id:}") String projectId,
            @Value("${google.cloud.location:us-central1}") String location,
            @Value("${google.cloud.vertex-model:gemini-2.5-flash}") String model
    ) {
        this.objectMapper = objectMapper;
        this.projectId = projectId;
        this.location = location;
        this.model = model;
        this.httpClient = HttpClient.newHttpClient();
    }

    public DadosBoletoExtraido extrairDados(byte[] arquivo, String mimeType) {
        if (arquivo == null || arquivo.length == 0) {
            throw new IllegalArgumentException("O arquivo enviado está vazio.");
        }
        if (mimeType == null || !List.of("image/jpeg", "image/png", "application/pdf").contains(mimeType)) {
            throw new IllegalArgumentException("Formato não suportado. Envie JPEG, PNG ou PDF.");
        }
        if (projectId.isBlank()) {
            throw new IllegalStateException("Configure GOOGLE_CLOUD_PROJECT para usar o Vertex AI.");
        }

        try {
            String accessToken = obterAccessToken();
            Map<String, Object> requestBody = Map.of(
                    "systemInstruction", Map.of("parts", List.of(Map.of("text", SYSTEM_PROMPT))),
                    "contents", List.of(Map.of("role", "user", "parts", List.of(
                            Map.of("text", "Analise o documento financeiro anexado."),
                            Map.of("inlineData", Map.of(
                                    "mimeType", mimeType,
                                    "data", Base64.getEncoder().encodeToString(arquivo)
                            ))
                    ))),
                    "generationConfig", Map.of("responseMimeType", "application/json")
            );

            String endpoint = "https://aiplatform.googleapis.com/v1/projects/%s/locations/%s/publishers/google/models/%s:generateContent"
                    .formatted(projectId, location, model);
            HttpRequest request = HttpRequest.newBuilder(URI.create(endpoint))
                    .header("Authorization", "Bearer " + accessToken)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(requestBody)))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() < 200 || response.statusCode() >= 300) {
                throw new IllegalStateException("Vertex AI respondeu com HTTP " + response.statusCode() + ".");
            }

            JsonNode payload = objectMapper.readTree(response.body());
            String jsonExtraido = payload.path("candidates").path(0).path("content").path("parts").path(0).path("text").asText();
            if (jsonExtraido.isBlank()) {
                throw new IllegalStateException("Vertex AI não retornou dados extraídos.");
            }
            return objectMapper.readValue(removerCercaMarkdown(jsonExtraido), DadosBoletoExtraido.class);
        } catch (IOException e) {
            throw new IllegalStateException("Falha ao comunicar ou interpretar a resposta do Vertex AI.", e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("A chamada ao Vertex AI foi interrompida.", e);
        }
    }

    private synchronized String obterAccessToken() throws IOException {
        if (credentials == null) {
            credentials = GoogleCredentials.getApplicationDefault().createScoped(CLOUD_PLATFORM_SCOPE);
        }
        credentials.refreshIfExpired();
        return credentials.getAccessToken().getTokenValue();
    }

    private String removerCercaMarkdown(String texto) {
        String json = texto.trim();
        if (json.startsWith("```")) {
            int inicioConteudo = json.indexOf('\n');
            int fimConteudo = json.lastIndexOf("```");
            if (inicioConteudo >= 0 && fimConteudo > inicioConteudo) {
                json = json.substring(inicioConteudo + 1, fimConteudo).trim();
            }
        }
        return json;
    }
}