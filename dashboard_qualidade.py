import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Qualidade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Dashboard de Qualidade")
st.markdown("---")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('qualidade_database.csv', encoding='utf-8')
    except:
        df = pd.read_csv('qualidade_database.csv', encoding='latin-1')
    
    # Converter data para datetime
    df['data_auditoria'] = pd.to_datetime(df['data_auditoria'])
    
    return df

df = load_data()

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# Filtro de data
min_date = df['data_auditoria'].min()
max_date = df['data_auditoria'].max()

date_range = st.sidebar.date_input(
    "Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtro de tipo de auditoria
tipos_auditoria = ['Todos'] + sorted(df['tipo_auditoria'].unique().tolist())
tipo_selecionado = st.sidebar.selectbox("Tipo de Auditoria", tipos_auditoria)

# Filtro de projeto
projetos = ['Todos'] + sorted(df['nome_projeto'].dropna().unique().tolist())
projeto_selecionado = st.sidebar.selectbox("Projeto", projetos)

# Aplicar filtros
df_filtered = df.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['data_auditoria'].dt.date >= date_range[0]) &
        (df_filtered['data_auditoria'].dt.date <= date_range[1])
    ]

if tipo_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['tipo_auditoria'] == tipo_selecionado]

if projeto_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['nome_projeto'] == projeto_selecionado]

# KPIs principais
st.header("📈 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_auditorias = len(df_filtered)
    st.metric(
        label="Total de Auditorias",
        value=total_auditorias,
        delta=None
    )

with col2:
    conformes = len(df_filtered[df_filtered['resultado_texto'] == 'Conforme'])
    taxa_conformidade = (conformes / total_auditorias * 100) if total_auditorias > 0 else 0
    st.metric(
        label="Taxa de Conformidade",
        value=f"{taxa_conformidade:.1f}%",
        delta=None
    )

with col3:
    nps_data = df_filtered[df_filtered['tipo_auditoria'] == 'NPS']
    media_nps = nps_data['resultado_valor'].mean() if len(nps_data) > 0 else 0
    st.metric(
        label="NPS Médio",
        value=f"{media_nps:.1f}",
        delta=None
    )

with col4:
    projetos_auditados = df_filtered['nome_projeto'].dropna().nunique()
    st.metric(
        label="Projetos Auditados",
        value=projetos_auditados,
        delta=None
    )

st.markdown("---")

# Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Distribuição por Tipo de Auditoria")
    
    tipo_counts = df_filtered['tipo_auditoria'].value_counts()
    
    fig_tipo = px.pie(
        values=tipo_counts.values,
        names=tipo_counts.index,
        title="",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_tipo.update_traces(textposition='inside', textinfo='percent+label')
    fig_tipo.update_layout(height=350)
    st.plotly_chart(fig_tipo, use_container_width=True)

with col_right:
    st.subheader("✅ Status de Conformidade")
    
    conformidade_counts = df_filtered['resultado_texto'].value_counts()
    
    colors = {
        'Conforme': '#2ecc71',
        'Não Conforme': '#e74c3c',
        'N/A': '#95a5a6'
    }
    
    fig_conf = go.Figure(data=[
        go.Bar(
            x=conformidade_counts.index,
            y=conformidade_counts.values,
            marker_color=[colors.get(x, '#3498db') for x in conformidade_counts.index],
            text=conformidade_counts.values,
            textposition='auto',
        )
    ])
    fig_conf.update_layout(
        height=350,
        xaxis_title="Status",
        yaxis_title="Quantidade",
        showlegend=False
    )
    st.plotly_chart(fig_conf, use_container_width=True)

# Gráfico de linha temporal
st.subheader("📅 Evolução Temporal das Auditorias")

timeline_data = df_filtered.groupby('data_auditoria').size().reset_index(name='quantidade')

fig_timeline = px.line(
    timeline_data,
    x='data_auditoria',
    y='quantidade',
    markers=True,
    title=""
)
fig_timeline.update_traces(line_color='#3498db', line_width=3)
fig_timeline.update_layout(
    height=300,
    xaxis_title="Data",
    yaxis_title="Número de Auditorias",
    hovermode='x unified'
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Análise de NPS
if len(df_filtered[df_filtered['tipo_auditoria'] == 'NPS']) > 0:
    st.subheader("⭐ Análise de NPS")
    
    col_nps1, col_nps2 = st.columns(2)
    
    with col_nps1:
        nps_df = df_filtered[df_filtered['tipo_auditoria'] == 'NPS'].copy()
        
        fig_nps = px.bar(
            nps_df,
            x='nome_projeto',
            y='resultado_valor',
            title="NPS por Projeto",
            color='resultado_valor',
            color_continuous_scale='RdYlGn',
            range_color=[0, 10]
        )
        fig_nps.update_layout(height=350)
        st.plotly_chart(fig_nps, use_container_width=True)
    
    with col_nps2:
        # Classificação NPS
        def classificar_nps(score):
            if score >= 9:
                return 'Promotor'
            elif score >= 7:
                return 'Neutro'
            else:
                return 'Detrator'
        
        nps_df['classificacao'] = nps_df['resultado_valor'].apply(classificar_nps)
        class_counts = nps_df['classificacao'].value_counts()
        
        fig_class = px.pie(
            values=class_counts.values,
            names=class_counts.index,
            title="Classificação NPS",
            color=class_counts.index,
            color_discrete_map={
                'Promotor': '#2ecc71',
                'Neutro': '#f39c12',
                'Detrator': '#e74c3c'
            }
        )
        fig_class.update_traces(textposition='inside', textinfo='percent+label')
        fig_class.update_layout(height=350)
        st.plotly_chart(fig_class, use_container_width=True)

# Tabela de detalhes
st.markdown("---")
st.subheader("📋 Detalhes das Auditorias")

# Preparar dados para exibição
df_display = df_filtered.copy()
df_display['data_auditoria'] = df_display['data_auditoria'].dt.strftime('%d/%m/%Y')
df_display = df_display.fillna('-')

# Configurar colunas para exibição
columns_to_show = [
    'id_auditoria',
    'data_auditoria',
    'nome_projeto',
    'tipo_auditoria',
    'item_auditado',
    'resultado_texto',
    'resultado_valor',
    'observacoes'
]

df_display = df_display[columns_to_show]
df_display.columns = [
    'ID',
    'Data',
    'Projeto',
    'Tipo',
    'Item',
    'Resultado',
    'Valor',
    'Observações'
]

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

# Botão de download
st.markdown("---")
csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥 Baixar dados filtrados (CSV)",
    data=csv,
    file_name=f"auditorias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        Dashboard de Qualidade | Última atualização: {}
    </div>
    """.format(datetime.now().strftime('%d/%m/%Y %H:%M')),
    unsafe_allow_html=True
)
