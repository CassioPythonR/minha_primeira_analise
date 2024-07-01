# Importa bibliotecas
import pandas as pd
import statsmodels.formula.api as smf
import plotly.express as px

# Importa dados
dados = pd.read_csv(filepath_or_buffer = "https://aluno.analisemacro.com.br/download/47784/?tmstv=1678715174") # arquivo dados.csv

# Estima modelo ("ols" descreve o modelo e "fit" o estima)
modelo = smf.ols("y ~ tempo", data = dados).fit()

# Imprime os coeficientes estimados
modelo.params

# Extrai o ajuste do modelo
ajuste = modelo.fittedvalues

# Cria nova coluna com os valores de ajuste e transforma coluna data para YYYY-MM-DD
dados["tendencia"] = ajuste
dados["data"] = pd.PeriodIndex(
    data = dados["data"].str.replace(" ", "-"),
    freq = "Q"
    ).to_timestamp()

# Cria gráfico de linha (valores observados e reta de ajuste)
g1 = px.line( # para criar gráfico de linha
    data_frame = dados, # tabela DataFrame de dados
    y = "y", # eixo Y
    x = "data", # eixo X
    title = "PIB do Brasil", # título do gráfico
    color = px.Constant("PIB"), # nome da série na legenda
    color_discrete_sequence = ["#282f6b"], 
    labels = dict(data = "", y = "Índice", color = "")  # título do eixo X, Y e da legenda
    )

g1.add_annotation( # adiciona texto de subtítulo
    text = "Preços de mercado, nº índice sazonalmente ajustado (média de 1995 = 100)",
     y = 1.1, 
     x = -0.11,
     yref = "paper", 
     xref = "paper",
     showarrow = False
     )

g1.add_annotation(  # adiciona e posiciona texto de fonte de dados
    showarrow = False,
    text = "Dados: IBGE | Elaboração: analisemacro.com.br",
    x = 1,
    xref = "paper",
    y = -0.18,
    yref = "paper"
    )

g1.add_scatter( # adiciona linha de tendência
    x = dados["data"],
    y = dados["tendencia"],
    name = "Tendência linear",
    line = dict(color = "#b22200") # cor da nova linha
    )
    
g1.show()