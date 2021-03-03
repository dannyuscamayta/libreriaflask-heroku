from flask import Flask, request
# aqui se esta importando la API del falsk_restful↓
from flask_restful import Api
from config.base_datos import bd
# ------------------------------------------------------------------------------------
# se esta importando desde autor.py para ponerlo todo a la base de datos
#from models.autor import AutorModel  # esto modelo ya no sera necesario porque estoy importando de forma global
from controllers.autor import AutoresController, AutorController
#from models.categoria import CategoriaModel
from controllers.categoria import CategoriaController
#from models.libro import LibroModel
from controllers.libro import LibrosController, LibroModel, RegistroLibroSedeController
#from models.sede import SedeModel
from controllers.sede import LibroCategoriaSedeController, LibroSedeController, SedesController
#from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
# esta linea ↓ es para la documentacio de swagger.ui 
#  -------------------------------------------------------------------
from flask_swagger_ui import get_swaggerui_blueprint
# desde la documentacion de swagger 
SWAGGER_URL = '' # esta variable se usa para documentar en que ENDPOINT se encontrara la documentacion
API_URL = '/static/swagger.json'  # se usa para indicar en que parte del proyecto se enciuentra el archivo de la documentacion
swagger_blueprint =get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Libreria Flask - swagger documentation"
    }
)
#  -------------------------------------------------------------------
app = Flask(__name__)
app.register_blueprint(swagger_blueprint)
# ------------------------------------------------
# para concetarse a la base de datos desde una ORM
#                                                               formato://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3306/flasklibreria'
#print(app.config)
# ---------------------------- esto es del api restful -------------------------------
api = Api(app)
# ------------------------------------------------------------------------------------
CORS(app) # esto es para el uso de los cors ↑↑↑↑ permitiendo a todos los METODOS, DOMINIOS Y HEADERs el accesso
# este SQLalchemy_track_modifications es para evitar el warning de la funcionalidad de sqlalchemy de track modification
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

# inicio de la aplicacion proveyendo todas las credenciales indicadas en el app,config pero aun nom se ha encontrado en la bd
bd.init_app(app)

# para bajarse los datos de la base de datos de mysql (se eleiminan todas las tablas MAPEADAS de mi BD)
# bd.drop_all(app=app)

# con esta linea de abajo recien se conecta con la base de datos, pero necesita el driver pip install mysqlclient, para poder conectarse
bd.create_all(app=app)

# ------------------------------------------------------------------------------------
# para crear una ruta DIRECTA de busqueda

@app.route('/buscar')
def buscarLibro():
    # De acuerdo a la PALABRA enviada ↓ que me de el resultado de la BUSQUEDA de todos los libros, si no hay
    # ningun libro con esa palabra clave o no se mando la palabra, Indicar que la busqueda no tuvo exito o efecto
    # se USARIA un BACK_REQUEST
    #print(request.args('/palabra'))
    palabra = request.args.get('palabra')
    if palabra:
        resultadoBusqueda = LibroModel.query.filter(LibroModel.libroNombre.like('%' + palabra + '%')).all()
        if resultadoBusqueda:
            resultado = []
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
            return {
                'success': True,
                'content': resultado,
                'message': None
            }

    return {
        'success': False,
        'content': None,
        'message': 'No se encontro nada para buscar o la busqueda no tuvo exito'
    }, 400


# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# AQUI ↓ IRAN LAS RUTAS DE MI API_RESTFUL : para poder probar en el postman

api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController, '/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias', '/categoria')
api.add_resource(LibrosController, '/libro', '/libros')
api.add_resource(SedesController, '/sedes', '/sede')
api.add_resource(LibroSedeController, '/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaSedeController, '/busquedaLibrosSedeCat')
api.add_resource(RegistroLibroSedeController, '/registrarSedesLibro') # para controlar el POST x donde (sede) se va a guardar el registro del libro
# ------------------------------------------------------------------------------------
#para levantar y probar que python este corriendo todo normal como servidor
if __name__ == '__main__':
    app.run(debug=True)
