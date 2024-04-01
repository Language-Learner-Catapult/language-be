import numpy as np
from gensim.models import KeyedVectors
import heapq
from util import difficulty
import sys

# Load the word embedding model
model = KeyedVectors.load('./vector_models/complete.kv', mmap='r')

# Initialize data structures
usage_counts = {word: 0 for word in model.index2word}
usability_scores = {word: np.random.uniform(0, 1) for word in model.index2word}

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

def recommend_words(query, proficiency, top_n=10):
    # Pre-filter the vocabulary based on the difficulty level
    candidate_words = [word for word in model.index2word if get_word_difficulty(word) <= proficiency + 10]

    # Filter the query to include only words present in the model
    query_words = [word for word in query.split() if word in model]

    # Limit the number of words for similarity calculation
    candidate_words = candidate_words[:1000]  # Adjust based on performance needs

    # Calculate similarity and composite score for the candidate words
    word_scores = []
    for candidate_word in candidate_words:
        # Compute similarities for each word in the query and take the average
        if query_words:
            similarities = [model.similarity(query_word, candidate_word) for query_word in query_words]
            avg_similarity = sum(similarities) / len(similarities)
            composite_score = avg_similarity + usage_counts[candidate_word] * 0.1 + usability_scores[candidate_word] * 0.1
            heapq.heappush(word_scores, (-composite_score, candidate_word))  # Using negative to prioritize higher scores

            # Keep only the top N scoring words in the heap
            if len(word_scores) > top_n:
                heapq.heappop(word_scores)
        else:
            break  # Exit the loop if no valid query words are found

    # Extract words from the heap, highest scores first
    recommended = [word for _, word in heapq.nlargest(top_n, word_scores)]
    return recommended



def process_query(query, current_proficiency):
    if(query == ''):
        return current_proficiency, []
    print('i get here')
    updated_proficiency = calculate_proficiency_update(query, current_proficiency)
    print('new proficiency: ', updated_proficiency)
    recommended_words = recommend_words(query, updated_proficiency, 3)  # Adjusted the argument to the function call
    print(recommended_words)
    return recommended_words, updated_proficiency