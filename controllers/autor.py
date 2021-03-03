from flask_restful import Resource, reqparse
from models.autor import AutorModel


serializer = reqparse.RequestParser()
serializer.add_argument(
    'autor_nombre',
    type=str,
    required=True,
    help='Falta el autor_nombre'
)


class AutoresController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        # para insertar un nuevo producto se tiene que importar de mis modelos la tabla models autor
        # se esta creando↓ una nueva instancia de nuestro modelo del autor, pero aun no se creado nada en la base de datos,
        # esto sirve para validad que los campos ingrersados cumplan con los requisitos o deficniciones de las columnas
        nuevoAutor = AutorModel(informacion['autor_nombre'])
        # Aqui ↓ ahora si se guardara los datos en la BD, si hubiese algun problema o error en la BD, pero ese indice
        # indice (pk), si es autoincrementable salta una posicion
        nuevoAutor.save()
        print(nuevoAutor)
        return {
            'succes': True,
            # se cambio de None para que se muestre el nombre del autor
            'content': nuevoAutor.json(),
            'message': 'Autor creado exitosamente!!'
        }, 201

    def get(self):
        # "select * from t_autor" # se llama al  AUTORMODEL y para decirle que se va utilizar el ORM se llama al QUERY
        lista_autores = AutorModel.query.all()
        # se le va a dar un resultado para que este lo vea el front-end
        resultado = []
        # se va a poner un ciclo FOR para traer la lsita autores
        for autor in lista_autores:
            resultado.append(autor.json())
            # nos va imprimir con el json un diccionario / cada vez que se llame con su id y su nombre correspondiente
            print(autor.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }

# -------------- Metodos para hacer busquedas -----------------------


class AutorController(Resource):
    # para devolver un solo autor, el para metro que debe de mandar el ID
    def get(self, id):
        # el .FIRST retorna el primer registro de coincidencias
        # el .ALL retorno todas las coincidencias => retorna una lista de instancias
        #
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        print(autorEncontrado)
        # si el autor se encontro retornara en el CONTENT su contenido, pero si no se hallo dicho autor,
        # indicara que el autor con el ID no existe
        # if autorEncontrado is not None: # es lo mismo poner esta linea con la de ↓ porque se sobre entiende con el condicional IF
        if autorEncontrado:
            return {
                'success': True,
                'content': autorEncontrado.json(),
                'message': None
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'El autor no existe'
            }, 404
# -----------------ACTUALIZAR O UPDATE ----se nesecitara tambien el BODY---------------------------------------

    def put(self, id):
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        # no siempre es necesaria hacer la validacion que el objeto exista, puesto que el front se debe encargar
        # de hacer toda la validacion
        if autorEncontrado:
            data = serializer.parse_args()
            autorEncontrado.autorNombre = data['autor_nombre']
            autorEncontrado.save()
            return {
                'success': True,
                'content': autorEncontrado.json(),
                'message': 'Se actualizo el autor con exito'
            }, 201
            # se utilizara el else ssi en el caso no cumple las condiciones del if
        else:  # si se usa el else se debe de indentar una linea el return
            return {
                'success': False,
                'content': None,
                'message': 'No se encontro el autor a actualizar'
            }, 404

    # ---------------------------------------------------------------------------------

    def delete(sel, id):
        autorEncontrado = AutorModel.query.filter_by(autorId=id).first()
        if autorEncontrado:
            autorEncontrado.delete()
            return {
                'success': True,
                'content': None,
                'message': 'Se elimino exitosamente el autor de la BD'
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'No se encontro el autor para eliminarlo! fuck!!'
            }, 404
        
