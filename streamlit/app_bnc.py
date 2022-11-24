import streamlit as st
import pandas as pd

st.markdown("<h1 style='text-align: center; color: grey;'>Brasil na COP</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Diplomacia e discursos ambientais 2004-2021</h4>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

arquivo = 'streamlit_final.csv'

@st.cache
def importar_csv(arquivo):
    data = pd.read_csv(arquivo, sep=';')
    return data

data = importar_csv(arquivo)
edicao = data['edicao'].sort_values().unique().tolist()
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    edicao_selecionada = st.selectbox('Escolha uma edição da COP', options=['-'] + edicao)
    if edicao_selecionada != '-':
        topicos = data.loc[data['edicao'] == edicao_selecionada, 'topico']
        if edicao_selecionada in ['COP10', 'COP11']:
            imagem = 'marina_silva.jpg'
        elif edicao_selecionada == 'COP13':
            imagem = 'amorim.jpg'
        elif edicao_selecionada == 'COP15':
            imagem = 'lula.jpg'
        elif edicao_selecionada in ['COP16', 'COP17', 'COP18', 'COP19', 'COP20']:
            imagem = 'izabella_teixeira.jpg'
        elif edicao_selecionada == 'COP21':
            imagem = 'dilma.jpg'
        elif edicao_selecionada in ['COP22', 'COP23']:
            imagem = 'sarney_filho.jpg'
        elif edicao_selecionada == 'COP24':
            imagem = 'duarte.jpg'
        elif edicao_selecionada == 'COP25':
            imagem = 'salles.jpg'
        elif edicao_selecionada == 'COP26':
            imagem = 'leite.jpg'
        topico = topicos.sort_values().unique().tolist()
        topico_selecionado = st.selectbox(f'Escolha um tópico da {edicao_selecionada}', options=['-'] + list(topico))
        if topico_selecionado != '-':
            trechos_df = data[(data['edicao'] == edicao_selecionada) & (data['topico'] == topico_selecionado)]
            autor_list = trechos_df['agente_cargo'].tolist()
            cid_list = trechos_df['cidade_pais'].tolist()
            ano_list = trechos_df['ano'].tolist()
            dicio = dict(zip(trechos_df['trecho_curto'], trechos_df['trecho_discurso']))
            if topico_selecionado != '-':
                st.image(f'fotos/{imagem}', use_column_width='always')
                st.write(f'<blockquote><i>{autor_list[0]}<br/>{cid_list[0]}, {int(ano_list[0])}</i></blockquote><br>', unsafe_allow_html=True)

with col2:
    try:
        if topico_selecionado != '-':
            for k, v in dicio.items():
                st.write(f'<p class="aspas">{k}</p>', unsafe_allow_html=True)
                integra = v
                if len(dicio) > 1:
                    st.write("<hr>", unsafe_allow_html=True)
            with st.expander("Discurso completo"):
                st.write(f'{integra}', unsafe_allow_html=True)
    except NameError:
       pass
