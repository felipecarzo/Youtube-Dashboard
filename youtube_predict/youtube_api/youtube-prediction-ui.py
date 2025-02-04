import streamlit as st
import pandas as pd
import joblib
import cv2
import numpy as np
from PIL import Image
import os

def carregar_modelo():
    return joblib.load("modelo_rf_otimizado.pkl")

def carregar_dados_treino():
    return joblib.load("X_train_columns.pkl"), joblib.load("df_videos.pkl")

def contar_palavras_nicho(titulo):
    palavras_chave_nicho = ["treino", "hipertrofia", "massa muscular", "exercício", "dieta", "proteína", "suplemento"]
    return sum(1 for palavra in palavras_chave_nicho if palavra in titulo.lower())

def analisar_thumbnail_local(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    brilho = np.mean(gray)
    contraste = gray.std()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    qtd_faces = len(faces)
    pixels = img.reshape(-1, 3)
    cor_predominante = np.mean(pixels, axis=0).mean()
    return brilho, contraste, cor_predominante, qtd_faces

st.title("📊 Previsão de Visualizações no YouTube")

modelo_rf = carregar_modelo()
X_train_columns, df_videos = carregar_dados_treino()

media_views_ultimos_10 = df_videos["views"].rolling(window=10, min_periods=1).mean().iloc[-1]

titulo_video = st.text_input("Digite o título do vídeo:")
thumb_upload = st.file_uploader("Carregue a thumbnail do vídeo", type=["jpg", "png", "jpeg"])

duration_sec = st.number_input("Duração do vídeo (segundos):", min_value=1, value=600)
data_video = st.date_input("Data de postagem:")
day_of_week = data_video.strftime("%A")

if st.button("📊 Fazer Previsão"):
    if titulo_video and thumb_upload:
        image = Image.open(thumb_upload)
        brilho, contraste, cor_predominante, qtd_faces = analisar_thumbnail_local(image)
        novo_video = pd.DataFrame({
            "title": [titulo_video],
            "duration_sec": [duration_sec],
            "year": [data_video.year],
            "month": [data_video.month],
            "day": [data_video.day],
            "weekday": [day_of_week],
            "likes": [0],
            "comments": [0],
            "likes_per_view": [0],
            "comments_per_view": [0],
            "title_word_count": [len(titulo_video.split())],
            "qtd_palavras_thumb": [3],
            "media_views_ultimos_10": [media_views_ultimos_10],
            "media_likes_per_view": [0.1],
            "media_comments_per_view": [0.02],
            "qtd_palavras_nicho": [contar_palavras_nicho(titulo_video)],
            "brilho": [brilho],
            "contraste": [contraste],
            "cor_predominante": [cor_predominante],
            "qtd_faces": [qtd_faces]
        })
        
        novo_video = pd.get_dummies(novo_video, columns=["weekday"])
        for col in X_train_columns:
            if col not in novo_video.columns:
                novo_video[col] = 0
        novo_video = novo_video[X_train_columns]
        novo_video = novo_video.apply(pd.to_numeric, errors="coerce").fillna(0)
        previsao = modelo_rf.predict(novo_video.to_numpy())
        st.success(f"📊 Previsão de Visualizações: {int(previsao[0])}")
    else:
        st.error("⚠️ Por favor, insira um título e uma thumbnail!")
