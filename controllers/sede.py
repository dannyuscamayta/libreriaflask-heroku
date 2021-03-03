from flask_restful import Resource, reqparse
from models.sede import SedeModel
# basico
# get all sede
# create sede
# vinvula una sede con varios libros y viceversa(un libro con varias sedes)
# el bundle_errors es para que me mande en el postman todos los datos o errores que falte
serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Falta la sede_ubicacion',
    location='json',
    # en vez de repetir 'sede_ubicacion' y reducir el codigo se puede poner DEST (sera como un alias) es como se va allamar una vez que hemos usado el metodo parse_args()
    dest='ubicacion'
)

serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    location='json',
    dest='latitud'
)

serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    location='json',
    dest='longitud'
)


class SedesController(Resource):
    def post(self):
        # para que funcione el filtro del serializer
        data = serializer.parse_args()
        print(data)
        # los tipos de datos que no son NI NUMERICOS, NI STRINGS = que son igual a DECIMAL; FECHA no puede hacer la conversion automatica
        # estos nombres o alias como latitud, longitud etc viene desde el DEST de serializer
        nuevaSede = SedeModel(
            data['ubicacion'], data['latitud'], data['longitud'])
        nuevaSede.save()
        return {
            'success': True,
            'content': nuevaSede.json(),
            'message': ' se creo la sede exitosamente'
        }, 201  # estado de creacion

    def get(self):
        sedes = SedeModel.query.all()
        resultado = []
        for sede in sedes:
            resultado.append(sede.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }


# busqueda de todos los libros de una clase

class LibroSedeController(Resource):
    def get(self, id_sede):
        # de acuerdo al id de la sede, devolver todos los libros que hay en esa sede
        sede = SedeModel.query.filter_by(sedeId=id_sede).first()
        sedeLibros = sede.libros  # todas mis sede libros
        libros = []
        for sedeLibro in sedeLibros:
            libro = sedeLibro.libroSede.json()
            # para mostrar el autor ↓ del libro ID ingresado en el postman
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            # para agregar la categoria del libro pero solamente su desccripcion(NO SE NECESITA EL ID) de la categoria
            libro['categoria'] = sedeLibro.libroSede.categoriaLibro.json()
            # para no mostrar la categoria (borrar los ID de la catgoria y del autor) para que no sea repetitivo DEL
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
        resultado = sede.json()
        resultado['libros'] = libros
        return {
            'succes': True,
            'content': resultado
        }
        # pass

# busqueda de todos los libros de una sede segun su categoria (es el mas dificil)
# categoria
# sede
# si quiero que mi ruta sea http://127.0.0.1:5000/buscarLibroCategoria?sede=1%categoria=2


class LibroCategoriaSedeController(Resource):

    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')

        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta la categoria',
            location='args'
        )

        serializer.add_argument(
            'sede',
            type=int,
            required=True,
            help='Falta la sede',
            location='args'  # ARGS es para que me mande la data por la URL ↑ querysString (de forma dinamica)
            # si se quiere recibir la data por el BODY seria => JSON
        )

        # buscar los todos lo libros segun  su SEDE
        data = serializer.parse_args()
        sede = SedeModel.query.filter_by(sedeId = data['sede']).first()
        #print(sede.libros)
        libros = []
        for sedelibro in sede.libros:
            print(sedelibro.libroSede.categoria)
            if(sedelibro.libroSede.categoria == data['categoria']):
                libros.append(sedelibro.libroSede.json())

        # para imprimir esto se necesitara la RUTA
        #print(data)
        return {
            'success': True,
            'content': libros
        }
