from collections import Counter
import random
import re

file_path = '/Users/jaafarbendriss/Downloads/black_hole_wiki.txt'

# Open the file and read its content
with open(file_path, 'r') as file:
    file_content = file.read()

raw_text = file_content

def add_start_end_sentence(text):
    return "start-of-sentence " + text.replace("."," end-of-sentence start-of-sentence")


def remove_citations(text):
    pattern = r"\[\d+\]"
    cleaned_text = re.sub(pattern, "", text)    
    return cleaned_text

def remove_spaces(text):
    pattern = r"\s+"
    cleaned_text = re.sub(pattern, " ", text)    
    return cleaned_text

def preprocess(text: str):
    return remove_spaces(remove_citations(add_start_end_sentence(text).lower().replace(" s ","").replace("\\","").replace("'"," ").replace('"',' ').replace(","," ").replace("\ s"," ").replace("\n"," ")))

preprocessed_text = preprocess(raw_text)

Counter(preprocessed_text.split(" ")).most_common(20)

preprocessed_text_array = preprocessed_text.split(" ")

def get_n_gram(n:str=2):
    ngrams = zip(*[preprocessed_text_array[i:] for i in range(n)])
    return ngrams#[" ".join(ngram) for ngram in ngrams]

bigram = get_n_gram(2)
counter_bigram = (Counter(bigram))

filtered_counts = {word: count for word, count in counter_bigram.items() if count >= 2}
# Calculate the total number of items
total_count = sum(filtered_counts.values())

# Calculate ratios
ratios = {word: count / total_count for word, count in filtered_counts.items()}

TOPN = 5

def get_next_words(first_word: str, ratio: bool = False):
    ngram = counter_bigram
    if (ratio):
        ngram = ratios
    return sorted([(k,v) for k,v in ngram.items() if (k[0] == first_word)], key=lambda x:x[1], reverse=True )[0:TOPN]

next_words = get_next_words("the", ratio=0)

def get_next_word(first_word: str, selection : str = "most_accurate"):
    next_words = get_next_words(first_word, ratio=False)
    if selection == "most_accurate":
        return next_words[0][0][1]
    
    if selection == "random":
        random_index = min(random.randint(0,TOPN), len(next_words)-1)
        return next_words[random_index][0][1]
    
    raise Exception("Failed option")

get_next_word("the")

def generate_sentence(N: int = 20, first_word: str = "start-of-sentence", selection: str= "random"):
    count = N
    outputed_words = []
    outputed_words.append(first_word)

    while count > 0:
        first_word = get_next_word(first_word, selection=selection)
        count-= 1
        outputed_words.append(first_word)

        if first_word == "end-of-sentence":
            break

    return " ".join(outputed_words)


for _ in range(12):
    print(generate_sentence())

