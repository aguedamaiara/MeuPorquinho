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


# Função para visualizar os gastos registrados no sistema para um usuário específico
def visualizar_gastos_usuario(conn, nome_usuario):
    cursor = conn.cursor()
    id_usuario = buscar_id_usuario(conn, nome_usuario)
    if id_usuario is None:
        st.error(f'Usuário "{nome_usuario}" não encontrado.')
        return
    cursor.execute('SELECT valor, descricao, data FROM Gasto WHERE id_usuario = ?', (id_usuario,))
    gastos = cursor.fetchall()
    if gastos:
        st.subheader(f'Gastos Registrados para {nome_usuario}')
        for gasto in gastos:
            st.write('Valor:', gasto[0])
            st.write('Descrição:', gasto[1])
            st.write('Data:', gasto[2])
            st.write('---')
    else:
        st.warning(f'Nenhum gasto encontrado para {nome_usuario}.')

# Função para buscar todos os nomes de usuários no banco de dados
def buscar_nomes_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM Usuario')
    nomes = cursor.fetchall()
    nomes = [nome[0] for nome in nomes]
    return nomes

# Interface com Streamlit
def exibir_interface():
    conn = criar_conexao()
    criar_tabelas(conn)

    # Adicionando a imagem
    st.image('https://i.imgur.com/XBNjQCE.png')
    
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
        nome_usuario = st.text_input('Nome do usuário')
        if st.form_submit_button('Adicionar Gasto') and valor and descricao and data and nome_usuario:
            adicionar_gasto(conn, valor, descricao, str(data), nome_usuario)

    with st.form('visualizar_gastos_form'):
        st.header('Visualizar Gastos')
        nomes_usuarios = buscar_nomes_usuarios(conn)
        nome_usuario = st.radio('Selecione um usuário', nomes_usuarios)
        if st.form_submit_button('Visualizar Gastos'):
            visualizar_gastos_usuario(conn, nome_usuario)

    conn.close()


exibir_interface()
