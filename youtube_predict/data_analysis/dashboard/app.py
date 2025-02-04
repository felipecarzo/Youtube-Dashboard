import streamlit as st
import pandas as pd
import sqlite3
from utils import load_data

# Configurar título da página e layout
st.set_page_config(page_title="Painel de Análise do YouTube", layout="wide")

# Estilização CSS
st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Criar título da página
st.title("📊 Fabrica de Monstros - Painel de Análise de Tendências")

# Criar colunas para layout mais organizado
col1, col2 = st.columns([1, 3])

# Criar filtros interativos no menu lateral
st.sidebar.header("🔍 Filtros")
video_type = st.sidebar.selectbox("Tipo de Vídeo", ["Todos", "Shorts", "Longos"])
date_range = st.sidebar.date_input("Selecione o período", [])

# Carregar os dados do banco SQLite
df_videos = load_data()

# Aplicar filtros aos dados
if video_type != "Todos":
    df_videos = df_videos[df_videos["video_type"] == video_type]

# Criar três colunas para métricas
with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("🎥 Total de Vídeos", df_videos.shape[0])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    
    # st.metric("📈 Média de Visualizações", f"{int(df_videos['views'].mean()):,}")
    # Evita erro caso o DataFrame esteja vazio
    media_visualizacoes = df_videos["views"].mean()
    media_visualizacoes = int(media_visualizacoes) if not pd.isna(media_visualizacoes) else 0
    st.metric("📈 Média de Visualizações", f"{media_visualizacoes:,}")
    
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    #st.metric("❤️ Média de Engajamento", f"{round(df_videos['likes_per_view'].mean(), 3)}")
    media_engajamento = df_videos["likes_per_view"].mean()
    media_engajamento = round(media_engajamento, 3) if not pd.isna(media_engajamento) else 0
    st.metric("❤️ Média de Engajamento", media_engajamento)

    
    
    
    st.markdown("</div>", unsafe_allow_html=True)

# Criar abas para organizar os dados
tab1, tab2 = st.tabs(["📊 Visualizações ao Longo do Tempo", "📈 Comparação de Shorts vs Longos"])

with tab1:
    st.subheader("📈 Evolução das Visualizações")
    st.line_chart(df_videos.groupby(df_videos["published_at"].dt.to_period("M"))["views"].sum())

with tab2:
    st.subheader("📊 Shorts vs Vídeos Longos")
    st.bar_chart(df_videos.groupby("video_type")["views"].mean())

# Adicionar botão de exportação
st.sidebar.download_button(
    label="📥 Exportar Dados (CSV)",
    data=df_videos.to_csv(index=False),
    file_name="dados_youtube.csv",
    mime="text/csv"
)

# Rodar o Streamlit:
# No terminal, execute: streamlit run app.py
