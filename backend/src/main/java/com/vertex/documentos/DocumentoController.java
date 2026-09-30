package com.vertex.documentos;

import java.io.IOException;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/documentos")
public class DocumentoController {
    private final VertexAiService vertexAiService;
    private final DocumentoFinanceiroRepository repository;

    public DocumentoController(VertexAiService vertexAiService, DocumentoFinanceiroRepository repository) {
        this.vertexAiService = vertexAiService;
        this.repository = repository;
    }

    @PostMapping(path = "/analisar", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DocumentoFinanceiro> analisar(@RequestParam("file") MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Envie um arquivo não vazio no campo 'file'.");
        }
        String mimeType = file.getContentType();
        if (mimeType == null || !List.of("image/jpeg", "image/png", "application/pdf").contains(mimeType)) {
            throw new ResponseStatusException(HttpStatus.UNSUPPORTED_MEDIA_TYPE, "Formato não suportado. Envie JPEG, PNG ou PDF.");
        }

        DadosBoletoExtraido dados = vertexAiService.extrairDados(file.getBytes(), mimeType);
        DocumentoFinanceiro documento = new DocumentoFinanceiro(dados);
        return ResponseEntity.ok(repository.save(documento));
    }
}