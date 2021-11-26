import numpy as np 
import pandas as pd
import requests

class DataLoader(): 
    def __init__(self, url):
        self.url = url
        self.data = pd.DataFrame()
        self.__load_data__()
        self.__format_data__()
    
    def __load_data__(self):
        r = requests.get(self.url)
        x = r.json()
        web_data = pd.DataFrame(x['results'])
        self.data =  web_data['url'].apply(lambda x: pd.Series(requests.get(x).json()))
        # self.data = pd.concat([web_data, web_data['url'].apply(lambda x: pd.Series(requests.get(x).json()))], axis = 1)

    def __format_data__(self):
        self.data['moves_len'] = self.data['moves'].apply(lambda x: len(x))
        self.data['abilities_len'] = self.data['abilities'].apply(lambda x: len(x))
                        

        self.data = pd.concat([self.data, self.data['stats']\
            .apply(lambda x: pd.Series({stat['stat']['name']: stat['base_stat'] for stat in x}))],axis=1)

        self.data['main_type'] = self.data['types'].apply(lambda x: x[0]['type']['name'])
        self.data = self.data.drop(['held_items', 'location_area_encounters', 'moves', 'abilities', 'stats', 'types',
                        'forms', 'game_indices', 'past_types', 'species', 'sprites'], axis=1)

    
    def save_data(self, file_name):
        self.data.to_csv(file_name)
