import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import psycopg2
from datetime import datetime
from .graficas import (
    obtener_datos_edad_equipo,
    obtener_datos_nacionalidades,
    obtener_datos_valor_liga,
    obtener_datos_top_usuarios,
)
# from .models import DetalleJugador

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def admin_view(request):
    return render(request, 'admin_panel.html')

def player_view(request):
    return render(request, 'player.html')

def reporte_solicitudes(request):
    return render(request, 'reporte_solicitudes.html')

def solicitudes_aprobadas(request):
    return render(request, 'solicitudes_aprobadas.html')

def usuarios_registrados(request):
    return render(request, 'usuarios_registrados.html')

def reporte_semanal(request):
    return render(request, 'reporte_semanal.html')

def vista_graficas(request):
    return render(request, 'graficas_tactico.html')

@require_GET
def obtener_jugadores_por_equipo(request):
    equipo_id = request.GET.get("equipo_id")
    if not equipo_id:
        return JsonResponse([], safe=False)

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            SELECT j.nombre, j.edad, dj.foto, j.id_jugador
            FROM jugador  j  inner join detalle_jugador dj on j.id_jugador = dj.id_jugador
            WHERE dj.id_equipo = %s
        """
        cursor.execute(query, (equipo_id,))
        resultados = cursor.fetchall()
        jugadores = [
            {"nombre": fila[0], "edad": fila[1], "img": fila[2], "id": fila[3]}
            for fila in resultados
        ]
        cursor.close()
        conexion.close()
        return JsonResponse(jugadores, safe=False)
    except Exception as e:
        print("Error en la consulta de jugadores:", e)
        return JsonResponse([], safe=False)

def player_view(request, id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Consulta principal de información del jugador
        cursor.execute("""
            SELECT dj.foto, j.nombre, e.nombre,dj.posicion,j.nacionalidad,j.edad,dj.valor_mercado 
            FROM public.detalle_jugador dj INNER JOIN public.jugador j 
            ON (j.id_jugador = dj.id_jugador )
            INNER JOIN public.equipos e ON (e.id_equipo = dj.id_equipo)
            WHERE dj.id_jugador = %s
        """, (id,))
        jugador_row = cursor.fetchone()

        if not jugador_row:
            return render(request, "player.html", {"player": None})

        # Mapeo de los datos
        jugador = {
            "imagen": jugador_row[0],          # dj.foto
            "nombre": jugador_row[1],          # j.nombre
            "equipo": jugador_row[2],          # e.nombre
            "posicion": jugador_row[3],        # dj.posicion
            "nacionalidad": jugador_row[4],    # j.nacionalidad
            "edad": jugador_row[5],            # j.edad
            "valor_mercado": jugador_row[6],   # dj.valor_mercado
        }


        # Consulta de estadísticas
        # cursor.execute("""
        #     SELECT temporada, partidos, goles, asistencias
        #     FROM estadistica_jugador
        #     WHERE id_jugador = %s
        #     ORDER BY temporada DESC
        # """, (id,))
        # estadisticas_rows = cursor.fetchall()

        # jugador["estadisticas"] = [
        #     {
        #         "temporada": row[0],
        #         "partidos": row[1],
        #         "goles": row[2],
        #         "asistencias": row[3]
        #     } for row in estadisticas_rows
        # ]

        cursor.close()
        conexion.close()

        print("Jugador:", jugador)

        return render(request, "player.html", {"player": jugador})

    except Exception as e:
        print("Error al obtener datos del jugador:", e)
        return render(request, "player.html", {"player": None})


def conectar():
    return psycopg2.connect(
        host="192.168.1.11",            # 128.0.194.53 o 192.168.1.11
        database="bdTransferP",  # reemplaza por el nombre real
        user="postgres",           # el que usas en pgAdmin
        password="admin",    # tu contraseña
        port="5432"                  # usualmente 5432
    )

@require_GET
def obtener_solicitudes(request):
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if not desde or not hasta:
        return JsonResponse([], safe=False)

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            select * from public.solicitudes_por_fecha(%s, %s)
        """
        cursor.execute(query, (desde, hasta))
        resultados = cursor.fetchall()

        solicitudes = [
            {
                "usuario": fila[0],
                "jugador": fila[1],
                "mensaje": fila[2],
                "estado": fila[3],
                "fecha": fila[4].strftime('%Y-%m-%d')
            }
            for fila in resultados
        ]

        cursor.close()
        conexion.close()
        return JsonResponse(solicitudes, safe=False)

    except Exception as e:
        print("Error en la consulta:", e)
        return JsonResponse([], safe=False)


@require_GET
def obtener_solicitudes_aprobadas(request):
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if not desde or not hasta:
        return JsonResponse([], safe=False)

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            select * from public.solicitudes_aprobadas(%s, %s)
        """
        cursor.execute(query, (desde, hasta))
        resultados = cursor.fetchall()

        solicitudes = [
            {
                "total": fila[0],
                "fecha": fila[1].strftime('%Y-%m-%d'),
                "estado": fila[2]
            }
            for fila in resultados
        ]

        cursor.close()
        conexion.close()
        return JsonResponse(solicitudes, safe=False)

    except Exception as e:
        print("Error en la consulta:", e)
        return JsonResponse([], safe=False)
    

@require_GET
def obtener_usuarios_registrados(request):
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if not desde or not hasta:
        return JsonResponse([], safe=False)

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            SELECT * FROM public.usuarios_registrados_fechas(%s, %s)
        """
        cursor.execute(query, (desde, hasta))
        resultados = cursor.fetchall()

        usuarios = [
            {
                "nombre": fila[0],
                "tipo": fila[1],
                "fecha": fila[2].strftime('%Y-%m-%d')
            }
            for fila in resultados
        ]

        cursor.close()
        conexion.close()
        return JsonResponse(usuarios, safe=False)

    except Exception as e:
        print("Error en la consulta:", e)
        return JsonResponse([], safe=False)
    

@require_GET
def obtener_solicitudes_semanales(request):
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    if not desde or not hasta:
        return JsonResponse([], safe=False)

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            SELECT * FROM public.solicitudes_atendidas_semanal(%s, %s)
        """
        cursor.execute(query, (desde, hasta))
        resultados = cursor.fetchall()

        datos = [
            {
                "semana": fila[0],
                "anio": fila[1],
                "total": fila[2]
            }
            for fila in resultados
        ]

        cursor.close()
        conexion.close()
        return JsonResponse(datos, safe=False)

    except Exception as e:
        print("Error en la consulta semanal:", e)
        return JsonResponse([], safe=False)

def reporte_datos(request, tipo):
    if tipo == "nacionalidades":
        top_n = request.GET.get("top_n", 7)
        try:
            top_n = int(top_n)
            if top_n < 1 or top_n > 50:  # opcional: límite superior
                top_n = 7
        except ValueError:
            top_n = 7
        datos = obtener_datos_nacionalidades(top_n)
    elif tipo == "edad_equipo":
        datos = obtener_datos_edad_equipo()
    elif tipo == "valor_liga":
        datos = obtener_datos_valor_liga()
    elif tipo == "top_usuarios":
        datos = obtener_datos_top_usuarios()
    else:
        datos = {}

    return JsonResponse(datos)

