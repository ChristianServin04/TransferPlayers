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
    obtener_promedio_valor_posicion,
    obtener_distribucion_anio_nacimiento,
    obtener_valor_mercado_por_liga,
    obtener_promedio_permanencia_equipo)
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import hashlib
from datetime import datetime
from django.urls import reverse
import re

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        correo = request.POST['email']
        password = request.POST['password']

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, tipo_usuario FROM usuarios
            WHERE correo = %s AND contrasena = %s AND status = 1
        """, (correo, password))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        # Si la petición es AJAX, responde con JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if usuario:
                request.session['id_usuario'] = usuario[0]
                request.session['nombre_usuario'] = usuario[1]
                request.session['tipo_usuario'] = usuario[2]
                return JsonResponse({'success': True, 'redirect_url': reverse('home')})
            else:
                return JsonResponse({'success': False, 'error': 'Correo o contraseña incorrectos.'})

        # Si no es AJAX, responde como antes
        if usuario:
            request.session['id_usuario'] = usuario[0]
            request.session['nombre_usuario'] = usuario[1]
            request.session['tipo_usuario'] = usuario[2]
            messages.success(request, f"Bienvenido(a), {usuario[1]}")
            print("Correo recibido:", correo)
            print("Password recibido:", password)
            print("Resultado de consulta:", usuario)
            return redirect("home")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            print("Correo recibido:", correo)
            print("Password recibido:", password)
            print("Resultado de consulta:", usuario)
            return redirect("login")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')

        # Validaciones
        if not nombre or not correo or not password or not confirm_password:
            error = "Todos los campos son obligatorios."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error})
            messages.error(request, error)
            return redirect("register")

        if password != confirm_password:
            error = "Las contraseñas no coinciden."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error})
            messages.error(request, error)
            return redirect("register")

        if len(password) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error})
            messages.error(request, error)
            return redirect("register")
        
        # Validación de caracteres permitidos en la contraseña
        if ' ' in password or not re.match(r'^[A-Za-z0-9@#$%^&+=!._-]+$', password):
            error = "La contraseña no debe contener espacios ni caracteres no permitidos."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error})
            messages.error(request, error)
            return redirect("login")

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            error = "El correo ya está registrado."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error})
            messages.error(request, error)
            return redirect("register")

        tipo_usuario = "Directivo"
        status = 1
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contrasena, tipo_usuario, status, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, correo, password, tipo_usuario, status, fecha_registro))

        conexion.commit()
        cursor.close()
        conexion.close()

        success = "Registro exitoso. Ya puedes iniciar sesión."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': '/login/', 'message': success})
        messages.success(request, success)
        return redirect("login")

    return render(request, "register.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")

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

def vista_graficas2(request):
    return render(request, 'graficas_estrategico.html')

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
    
def buscar_jugadores(request):
    query = request.GET.get("q", "").lower()

    if not query:
        return JsonResponse([], safe=False)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT j.id_jugador, j.nombre, j.edad, dj.foto
        FROM jugador j
        INNER JOIN detalle_jugador dj ON j.id_jugador = dj.id_jugador
        WHERE LOWER(j.nombre) LIKE %s
        LIMIT 10
    """, (f"%{query}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    jugadores = [
        {
            "id": row[0],
            "nombre": row[1],
            "edad": row[2],
            "img": row[3]
        } for row in resultados
    ]

    return JsonResponse(jugadores, safe=False)

