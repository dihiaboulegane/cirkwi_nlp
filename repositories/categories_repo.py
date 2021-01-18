import json
from itertools import groupby

class CategoryRepo:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        with open(endpoint, "r") as read_file:
            self.data = json.load(read_file)
    
    def get_all_categories(self):
        return self.data

    def get_all_categories_ids(self):
        return([cat['_id'] for cat in self.data])
    
    def get_category_label_by_id(self, category_id_lst=None, language='en_EN'):
        if category_id_lst is not None:
            # return labels of given ids
            selected_categories = [category for category in self.data if category['_id'] in category_id_lst]
            
        else:
            # return labels of all categories
            selected_categories = self.data
        return [(category['_id'], category['translations'][language]) for category in selected_categories]


    def get_parent_by_category(self):
        return([{"_id":cat['_id'], "idParentCategory":cat['idParentCategory']} for cat in self.data])
    
    def get_children_by_category(self):
        children_by_cat_groups = groupby(self.data,key=lambda x:x['idParentCategory'])
        for parent, children in children_by_cat_groups:
            print(parent, list(children))

