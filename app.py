"""
Este módulo contém o código para o meu aplicativo Streamlit.
Ele exibe inputs e permite gravação de dados.
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
st.header('Adicionar Usuário')
nome = st.text_input('Nome')
salario_mensal = st.number_input('Salário Mensal', min_value=0.0)
if st.button('Adicionar Usuário') and nome and salario_mensal:
    adicionar_usuario(nome, salario_mensal)

# Página de adicionar gasto
st.header('Adicionar Gasto')
valor = st.number_input('Valor', min_value=0.0)
data = st.date_input('Data')
id_usuario_gasto = st.number_input('ID do Usuário')
if st.button('Adicionar Gasto') and valor and data and id_usuario_gasto:
    adicionar_gasto(valor, str(data), id_usuario_gasto)

# Página de adicionar despesa
st.header('Adicionar Despesa')
valor = st.number_input('Valor', min_value=0.0)
id_categoria = st.number_input('ID da Categoria')
id_usuario_despesa = st.number_input('ID do Usuário')
if st.button('Adicionar Despesa') and valor and id_categoria and id_usuario_despesa:
    adicionar_despesa(valor, id_categoria, id_usuario_despesa)

# Página de adicionar meta
st.header('Adicionar Meta')
nome = st.text_input('Nome')
valor = st.number_input('Valor', min_value=0.0)
id_usuario_meta = st.number_input('ID do Usuário')
if st.button('Adicionar Meta') and nome and valor and id_usuario_meta:
    adicionar_meta(nome, valor, id_usuario_meta)

# Página de visualizar gastos
st.header('Visualizar Gastos')
id_usuario_visualizacao = st.number_input('ID do Usuário')
if st.button('Visualizar Gastos') and id_usuario_visualizacao:
    visualizar_gastos(id_usuario_visualizacao)

# Fecha a conexão com o banco de dados
conn.close()
