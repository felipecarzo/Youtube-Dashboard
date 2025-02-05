import streamlit as st
import pandas as pd
import sqlite3
from utils import load_data

# Configurar título da página e layout
st.set_page_config(page_title="Painel de Análise do YouTube", layout="wide")

# Criar título da página
st.title("📊 Fabrica de Monstros - Painel de Análise de Tendências")

# Carregar os dados do banco SQLite
df_videos = load_data()

# Converter 'published_at' para datetime **somente uma vez**
df_videos["published_at"] = pd.to_datetime(df_videos["published_at"], errors="coerce").dt.tz_localize(None)

# Criar colunas para layout mais organizado
col1, col2 = st.columns([1, 3])

# Criar filtros interativos no menu lateral
st.sidebar.header("🔍 Filtros")
video_type = st.sidebar.selectbox("Tipo de Vídeo", ["Todos", "Shorts", "Longos"])

# Adiciona um filtro de data interativo no Streamlit
date_range = st.sidebar.date_input("Selecione o período", [])

# Criar um DataFrame atualizado com base nos filtros
df_filtered = df_videos.copy()

# Aplicar filtro de tipo de vídeo
if video_type != "Todos":
    df_filtered = df_filtered[df_filtered["video_type"] == video_type]

# Aplicar filtro de data
if date_range and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range).tz_localize(None)
    df_filtered = df_filtered[
        (df_filtered["published_at"] >= start_date) &
        (df_filtered["published_at"] <= end_date)
    ]

# Criar abas para organizar os dados
tab1, tab2 = st.tabs(["📊 Visualizações ao Longo do Tempo", "📈 Comparação de Shorts vs Longos"])

# Verificar se há dados após o filtro
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros aplicados.")
    st.stop()

else:
    # Atualizar as métricas
    with col1:
        st.metric("🎥 Total de Vídeos", df_filtered.shape[0])
        media_visualizacoes = df_filtered["views"].mean()
        st.metric("📈 Média de Visualizações", f"{int(media_visualizacoes):,}" if not pd.isna(media_visualizacoes) else "0")
        media_engajamento = df_filtered["likes_per_view"].mean()
        st.metric("❤️ Média de Engajamento", round(media_engajamento, 3) if not pd.isna(media_engajamento) else "0")

    # Atualizar os gráficos com os dados filtrados
    with tab1:
        st.subheader("📈 Evolução das Visualizações")

        # Agrupar os dados por dia (em vez de mês) para garantir flexibilidade no filtro
        df_plot = df_filtered.groupby(df_filtered["published_at"].dt.date)["views"].sum().reset_index()

        # Converter a coluna para datetime para evitar problemas de ordenação
        df_plot["published_at"] = pd.to_datetime(df_plot["published_at"])

        if df_plot.empty or df_plot["views"].sum() == 0:
            st.warning("⚠️ Nenhum dado disponível no período selecionado.")
        else:
            st.line_chart(df_plot.set_index("published_at"))

    with tab2:
        st.subheader("📊 Shorts vs Vídeos Longos")
        st.bar_chart(df_filtered.groupby("video_type")["views"].mean())

    # Atualizar CSV para exportação com os dados filtrados
    csv = df_filtered[['video_id', 'title', 'published_at', 'views', 'likes', 'comments', 'duration_sec', 'video_type']]
    st.sidebar.download_button(
        label="📥 Exportar Dados (CSV)",
        data=csv.to_csv(index=False),
        file_name="youtube_videos_filtered.csv",
        mime="text/csv"
    )

# Rodar o Streamlit:
# No terminal, execute: streamlit run app.py