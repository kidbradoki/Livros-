import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Conteúdo do livro
BOOK_TEXT = """
Capítulo 1
Era uma vez um leitor que precisava salvar sua página automaticamente.
Este app faz exatamente isso.
""" * 50

@app.route('/')
def home():
    return render_template('index.html', book_text=BOOK_TEXT)

@app.route('/save_position', methods=['POST'])
def save_position():
    data = request.json
    position = data.get('position', 0)
    print(f'Posição salva: {position}')
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Esta é a parte que falta! O Render precisa disto:
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
