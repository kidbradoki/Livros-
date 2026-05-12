import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Interface do Leitor GHOST v1.0
H = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GHOST Reader v1.0</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
    <style>
        body { background: #1a1a1a; color: #ccc; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        header { background: #000; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #00FF41; }
        #viewer-container { flex: 1; overflow: auto; display: flex; justify-content: center; background: #333; }
        canvas { box-shadow: 0 0 20px rgba(0,0,0,0.5); margin: 20px 0; max-width: 100%; }
        .controls { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; background: rgba(0,0,0,0.8); padding: 10px; border-radius: 30px; border: 1px solid #00FF41; }
        button { background: #00FF41; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        input[type="file"] { display: none; }
        #page-info { color: #00FF41; font-family: monospace; align-self: center; }
    </style>
</head>
<body>

<header>
    <span style="color:#00FF41; font-weight:bold;">GHOST READER</span>
    <button onclick="document.getElementById('file-input').click()">ABRIR LIVRO</button>
    <input type="file" id="file-input" accept="application/pdf">
</header>

<div id="viewer-container">
    <canvas id="pdf-canvas"></canvas>
</div>

<div class="controls">
    <button onclick="prevPage()"> < </button>
    <span id="page-info">Pág: <span id="page-num">1</span> / <span id="page-count">0</span></span>
    <button onclick="nextPage()"> > </button>
    <button onclick="saveMark()" style="background:#ffcc00">GRIFAR</button>
</div>

<script>
    let pdfDoc = null,
        pageNum = 1,
        pageRendering = false,
        pageNumPending = null,
        canvas = document.getElementById('pdf-canvas'),
        ctx = canvas.getContext('2d');

    // Função para renderizar a página
    function renderPage(num) {
        pageRendering = true;
        pdfDoc.getPage(num).then(page => {
            const viewport = page.getViewport({scale: 1.5});
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            const renderContext = { canvasContext: ctx, viewport: viewport };
            const renderTask = page.render(renderContext);

            renderTask.promise.then(() => {
                pageRendering = false;
                if (pageNumPending !== null) {
                    renderPage(pageNumPending);
                    pageNumPending = null;
                }
                // SALVA O PROGRESSO AUTOMATICAMENTE
                localStorage.setItem('ghost_last_page', num);
            });
        });
        document.getElementById('page-num').textContent = num;
    }

    // Carregar o PDF selecionado
    document.getElementById('file-input').addEventListener('change', e => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function() {
                const typedarray = new Uint8Array(this.result);
                pdfjsLib.getDocument(typedarray).promise.then(pdf => {
                    pdfDoc = pdf;
                    document.getElementById('page-count').textContent = pdf.numPages;
                    
                    // VERIFICA SE JÁ EXISTE PÁGINA SALVA
                    const savedPage = localStorage.getItem('ghost_last_page');
                    pageNum = savedPage ? parseInt(savedPage) : 1;
                    
                    renderPage(pageNum);
                });
            };
            reader.readAsArrayBuffer(file);
        }
    });

    function prevPage() { if (pageNum <= 1) return; pageNum--; renderPage(pageNum); }
    function nextPage() { if (pageNum >= pdfDoc.numPages) return; pageNum++; renderPage(pageNum); }

    // Placeholder para função de grifar (usaremos camadas de desenho na v2)
    function saveMark() {
        alert("Modo Grifar: Selecione o texto (Em desenvolvimento na v1.1)");
    }
</script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(H)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
