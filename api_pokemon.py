from flask import Flask, Response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class PokemonList(Resource):
    def get(self):
        return Response(my_data.data.to_json(orient='records'), content_type='application/json')

class Pokemon(Resource):
    def get(self, pokemon_id):
        pokemon_procurado = my_data.data['id'] == pokemon_id
        pokemon = my_data.data[pokemon_procurado]
        return Response(pokemon.to_json(orient='records'), content_type='application/json')

api.add_resource(Pokemon, '/pokemon/<int:pokemon_id>')
api.add_resource(PokemonList, '/pokemon')
