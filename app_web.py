from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    return send_from_directory('templates', 'index.html')

@app.route('/static/evidencia.jpg')
def serve_image():
    if os.path.exists('evidencia_rescate.jpg'):
        return send_from_directory('.', 'evidencia_rescate.jpg')
    else:
        return "Aún no hay evidencia. El dron está escaneando.", 404

if __name__ == '__main__':
    print("=======================================")
    print(" INICIANDO SERVIDOR WEB DE NATALY...   ")
    print(" Abre tu navegador en: http://localhost:5000")
    print("=======================================")
    app.run(host='0.0.0.0', port=5000, debug=False)
