import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2 # Instale com: pip install PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializa o Banco de Dados SQLite
def init_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros 
                      (id INTEGER PRIMARY KEY, titulo TEXT, conteudo TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS progresso 
                      (livro_id INTEGER PRIMARY KEY, posicao INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return render_template('index.html', livros=livros)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files: return "Nenhum arquivo"
    file = request.files['file']
    if file.filename == '': return "Nome vazio"
    
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    # Extrair texto do PDF
    texto = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text() + "\n"

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livros (titulo, conteudo) VALUES (?, ?)", (filename, texto))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/ler/<int:id>')
def ler(id):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, conteudo FROM livros WHERE id=?", (id,))
    livro = cursor.fetchone()
    cursor.execute("SELECT posicao FROM progresso WHERE livro_id=?", (id,))
    pos = cursor.fetchone()
    conn.close()
    return render_template('leitor.html', livro=livro, id=id, pos=pos[0] if pos else 0)

@app.route('/salvar', methods=['POST'])
def salvar():
    data = request.json
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO progresso (livro_id, posicao) VALUES (?, ?)", 
                   (data['id'], data['pos']))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