def player_view(request, id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Consulta principal de información del jugador con joins
        cursor.execute("""
            SELECT dj.foto, j.nombre, e.nombre, dj.posicion, j.nacionalidad, j.edad, dj.valor_mercado 
            FROM public.detalle_jugador dj 
            INNER JOIN public.jugador j ON j.id_jugador = dj.id_jugador
            INNER JOIN public.equipos e ON e.id_equipo = dj.id_equipo
            WHERE dj.id_jugador = %s
        """, (id,))
        jugador_row = cursor.fetchone()

        if not jugador_row:
            return render(request, "player.html", {"player": None})

        # Diccionario base del jugador, ahora incluye el id
        jugador = {
            "id": id,                          # <-- Agrega el id aquí
            "imagen": jugador_row[0],          # dj.foto
            "nombre": jugador_row[1],          # j.nombre
            "equipo": jugador_row[2],          # e.nombre
            "posicion": jugador_row[3],        # dj.posicion
            "nacionalidad": jugador_row[4],    # j.nacionalidad
            "edad": jugador_row[5],            # j.edad
            "valor_mercado": jugador_row[6],   # dj.valor_mercado
        }

        # Número de partidos jugados desde la función personalizada
        cursor.execute("SELECT * FROM public.partidos(%s)", (id,))
        resultado_partidos = cursor.fetchone()
        num_partidos = resultado_partidos[0] if resultado_partidos else 0

        # Goles y asistencias desde historial_partido
        cursor.execute("""
            SELECT COALESCE(SUM(goles), 0), COALESCE(SUM(asistencias), 0)
            FROM historial_partido
            WHERE id_jugador = %s AND status = 1
        """, (id,))
        resultado_estadisticas = cursor.fetchone()
        num_goles = resultado_estadisticas[0] if resultado_estadisticas else 0
        num_asistencias = resultado_estadisticas[1] if resultado_estadisticas else 0

        # Agregar estadísticas al jugador
        jugador["estadisticas"] = {
            "partidos": num_partidos,
            "goles": num_goles,
            "asistencias": num_asistencias
        }

        cursor.close()
        conexion.close()

        print("Jugador:", jugador)
        
        return render(request, "player.html", {"player": jugador})

    except Exception as e:
        messages.error(request, f"Error al obtener datos del jugador: {e}")
        print("Jugador:", jugador)
        return render(request, "player.html", {"player": None})
    
def solicitud_info_view(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_usuario = request.session.get('id_usuario')
        id_jugador = request.POST.get('id_jugador')
        mensaje = request.POST.get('mensaje', '').strip()
        estado = "Pendiente"
        fecha_solicitud = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"id_usuario: {id_usuario}, id_jugador: {id_jugador}, mensaje: {mensaje}")

        # Validar si el usuario está logueado
        if not id_usuario:
            return JsonResponse({'success': False, 'error': 'Debes iniciar sesión para realizar una solicitud.'})

        # Validar datos completos
        if not id_jugador or not mensaje:
            return JsonResponse({'success': False, 'error': 'Datos incompletos.'})


        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO solicitudes_info (id_usuario, id_jugador, mensaje, estado, fecha_solicitud)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_usuario, id_jugador, mensaje, estado, fecha_solicitud))
        conexion.commit()
        cursor.close()
        conexion.close()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


def conectar():
    return psycopg2.connect(
        # #Ip Majo
        # host="128.0.194.53",            # 128.0.194.53 o 192.168.1.11
        # database="bdTransferP",  # reemplaza por el nombre real
        # user="postgres",           # el que usas en pgAdmin
        # password="admin",    # tu contraseña
        # port="5432"                  # usualmente 5432

        #Local
        host="localhost",
        database="bdTransferP",
        user="postgres",
        password="admin",
        port="5432"
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

from django.http import JsonResponse

def reporte_datos(request, tipo):
    if tipo == "nacionalidades":
        top_n = request.GET.get("top_n", 7)
        try:
            top_n = int(top_n)
            if top_n < 1 or top_n > 50:
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

    # Nuevos reportes estratégicos
    elif tipo == "promedio_valor_posicion":
        datos = obtener_promedio_valor_posicion()

    elif tipo == "distribucion_anio_nacimiento":
        datos = obtener_distribucion_anio_nacimiento()

    elif tipo == "valor_mercado_liga":
        datos = obtener_valor_mercado_por_liga()

    elif tipo == "promedio_permanencia":
        datos = obtener_promedio_permanencia_equipo()

    else:
        datos = {}

    return JsonResponse(datos)


def obtener_jugadores_bd():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT j.id_jugador, j.nombre, j.edad, dj.posicion, dj.valor_mercado, e.nombre, j.fecha_nacimiento, j.status
        FROM jugador j
        INNER JOIN detalle_jugador dj ON j.id_jugador = dj.id_jugador
        INNER JOIN equipos e ON dj.id_equipo = e.id_equipo
    """)
    resultados = cursor.fetchall()
    jugadores = [
        {
            "id": row[0],
            "nombre": row[1],
            "edad": row[2],
            "posicion": row[3],
            "valor_mercado": row[4],
            "equipo": row[5],
            "fecha_nacimiento": row[6].strftime('%Y-%m-%d') if row[6] else "",
            "estatus": row[7]
        }
        for row in resultados
    ]
    cursor.close()
    conexion.close()
    return jugadores

def obtener_solicitudes_bd():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT s.id_solicitud, u.nombre, j.nombre, s.mensaje, s.fecha_solicitud, s.estado
        FROM solicitudes_info s
        INNER JOIN usuarios u ON s.id_usuario = u.id_usuario
        INNER JOIN jugador j ON s.id_jugador = j.id_jugador
    """)
    resultados = cursor.fetchall()
    solicitudes = [
        {
            "id": row[0],
            "usuario": row[1],
            "jugador": row[2],
            "mensaje": row[3],
            "fecha": row[4].strftime('%Y-%m-%d') if row[4] else "",
            "estatus": row[5]
        }
        for row in resultados
    ]
    cursor.close()
    conexion.close()
    return solicitudes

