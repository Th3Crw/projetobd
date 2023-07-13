from flask import Blueprint, render_template, request, flash
import mysql.connector

auth = Blueprint('auth', __name__)

def get_connection():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'avaliacao_unb'
    }
    return mysql.connector.connect(**config)


def obter_dados():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tabela"
    cursor.execute(query)
    dados = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return dados

def inserir_dados_estudante(nome, email, matricula, curso, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO Estudantes (nome, email, matricula, curso, senha) VALUES ('{nome}', '{email}','{matricula}','{curso}','{senha}')"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('password')
        connection = get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM Estudantes WHERE matricula = %s AND senha = %s"
        values = (matricula, senha)

        cursor.execute(select_query, values)
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            flash("Login realizado com sucesso", category="success")
            return render_template('home.html')
        else:
            flash("Matrícula ou senha inválida", category="error")

    return render_template('login.html')

@auth.route('/logout')
def logout():
    flash("Deslogado com Sucesso", category="success")
    return render_template('home.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        matricula = request.form.get('matricula')
        curso = request.form.get('curso')
        senha = request.form.get('password1')
        confirma_senha = request.form.get('password2')

        if len(nome) < 3:
            flash("Insira um nome válido", category="error")
        elif len(email) < 4:
            flash("Insira um email válido", category="error")
        elif len(senha)< 3:
            flash("Digite uma senha válida", category="error")
        elif senha != confirma_senha:
            flash("A confirmação da senha deve ser igual à senha", category="error")
        else:
            inserir_dados_estudante(nome, email, matricula, curso, senha)
            flash("Usuário cadastrado com sucesso", category="success")
    
    return render_template('signup.html')
