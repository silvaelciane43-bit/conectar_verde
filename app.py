import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Configuração correta do Flask
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = CURRENT_DIR  # Os templates estão na raiz
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Configuração de onde as fotos serão salvas
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

# Extensões de arquivos permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Garantir que a pasta de uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/perfil")
def perfil():
    return render_template("profile.html")


@app.route("/enviar", methods=["GET", "POST"])
def enviar_acao():
    if request.method == "POST":
        try:
            # Verifica se o arquivo foi enviado
            if "foto" not in request.files:
                return render_template("enviar.html", erro="Nenhuma foto foi enviada!")

            file = request.files["foto"]
            descricao = request.form.get("descricao", "").strip()

            # Validação
            if not descricao:
                return render_template(
                    "enviar.html", erro="Por favor, descreva sua ação!"
                )

            if not file or file.filename == "":
                return render_template(
                    "enviar.html", erro="Por favor, selecione uma imagem!"
                )

            if not allowed_file(file.filename):
                return render_template(
                    "enviar.html",
                    erro="Formato de arquivo não permitido! Use PNG, JPG, JPEG ou GIF.",
                )

            # Limpa o nome do arquivo por segurança
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Log da ação
            print(f"✅ Ação recebida: {descricao}. Foto salva como: {filename}")

            return render_template(
                "sucesso.html", descricao=descricao, arquivo=filename
            )

        except Exception as e:
            print(f"❌ Erro ao enviar: {str(e)}")
            return render_template(
                "enviar.html", erro=f"Erro ao enviar a ação. Tente novamente."
            )

    return render_template("enviar.html")


@app.route("/ranking")
def ranking():
    return render_template("ranking.html")


if __name__ == "__main__":
    print(f"📁 Template folder: {TEMPLATE_DIR}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print("🚀 Iniciando servidor...")
    app.run(debug=True, host="127.0.0.1", port=5000)
