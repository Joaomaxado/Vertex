package com.vertex.documentos;

public record DadosBoletoExtraido(
        String fornecedor,
        Double valorTotal,
        String dataVencimento,
        String codigoBarras,
        String categoriaSugerida
) {
}