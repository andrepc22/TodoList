from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at, t.category '
        'from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by display_order', (g.user['id'],)
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        # category = request.form['category']
        category = request.form.get('category')
        error = None

        if not description:
            error = 'Descripción requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'select t.display_order, t.id_user '
                'from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by display_order desc',
                (g.user['id'],)
            )
            autoincrement = c.fetchone()
            # print(autoincrement)
            if autoincrement is not None :
                autoincrement['display_order'] += 1
                autoincrement['id_user'] += 1
                # print(autoincrement['display_order'], autoincrement['id_user'])
                c.execute(
                    'insert into todo (description, completed, created_by, display_order, id_user, category)'
                    ' values (%s, %s, %s, %s, %s, %s)',
                    (description, False, g.user['id'], autoincrement['display_order'], autoincrement['id_user'], category)
                )
            else:
                c.execute(
                    'insert into todo (description, completed, created_by, category)'
                    ' values (%s, %s, %s, %s)',
                    (description, False, g.user['id'], category)
                )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

@bp.route('/move', methods=['GET', 'POST'])
@login_required
def move():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.id_user, t.display_order '
        'from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by display_order', (g.user['id'],)
    )
    todos = c.fetchall()
    if request.method == 'POST':
        getorder = request.form['order']
        order = getorder.split(",")
        print(order, flush=True)

        # prio = []
        # for j in todos:
            # prio.append(j['id_user'])
        # print(prio, flush=True)

        # print(todos[0]['id_user'], flush=True)
        # for i, j in zip(order, prio):
            # print(i,j, flush=True)
            # c.execute(
                # 'update todo set display_order = %s'
                # ' where id_user =%s and created_by = %s',
                # (i, j, g.user['id'])
            # )
        count = 0
        for i in order:
            count += 1
            c.execute(
                'update todo set display_order = %s'
                ' where id_user =%s and created_by = %s',
                (i, count, g.user['id'])
            )
        db.commit()
        return redirect(url_for('todo.index'))

    return render_template('todo/move.html', todos=todos )

def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, u.username, t.category '
        'from todo t join user u on t.created_by = u.id where t.id = %s',
        (id,)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "El todo de id {0} no existe".format(id))

    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        category = request.form.get( 'category' )
        error = None

        if not description:
            error = "La descripción es requerida"

        if error is not None:
            flash(error)
        else:
            db,c = get_db()
            c.execute(
                'update todo set description = %s, completed = %s, category = %s'
                ' where id = %s and created_by = %s',
                (description, completed, category, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from todo where id = %s and created_by = %s', (id, g.user['id'])
    )
    db.commit()
    return redirect(url_for('todo.index'))
