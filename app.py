import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)

# Configurações de caminhos absolutos para o Railway
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'biblioteca.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados
def init_db():
    with get_db() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, conteudo TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS progresso (id_livro INTEGER PRIMARY KEY, posicao INTEGER, dark_mode INTEGER DEFAULT 0)')
        conn.commit()

init_db()

# Rota para servir os arquivos PDF originais (resolve o problema das imagens)
@app.route('/uploads/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    db = get_db()
    livros = db.execute('SELECT id, titulo FROM livros').fetchall()
    return render_template('biblioteca.html', livros=livros)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        # Mantemos a extração de texto para busca, mas exibiremos o PDF real
        texto = ""
        try:
            with open(path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                for page in pdf.pages:
                    texto += page.extract_text() + "\n"
            
            db = get_db()
            db.execute('INSERT INTO livros (titulo, conteudo) VALUES (?, ?)', (filename, texto))
            db.commit()
        except Exception as e:
            print(f"Erro no processamento: {e}")
                
    return redirect(url_for('index'))

@app.route('/ler/<int:id>')
def ler(id):
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
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
