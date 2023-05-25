"""
Este módulo contém o código para o meu aplicativo Streamlit.
Ele exibe uma saudação simples e uma mensagem de boas-vindas.
"""
import streamlit as st

# Título da aplicação
st.title("Minha primeira aplicação com Streamlit")

# Adicione um texto
st.write("Olá, mundo!")

# Adicione um gráfico
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
st.line_chart(df)

# Adicione um botão
if st.button('Saudação'):
    st.write('Olá, Streamlit!')

