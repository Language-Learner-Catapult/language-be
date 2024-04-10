import numpy as np
def get_word_length(word):
    return len(word)

def get_pronunciation_complexity(word):
    # This would ideally be a lookup in a phonetic database
    # For now, we'll assume a complexity based on word length as a placeholder
    return np.log(len(word) + 1)

def get_usage_frequency(word,model):
    # Infer usage frequency from the word's vector magnitude or frequency count if available
    # High frequency words tend to have vectors with smaller magnitudes due to normalization
    if word in model:
        return 1 / (np.linalg.norm(model[word]) + 0.0001)  # Adding a small value to avoid division by zero
    return 0

def get_morphological_complexity(word):
    # Simplified approximation: count of syllables or morphemes
    # Here, just a placeholder based on the length of the word
    return len(word) // 3 + 1

def get_context_variability(word,model):
    # If available, use data on how many different contexts the word appears in
    # Here, we might use vector variance as a proxy, but this is a placeholder
    return np.var(model[word]) if word in model else 0

def get_word_difficulty(word, model):
    # Calculate the difficulty components
    length_difficulty = get_word_length(word)
    pronunciation_complexity = get_pronunciation_complexity(word)
    usage_frequency = get_usage_frequency(word, model)
    morphological_complexity = get_morphological_complexity(word)
    context_variability = get_context_variability(word,model)

    # Combine these factors into a single difficulty score
    difficulty = (length_difficulty * 0.2 +
                  pronunciation_complexity * 0.2 +
                  usage_frequency * 0.2 +
                  morphological_complexity * 0.2 +
                  context_variability * 0.2)

    # Normalize or scale the difficulty score
    normalized_difficulty = np.tanh(difficulty / 50)  # Using hyperbolic tangent for scaling to [0,1]

    return normalized_difficulty
