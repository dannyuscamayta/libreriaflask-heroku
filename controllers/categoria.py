# create categoria y un read all de categoria

from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel

serializer = reqparse.RequestParser()
serializer.add_argument(
    'categoria_descripcion',
    type=str,
    required=True,
    help='Falta la categoria descripcion',
    # por default intenta BUSCAR en todos los campos posibles, y si lo encuentra NO dara error, pero si queremos
    # indicar exactamente poeque medio me lo tiene que pasar debemos iundicarle la LOCATION
    location='json'
)


class CategoriaController(Resource):

    def get(self):
        categorias = CategoriaModel.query.all()
        resultado = []
        for categoria in categorias:
            # este metodo apunta a el JSON de categorias models
            resultado.append(categoria.json())
            print(categoria)
        return {
            'success': True,
            'content': resultado,
            'message': None
        }

    def post(self):
        data = serializer.parse_args()
        nuevaCategoria = CategoriaModel(data['categoria_descripcion'])
        nuevaCategoria.save()
        return {
            'success': True,
            'content': nuevaCategoria.json(),
            'messsage': 'Categoria creada exitosamente'
        }, 201

