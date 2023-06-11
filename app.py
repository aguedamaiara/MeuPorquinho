import sqlite3
import streamlit as st

# Função para criar a conexão com o banco de dados
def criar_conexao():
    conn = sqlite3.connect('meu_porquinho.db')
    return conn

# Função para criar as tabelas se não existirem
def criar_tabelas(conn):
    cursor = conn.cursor()
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

    # Crie as outras tabelas...

# Função para adicionar um usuário
def adicionar_usuario(conn, nome, salario_mensal):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuario (nome, salario_mensal) VALUES (?, ?)', (nome, salario_mensal))
    conn.commit()
    st.success('Usuário adicionado com sucesso!')

# Função para adicionar um gasto
def adicionar_gasto(conn, valor, data, id_usuario):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Gasto (valor, data, id_usuario) VALUES (?, ?, ?)', (valor, data, id_usuario))
    conn.commit()
    st.success('Gasto adicionado com sucesso!')

# Função para visualizar os gastos de um usuário
# Função para visualizar os gastos de um usuário
def visualizar_gastos(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id_gasto, valor, data FROM Gasto')
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
def exibir_interface():
    conn = criar_conexao()
    criar_tabelas(conn)

    st.title('Meu Porquinho - App de Planejamento Financeiro')

    with st.form('adicionar_usuario_form'):
        st.header('Adicionar Usuário')
        nome = st.text_input('Nome')
        salario_mensal = st.number_input('Salário Mensal', min_value=0.0)
        if st.form_submit_button('Adicionar Usuário') and nome and salario_mensal:
            adicionar_usuario(conn, nome, salario_mensal)

    with st.form('adicionar_gasto_form'):
        st.header('Adicionar Gasto')
        valor = st.number_input('Valor', min_value=0.0)
        data = st.date_input('Data')
        id_usuario_gasto = st.number_input('ID do Usuário')
        if st.form_submit_button('Adicionar Gasto') and valor and data and id_usuario_gasto:
            adicionar_gasto(conn, valor, str(data), id_usuario_gasto)

    with st.form('visualizar_gastos_form'):
        st.header('Visualizar Gastos')
        id_usuario_visualizacao = st.number_input('ID do Usuário')
        if st.form_submit_button('Visualizar Gastos') and id_usuario_visualizacao:
            visualizar_gastos(conn, id_usuario_visualizacao)

    conn.close()

exibir_interface()
