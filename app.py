import os
from flask import Flask, render_template

app = Flask(__name__)

# --- ROTAS DO SISTEMA GHOST READER ---

@app.route('/')
def index():
    """Rota da tela inicial: Sua Biblioteca de Livros"""
    return render_template('biblioteca.html')

@app.route('/leitor')
def leitor():
    """Rota do motor de leitura: Onde o PDF é renderizado"""
    return render_template('leitor.html')

# --- CONFIGURAÇÃO DE SERVIDOR ---

if __name__ == '__main__':
    # O Railway fornece a porta automaticamente pela variável de ambiente PORT
    # Se não encontrar, usa a 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    
    # Rodando o servidor
    # host='0.0.0.0' é obrigatório para ser acessível externamente
    app.run(host='0.0.0.0', port=port)
