package com.vertex.documentos;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "documentos_financeiros")
public class DocumentoFinanceiro {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 300)
    private String fornecedor;

    private Double valorTotal;

    @Column(length = 10)
    private String dataVencimento;

    @Column(length = 100)
    private String codigoBarras;

    @Column(length = 120)
    private String categoriaSugerida;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private StatusDocumento status;

    @Column(nullable = false)
    private LocalDateTime dataCadastro;

    protected DocumentoFinanceiro() {
    }

    public DocumentoFinanceiro(DadosBoletoExtraido dados) {
        fornecedor = dados.fornecedor();
        valorTotal = dados.valorTotal();
        dataVencimento = dados.dataVencimento();
        codigoBarras = dados.codigoBarras();
        categoriaSugerida = dados.categoriaSugerida();
        status = StatusDocumento.PENDENTE;
    }

    @PrePersist
    void prepararCadastro() {
        if (dataCadastro == null) {
            dataCadastro = LocalDateTime.now();
        }
        if (status == null) {
            status = StatusDocumento.PENDENTE;
        }
    }

    public Long getId() {
        return id;
    }

    public String getFornecedor() {
        return fornecedor;
    }

    public Double getValorTotal() {
        return valorTotal;
    }

    public String getDataVencimento() {
        return dataVencimento;
    }

    public String getCodigoBarras() {
        return codigoBarras;
    }

    public String getCategoriaSugerida() {
        return categoriaSugerida;
    }

    public StatusDocumento getStatus() {
        return status;
    }

    public LocalDateTime getDataCadastro() {
        return dataCadastro;
    }
}