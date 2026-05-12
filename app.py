import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Interface do Leitor GHOST v1.1
H = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GHOST Reader v1.1</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
    <style>
        body { background: #0a0a0a; color: #00FF41; font-family: 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        header { background: #000; padding: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #00FF41; box-shadow: 0 0 15px rgba(0,255,65,0.2); }
        #viewer-container { flex: 1; overflow: auto; display: flex; justify-content: center; background: #111; padding: 10px; }
        canvas { box-shadow: 0 0 30px rgba(0,0,0,0.8); border: 1px solid #333; max-width: 100%; }
        .controls { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px; background: rgba(0,0,0,0.9); padding: 12px 25px; border-radius: 50px; border: 1px solid #00FF41; backdrop-filter: blur(5px); }
        button { background: #00FF41; color: #000; border: none; padding: 8px 18px; border-radius: 15px; cursor: pointer; font-weight: bold; text-transform: uppercase; font-size: 0.7rem; }
        button:active { transform: scale(0.95); }
        input[type="file"] { display: none; }
        #page-info { font-size: 0.8rem; align-self: center; letter-spacing: 1px; }
    </style>
</head>
<body>

<header>
    <span style="letter-spacing: 2px;">[ GHOST_READER_V1.1 ]</span>
    <button onclick="document.getElementById('file-input').click()">CARREGAR_ALVO</button>
    <input type="file" id="file-input" accept="application/pdf">
</header>

<div id="viewer-container">
    <canvas id="pdf-canvas"></canvas>
</div>

<div class="controls">
    <button onclick="prevPage()"> << </button>
    <span id="page-info">PAG: <span id="page-num">1</span> / <span id="page-count">0</span></span>
    <button onclick="nextPage()"> >> </button>
</div>

<script>
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';

    let pdfDoc = null, pageNum = 1, currentBookId = "";
    const canvas = document.getElementById('pdf-canvas'), ctx = canvas.getContext('2d');

    function renderPage(num) {
        pdfDoc.getPage(num).then(page => {
            const viewport = page.getViewport({scale: 1.5});
            canvas.height = viewport.height; canvas.width = viewport.width;
            page.render({ canvasContext: ctx, viewport: viewport }).promise.then(() => {
                // SALVA O PROGRESSO USANDO O NOME DO LIVRO COMO CHAVE
                localStorage.setItem('ghost_p_' + currentBookId, num);
            });
        });
        document.getElementById('page-num').textContent = num;
    }

    document.getElementById('file-input').addEventListener('change', e => {
        const file = e.target.files[0];
        if (file) {
            currentBookId = btoa(file.name); // Cria um ID único baseado no nome do arquivo
            const reader = new FileReader();
            reader.onload = function() {
                pdfjsLib.getDocument(new Uint8Array(this.result)).promise.then(pdf => {
                    pdfDoc = pdf;
                    document.getElementById('page-count').textContent = pdf.numPages;
                    
                    // RECUPERA A PÁGINA ESPECÍFICA DESTE LIVRO
                    const saved = localStorage.getItem('ghost_p_' + currentBookId);
                    pageNum = saved ? parseInt(saved) : 1;
                    renderPage(pageNum);
                });
            };
            reader.readAsArrayBuffer(file);
        }
    });

    function prevPage() { if (pageNum <= 1) return; pageNum--; renderPage(pageNum); }
    function nextPage() { if (pageNum >= pdfDoc.numPages) return; pageNum++; renderPage(pageNum); }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(H)

if __name__ == '__main__':
    # Configuração correta para o Railway ler a porta dinâmica
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