def obtener_usuarios_bd():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_usuario, nombre, tipo_usuario, correo, status, fecha_registro
        FROM usuarios
    """)
    resultados = cursor.fetchall()
    usuarios = [
        {
            "id_usuario": row[0],
            "nombre": row[1],
            "tipo_usuario": row[2],
            "correo": row[3],
            "status": row[4],
            "fecha_registro": row[5].strftime('%Y-%m-%d') if row[5] else ""
        }
        for row in resultados
    ]
    cursor.close()
    conexion.close()
    return usuarios

def admin_panel(request):
    estatus = request.GET.get('estatus', 'todos')

    # --- Jugadores ---
    jugadores_list = obtener_jugadores_bd()
    if estatus == 'activos':
        jugadores_list = [j for j in jugadores_list if str(j['estatus']) == '1']
    elif estatus == 'inactivos':
        jugadores_list = [j for j in jugadores_list if str(j['estatus']) == '0']
    # 'todos' no filtra

    page_number_j = request.GET.get('page', 1)
    paginator_j = Paginator(jugadores_list, 10)
    jugadores = paginator_j.get_page(page_number_j)

    # --- Solicitudes pendientes ---
    solicitudes_list = obtener_solicitudes_bd()
    solicitudes_pendientes = [s for s in solicitudes_list if s["estatus"].lower() == "pendiente"]
    
    page_number_s = request.GET.get('page_solicitudes', 1)
    paginator_s = Paginator(solicitudes_pendientes, 10)
    solicitudes = paginator_s.get_page(page_number_s)

    # --- Usuarios ---
    usuarios_list = obtener_usuarios_bd()
    page_number_u = request.GET.get('page_usuarios', 1)
    paginator_u = Paginator(usuarios_list, 10)
    usuarios = paginator_u.get_page(page_number_u)

    return render(request, 'admin_panel.html', {
        'jugadores': jugadores,
        'solicitudes': solicitudes,
        'usuarios': usuarios,
    })

def agregar_registro_partido(request):
    if request.method == "POST":
        id_jugador = request.POST.get("id_jugador")
        goles = request.POST.get("goles")
        asistencias = request.POST.get("asistencias")
        lesion = request.POST.get("lesion")
        fecha = request.POST.get("fecha")

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # 1. Obtener id_equipo e id_liga usando el id_jugador
            cursor.execute("""
                SELECT dj.id_equipo, e.id_liga
                FROM detalle_jugador dj
                INNER JOIN equipos e ON dj.id_equipo = e.id_equipo
                WHERE dj.id_jugador = %s
            """, (id_jugador,))
            resultado = cursor.fetchone()
            if resultado:
                id_equipo, id_liga = resultado
            else:
                id_equipo, id_liga = None, None

            # 2. Insertar el registro solo si se obtuvieron los datos
            if id_equipo and id_liga:
                cursor.execute("""
                    INSERT INTO historial_partido (id_jugador, id_liga, id_equipo, goles, asistencias, lesion, fecha, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_jugador, id_liga, id_equipo, goles, asistencias, lesion, fecha, 1))
                conexion.commit()
            else:
                print("No se encontró equipo o liga para el jugador.")

            cursor.close()
            conexion.close()
            messages.success(request, "El registro de partido se guardó correctamente.")
        except Exception as e:
            print("Error al insertar registro de partido:", e)
            messages.error(request, "Error al guardar el registro.")
        return redirect('admin_panel')
    
def modificar_jugador(request):
    if request.method == "POST":
        id_jugador = request.POST.get("id_jugador")
        edad = request.POST.get("edad")
        posicion = request.POST.get("posicion")
        valor_mercado = request.POST.get("valor_mercado")

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            # Actualiza edad y valor en la tabla jugador
            cursor.execute("""
                UPDATE jugador
                SET edad = %s
                WHERE id_jugador = %s
            """, (edad, id_jugador))
            # Actualiza posición y valor_mercado en detalle_jugador
            cursor.execute("""
                UPDATE detalle_jugador
                SET posicion = %s, valor_mercado = %s
                WHERE id_jugador = %s
            """, (posicion, valor_mercado, id_jugador))
            conexion.commit()
            cursor.close()
            conexion.close()
            messages.success(request, "El jugador se modificó exitosamente.")
        except Exception as e:
            print("Error al modificar jugador:", e)
            messages.error(request, "Error al modificar el jugador.")
        return redirect('admin_panel')
    
