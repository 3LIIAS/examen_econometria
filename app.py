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
        fecha_inicio = request.form.get('fecha_inicio', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Respuestas
        respuesta_ventas = request.form.get('respuesta_ventas', '')
        respuesta_empleo = request.form.get('respuesta_empleo', '')
        respuesta_correlograma = request.form.get('respuesta_correlograma', '')
        respuesta_logempleo = request.form.get('respuesta_logempleo', '')

        # Evaluar contenido
        respuestas = [respuesta_ventas, respuesta_empleo, respuesta_correlograma, respuesta_logempleo]
        completadas = sum(1 for r in respuestas if r and len(r.strip()) >= 10)
        porcentaje = int((completadas / 4) * 100)

        if porcentaje >= 85:
            mensaje = "¡Muy bien! Tus respuestas están completas y bien desarrolladas."
        elif porcentaje >= 60:
            mensaje = "Has cubierto parte del examen, pero podrías desarrollar mejor tus respuestas."
        else:
            mensaje = "Revisa y asegúrate de responder con más profundidad."

        # Guardar CSV
        archivo_csv = 'respuestas_examen.csv'
        existe = os.path.isfile(archivo_csv)

        with open(archivo_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not existe:
                writer.writerow(['Nombre', 'Fecha Inicio', 'Fecha Envío',
                                 'Pregunta 1', 'Pregunta 2', 'Pregunta 3', 'Pregunta 4'])
            writer.writerow([nombre, fecha_inicio, fecha_envio,
                             respuesta_ventas, respuesta_empleo, respuesta_correlograma, respuesta_logempleo])

        return render_template('gracias.html', nombre=nombre, porcentaje=porcentaje, mensaje=mensaje)

    return render_template('examen.html', fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
