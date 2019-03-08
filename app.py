from flask import Flask
from flask_restful import fields, marshal_with, reqparse, Resource, Api
from App.BackEnd.database.manager import Manager
from App.BackEnd.resources.Tienda.Tienda import Tienda

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'id_tienda', dest='id_tienda',
    type=int, location='form',
    required=True
)
post_parser.add_argument(
    'nombre_tienda', dest='nombre_tienda',
    location='form', required=True
)
post_parser.add_argument(
    'direccion_tienda', dest='direccion_tienda',
    location='form',
    required=True
)
post_parser.add_argument(
    'categoria', dest='categoria',
    location='form',
    required=True
)
post_parser.add_argument(
    'imagen_portada_tienda', dest='imagen_portada_tienda',
    location='form',
    required=True
)
post_parser.add_argument(
    'contacto', dest='contacto',
    location='form',
    required=True
)

tienda_fields = {
    'id_tienda': fields.Integer,
    'nombre_tienda': fields.String,
    'direccion_tienda': fields.String,
    'categoria': fields.String,
    'imagen_portada_tienda': fields.String,
    'contacto': fields.String
}

#
# tienda = Tienda(args['id_tienda'],              args['nombre_tienda'],
#                         args['direccion_tienda'],       args['categoria'],


db = Manager()
db.agregar_tienda(Tienda(111, "test", "sarasa street", "random", "fake_url.com", "01101010"))
tiendas = db.extraer_todas_tiendas()

class TiendaEndpoint(Resource):

    @marshal_with(tienda_fields)
    def get(self, id_tienda):
        tienda = db.extraer_tienda(id_tienda)
        return tienda

    @marshal_with(tienda_fields)
    def post(self):
        args = post_parser.parse_args()
        pass

app = Flask(__name__)
api = Api(app)
api.add_resource(TiendaEndpoint, '/api/tienda/<int:id_tienda>')

if __name__ == '__main__':
    app.run(debug=True)