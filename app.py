import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados
with get_db() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY, titulo TEXT, conteudo TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS progresso (id_livro INTEGER PRIMARY KEY, posicao INTEGER, dark_mode INTEGER)')

@app.route('/')
def biblioteca():
    db = get_db()
    livros = db.execute('SELECT * FROM livros').fetchall()
    return render_template('biblioteca.html', livros=livros)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        texto = ""
        with open(path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                texto += page.extract_text() + "\n"
        
        db = get_db()
        db.execute('INSERT INTO livros (titulo, conteudo) VALUES (?, ?)', (filename, texto))
        db.commit()
    return redirect(url_for('biblioteca'))

@app.route('/ler/<int:id>')
def leitor(id):
    db = get_db()
    livro = db.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    progresso = db.execute('SELECT * FROM progresso WHERE id_livro = ?', (id,)).fetchone()
    return render_template('leitor.html', livro=livro, progresso=progresso)

@app.route('/salvar_progresso', methods=['POST'])
def salvar():
    data = request.json
    db = get_db()
    db.execute('INSERT OR REPLACE INTO progresso (id_livro, posicao, dark_mode) VALUES (?, ?, ?)',
               (data['id'], data['pos'], data['dark']))
    db.commit()
    return jsonify({"status": "salvo"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
