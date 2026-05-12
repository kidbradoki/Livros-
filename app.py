<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Biblioteca</title>
    <style>
        body { font-family: sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #2c3e50; }
        .upload-section { border: 2px dashed #ccc; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 20px; }
        .btn-upload { background: #28a745; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }
        .livro-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid #eee; }
        .btn-ler { text-decoration: none; background: #007bff; color: white; padding: 6px 12px; border-radius: 4px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📚 Meus Livros</h2>
        <div class="upload-section">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" required>
                <button type="submit" class="btn-upload">Enviar PDF</button>
            </form>
        </div>
        <div>
            {% for livro in livros %}
            <div class="livro-item">
                <span style="font-size: 14px; max-width: 60%; overflow: hidden;">{{ livro['titulo'] }}</span>
                <a href="/ler/{{ livro['id'] }}" class="btn-ler">Ler</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
