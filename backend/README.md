# Vertex Backend

Backend Spring Boot para análise multimodal de documentos financeiros e persistência relacional.

## Pré-requisitos

- Java 17 ou superior
- Maven 3.9 ou superior
- Projeto Google Cloud com Vertex AI API habilitada
- Credenciais Application Default configuradas

No PowerShell, configure a chave de serviço e o projeto antes de iniciar:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\caminho\service-account.json"
$env:GOOGLE_CLOUD_PROJECT = "seu-projeto-gcp"
mvn spring-boot:run
```

As credenciais também podem ser configuradas por `gcloud auth application-default login`. A localização padrão é `us-central1` e o modelo padrão é `gemini-2.5-flash`; ambos podem ser alterados por `GOOGLE_CLOUD_LOCATION` e `VERTEX_AI_MODEL`.

O banco H2 em arquivo é usado por padrão para desenvolvimento. Para PostgreSQL, defina `DB_URL`, `DB_USERNAME` e `DB_PASSWORD`, por exemplo `jdbc:postgresql://localhost:5432/vertex`.

## Endpoint

`POST /api/documentos/analisar` recebe `multipart/form-data` com o campo `file` em JPEG, PNG ou PDF. A resposta contém os campos extraídos, o status inicial `PENDENTE` e a data de cadastro.