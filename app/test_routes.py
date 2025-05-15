from flask import Blueprint, request, jsonify
from app.models import db, Evento

# Blueprint solo con endpoints de prueba para cursos
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/eventos', methods=['GET'])
def listar_eventos():
    """
    Retorna una lista de eventos (JSON).
    """
    evento = Evento.query.all()

    data = [
        {'id': evento.id, 'nombre': evento.nombre, 'descripcion': evento.descripcion, 'fecha': evento.fecha, 'lugar': evento.lugar, 'tipo': evento.tipo, 'capacidad': evento.capacidad, 'precio': evento.precio, 'organizador_id': evento.organizador_id}
        for evento in evento
    ]
    return jsonify(data), 200


@main.route('/eventos/<int:id>', methods=['GET'])
def listar_un_evento(id):
    """
    Retorna un solo evento por su ID (JSON).
    """
    evento = Evento.query.get_or_404(id)

    data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'ubicacion': evento.ubicacion,
        'fecha_hora': evento.fecha_hora,
        'capacidad': evento.capacidad,
        'descripcion': evento.descripcion,
        'organizador_id': evento.organizador_id
    }

    return jsonify(data), 200


@main.route('/eventos', methods=['POST'])
def crear_evento():
    """
    Crea un evento sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'profesor_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    evento = evento(
        nombre=data.get('nombre'),
        ubicacion=data.get('ubicacion'),
        fecha_hora=data.get('fecha_hora'),
        capacidad=data.get('capacidad'),
        descripcion=data.get('descripcion'),
        organizador_id=data.get('organizador_id')  # sin validación de usuario
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify({'message': 'Evento creado', 'id': evento.id, 'organizador_id': evento.organizador_id}), 201

@main.route('/evento/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    """
    Actualiza un evento sin validación de usuario o permisos.
    """
    evento = Evento.query.get_or_404(id)
    data = request.get_json()

    evento.nombre = data.get('nombre', evento.nombre)
    evento.ubicacion = data.get('ubicacion', evento.ubicacion)
    evento.fecha_hora = data.get('fecha_hora', evento.fecha_hora)
    evento.capacidad = data.get('capacidad', evento.capacidad)
    evento.descripcion = data.get('descripcion', evento.descripcion)
    evento.organizador_id = data.get('organizador_id', evento.organizador_id)

    db.session.commit()

    return jsonify({'message': 'Evento actualizado', 'id': evento.id}), 200

@main.route('/eventos/<int:id>', methods=['DELETE'])
def eliminar_evento(id):
    """
    Elimina un evento sin validación de permisos.
    """
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message': 'Evento eliminado', 'id': evento.id}), 200