def dar_de_baja_jugador(request):
    if request.method == "POST":
        id_jugador = request.POST.get("id_jugador")
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE jugador
                SET status = 0
                WHERE id_jugador = %s
            """, (id_jugador,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messages.success(request, "Se dió de baja al jugador correctamente.")
        except Exception as e:
            print("Error al dar de baja al jugador:", e)
            messages.error(request, "Error al dar de baja al jugador.")
        return redirect('admin_panel')
    
def dar_de_alta_jugador(request):
    if request.method == "POST":
        id_jugador = request.POST.get("id_jugador")
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE jugador
                SET status = 1
                WHERE id_jugador = %s
            """, (id_jugador,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messages.success(request, "Se dió de alta al jugador correctamente.")
        except Exception as e:
            print("Error al dar de alta al jugador:", e)
            messages.error(request, "Error al dar de alta al jugador.")
        return redirect('admin_panel')

def agregar_jugador(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        posicion = request.POST.get("posicion")
        valor_mercado = request.POST.get("valor_mercado")
        equipo_nombre = request.POST.get("equipo")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        nacionalidad = request.POST.get("nacionalidad")
        imagen = request.FILES.get("imagen")

        imagen_ruta = ""
        if imagen:
            ruta_carpeta = os.path.join(settings.BASE_DIR, 'core', 'static', 'imagenes', 'jugadores')
            os.makedirs(ruta_carpeta, exist_ok=True)
            nombre_archivo = imagen.name
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_completa, 'wb+') as destino:
                for chunk in imagen.chunks():
                    destino.write(chunk)
            imagen_ruta = f"imagenes/jugadores/{nombre_archivo}"

        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # Obtener ID del equipo
            cursor.execute("SELECT id_equipo FROM equipos WHERE nombre = %s", (equipo_nombre,))
            resultado = cursor.fetchone()
            if resultado:
                id_equipo = resultado[0]
            else:
                raise Exception(f"Equipo '{equipo_nombre}' no encontrado.")

            # Insertar jugador y obtener ID con RETURNING
            cursor.execute("""
                INSERT INTO jugador (nombre, edad, fecha_nacimiento, nacionalidad, status)
                VALUES (%s, %s, %s, %s, 1)
                RETURNING id_jugador
            """, (nombre, edad, fecha_nacimiento, nacionalidad))
            id_jugador = cursor.fetchone()[0]

            # Insertar detalle_jugador
            cursor.execute("""
                INSERT INTO detalle_jugador (id_jugador, id_equipo, posicion, valor_mercado, foto, status)
                VALUES (%s, %s, %s, %s, %s, 1)
            """, (id_jugador, id_equipo, posicion, valor_mercado, imagen_ruta))

            conexion.commit()
            cursor.close()
            conexion.close()
            messages.success(request, "El jugador se agregó correctamente.")
        except Exception as e:
            messages.error(request, f"Error al agregar jugador: {e}")
        return redirect('admin_panel')




def buscar_equipos(request):
    termino = request.GET.get('q', '')
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre FROM equipos
        WHERE nombre ILIKE %s
        LIMIT 5
    """, (f"%{termino}%",))
    equipos = cursor.fetchall()
    cursor.close()
    conexion.close()
    resultados = [nombre for (nombre,) in equipos]
    return JsonResponse(resultados, safe=False)

def actualizar_solicitud(request, solicitud_id):
    accion = request.POST.get("accion")
    
    if accion not in ["aprobar", "rechazar"]:
        messages.error(request, "Acción no válida.")
        return redirect("admin_view")  # O el nombre que tengas en urls.py para admin_panel

    nuevo_estado = "Aprobada" if accion == "aprobar" else "Rechazada"

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE solicitudes_info
            SET estado = %s
            WHERE id_solicitud = %s
        """, (nuevo_estado, solicitud_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        messages.success(request, f"Solicitud marcada como {nuevo_estado}.")
    except Exception as e:
        messages.error(request, "Ocurrió un error al actualizar la solicitud.")
        print("Error actualizando solicitud:", e)

    return redirect("admin_panel")  

# def enviar_solicitud(request, jugador_id):
#     if request.method == "POST":
#         mensaje = request.POST.get("mensaje")
#         usuario_id = request.session.get("id_usuario")  # ajusta esto según cómo guardes el usuario

#         if not usuario_id:
#             messages.error(request, "Debes iniciar sesión para enviar una solicitud.")
#             return redirect("login")  # o la vista correspondiente

#         conexion = conectar()
#         cursor = conexion.cursor()
#         cursor.execute("""
#             INSERT INTO solicitudes_info (id_usuario, id_jugador, mensaje, fecha_solicitud, estado)
#             VALUES (%s, %s, %s, CURRENT_DATE, 'Pendiente')
#         """, (usuario_id, jugador_id, mensaje))
#         conexion.commit()
#         cursor.close()
#         conexion.close()

#         messages.success(request, "Tu solicitud fue enviada correctamente.")
#         return redirect("player", jugador_id=jugador_id)