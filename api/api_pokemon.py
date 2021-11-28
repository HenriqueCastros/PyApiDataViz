from flask import Flask, Response
from flask_restful import Resource, Api
from .database import Database 

print("Building API...")
app = Flask(__name__)
api = Api(app)
db = Database('https://pokeapi.co/api/v2/pokemon?limit=151')
db.save_data('./data/db.csv')

class PokemonList(Resource):
    def get(self):
        return Response(db.data.to_json(orient='records'), content_type='application/json')

class Pokemon(Resource):
    def get(self, pokemon_id):
        pokemon_procurado = db.data['id'] == pokemon_id
        pokemon = db.data[pokemon_procurado]
        return Response(pokemon.to_json(orient='records'), content_type='application/json')

api.add_resource(Pokemon, '/pokemon/<int:pokemon_id>')
api.add_resource(PokemonList, '/pokemon')
print('API ready to run!')