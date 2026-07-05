import pandas as pd
from src.cleaning import cleaning

def analise(df_bruto):
    df = cleaning(df_bruto)
    
    # Cancelamentos
    df_cancelados = df[df['STATUS FINAL DO PEDIDO'].str.upper().str.contains('CANCELADO', na=False)]

    # Faturamento Bruto
    df['TOTAL PAGO PELO CLIENTE (R$)'] = pd.to_numeric(df['TOTAL PAGO PELO CLIENTE (R$)'])
    faturamento_bruto = df['TOTAL PAGO PELO CLIENTE (R$)'].sum()
    
    # Gráfico de linha do faturamento
    df['DATA_DIA'] = df['DATA E HORA DO PEDIDO'].dt.date
    df_linha = df.groupby('DATA_DIA')['TOTAL PAGO PELO CLIENTE (R$)'].sum().reset_index()
    df_linha.columns = ['Dia', 'Faturamento Bruto (R$)']
    df_linha = df_linha.sort_values('Dia')

    # Faturamento líquido
    df['VALOR LIQUIDO (R$)'] = pd.to_numeric(df['VALOR LIQUIDO (R$)'])
    faturamento_liquido = df['VALOR LIQUIDO (R$)'].sum()

    # Valor pago em taxas
    df['TAXAS E COMISSOES (R$)'] = pd.to_numeric(df['TAXAS E COMISSOES (R$)'])
    taxas = df['TAXAS E COMISSOES (R$)'].sum()

    # Formas de pagamento 
    pagamento = df['FORMA DE PAGAMENTO'].value_counts()

    # Ticket médio
    df['VALOR DOS ITENS (R$)'] = pd.to_numeric(df['VALOR DOS ITENS (R$)'])
    ticket_medio = df['VALOR DOS ITENS (R$)'].mean()

    # Porcentagem pago em taxas
    porcentagem_taxas = (taxas / faturamento_bruto) * 100

    # Tempo de entrega até o cliente 
    df['TEMPO DA ENTREGA REALIZADA (MIN)'] = pd.to_numeric(df['TEMPO DA ENTREGA REALIZADA (MIN)'])
    tempo_medio_entrega = df['TEMPO DA ENTREGA REALIZADA (MIN)'].mean()

    # Tempo do entregdor ir até o cliente
    df['TEMPO DO ENTREGADOR À CAMINHO DO CLIENTE (MIN)'] = pd.to_numeric(df['TEMPO DO ENTREGADOR À CAMINHO DO CLIENTE (MIN)'])
    tempo_medio_entregador = df['TEMPO DO ENTREGADOR À CAMINHO DO CLIENTE (MIN)'].mean()
    
    # Média de distância percorrida
    df['DISTÂNCIA PERCORRIDA ATÉ O CLIENTE (KM)'] = pd.to_numeric(df['DISTÂNCIA PERCORRIDA ATÉ O CLIENTE (KM)'])
    distancia_media = df['DISTÂNCIA PERCORRIDA ATÉ O CLIENTE (KM)'].mean()

    # Quilometragem geral rodada
    km_total = df['DISTÂNCIA PERCORRIDA ATÉ O CLIENTE (KM)'].sum()

    # Horário de pico
    df['HORA'] = df['DATA E HORA DO PEDIDO'].dt.hour
    picos_pedidos = df.groupby('HORA')['STATUS FINAL DO PEDIDO'].count().reset_index()
    picos_pedidos = picos_pedidos.rename(columns={'STATUS FINAL DO PEDIDO': 'QUANTIDADE_PEDIDOS'})
    picos_ordenados = picos_pedidos.sort_values(by='QUANTIDADE_PEDIDOS', ascending=False)

    hora_pico = picos_ordenados.iloc[0]['HORA']
    qtd_pico = picos_ordenados.iloc[0]['QUANTIDADE_PEDIDOS']    


    return df, faturamento_bruto, faturamento_liquido, taxas, pagamento, ticket_medio, porcentagem_taxas, hora_pico, qtd_pico, tempo_medio_entrega, tempo_medio_entregador, distancia_media, km_total, df_linha, df_cancelados