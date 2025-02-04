import openai
import os
from dotenv import load_dotenv

# 🚀 Carregar chave da API do OpenAI do arquivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🚀 Função para analisar título e descrição com GPT
def analisar_titulo_descricao(titulo, descricao):
    prompt = f"""
Analise o seguinte título e descrição de um vídeo do YouTube e me dê as seguintes avaliações de 0 a 1:

- **Engajamento do título** (0 = sem graça, 1 = super atrativo)
- **Clickbait do título** (0 = informativo, 1 = sensacionalista)
- **Tom da descrição** (0 = técnico, 1 = emocional)
- **Probabilidade de viralizar** (0 = baixa, 1 = alta)

**Título:** {titulo}
**Descrição:** {descricao}

Responda apenas com os valores em JSON. Exemplo:
{{
    "engajamento_titulo": 0.85,
    "clickbait_titulo": 0.70,
    "tom_descricao": 0.60,
    "probabilidade_viralizar": 0.90
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Você é um especialista em análise de vídeos do YouTube."},
                      {"role": "user", "content": prompt}]
        )
        resposta_json = response["choices"][0]["message"]["content"]
        return eval(resposta_json)  # Converte string JSON em dicionário Python
    
    except Exception as e:
        print(f"Erro ao chamar API da OpenAI: {e}")
        return None