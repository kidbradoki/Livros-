import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulação de conteúdo do livro (Você pode trocar por um texto real depois)
BOOK_TEXT = """
Capítulo 1: O Início do Projeto

Este é o seu leitor de livros personalizado rodando diretamente na nuvem.
O objetivo deste código é salvar sua posição automaticamente.

Role para baixo para testar...

""" + ("\nEsta é uma linha de exemplo para criar volume de leitura e testar o scroll automático do seu app.\n" * 100)

@app.route('/')
def home():
    # Passamos o texto para o HTML
    return render_template('index.html', book_text=BOOK_TEXT)

@app.route('/save_position', methods=['POST'])
def save_position():
    data = request.json
    position = data.get('position', 0)
    
    # O log aparece no painel do Railway (View Logs)
    print(f'==> Analista Ghost: Posição {position} recebida via API.')
    
    return jsonify({'status': 'success', 'received': position})

if __name__ == '__main__':
    # Configuração vital para o Railway e outros servidores de nuvem
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
