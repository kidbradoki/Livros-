<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title> ANDRESSA Reader v1.2</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
    <style>
        body { background: #000; color: #00FF41; font-family: monospace; margin: 0; touch-action: none; }
        .topo { background: #111; padding: 10px; display: flex; justify-content: space-between; border-bottom: 1px solid #00FF41; position: sticky; top: 0; z-index: 10; }
        #canvas-container { position: relative; width: 100%; display: flex; justify-content: center; background: #111; }
        canvas { display: block; max-width: 100%; }
        /* Camada transparente para grifar */
        #highlight-canvas { position: absolute; top: 0; left: 50%; transform: translateX(-50%); cursor: crosshair; }
        .controles { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.9); padding: 10px; border-radius: 30px; border: 1px solid #00FF41; display: flex; gap: 15px; z-index: 100; }
        button { background: #00FF41; border: none; padding: 8px 15px; border-radius: 10px; font-weight: bold; cursor: pointer; color: #000; }
        .btn-limpar { background: #ff4141; color: #fff; }
    </style>
</head>
<body>
    <div class="topo">
        <a href="/" style="color: #00FF41; text-decoration: none;">< VOLTAR</a>
        <span id="book-title" style="font-size: 0.6rem; max-width: 150px; overflow: hidden;">Carregando...</span>
        <button class="btn-limpar" onclick="limparGrifos()">LIMPAR</button>
    </div>

    <div id="canvas-container">
        <canvas id="pdf-render"></canvas>
        <canvas id="highlight-canvas"></canvas>
    </div>

    <div class="controles">
        <button onclick="changePage(-1)"> << </button>
        <span id="p-num" style="align-self: center;">1</span>
        <button onclick="changePage(1)"> >> </button>
    </div>

    <script>
        const pdfData = localStorage.getItem('current_pdf');
        const pdfName = localStorage.getItem('current_pdf_name');
        const bookId = btoa(pdfName);
        let pdfDoc = null, pageNum = 1, isDrawing = false;

        const canvas = document.getElementById('pdf-render');
        const hCanvas = document.getElementById('highlight-canvas');
        const ctx = canvas.getContext('2d');
        const hCtx = hCanvas.getContext('2d');

        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';

        // Inicialização
        if (!pdfData) window.location.href = '/';
        document.getElementById('book-title').innerText = pdfName;

        pdfjsLib.getDocument(pdfData).promise.then(pdf => {
            pdfDoc = pdf;
            const saved = localStorage.getItem('p_' + bookId);
            pageNum = saved ? parseInt(saved) : 1;
            renderPage(pageNum);
        });

        function renderPage(num) {
            pdfDoc.getPage(num).then(page => {
                const viewport = page.getViewport({ scale: 1.5 });
                
                // Ajusta os dois canvas
                canvas.height = hCanvas.height = viewport.height;
                canvas.width = hCanvas.width = viewport.width;

                page.render({ canvasContext: ctx, viewport: viewport }).promise.then(() => {
                    localStorage.setItem('p_' + bookId, num);
                    carregarGrifos(num);
                });
                document.getElementById('p-num').innerText = num;
            });
        }

        // LÓGICA DO GRIFO (Touch e Mouse)
        function carregarGrifos(p) {
            const grifos = JSON.parse(localStorage.getItem('g_' + bookId + '_' + p) || "[]");
            hCtx.clearRect(0, 0, hCanvas.width, hCanvas.height);
            hCtx.strokeStyle = "rgba(255, 255, 0, 0.4)"; // Cor Amarela Transparente
            hCtx.lineWidth = 20;
            hCtx.lineCap = "round";
            
            grifos.forEach(path => {
                hCtx.beginPath();
                hCtx.moveTo(path[0].x, path[0].y);
                path.forEach(pt => hCtx.lineTo(pt.x, pt.y));
                hCtx.stroke();
            });
        }

        let currentPath = [];
        function startDrawing(e) {
            isDrawing = true;
            currentPath = [];
            const pos = getPos(e);
            hCtx.beginPath();
            hCtx.moveTo(pos.x, pos.y);
            currentPath.push(pos);
        }

        function draw(e) {
            if (!isDrawing) return;
            const pos = getPos(e);
            hCtx.lineTo(pos.x, pos.y);
            hCtx.stroke();
            currentPath.push(pos);
        }

        function stopDrawing() {
            if (!isDrawing) return;
            isDrawing = false;
            const key = 'g_' + bookId + '_' + pageNum;
            const grifos = JSON.parse(localStorage.getItem(key) || "[]");
            grifos.push(currentPath);
            localStorage.setItem(key, JSON.stringify(grifos));
        }

        function getPos(e) {
            const rect = hCanvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return { x: clientX - rect.left, y: clientY - rect.top };
        }

        function limparGrifos() {
            if(confirm("Limpar marcações desta página?")) {
                localStorage.removeItem('g_' + bookId + '_' + pageNum);
                renderPage(pageNum);
            }
        }

        function changePage(delta) {
            if (!pdfDoc || (pageNum + delta < 1) || (pageNum + delta > pdfDoc.numPages)) return;
            pageNum += delta;
            renderPage(pageNum);
        }

        // Eventos
        hCanvas.addEventListener('mousedown', startDrawing);
        hCanvas.addEventListener('mousemove', draw);
        window.addEventListener('mouseup', stopDrawing);
        hCanvas.addEventListener('touchstart', startDrawing);
        hCanvas.addEventListener('touchmove', draw);
        hCanvas.addEventListener('touchend', stopDrawing);
    </script>
</body>
</html>
