from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import EventoForm, ChangePasswordForm, DeleteForm
from app.models import db, Evento, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los cursos si no es estudiante.
    """
    delete_form = DeleteForm()

    if current_user.role.name == 'Participante': # Change this for your project
        eventos = Evento.query.all()
    else:
        eventos = Evento.query.filter_by(organizador_id=current_user.id).all()


    return render_template('dashboard.html', eventos=eventos, delete_form=delete_form)

@main.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    """
    Permite crear un nuevo evento. Solo disponible para organizador o admins.
    """
    form = EventoForm()
    if form.validate_on_submit():
        print("✅ El formulario es válido")
        evento = Evento(
            nombre=form.nombre.data,
            ubicacion=form.ubicacion.data,
            fecha_hora=form.fecha_hora.data,
            capacidad=form.capacidad.data,
            descripcion=form.descripcion.data,
            organizador_id=current_user.id
        )
        db.session.add(evento)
        db.session.commit()
        flash("Event created successfully.", 'success')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))
    
    print("❌ El formulario no es válido o es GET")
    return render_template('evento_form.html', form=form)

@main.route('/eventos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    """
    Permite editar un evento existente. Solo si es admin o el profesor dueño.
    """
    evento = Evento.query.get_or_404(id)

    # Validación de permisos
    if current_user.role.name not in ['Admin', 'Organizador'] or (
    evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to edit this event.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    form = EventoForm(obj=evento)

    if form.validate_on_submit():
        evento.nombre = form.nombre.data
        evento.ubicacion = form.ubicacion.data
        evento.fecha_hora = form.fecha_hora.data
        evento.capacidad = form.capacidad.data
        evento.descripcion = form.descripcion.data
        db.session.commit()
        flash("Event updated successfully.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('evento_form.html', form=form, editar=True)

@main.route('/eventos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_evento(id):
    """
    Elimina un evento si el usuario es admin o su profesor creador.
    """
    evento = Evento.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Organizador'] or (
        evento.organizador_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this Event.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    db.session.delete(evento)
    db.session.commit()
    flash("Event deleted successfully.")  # 🔁 Traducido
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
