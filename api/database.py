import pandas as pd
import requests

class Database(): 
    def __init__(self, url, top_n_types=5):
        self.url = url
        self.top_n_types = top_n_types
        self.data = pd.DataFrame()
        self.aggr_data = pd.DataFrame()
        self.__load_data__()
        self.__format_data__()
        self.__aggr_data__()
    
    def __load_data__(self):
        print('Importing data...')
        r = requests.get(self.url)
        x = r.json()
        web_data = pd.DataFrame(x['results'])
        self.data = web_data['url'].apply(lambda x: pd.Series(requests.get(x).json()))
        print('Data successfully imported!')

    def __format_data__(self):
        self.data['moves_len'] = self.data['moves'].apply(lambda x: len(x))
        self.data['abilities_len'] = self.data['abilities'].apply(lambda x: len(x))
                        

        self.data = pd.concat([self.data, self.data['stats']\
            .apply(lambda x: pd.Series({stat['stat']['name']: stat['base_stat'] for stat in x}))],axis=1)

        self.data['main_type'] = self.data['types'].apply(lambda x: x[0]['type']['name'])
        self.data = self.data.drop(['held_items', 'location_area_encounters', 'moves', 'abilities', 'stats', 'types',
                        'forms', 'game_indices', 'past_types', 'species', 'sprites'], axis=1)

        other_types = self.data.groupby(['main_type']).count().sort_values(by=['id'], ascending=False).index[self.top_n_types:]
        self.data['top_n_types'] = self.data['main_type'].apply(lambda x: x if x not in other_types else 'other')

    def __aggr_data__(self):
        stats_df = self.data[['top_n_types', 'hp', 'attack', 'defense', 'special-attack','special-defense','speed']]
        self.aggr_data = pd.melt(stats_df, 'top_n_types', var_name='stat')\
            .groupby(by=['top_n_types','stat'])['value']\
                .agg(['mean', 'max', 'min','std']).reset_index()

    def save_data(self, file_name):
        self.data.to_csv(file_name)
