import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações de caminhos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'biblioteca.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria a pasta de uploads se não existir para evitar erros de escrita
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inicialização do Banco de Dados
with get_db() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT)')
    conn.commit()

@app.route('/')
def index():
    db = get_db()
    livros = db.execute('SELECT id, titulo FROM livros').fetchall()
    # Enviamos 'livros' (lista), não 'livro' (único)
    return render_template('biblioteca.html', livros=livros)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        db = get_db()
        db.execute('INSERT INTO livros (titulo) VALUES (?)', (filename,))
        db.commit()
    return redirect(url_for('index'))

@app.route('/ler/<int:id>')
def ler(id):
    db = get_db()
    # Busca apenas o livro clicado. Aqui a variável 'livro' é definida.
    livro = db.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    if livro:
        return render_template('leitor.html', livro=livro)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
