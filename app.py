import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração de onde as fotos serão salvas
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões de arquivos permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Garantir que a pasta de uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Agora ele vai carregar o arquivo index.html em vez de só mostrar um texto
    return render_template('index.html')

@app.route('/enviar', methods=['GET', 'POST'])
def enviar_acao():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'foto' not in request.files:
            return "Nenhuma foto enviada"

        file = request.files['foto']
        descricao = request.form.get('descricao')

        if file and allowed_file(file.filename):
            # Limpa o nome do arquivo por segurança
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Aqui no futuro você salvaria 'filename' e 'descricao' no banco de dados
            print(f"Ação recebida: {descricao}. Foto salva como: {filename}")

            return "Sua ação foi enviada com sucesso! Aguarde a moderação para ganhar seus pontos."

        return render_template('enviar.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

if __name__ == '__main__':
    app.run(debug=True)
