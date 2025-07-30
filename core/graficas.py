import psycopg2
import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from django.http import HttpResponse
from django.shortcuts import render

def conectar():
    try:
        conexion = psycopg2.connect(
            host="192.168.1.11",
            database="bdTransferP",
            user="postgres",
            password="admin",
            port="5432"
        )
        conexion.set_client_encoding('UTF8')
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None

def grafica_base64(fig):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    imagen_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(imagen_png).decode('utf-8')

def obtener_datos_edad_equipo():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT e.nombre AS equipo, ROUND(AVG(j.edad), 1) AS promedio_edad
        FROM jugador j
        JOIN detalle_jugador dj ON j.id_jugador = dj.id_jugador
        JOIN equipos e ON dj.id_equipo = e.id_equipo
        GROUP BY e.nombre
        ORDER BY promedio_edad DESC;
    """)
    equipos = []
    edades = []
    for fila in cursor:
        equipos.append(fila[0])
        edades.append(fila[1])
    cursor.close()
    conexion.close()
    return {"equipos": equipos, "edades": edades}


def obtener_datos_nacionalidades(top_n=7):
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nacionalidad, COUNT(*) AS cantidad
        FROM jugador
        GROUP BY nacionalidad
        ORDER BY cantidad DESC
        LIMIT %s;
    """, (top_n,))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    labels = [fila[0] for fila in resultados]
    values = [fila[1] for fila in resultados]
    return {"labels": labels, "values": values}



def obtener_datos_valor_liga():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT l.nombre AS liga, ROUND(AVG(dj.valor_mercado), 2) AS promedio_valor
        FROM detalle_jugador dj
        JOIN equipos e ON dj.id_equipo = e.id_equipo
        JOIN ligas l ON e.id_liga = l.id_liga
        GROUP BY l.nombre
        ORDER BY promedio_valor DESC;
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    ligas = [fila[0] for fila in resultados]
    valores = [fila[1] for fila in resultados]
    return {"ligas": ligas, "valores": valores}


def obtener_datos_top_usuarios():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT u.nombre, COUNT(s.id_solicitud) AS total_solicitudes
        FROM solicitudes_info s
        JOIN usuarios u ON s.id_usuario = u.id_usuario
        GROUP BY u.nombre
        ORDER BY total_solicitudes DESC
        LIMIT 10;
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    usuarios = [fila[0] for fila in resultados]
    solicitudes = [fila[1] for fila in resultados]
    return {"usuarios": usuarios, "solicitudes": solicitudes}

