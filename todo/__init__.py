# importamos os para poder hacer uso de las variables de entorno
import os
from flask import Flask

# creamos esta función para poder luego testear la app o crear varias instancias de la misma
def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        # flask necesita de este string para poder crear las sesiones, una buena práctica es que este string sea más complicado
        SECRET_KEY='mykey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    # vamos a llamar a nuestra base de datos
    from . import db

    db.init_app(app)

    # añadiendo el blueprint
    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    # vamos a crear una ruta de pruebas
    # en la terminal corremos
    # export FLASK_APP=todo
    # export FLASK_ENV=development
    @app.route('/hola')
    def hola():
        return 'pruebita'

    return app
