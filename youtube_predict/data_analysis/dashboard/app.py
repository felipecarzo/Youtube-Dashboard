import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Configurar título e layout
st.set_page_config(page_title="Painel de Análise do YouTube", layout="wide")

# Criar título
st.title("📊 Fabrica de Monstros - Painel de Análise de Tendências")

# Carregar os dados do banco SQLite
df_videos = load_data()


# DEPURAÇÃO: Verificar se a coluna 'video_type' está carregada corretamente
# st.subheader("🚀 Debug: Verificando 'video_type'")
# if "video_type" not in df_videos.columns:
#     st.error("🚨 ERRO: A coluna 'video_type' não foi encontrada no DataFrame!")
# else:
#     st.write("📌 Tipos de vídeos disponíveis:", df_videos["video_type"].unique())
# FIM DA DEPURAÇÃO


# Converter a coluna 'published_at' para datetime
df_videos["published_at"] = pd.to_datetime(df_videos["published_at"], errors="coerce").dt.tz_localize(None)

# Criar filtros no menu lateral
st.sidebar.header("🔍 Filtros")
video_type = st.sidebar.selectbox("Tipo de Vídeo", ["Todos", "Short", "Longo"])
date_range = st.sidebar.date_input("Selecione o período", [])

# Criar DataFrame atualizado com base nos filtros
df_filtered = df_videos.copy()

# Aplicar filtro de tipo de vídeo
if video_type != "Todos":
    df_filtered = df_filtered[df_filtered["video_type"] == video_type]

# Aplicar filtro de data corretamente
if date_range and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range).tz_localize(None)
    df_filtered = df_filtered[
        (df_filtered["published_at"] >= start_date) &
        (df_filtered["published_at"] <= end_date)
    ]

# 📢 Se nenhum dado for encontrado após a filtragem
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros aplicados.")
    st.stop()

# 🔹 Criar métricas principais 🔹
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎥 Total de Vídeos", df_filtered.shape[0])
    st.metric("📈 Média de Visualizações", f"{df_filtered['views'].mean():,.0f}")
    st.metric("⏳ Tempo Total de Exibição", f"{df_filtered['duration_sec'].sum()/60:,.0f} min")

with col2:
    st.metric("👍 Média de Likes", f"{df_filtered['likes'].mean():,.0f}")
    st.metric("💬 Média de Comentários", f"{df_filtered['comments'].mean():,.0f}")
    st.metric("📊 Taxa de Retenção (média)", f"{(df_filtered['duration_sec'].mean() / df_filtered['duration_sec'].max())*100:.2f}%")

# Evitar erro se a coluna CTR não existir
if "ctr" in df_filtered.columns:
    ctr_medio = df_filtered["ctr"].mean()
    ctr_medio = round(ctr_medio, 2) if not pd.isna(ctr_medio) else "N/A"
else:
    ctr_medio = "N/A"  # Se a coluna não existir, exibe "N/A"

# Evitar erro se a coluna `traffic_source` não existir
if "traffic_source" in df_filtered.columns and not df_filtered["traffic_source"].isna().all():
    fonte_trafego = df_filtered["traffic_source"].mode()[0]
else:
    fonte_trafego = "Desconhecido"

# Evitar erro se a coluna `device` não existir
if "device" in df_filtered.columns and not df_filtered["device"].isna().all():
    dispositivo_mais_usado = df_filtered["device"].mode()[0]
else:
    dispositivo_mais_usado = "Desconhecido"

with col3:
    st.metric("📢 CTR Médio (Click-Through Rate)", f"{ctr_medio}%")
    st.metric("🌎 Fonte de Tráfego Principal", fonte_trafego)
    st.metric("📱 Dispositivo Mais Usado", df_filtered["device"].mode()[0])

# 📊 Criar abas para melhor organização
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visualizações ao Longo do Tempo",
    "📈 Correlação Duração x Visualizações",
    "💬 Engajamento: Shorts vs Longos",
    "📅 Desempenho por Dia da Semana",
    "📏 Distribuição de Duração"
])

# 📊 Gráfico de Visualizações ao longo do tempo (corrigido)
with tab1:
    st.subheader("📈 Evolução das Visualizações")
    df_plot = df_filtered.copy()
    df_plot["published_at"] = df_plot["published_at"].dt.date
    df_plot = df_plot.groupby("published_at", as_index=False)["views"].sum()

    if df_plot.empty or df_plot["views"].sum() == 0:
        st.warning("⚠️ Nenhum dado disponível no período selecionado.")
    else:
        fig = px.line(df_plot, x="published_at", y="views", title="Visualizações ao Longo do Tempo")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("⏳ Correlação entre Duração do Vídeo e Visualizações")
    if df_filtered.empty:
        st.warning("⚠️ Nenhum dado disponível para exibição.")
    else:
        # Remover linhas com valores nulos ou zero em 'duration_sec' ou 'views'
        df_plot = df_filtered.dropna(subset=['duration_sec', 'views'])
        df_plot = df_plot[(df_plot['duration_sec'] > 0) & (df_plot['views'] > 0)]

        if df_plot.empty:
            st.warning("⚠️ Dados insuficientes após a limpeza para gerar o gráfico.")
        else:
            fig = px.scatter(df_plot, x=df_plot["duration_sec"] / 60, y="views", 
                             title="Duração do Vídeo vs Visualizações", 
                             labels={"x": "Duração (minutos)", "y": "Visualizações"})
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("💬 Comparação de Engajamento (Likes e Comentários) entre Shorts e Longos")
    if df_filtered.empty:
        st.warning("⚠️ Nenhum dado disponível para este período.")
    else:
        df_engajamento = df_filtered.groupby("video_type")[["likes", "comments"]].mean().reset_index()
        fig = px.bar(df_engajamento, x="video_type", y=["likes", "comments"], barmode="group", 
                     title="Engajamento Médio por Tipo de Vídeo")
        st.plotly_chart(fig, use_container_width=True)

# 📅 Desempenho por Dia da Semana
with tab4:
    st.subheader("📅 Desempenho por Dia da Semana")
    if df_filtered.empty:
        st.warning("⚠️ Nenhum dado disponível para exibição.")
    else:
        df_filtered["weekday"] = df_filtered["published_at"].dt.day_name()
        df_plot = df_filtered.groupby("weekday")["views"].mean().reset_index()
        fig = px.bar(df_plot, x="weekday", y="views", title="Média de Visualizações por Dia da Semana")
        st.plotly_chart(fig, use_container_width=True)

# 📏 Distribuição da Duração dos Vídeos
with tab5:
    st.subheader("📏 Distribuição da Duração dos Vídeos")
    if df_filtered.empty:
        st.warning("⚠️ Nenhum dado disponível para este período.")
    else:
        fig = px.histogram(df_filtered, x=df_filtered["duration_sec"] / 60, nbins=20, 
                           title="Distribuição da Duração dos Vídeos", labels={"x": "Duração (minutos)"})
        st.plotly_chart(fig, use_container_width=True)

# Rodar o Streamlit:
# No terminal, execute: streamlit run app.py

TEST = TEST.WEBHOOK.DISCORD