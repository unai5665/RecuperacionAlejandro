# Unai Perez Toscano
# Login
# Crear proyecto
# Asignar gestor a proyecto
# Asignar cliente a proyecto
# Crear tareas a proyecto (debo estar asignado)
# Asignar programador a proyecto
# Asignar programadores a tareas
# Obtener programadores
# Obtener proyectos (activos o todos)
# Obtener tareas de un proyecto (sin asignar o asignada)
from contextlib import nullcontext

import psycopg2
from flask import Flask, jsonify, request
import logging

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "alexsoft",
    "user": "postgres",
    "password": "postgres"
}

# Crear aplicación Flask
app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)


# Conexión a la base de datos
def conectar_bd():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        logging.error(f"Error de conexión a la base de datos: {e}")
        return None


# Ejecutar consultas SQL de manera segura
def ejecutar_sql(query, params=None):
    connection = conectar_bd()
    if connection is None:
        return jsonify({"error": "Error de conexión a la base de datos."}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        if cursor.description:
            columnas = [desc[0] for desc in cursor.description]
            resultados = cursor.fetchall()
            data = [dict(zip(columnas, fila)) for fila in resultados]
        else:
            connection.commit()
            data = {"mensaje": "Operación realizada con éxito"}
        cursor.close()
        connection.close()
        return jsonify(data), 200
    except psycopg2.Error as e:
        logging.error(f"Error al ejecutar SQL: {e}")
        return jsonify({"error": f"Error al ejecutar SQL: {e}"}), 500




@app.route('/login', methods=['POST']) #Funciona
def login():
    body_request = request.json
    user = body_request.get("user")
    passwd = body_request.get("passwd")

    if not user or not passwd:
        return jsonify({"error": "Faltan credenciales."}), 400

    query = """
        SELECT * FROM public."Gestor" WHERE usuario = %s AND passwd = %s;
    """
    is_logged, status_code = ejecutar_sql(query, (user, passwd))

    if status_code != 200 or len(is_logged.json) == 0:
        return jsonify({"msg": "login error"}), 401

    gestor_id = is_logged.json[0]["id"]
    empleado_id = is_logged.json[0]["empleado"]

    query_empleado = """
        SELECT * FROM public."Empleado" WHERE id = %s;
    """
    empleado, _ = ejecutar_sql(query_empleado, (empleado_id,))

    return jsonify({
        "id_empleado": empleado.json[0]["id"],
        "id_gestor": gestor_id,
        "nombre": empleado.json[0]["nombre"],
        "email": empleado.json[0]["email"]
    }), 200

@app.route('/empleado/empleados', methods=['GET']) # Funciona
def obtener_empleados():
    query = """
        SELECT e.id, e.nombre, 
            CASE 
                WHEN p.id IS NOT NULL THEN 'Programador'
                ELSE 'Gestor'
            END AS rol
        FROM public."Empleado" e
        LEFT JOIN public."Programador" p ON e.id = p.id
        ORDER BY e.id ASC;
    """
    return ejecutar_sql(query)

@app.route('/proyecto/crear', methods=['POST']) # No funciona correctamente
def crear_proyecto():
    data = request.json
    campos_requeridos = ['nombre', 'descripcion', 'fecha_inicio', 'cliente']

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400

    cliente_id = data['cliente']
    query_verificar_cliente = """
        SELECT COUNT(*) AS count FROM public."Cliente" WHERE id = %s;
    """
    resultado, status_code = ejecutar_sql(query_verificar_cliente, (cliente_id,))
    if status_code != 200:
        return resultado

    if not resultado.json or resultado.json[0]['count'] == 0:
        return jsonify({"error": f"El cliente con ID {cliente_id} no existe en la base de datos."}), 400

    fecha_finalizacion = data.get(nullcontext, f"{data['NOW'][:4]}-12-31")

    query = """
        INSERT INTO public."Proyecto" (nombre, descripcion, fecha_creacion, fecha_inicio, fecha_finalizacion, cliente)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s) RETURNING id;
    """
    params = (data['nombre'], data['descripcion'], data['NOW'], fecha_finalizacion, cliente_id)
    resultado, status_code = ejecutar_sql(query, params)
    if status_code != 200:
        return resultado

    return jsonify({"mensaje": "Proyecto creado exitosamente", "id": resultado.json[0]['id']}), 201

@app.route('/proyecto/asignar_gestor', methods=['POST']) # Funciona
def asignar_gestor():
    data = request.json
    try:
        proyecto_id = int(data['proyecto'])
        gestor_id = int(data['gestor'])
        fecha_asignacion = data.get('fecha_asignacion')  # Espera una fecha en formato ISO
        if not fecha_asignacion:
            return jsonify({"error": "Falta el campo 'fecha_asignacion'."}), 400
    except ValueError:
        return jsonify({"error": "Los valores de 'proyecto' y 'gestor' deben ser enteros."}), 400

    query = """
        INSERT INTO public."GestoresProyecto" (proyecto, gestor, fecha_asignacion)
        VALUES (%s, %s, %s);
    """
    return ejecutar_sql(query, (proyecto_id, gestor_id, fecha_asignacion))



@app.route('/proyecto/asignar_cliente', methods=['POST']) # Funciona
def asignar_cliente():
    data = request.json
    query = """
        UPDATE public."Proyecto"
        SET cliente = %s
        WHERE id = %s;
    """
    return ejecutar_sql(query, (data['cliente'], data['proyecto']))


@app.route('/proyecto/asignar_tarea', methods=['POST']) # Funciona
def crear_tarea_proyecto():
    data = request.json


    query = """
        INSERT INTO public."Tarea" (
            nombre, 
            descripcion, 
            estimacion, 
            fecha_creacion, 
            fecha_finalizacion, 
            programador, 
            proyecto
        )
        VALUES (%s, %s, %s, NOW(), NULL, %s, %s);
    """

    return ejecutar_sql(query, (
        data['nombre'],  # Campo obligatorio
        data['descripcion'],  # Campo obligatorio
        data.get('estimacion', None),  # Valor opcional, puede ser None
        data.get('programador', None),  # Valor opcional, puede ser None
        data['proyecto']  # Campo obligatorio
    ))


@app.route('/proyecto/asignar_programador', methods=['POST']) # Funciona
def asignar_programador_proyecto():
    data = request.json
    try:
        if 'proyecto' not in data or 'programador' not in data:
            return jsonify({"error": "Datos incompletos. Se requieren 'proyecto' y 'programador'."}), 400

        proyecto_id = data['proyecto']
        query_verificar = """
            SELECT COUNT(*) AS count
            FROM public."Proyecto"
            WHERE id = %s;
        """
        resultado, _ = ejecutar_sql(query_verificar, (proyecto_id,))
        if resultado.json[0]['count'] == 0:
            return jsonify({"error": f"El proyecto con ID {proyecto_id} no existe en la base de datos."}), 400

        query = """
            INSERT INTO public."ProgramadoresProyecto" (proyecto, programador, fecha_asignacion)
            VALUES (%s, %s, CURRENT_TIMESTAMP);
        """
        return ejecutar_sql(query, (data['proyecto'], data['programador']))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tarea/asignar_programador', methods=['POST']) # Funciona
def asignar_programador_tarea():
    data = request.json
    try:
        if 'programador' not in data or 'tarea' not in data:
            return jsonify({"error": "Datos incompletos. Se requieren 'programador' y 'tarea'."}), 400

        query = """
            UPDATE public."Tarea"
            SET programador = %s
            WHERE id = %s;
        """
        return ejecutar_sql(query, (data['programador'], data['tarea']))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/empleado/programadores', methods=['GET']) # Funciona
def obtener_programadores():
    query = """
        SELECT e.id, e.nombre
        FROM public."Empleado" e
        INNER JOIN public."Programador" p ON e.id = p.id
        ORDER BY e.id ASC;
    """
    return ejecutar_sql(query)

@app.route('/proyecto/proyectos', methods=['GET']) # Funciona
def obtener_proyectos():
    query = """
        SELECT * FROM public."Proyecto"
        ORDER BY id ASC
    """
    return ejecutar_sql(query)



@app.route('/proyecto/proyectos_gestor', methods=['GET']) # Funciona
def obtener_proyectos_gestor_id():
    empleado_id = request.args.get('id')
    query = """
        SELECT * FROM public."Proyecto" p
        INNER JOIN public."GestoresProyecto" gp ON p.id = gp.proyecto
        WHERE gp.gestor = %s;
    """
    return ejecutar_sql(query, (empleado_id,))




@app.route('/proyecto/tareas', methods=['GET'])
def obtener_tareas_proyecto():
    proyecto_id = request.args.get('proyecto_id')
    asignada = request.args.get('asignada')  # true o false
    query = """
        SELECT * FROM public."Tarea"
        WHERE proyecto = %s
          AND (%s::BOOLEAN IS NULL OR (programador IS NOT NULL) = %s::BOOLEAN);
    """
    params = (proyecto_id, asignada, asignada)
    return ejecutar_sql(query, params)

@app.route('/proyecto/historial_gestor', methods=['GET']) # Funciona
def historial_proyectos_terminados_gestor():
    gestor_id = request.args.get('id')
    if not gestor_id:
        return jsonify({"error": "Falta el parámetro 'id' del gestor"}), 400

    query = """
        SELECT p.*
        FROM public."Proyecto" p
        INNER JOIN public."GestoresProyecto" gp ON p.id = gp.proyecto
        WHERE gp.gestor = %s
          AND p.fecha_finalizacion < CURRENT_DATE
        ORDER BY p.fecha_finalizacion DESC;
    """
    return ejecutar_sql(query, (gestor_id,))


if __name__ == '__main__':
    app.run(debug=True)

