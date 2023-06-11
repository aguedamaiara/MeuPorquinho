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
            descricao TEXT,
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

# Função para buscar o ID do usuário com base no nome
def buscar_id_usuario(conn, nome):
    cursor = conn.cursor()
    cursor.execute('SELECT id_usuario FROM Usuario WHERE nome = ?', (nome,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

# Função para adicionar um gasto
def adicionar_gasto(conn, valor, descricao, data, nome_usuario):
    cursor = conn.cursor()
    id_usuario = buscar_id_usuario(conn, nome_usuario)
    if id_usuario is None:
        st.error(f'Usuário "{nome_usuario}" não encontrado.')
        return
    cursor.execute('INSERT INTO Gasto (valor, descricao, data, id_usuario) VALUES (?, ?, ?, ?)', (valor, descricao, data, id_usuario))
    conn.commit()
    st.success('Gasto adicionado com sucesso!')




# Função para visualizar os gastos registrados no sistema
def visualizar_gastos(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT valor, descricao, data FROM Gasto')
    gastos = cursor.fetchall()
    if gastos:
        st.subheader('Gastos Registrados')
        for gasto in gastos:
            st.write('Valor:', gasto[0])
            st.write('Descrição:', gasto[1])
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
        descricao = st.text_input('Descrição')
        data = st.date_input('Data')
        if st.form_submit_button('Adicionar Gasto') and valor and descricao and data:
            adicionar_gasto(conn, valor, descricao, str(data))

    with st.form('visualizar_gastos_form'):
        st.header('Visualizar Gastos')
        if st.form_submit_button('Visualizar Gastos'):
            visualizar_gastos(conn)

    conn.close()

exibir_interface()
