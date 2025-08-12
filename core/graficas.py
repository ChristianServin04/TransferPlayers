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
            # host="128.0.194.53",            # 128.0.194.53 o 192.168.1.11
            # database="bdTransferP",
            # user="postgres",
            # password="admin",
            # port="5432"

            #Local
            host="localhost",
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

# Gráficas nivel táctico
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

# Gráficas nivel estratégico
def obtener_promedio_valor_posicion():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM public.promedioposicion();")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    posiciones = [fila[0] for fila in resultados]
    valores = [float(fila[1]) for fila in resultados]
    return {"posiciones": posiciones, "valores": valores}


def obtener_distribucion_anio_nacimiento():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM public.promedio_anio_jugador();")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    anios = [int(fila[0]) for fila in resultados]
    total = [int(fila[1]) for fila in resultados]
    return {"anios": anios, "total": total}


def obtener_valor_mercado_por_liga():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM public.valor_mercado_por_liga();")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    ligas = [fila[0] for fila in resultados]
    valores = [float(fila[1]) for fila in resultados]
    return {"ligas": ligas, "valores": valores}


def obtener_promedio_permanencia_equipo():
    conexion = conectar()
    if not conexion:
        return {}
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM public.promedio_permanencia_equipos();")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    equipos = [fila[0] for fila in resultados]
    promedio = [float(fila[1]) for fila in resultados]
    print(equipos, promedio)
    return {"equipos": equipos, "promedio": promedio}
