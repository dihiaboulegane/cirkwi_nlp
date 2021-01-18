import json
from itertools import groupby

class POIRepo:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        with open(endpoint, "r") as read_file:
            self.data = json.load(read_file)
    
    def get_all_pois(self):
         return self.data

    def get_categories_by_poi(self, unique_id=None):
        if unique_id is not None:
            # Return categories of a given POI
            poi = next((p for p in self.data if p['id'] == unique_id), None)
            return poi['categories']
        else:
            # Return categories by POI
            return [(poi['id'], poi['categories']) for poi in self.data]
    
    def get_informations_by_poi(self, poi_id_lst=None):
        # reformat 
        if poi_id_lst is not None:
            # Filter POIs in list only
            poi_lst = [poi for poi in self.data if poi['id'] in poi_id_lst]
        else:
            poi_lst = self.data
        # reformat POIs to handle en_EN and fr_FR labels
        # Information is kept in field 'locales'


        return [ {'id': poi['id'], 
                  'title': poi[f'translations.{poi["locales"][0]}.title'] , 
                  'description': poi[f'translations.{poi["locales"][0]}.description'], 
                  'categories': poi['categories']} for poi in poi_lst]

    def get_pois_by_category(self, category_id=None):
        if category_id is not None:
            # Documeznts of a given category
            return [d for d in self.data if category_id in d['categories']]
        else:
            # Map for each category its documents
            # Get list of categories
            category_id_lst = set()
            _ = [category_id_lst.update(d['categories']) for d in self.data]
            
            category_id_lst = list(category_id_lst)
            
            poi_by_category = map(lambda cat_id: [d for d in self.data if cat_id in d['categories']], category_id_lst)
            return {cat:poi_lst for cat, poi_lst in zip(category_id_lst, poi_by_category)}
