import pandas as pd


from repositories import CategoryRepo, POIRepo
from text_similarity import tf_idf_embedding

_FR_LANG = 'fr_FR'
_ENG_LANG = 'en_EN'



def display_information_by_POI(language=_ENG_LANG):
    poi_lst = poi_repo.get_informations_by_poi()
    # poi_lst = poi_repo.get_all_pois()
    for poi in poi_lst:
        categories_labels = cat_repo.get_category_label_by_id(poi['categories'], language=language)
        poi['labels'] = [cat[1] for cat in categories_labels]
    
    df = pd.DataFrame(poi_lst)
    df.style.set_properties(**{'text-align': 'center'})
    df.to_html('pois.html', columns=['title', 'description', 'labels'], index=False, justify='center')
    # print(poi_lst)


def category_similarity_by_poi():
    # Get POIs  by category, every category will be  represented by its POIs
    pois_by_category = poi_repo.get_pois_by_category()
    # attach to each category the title and description of its POIs
    category_text = {}
    for category, poi_lst in pois_by_category.items():
        
        pois_text = poi_repo.get_informations_by_poi([poi['id'] for poi in poi_lst])
        
        pois_text = [' '.join([poi['title'], poi['description']]) for poi in pois_text]
        
        category_text[category] = ' '.join(pois_text)
    # Pairwise similarity matrix using TF-IDF and Cosine similarity
    pairwise_similarity = tf_idf_embedding(category_text.values())
    
    # Compute for each POI, pairwise similarity of its categories
    all_pois_lst = poi_repo.get_all_pois()
    all_categories_id = list(category_text.keys())
    for poi in all_pois_lst:
        
        poi_categories = poi['categories']
        poi_categories_label = [cat_label for cat_id, cat_label in cat_repo.get_category_label_by_id(poi_categories)]
        print(f'######## \nPOI: {poi["id"]} \nCategories: {", ".join(poi_categories_label)}')
        poi_categories_idx = [all_categories_id.index(cat) for cat in poi_categories]
        # print(all_categories_id)
        category_pairwise_sim = pairwise_similarity[poi_categories_idx, :][:, poi_categories_idx]
        category_pairwise_sim_df = pd.DataFrame(category_pairwise_sim, columns=poi_categories_label, index=poi_categories_label)
        print(category_pairwise_sim_df)
        


if __name__ == "__main__":
    
    # POI information display
    cat_repo = CategoryRepo(endpoint='datasets/categories.json')
    poi_repo = POIRepo(endpoint='datasets/pois.json')
    # Ouput is provided as an html file to be viewd in the browser
    display_information_by_POI()

    # Text similarity
    category_similarity_by_poi()
    
