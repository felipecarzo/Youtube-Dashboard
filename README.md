# YouTube Dashboard

## Descrição do Projeto
O **YouTube Dashboard** é uma ferramenta analítica robusta destinada a maximizar a compreensão do desempenho de conteúdos no YouTube. Utilizando técnicas avançadas de data science, este projeto permite que criadores de conteúdo e analistas de mídia visualizem, analisem e prevejam o desempenho de vídeos com base em uma série de métricas críticas como visualizações, engajamento, CTR, fontes de tráfego e demografia do público.

## Conhecimentos Aplicados
- **Análise Exploratória de Dados**: Manipulação e exploração de datasets usando pandas e numpy.
- **Visualização de Dados**: Geração de gráficos interativos com Plotly e Streamlit.
- **Machine Learning**: Aplicação de modelos preditivos usando scikit-learn para prever tendências de visualização e engajamento.
- **Integração com API**: Captação de dados em tempo real utilizando a API do YouTube.
- **Modelagem Estatística**: Uso de técnicas estatísticas para análise e inferência de dados complexos.

## Estrutura do Repositório

/Youtube-Dashboard <br>
│── app.py                  # Arquivo principal do dashboard Streamlit <br>
│── load_data.py            # Script para carregar e processar dados <br>
│── utils.py                # Funções auxiliares para manipulação de dados <br>
│── youtube_api_client.py   # Cliente da API do YouTube para coleta de dados <br>
│ <br>
│── models
│   ├── model_rf.pkl        # Modelo Random Forest serializado <br>
│   ├── model_lr.pkl        # Modelo Linear Regression serializado <br>
│ <br>
│── data <br>
│   ├── raw                 # Dados brutos coletados da API <br>
│   ├── processed           # Dados processados para análise <br>
│ <br>
│── notebooks               # Jupyter Notebooks para exploração de dados e prototipagem <br>
│ <br>
│── requirements.txt        # Dependências do projeto <br>
│── README.md               # Documentação do projeto <br>



## Tecnologias Utilizadas
- **Python**: Linguagem de programação para desenvolvimento do projeto.
- **Streamlit**: Framework para criação de aplicativos de dados na web.
- **Plotly**: Biblioteca para visualização de dados interativos.
- **Pandas/Numpy**: Bibliotecas para manipulação e análise de dados.
- **Scikit-learn**: Ferramenta para construção de modelos de machine learning.
- **SQLite**: Sistema de gerenciamento de banco de dados para armazenamento de dados.

## Passos para Instalação e Execução
1. Clone este repositório:
```bash
git clone https://github.com/felipecarzo/Youtube-Dashboard

	2.	Acesse o diretório do projeto:

cd Youtube-Dashboard

	3.	Instale as dependências:

pip install -r requirements.txt

	4.	Execute o aplicativo Streamlit:

streamlit run app.py

Explore as visualizações interativas e obtenha insights valiosos sobre o desempenho dos seus vídeos no YouTube diretamente do seu navegador.

Para mais informações, acesse o repositório do projeto.
