"""
Este módulo contém o código para o meu aplicativo Streamlit.
Ele exibe uma saudação simples e uma mensagem de boas-vindas.
"""
import sqlite3

banco = sqlite3.connect('primeiro_projeto.db')

cursor = banco.cursor()

#cursor.execute("CREATE TABLE usuarios(id_usuari integer, name text, salario_mensal float)")

cursor.execute("INSERT INTO usuarios VALUES(01,'MARIA',1500)")

banco.commit()
 

cursor.execute("SELECT *FROM usuarios")
print(cursor.fetchall())
