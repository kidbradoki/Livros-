
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
    return render_template('index.html', book_text=BOOK_TEXT)


@app.route('/save_position', methods=['POST'])
def save_position():
    data = request.json
    position = data.get('position', 0)

    # Aqui você poderia salvar em banco de dados
    print(f'Posição salva: {position}')

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
