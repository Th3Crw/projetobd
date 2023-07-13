from flask import Blueprint, render_template, Flask, request, flash
import mysql.connector

views = Blueprint('views', __name__)

def get_connection():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'avaliacao_unb'
    }
    return mysql.connector.connect(**config)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/avaliar', methods=['GET', 'POST'])
def avaliar():
    if request.method == 'GET':
        connection = get_connection()
        cursor = connection.cursor()

        select_estudantes_query = "SELECT id, nome FROM Estudantes"
        cursor.execute(select_estudantes_query)
        estudantes = cursor.fetchall()

        select_disciplinas_query = "SELECT id, nome FROM Disciplinas"
        cursor.execute(select_disciplinas_query)
        disciplinas = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('avaliar.html', estudantes=estudantes, disciplinas=disciplinas)
    
    elif request.method == 'POST':
        nome_estudante = request.form.get('nome')
        senha = request.form.get('senha')
        disciplina = request.form.get('disciplina')
        nota = request.form.get('nota')
        comentario = request.form.get('comentario')

        connection = get_connection()
        cursor = connection.cursor()

        select_estudante_query = "SELECT senha FROM Estudantes WHERE id = %s"
        cursor.execute(select_estudante_query, (nome_estudante,))
        estudante = cursor.fetchone()

        if estudante and senha == estudante[0]:
            insert_avaliacao_query = "INSERT INTO Avaliacoes (estudante_id, disciplina_id, nota, comentario) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_avaliacao_query, (nome_estudante, disciplina, nota, comentario))
            connection.commit()

            cursor.close()
            connection.close()

            flash("Avaliação cadastrada com sucesso!", category="success")
        else:
            flash("Senha incorreta!", category="error")
    return render_template('avaliar.html')

@views.route('/avaliacoes')
def avaliacoes():
    connection = get_connection()
    cursor = connection.cursor()

    select_query = """
    SELECT Avaliacoes.id, Estudantes.nome, Disciplinas.nome, Turmas.semestre, Professores.nome, Avaliacoes.nota, Avaliacoes.comentario
    FROM Avaliacoes
    INNER JOIN Estudantes ON Avaliacoes.estudante_id = Estudantes.id
    INNER JOIN Turmas ON Avaliacoes.turma_id = Turmas.id
    INNER JOIN Disciplinas ON Turmas.disciplina_id = Disciplinas.id
    INNER JOIN Professores ON Turmas.professor_id = Professores.id
    """
    cursor.execute(select_query)
    avaliacoes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('avaliacoes.html', avaliacoes=avaliacoes)
