import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Qualidade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado ultra moderno
st.markdown("""
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Estilos globais */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fundo com gradiente */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0rem 1rem;
    }
    
    /* Container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Título principal com gradiente */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Cards de métricas personalizados */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 500;
        color: #7f8c8d;
    }
    
    /* Melhorar aparência das métricas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar estilizada */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Headers de seção */
    h2 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    h3 {
        color: #34495e;
        font-weight: 600;
        font-size: 1.3rem !important;
    }
    
    /* Botões */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabela estilizada */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Divisores */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Animação de fade-in */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Card de informação */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Melhorar gráficos */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #7f8c8d;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho com animação
st.markdown("""
    <h1>📊 Dashboard de Qualidade</h1>
    <p class="subtitle">Sistema de Monitoramento e Análise de Auditorias</p>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    # Procura o arquivo no diretório atual ou no caminho do script
    possible_paths = [
        'qualidade_database.csv',
        './qualidade_database.csv',
        os.path.join(os.path.dirname(__file__), 'qualidade_database.csv')
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path, encoding='utf-8')
            break
        except:
            try:
                df = pd.read_csv(path, encoding='latin-1')
                break
            except:
                continue
    
    if df is None:
        st.error("❌ Arquivo qualidade_database.csv não encontrado!")
        st.stop()
    
    # Converter data para datetime
    df['data_auditoria'] = pd.to_datetime(df['data_auditoria'])
    
    return df

df = load_data()

# Sidebar com filtros elegante
st.sidebar.markdown("### 🔍 Filtros de Dados")
st.sidebar.markdown("---")

# Filtro de data
min_date = df['data_auditoria'].min()
max_date = df['data_auditoria'].max()

date_range = st.sidebar.date_input(
    "📅 Período de Análise",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtro de tipo de auditoria
tipos_auditoria = ['Todos'] + sorted(df['tipo_auditoria'].unique().tolist())
tipo_selecionado = st.sidebar.selectbox(
    "📋 Tipo de Auditoria",
    tipos_auditoria,
    index=0
)

# Filtro de projeto
projetos = ['Todos'] + sorted(df['nome_projeto'].dropna().unique().tolist())
projeto_selecionado = st.sidebar.selectbox(
    "🎯 Projeto",
    projetos,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 2rem;'>
        <p style='color: white; font-size: 0.85rem; margin: 0;'>
            💡 <strong>Dica:</strong> Use os filtros acima para personalizar a visualização dos dados.
        </p>
    </div>
""", unsafe_allow_html=True)

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

# KPIs principais com cards estilizados
st.markdown("## 📈 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_auditorias = len(df_filtered)
    st.metric(
        label="🔍 Total de Auditorias",
        value=total_auditorias,
        delta=None
    )

with col2:
    conformes = len(df_filtered[df_filtered['resultado_texto'] == 'Conforme'])
    taxa_conformidade = (conformes / total_auditorias * 100) if total_auditorias > 0 else 0
    st.metric(
        label="✅ Taxa de Conformidade",
        value=f"{taxa_conformidade:.1f}%",
        delta=f"{conformes} conformes"
    )

with col3:
    nps_data = df_filtered[df_filtered['tipo_auditoria'] == 'NPS']
    media_nps = nps_data['resultado_valor'].mean() if len(nps_data) > 0 else 0
    st.metric(
        label="⭐ NPS Médio",
        value=f"{media_nps:.1f}",
        delta="Excelente" if media_nps >= 9 else ("Bom" if media_nps >= 7 else "Atenção")
    )

with col4:
    projetos_auditados = df_filtered['nome_projeto'].dropna().nunique()
    st.metric(
        label="🎯 Projetos Auditados",
        value=projetos_auditados,
        delta=None
    )

st.markdown("---")

# Resumo rápido em card
if total_auditorias > 0:
    nao_conformes = len(df_filtered[df_filtered['resultado_texto'] == 'Não Conforme'])
    st.markdown(f"""
        <div class="info-card">
            <h3 style="color: white; margin-top: 0;">📊 Resumo Rápido</h3>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                De <strong>{total_auditorias}</strong> auditorias analisadas, 
                <strong>{conformes}</strong> estão conformes ({taxa_conformidade:.1f}%) e 
                <strong>{nao_conformes}</strong> apresentam não conformidades.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Gráficos principais
st.markdown("## 📊 Análise Visual")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎨 Distribuição por Tipo")
    
    tipo_counts = df_filtered['tipo_auditoria'].value_counts()
    
    fig_tipo = px.pie(
        values=tipo_counts.values,
        names=tipo_counts.index,
        title="",
        color_discrete_sequence=px.colors.sequential.Purples_r,
        hole=0.4
    )
    fig_tipo.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(line=dict(color='white', width=2))
    )
    fig_tipo.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_tipo, use_container_width=True)

with col_right:
    st.markdown("### ✅ Status de Conformidade")
    
    conformidade_counts = df_filtered['resultado_texto'].value_counts()
    
    colors_map = {
        'Conforme': '#10b981',
        'Não Conforme': '#ef4444',
        'N/A': '#8b5cf6'
    }
    
    fig_conf = go.Figure(data=[
        go.Bar(
            x=conformidade_counts.index,
            y=conformidade_counts.values,
            marker_color=[colors_map.get(x, '#3b82f6') for x in conformidade_counts.index],
            text=conformidade_counts.values,
            textposition='outside',
            textfont=dict(size=16, color='#2c3e50'),
            marker=dict(
                line=dict(color='white', width=2)
            )
        )
    ])
    fig_conf.update_layout(
        height=400,
        xaxis_title="Status",
        yaxis_title="Quantidade",
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=14, color='#2c3e50')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#2c3e50')
        )
    )
    st.plotly_chart(fig_conf, use_container_width=True)

