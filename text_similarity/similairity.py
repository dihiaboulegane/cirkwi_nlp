import nltk, string
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


from google_trans_new import google_translator  
translator = google_translator()

from sklearn.metrics.pairwise import cosine_similarity

# Stemmer will be used to transform words into their respective stems
# This will group words with the same meaning but different derivations into the same root
stemmer = nltk.stem.porter.PorterStemmer()

def translate_text(text, dest):
    # Language is detected automatically
    result = translator.translate(text, lang_tgt=dest)
    return result


def clean_text(text, language='english'):
    # Pepresent as bag of words
    text = translate_text(text.lower(), language)
    bag_of_words = word_tokenize(text)
    # Remove ponctuation
    bag_of_words = [w for w in bag_of_words if w  not in string.punctuation]
    # Remove stop words
    bag_of_words = [w for w in bag_of_words if w  not in stopwords.words(language)] 
    # Stemming
    bag_of_words = [stemmer.stem(w) for w in bag_of_words]
    
    return bag_of_words


def word_frequency(bag_of_words):
    word_counter = Counter(bag_of_words)
    print(word_counter)

def tf_idf_embedding(corpus):
    # Clean each text in corpus
    corpus = [''.join(clean_text(text)) for text in corpus]
    # Fit a TF-IDF word Model
    vectorizer = TfidfVectorizer()
    tf_idf_model  = vectorizer.fit_transform(corpus)
    pairwise_similarity = cosine_similarity(tf_idf_model)
    # pairwise_similarity = tf_idf_model * tf_idf_model.T 
    print(pairwise_similarity)
    return pairwise_similarity


if __name__ == "__main__":
    print(translate_text('Bonjour', 'en'))
    text = "The Saint-Michel church, like all the churches of Haute Maurienne Vanoise, has undergone major changes over the centuries. It shelters the relics of Saint-Landry, monk of the abbey of Novalaise."
    text = "Instants Nature - Au choeur du brame en Sologne. Les Rencontres avec la faune. Vivez des instants précieux dans l'intimité du Cerf. Plongés au cœur du brame, dans l'obscurité de la nuit, frissons et émotions seront au rendez-vous. Une balade en quête d'indices de présence et une pause gourmande au milieu des bois compléteront agréablement cette sortie."
    # text_2 = "The Chemins of the History of Val Cenis in Haute Maurienne Vanoise is a circuit gathering the discovery of several chapels starting from the chapel Saint-Roch (see opening time). A key given by the hostess will allow you their opening."

    text = clean_text(text)
    print(text)
    # tf_idf_embedding([text, text_2])