from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

# Ruta fija de tus libros
carpeta_general = "C:/Users/jahib/Documents/mis_libros"

if not os.path.exists(carpeta_general):
    print("La carpeta no existe.")
    exit()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = carpeta_general

# Ruta principal
@app.route('/')
def index():
    categorias = {}
    for categoria in os.listdir(app.config['UPLOAD_FOLDER']):
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], categoria)
        if os.path.isdir(ruta):
            archivos = os.listdir(ruta)
            categorias[categoria] = archivos
    return render_template('index.html', categorias=categorias)

# Subir archivo
@app.route('/upload', methods=['POST'])
def upload():
    archivo = request.files['libro']
    categoria = request.form['categoria'].strip()
    ruta_categoria = os.path.join(app.config['UPLOAD_FOLDER'], categoria)
    os.makedirs(ruta_categoria, exist_ok=True)
    archivo_path = os.path.join(ruta_categoria, secure_filename(archivo.filename))
    archivo.save(archivo_path)
    return redirect('/')

# Ver archivo PDF (abrir en iframe)
@app.route('/ver/<categoria>/<archivo>')
def ver_pdf(categoria, archivo):
    ruta_categoria = os.path.join(app.config['UPLOAD_FOLDER'], categoria)
    return send_from_directory(ruta_categoria, archivo)

# Descargar (opcional)
@app.route('/libros/<categoria>/<archivo>')
def descargar(categoria, archivo):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], categoria), archivo)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
