import tqdm
import pickle
from nltk.corpus import stopwords
from scipy import spatial
import logging
from pymagnitude import *


def load_document(file):
    with open(file, "r") as f:
        data = f.read().replace('\n', ' ')
    return data


# Tokenize words
def unicode_text(text):
    pattern = r'[\w-]+'
    unicode_pattern = re.compile(pattern, re.UNICODE)
    words_list = unicode_pattern.findall(text)
    text = [i for i in words_list]
    text = remove_stop_words(text)
    return text


def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokens if w not in stop_words]
    return filtered_sentence


def load_embeddings():
    embeddings = {}
    with open("../model/glove.6B/glove.6B.300d.txt") as glove_file:
        for line in tqdm.tqdm(glove_file, desc="reading embeddings", total=400000):
            start = line.find(" ")
            word = line[:start]
            embeddings[word] = np.fromstring(line[start:], sep=" ", dtype=np.float32)

    return embeddings


def load_embeddings_mg():
    vectors = Magnitude("../model/glove.6B/glove.6B.300d.magnitude")

    return vectors


def preprocess_embeddings(text, embeddings):
    weights = embeddings.query(text)
    weights = [w/len(weights) for w in list(map(sum, zip(*weights)))]

    return weights


def process(title):
    titles = []
    embeddings = load_embeddings_mg()
    logging.info('Embeddingns loaded')

    if os.path.exists('../resources/saved_noc_titles_embeddings_glove.6B.300d.pkl'):
        noc_embeddings = pickle.load(open('../resources/saved_noc_titles_embeddings_glove.6B.300d.pkl', 'rb'))
    else:
        for file in os.listdir('../resources/jds'):
            if not file.endswith('.DS_Store'):
                titles.append([file, file.split('_')[1].split(': ')[0].split('.txt')[0]])
        logging.info('Titles loaded')

        noc_embeddings = [[document[0], preprocess_embeddings(unicode_text(document[1]), embeddings)] for document in titles]
        with open('../resources/saved_noc_titles_embeddings_glove.6B.300d.pkl', 'wb') as f:
            pickle.dump(noc_embeddings, f)
    logging.info('Embeddings processed')

    my_embedding = preprocess_embeddings(unicode_text(title), embeddings)
    #
    # r1 = {noc_embeddings[n][0]:sum([(x1 - x2) ** 2 for (x1, x2) in zip(noc_embeddings[n][1], my_embedding)]) ** 0.5 for n in range(len(noc_embeddings))}
    # print(sorted(r1.items(), key=lambda x:x[1])[0:3])

    cos_results = {noc_embeddings[n][0]: spatial.distance.cosine(noc_embeddings[n][1], my_embedding) for n in range(len(noc_embeddings))}
    top_results = sorted(cos_results.items(), key=lambda x: x[1])[0:3]
    top_names = []
    top_codes = []
    top_distance = []
    for item in top_results:
        splitted_names = item[0].split('_')
        top_codes.append(splitted_names[0])
        top_names.append(splitted_names[1].split('.txt')[0])
        top_distance.append(item[1])

    return top_codes, top_names


def main():
    top_codes, top_names = process('Backend Software Engineer')
    print(list(zip(top_codes, top_names)))


if __name__ == '__main__':
    main()
