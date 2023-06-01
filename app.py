"""
Este módulo contém o código para o meu aplicativo Streamlit.
Ele exibe inputs e permite gravação de dados.
Data da ultima att: 01/06/2023
"""
import sqlite3
import streamlit as st

# Cria a conexão com o banco de dados
conn = sqlite3.connect('meu_porquinho.db')
cursor = conn.cursor()

# Cria as tabelas se não existirem
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario INTEGER PRIMARY KEY,
        nome TEXT,
        salario_mensal REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gasto (
        id_gasto INTEGER PRIMARY KEY,
        valor REAL,
        data TEXT,
        id_usuario INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categoria (
        id_categoria INTEGER PRIMARY KEY,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Despesa (
        id_despesa INTEGER PRIMARY KEY,
        valor REAL,
        id_categoria INTEGER,
        id_usuario INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES Categoria (id_categoria),
        FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meta (
        id_meta INTEGER PRIMARY KEY,
        nome TEXT,
        valor REAL,
        id_usuario INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario)
    )
''')

# Função para adicionar um usuário
def adicionar_usuario(nome, salario_mensal):
    cursor.execute('INSERT INTO Usuario (nome, salario_mensal) VALUES (?, ?)', (nome, salario_mensal))
    conn.commit()
    st.success('Usuário adicionado com sucesso!')

# Função para adicionar um gasto
def adicionar_gasto(valor, data, id_usuario):
    cursor.execute('INSERT INTO Gasto (valor, data, id_usuario) VALUES (?, ?, ?)', (valor, data, id_usuario))
    conn.commit()
    st.success('Gasto adicionado com sucesso!')

# Função para adicionar uma despesa
def adicionar_despesa(valor, id_categoria, id_usuario):
    cursor.execute('INSERT INTO Despesa (valor, id_categoria, id_usuario) VALUES (?, ?, ?)', (valor, id_categoria, id_usuario))
    conn.commit()
    st.success('Despesa adicionada com sucesso!')

# Função para adicionar uma meta
def adicionar_meta(nome, valor, id_usuario):
    cursor.execute('INSERT INTO Meta (nome, valor, id_usuario) VALUES (?, ?, ?)', (nome, valor, id_usuario))
    conn.commit()
    st.success('Meta adicionada com sucesso!')

# Função para visualizar os gastos de um usuário
def visualizar_gastos(id_usuario):
    cursor.execute('SELECT id_gasto, valor, data FROM Gasto WHERE id_usuario = ?', (id_usuario,))
    gastos = cursor.fetchall()
    if gastos:
        st.subheader('Gastos')
        for gasto in gastos:
            st.write('ID:', gasto[0])
            st.write('Valor:', gasto[1])
            st.write('Data:', gasto[2])
            st.write('---')
    else:
        st.warning('Nenhum gasto encontrado.')

# Interface com Streamlit
st.title('Meu Porquinho - App de Planejamento Financeiro')

# Página de adicionar usuário
if st.sidebar.button('Adicionar Usuário'):
    st.sidebar.subheader('Adicionar Usuário')
    nome = st.sidebar.text_input('Nome')
    salario_mensal = st.sidebar.number_input('Salário Mensal', min_value=0.0)
    if st.sidebar.button('Salvar Usuário') and nome and salario_mensal:
        adicionar_usuario(nome, salario_mensal)
  

# Página de adicionar gasto
if st.sidebar.button('Adicionar Gasto'):
    st.sidebar.subheader('Adicionar Gasto')
    valor = st.sidebar.number_input('Valor', min_value=0.0)
    data = st.sidebar.date_input('Data')
    id_usuario = st.sidebar.number_input('ID do Usuário')
    if st.sidebar.button('Salvar Gasto')  and valor and data and id_usuario:
        adicionar_gasto(valor, str(data), id_usuario)

# Página de adicionar despesa
if st.sidebar.button('Adicionar Despesa'):
    st.sidebar.subheader('Adicionar Despesa')
    valor = st.sidebar.number_input('Valor', min_value=0.0)
    id_categoria = st.sidebar.number_input('ID da Categoria')
    id_usuario = st.sidebar.number_input('ID do Usuário')
    if st.sidebar.button('Salvar Despesa') and valor and id_categoria and id_usuario:
        adicionar_despesa(valor, id_categoria, id_usuario)

# Página de adicionar meta
if st.sidebar.button('Adicionar Meta'):
    st.sidebar.subheader('Adicionar Meta')
    nome = st.sidebar.text_input('Nome')
    valor = st.sidebar.number_input('Valor', min_value=0.0)
    id_usuario = st.sidebar.number_input('ID do Usuário')
    if st.sidebar.button('Salvar Meta') and nome and valor and id_usuario:
        adicionar_meta(nome, valor, id_usuario)

# Página de visualizar gastos
if st.sidebar.button('Visualizar Gastos'):
    st.sidebar.subheader('Visualizar Gastos')
    id_usuario = st.sidebar.number_input('ID do Usuário')
    if st.sidebar.button('Salvar Gasto') and id_usuario:
        visualizar_gastos( id_usuario)

# Fecha a conexão com o banco de dados
conn.close()