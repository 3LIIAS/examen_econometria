import webbrowser
from app import app

if __name__ == '__main__':
    # Abre el navegador automáticamente
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
