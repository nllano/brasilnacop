import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

# Streamlit usa funções como:
# - st.title(): adiciona título da página
# - st.text(): adiciona texto
# - st.write(): adiciona objetos como dataframes
# - st.bar_chart(): adiciona gráficos de barra
# - st.map(): adiciona mapa
# - etc.
# Mais funções podem ser vistas aqui:
# https://docs.streamlit.io/library/get-started/main-concepts#display-and-style-data
st.title('Corridas de Uber em NYC')

# Nas linhas abaixo, repare: o upload de dados (pd.read_csv()) é feito
# dentro de uma função (def load_dada()). Isso é feito com Streamlit
# para poder usar o decorator @st.cache. Trata-se de um "termo mágico"
# de Streamlit que indica: "a função a seguir, quando acionada, salve
# os dados em cache". Com isso a leitura dos dados no site fica mais
# rápido.
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date/time'] = pd.to_datetime(data['date/time'])
    return data

data_load_state = st.text('Loading...')
data = load_data(10000) # carrego apenas 10 mil registros
data_load_state.text("Feito!")

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

st.subheader('Números de corridas por hora')
hist_values = np.histogram(data['date/time'].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Para criar o slider com a hora, uso st.slider() e salvo
# na variável hour_to_filter. a função st.slider() recebe
# três números: o primeiro é o início (0 hora), o segundo
# é o fim (23 horas), e o terceiro é o número default --
# ou seja, quando eu abrir a página, o slider vai estar em
# que posição? -- (17 horas).
#
# A lógica aqui: cada vez que mudo o valor no slider no site,
# o dataframe muda seu filtro. Com isso, os valores apresentados
# no dataframe são apenas aqueles indicados pelo slider.
hour_to_filter = st.slider('hora', 0, 23, 17)
filtered_data = data[data['date/time'].dt.hour == hour_to_filter]

st.subheader('Mapa de todas as corridas às {}:00'.format(hour_to_filter))
st.map(filtered_data)