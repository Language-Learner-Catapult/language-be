import numpy as np
#from gensim.models import KeyedVectors
import heapq
from util import difficulty
import sys

# Load the word embedding model
#model = KeyedVectors.load('./vector_models/complete.kv', mmap='r')

# Initialize data structures
#usage_counts = {word: 0 for word in model.index2word}
#usability_scores = {word: np.random.uniform(0, 1) for word in model.index2word}

def is_spanish(word):
    # Placeholder for a more accurate language detection mechanism
    return word in model

def get_word_difficulty(word):
    # Placeholder function for word difficulty
    return difficulty.get_word_difficulty(word, model)

def calculate_proficiency_update(query, current_proficiency):
    words = query.split()
    spanish_words = [word for word in words if is_spanish(word)]
    spanish_percentage = len(spanish_words) / len(words) if words else 0

    if spanish_words:
        difficulties = [get_word_difficulty(word) for word in spanish_words]
        avg_difficulty = np.mean(difficulties)
    else:
        avg_difficulty = current_proficiency

    # Calculate the updated proficiency based on the Spanish percentage and word difficulties
    proficiency_change = spanish_percentage * (avg_difficulty - current_proficiency)
    updated_proficiency = min(max(current_proficiency + proficiency_change, 1), 100)

    return updated_proficiency

def recommend_words(query, proficiency, top_n=3):
    # Filter the query to include only words present in the model
    query_words = [word for word in query.split() if word in model]

    # Initialize an empty list for the final recommended words
    recommended = []

    if query_words:
        # For each query word, find the top 50 similar words in the model
        all_similar_words = []
        for query_word in query_words:
            all_similar_words.extend(model.most_similar(query_word, topn=50))

        # Rank these words based on a composite score that considers similarity, usage counts, and word difficulty
        word_scores = []
        for word, similarity in all_similar_words:
            # Only consider words that are within the desired difficulty range
            if get_word_difficulty(word) <= proficiency + 10:
                composite_score = similarity + usage_counts[word] * 0.1 - get_word_difficulty(word) * 0.1
                heapq.heappush(word_scores, (composite_score, word))

        # Get the top N words based on the composite score
        recommended = [word for _, word in heapq.nlargest(top_n, word_scores)]

    return recommended


def process_query(query, current_proficiency):
    if(query == ''):
        return [], 0
    print('i get here')
    updated_proficiency = calculate_proficiency_update(query, current_proficiency)
    print('new proficiency: ', updated_proficiency)
    recommended_words = recommend_words(query, updated_proficiency, 3)  # Adjusted the argument to the function call
    print(recommended_words)
    return recommended_words, updated_proficiency