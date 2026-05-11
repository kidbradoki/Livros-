
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulação de conteúdo do livro
BOOK_TEXT = """
Capítulo 1

Era uma vez um leitor que precisava salvar sua página automaticamente.

Este app faz exatamente isso.

Você pode continuar adicionando texto do livro aqui.

""" * 50

@app.route('/')
def home():
    # Garanta que o arquivo index.html esteja na pasta /templates
    return render_template('index.html', book_text=BOOK_TEXT)

@app.route('/save_position', methods=['POST'])
def save_position():
    data = request.json
    position = data.get('position', 0)

    # O print aparecerá nos logs do Render
    print(f'Posição salva: {position}')

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # CRUCIAL PARA O RENDER: O servidor precisa ler a porta dinâmica
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
