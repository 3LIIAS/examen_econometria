from flask import Flask, render_template, request
from datetime import datetime
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/examen', methods=['GET', 'POST'])
def examen():
    if request.method == 'POST':
        nombre = request.form.get('nombre', 'Anónimo')
        hora_inicio = request.form.get('hora_inicio', '')
        fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # A partir de aqui guardamos todas las respuestas del examen en variables
        respuesta_ventas = request.form.get('respuesta_ventas', '')
        respuesta_empleo = request.form.get('respuesta_empleo', '')
        respuesta_varianza = request.form.get('respuesta_varianza', '')
        respuesta_pregunta4 = request.form.get('pregunta4', '')
        respuesta_mco = request.form.get('respuesta_mco', '')
        respuesta_hipotesis = request.form.get('respuesta_hipotesis', '')
        respuesta_autocorrelacion = request.form.get('respuesta_autocorrelacion', '')

        respuestas = [
            respuesta_ventas,
            respuesta_empleo,
            respuesta_varianza,
            respuesta_pregunta4,
            respuesta_mco,
            respuesta_hipotesis,
            respuesta_autocorrelacion
        ]

        completadas = sum(1 for r in respuestas if r and len(r.strip()) >= 10)
        porcentaje = int((completadas / 7) * 100)

        if porcentaje >= 85:
            mensaje = "¡Muy bien! Tus respuestas están completas y bien desarrolladas."
        elif porcentaje >= 60:
            mensaje = "Has cubierto parte del examen, pero podrías desarrollar mejor tus respuestas."
        else:
            mensaje = "Revisa y asegúrate de responder con más profundidad."

        # Guardar en CSV
        archivo_csv = 'respuestas_examen.csv'
        existe = os.path.isfile(archivo_csv)

        with open(archivo_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not existe:
                writer.writerow([
                    'Nombre', 'Hora de inicio', 'Fecha de envío',
                    'Pregunta 1 (Ventas)', 'Pregunta 2 (Empleo)', 'Pregunta 3 (Varianza)',
                    'Pregunta 4', 'Pregunta 5 (MCO)', 'Pregunta 6 (Hipótesis)',
                    'Pregunta 7 (Autocorrelación)'
                ])
            writer.writerow([
                nombre, hora_inicio, fecha_envio,
                respuesta_ventas, respuesta_empleo, respuesta_varianza,
                respuesta_pregunta4, respuesta_mco, respuesta_hipotesis,
                respuesta_autocorrelacion
            ])

        return render_template('gracias.html', nombre=nombre, porcentaje=porcentaje, mensaje=mensaje)

    hora_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('examen.html', fecha=hora_inicio, hora_inicio=hora_inicio)