# Gráfico de linha temporal mais bonito
st.markdown("## 📅 Evolução Temporal")

timeline_data = df_filtered.groupby('data_auditoria').size().reset_index(name='quantidade')

fig_timeline = go.Figure()

fig_timeline.add_trace(go.Scatter(
    x=timeline_data['data_auditoria'],
    y=timeline_data['quantidade'],
    mode='lines+markers',
    name='Auditorias',
    line=dict(color='#667eea', width=3, shape='spline'),
    marker=dict(size=10, color='#764ba2', line=dict(color='white', width=2)),
    fill='tozeroy',
    fillcolor='rgba(102, 126, 234, 0.2)'
))

fig_timeline.update_layout(
    height=350,
    xaxis_title="Data",
    yaxis_title="Número de Auditorias",
    hovermode='x unified',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        tickfont=dict(size=12)
    )
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Análise de NPS melhorada
if len(df_filtered[df_filtered['tipo_auditoria'] == 'NPS']) > 0:
    st.markdown("## ⭐ Análise Detalhada de NPS")
    
    col_nps1, col_nps2 = st.columns(2)
    
    with col_nps1:
        st.markdown("### 📊 NPS por Projeto")
        nps_df = df_filtered[df_filtered['tipo_auditoria'] == 'NPS'].copy()
        
        fig_nps = go.Figure(data=[
            go.Bar(
                x=nps_df['nome_projeto'],
                y=nps_df['resultado_valor'],
                marker=dict(
                    color=nps_df['resultado_valor'],
                    colorscale='RdYlGn',
                    cmin=0,
                    cmax=10,
                    line=dict(color='white', width=2)
                ),
                text=nps_df['resultado_valor'],
                textposition='outside',
                textfont=dict(size=14, color='#2c3e50')
            )
        ])
        fig_nps.update_layout(
            height=400,
            xaxis_title="Projeto",
            yaxis_title="NPS Score",
            yaxis=dict(range=[0, 10]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        st.plotly_chart(fig_nps, use_container_width=True)
    
    with col_nps2:
        st.markdown("### 🎯 Classificação NPS")
        
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
            title="",
            color=class_counts.index,
            color_discrete_map={
                'Promotor': '#10b981',
                'Neutro': '#f59e0b',
                'Detrator': '#ef4444'
            },
            hole=0.4
        )
        fig_class.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_class.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )
        st.plotly_chart(fig_class, use_container_width=True)

# Tabela de detalhes melhorada
st.markdown("---")
st.markdown("## 📋 Detalhes das Auditorias")

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
    hide_index=True,
    height=400
)

# Botão de download estilizado
st.markdown("---")
col_download, col_info = st.columns([1, 3])

with col_download:
    csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Baixar Dados (CSV)",
        data=csv,
        file_name=f"auditorias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col_info:
    st.info(f"💡 Exportando {len(df_filtered)} registros filtrados para análise offline.")

# Rodapé elegante
st.markdown(f"""
    <div class="footer">
        <p style="margin: 0; font-size: 1rem; font-weight: 600;">
            Dashboard de Qualidade
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            🕒 Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #95a5a6;">
            Desenvolvido com ❤️ usando Streamlit
        </p>
    </div>
""", unsafe_allow_html=True)