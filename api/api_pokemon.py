from flask import Flask, Response
from flask_restful import Resource, Api
from .database import Database 
import matplotlib.pyplot as plt
import seaborn as sns

print("Building API...")
app = Flask(__name__)
api = Api(app)
db = Database('https://pokeapi.co/api/v2/pokemon?limit=151')
db.save_data('./data/db.csv')

plt.ioff()
sns.set_style('darkgrid')
sns.set(rc={'figure.figsize':(16,6)})
pallete = sns.color_palette('deep')
new_palette = dict(water=pallete[0], fire=pallete[3], bug=pallete[2], normal=pallete[5], poison=pallete[4], other=pallete[7])

class PokemonStat(Resource):
    def __save_plots__(self):
        fig, axes = plt.subplots(1, 2, sharey=True)
        sns.boxplot(x = db.data['attack'], y=db.data['top_n_types'], palette=new_palette,  ax=axes[0])
        sns.boxplot(x = db.data['defense'], y=db.data['top_n_types'], palette=new_palette,  ax=axes[1])
        plt.savefig('./last_request/boxplot.png')

        sns.jointplot(x=db.data['attack'], y=db.data['defense'], kind='reg')
        plt.savefig('./last_request/scatter.png')

        sns.pairplot(db.data[['attack', 'defense', 'speed']])
        plt.savefig('./last_request/pairplot.png')

    def get(self):
        db.aggr_data.to_csv('./last_request/stats.csv')
        self.__save_plots__()
        return Response(db.aggr_data.to_json(orient='records'), content_type='application/json')

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
api.add_resource(PokemonStat, '/pokemon_stats')
print('API ready to run!')