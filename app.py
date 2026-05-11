import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BOOK_TEXT = """
Capítulo 1: O Recomeço
Aqui começa o seu novo livro. Este texto será exibido no navegador
e a sua posição de leitura será salva automaticamente.
""" * 100  # Multiplicado para gerar scroll

@app.route('/')
def home():
    return render_template('index.html', book_text=BOOK_TEXT)

@app.route('/save_position', methods=['POST'])
def save_position():
    data = request.json
    position = data.get('position', 0)
    print(f"Posição recebida: {position}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
