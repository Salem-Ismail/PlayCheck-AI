import json
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Get logger
logger = logging.getLogger(__name__)

# Load FIFA Laws from JSON file
def load_fifa_laws():
    with open("fifa_laws.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Preprocess laws for keyword extraction
def preprocess_laws(laws):
    law_texts = [law["summary"].lower() for law in laws]
    return law_texts

# Search function using TF-IDF ranking
def search_law(user_query, laws, top_n=3):
    
    vectorizer = TfidfVectorizer()
    law_texts = [law["summary"] for law in laws]
    tfidf_matrix = vectorizer.fit_transform(law_texts)
    
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    top_indices = similarities.argsort()[-top_n:][::-1]  # Get top N matches
    return [(laws[i], similarities[i]) for i in top_indices]  # Return a list of top matches


# Load laws (only when module is run directly, not when imported)
if __name__ == "__main__":
    laws = load_fifa_laws()["laws"]
    logger.info(f"Loaded {len(laws)} laws from JSON file")
    
    # Example user query
    user_query = "Can a player take off their shirt when celebrating?"
    result = search_law(user_query, laws)
    logger.info(f"Search result: {result}")
