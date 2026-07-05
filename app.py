import streamlit as st
from src.extration import extration 
from src.analise_dados import analise
import plotly.express as px

st.set_page_config('Vertex', layout='wide')
st.markdown(
    """
    <style>
    /* Fundo do app e cor do texto principal */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Força os cabeçalhos e textos comuns a ficarem legíveis */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #FAFAFA !important;
    }
    
    /* CORREÇÃO DO UPLOADER: Ajusta a caixa de arrastar arquivo */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #161B22 !important;
        border: 1px dashed #30363D !important;
    }
    
    /* CORREÇÃO DO BOTÃO: Ajusta o texto de dentro do botão "Upload" */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #21262D !important;
        color: #FAFAFA !important;
        border: 1px solid #30363D !important;
    }

    /* Ajusta a cor do texto secundário (ex: "200MB per file") */
    [data-testid="stFileUploaderDropzone"] section {
        color: #8B949E !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title('Painel de Controle Vertex')
st.markdown('**A melhor e mais eficiente ferramenta financeira do ramo alimentício dentro do ifood.**')

# ---------- RECEBIMENTO DO RELATÓRIO -------
st.markdown('---')

area_upload = st.empty()
with area_upload.container():
    st.subheader('Para que a ferramenta funcione perfeitamente, primeiro coloque o seu relatório do iFood.')
    file = st.file_uploader('SUBA O ARQUIVO AQUI', type = ['xlsx'])
if file is not None:
    area_upload.empty()
    df_bruto = extration(file)
    st.success('Arquivo carregado com sucesso!')
    df, faturamento_bruto, faturamento_liquido, taxas, pagamento, ticket_medio, porcentagem_taxas, hora_pico, qtd_pico, tempo_medio_entrega, tempo_medio_entregador, distancia_media, km_total, df_linha, df_cancelados = analise(df_bruto)

    # -------- FATURAMENTO E TAXAS ----------
    st.title('Faturamento e Taxas')
    st.subheader('Nesta aba é mostrado o quanto foi FATURADO e pago em TAXAS')

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label = 'Faturamento Bruto', value = f'R${faturamento_bruto}')
    with col2:
        st.metric(label = 'Faturamento Líquido', value = f'R${faturamento_liquido}')

    st.subheader('Volume de Vendas')
    fig_linha = px.line(
        df_linha,
        x = 'Dia',
        y = 'Faturamento Bruto (R$)',
        markers = True
    )
    fig_linha.update_traces(line=dict(color='#FF4B4B', width=3), line_shape='spline')
    fig_linha.update_layout(template='plotly_dark')
    st.plotly_chart(fig_linha, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label = 'Porcentagem pago em taxas', value =f'{porcentagem_taxas:.2f}%')

    with col2:
        st.metric(label = 'Ticket Médio', value = f'R${ticket_medio:.2f}')

    with col3:
        st.metric(label = 'Total Pago em Taxas', value = f'R${taxas}')

    
    # -------- MÉTRICAS ATÉ A ENTREGA --------
    st.markdown('---')
    st.title('**Tempo de Operação**')
    st.subheader('Nesta aba é mostrado o tempo MÉDIO levado para finalizar cada operação')

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label = 'Tempo médio de entrega até cliente', value = f'{tempo_medio_entrega:.2f}')
    with col2:
        st.metric(label = 'Tempo médio do entregador ir até o cliente', value = f'{tempo_medio_entregador:.2f}')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label = 'Distância média percorrida', value = f'{distancia_media:.2f}')
    with col2:
        st.metric(label = 'Quilometragem Geral rodada (KM)', value = f'{km_total:.2f}')

    st.metric(label="Horário de Maior Movimento", value=f"{hora_pico}h", delta=f"{qtd_pico} pedidos")


    # -------- CANCELAMENTOS ---------
    if len(df_cancelados) > 0:
        df_motivos = df_cancelados['MOTIVO DO CANCELAMENTO'].value_counts().reset_index()
        df_motivos.columns = ['Motivo', 'Quantidade']
        
        fig_cancelamento = px.bar(
            df_motivos, x='Quantidade', y='Motivo', orientation='h',
            color='Quantidade', color_continuous_scale='Reds'
        )
        fig_cancelamento.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_dark")
        st.plotly_chart(fig_cancelamento, use_container_width=True)
    else:
        st.info("Nenhum cancelamento registrado neste intervalo de tempo.")
else:
    st.info('Por favor, faça o upload do arquivo Excel.')