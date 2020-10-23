import tqdm
import pickle
from nltk.corpus import stopwords
from scipy import spatial
import logging
from deprecated import deprecated
from pymagnitude import *


class Compare:

    def __init__(self, type='all', model_version='300d'):
        self.type = type
        self.model_version = model_version
        self.saved_ebeds_dir = {'all': '../resources/saved_noc_embeddings_glove.6B.{}.pkl'.format(self.model_version),
                                'title': '../resources/saved_noc_titles_embeddings_glove.6B.{}.pkl'.format(self.model_version),
                                'description': '../resources/saved_noc_desc_embeddings_glove.6B.{}.pkl'.format(self.model_version)}[type]
        self.embeddings = self.load_embeddings_mg(self.model_version)
        self.noc_embeddings = self.get_noc_embeddings()


    @staticmethod
    def load_document(file):
        with open(file, "r") as f:
            data = f.read().replace('\n', ' ')
        return data


    # Tokenize words
    def unicode_text(self,text):
        pattern = r'[\w-]+'
        unicode_pattern = re.compile(pattern, re.UNICODE)
        words_list = unicode_pattern.findall(text)
        text = [i for i in words_list]
        text = self.remove_stop_words(text)

        return text

    @staticmethod
    def remove_stop_words(tokens):
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in tokens if w not in stop_words and not re.search(r'\d+', w)]
        return filtered_sentence


    @deprecated
    def load_embeddings(self, model_version):
        embeddings = {}
        with open("../model/glove.6B/glove.6B.{}.txt".format(model_version)) as glove_file:
            for line in tqdm.tqdm(glove_file, desc="reading embeddings", total=400000):
                start = line.find(" ")
                word = line[:start]
                embeddings[word] = np.fromstring(line[start:], sep=" ", dtype=np.float32)

        return embeddings


    @staticmethod
    def load_embeddings_mg(model_version):
        vectors = Magnitude("../model/glove.6B/glove.6B.{}.magnitude".format(model_version))
        logging.info('Embeddingns loaded')

        return vectors


    @staticmethod
    def preprocess_embeddings(text, embeddings):
        weights = embeddings.query(text)
        weights = [w/len(weights) for w in list(map(sum, zip(*weights)))]

        return weights

    def get_noc_embeddings(self):
        documents = []
        if os.path.exists(self.saved_ebeds_dir):
            noc_embeddings = pickle.load(open(self.saved_ebeds_dir, 'rb'))
        else:
            if self.type is 'description':
                for file in os.listdir('../resources/jds'):
                    if not file.endswith('.DS_Store'):
                        documents.append([file, self.load_document(os.path.join('../resources/jds', file))])
                logging.info('Descriptions loaded')
            elif self.type is 'title':
                for file in os.listdir('../resources/jds'):
                    if not file.endswith('.DS_Store'):
                        documents.append([file, file.split('_')[1].split(': ')[0].split('.txt')[0]])
                logging.info('Titles loaded')
            else:
                for file in os.listdir('../resources/jds'):
                    if not file.endswith('.DS_Store'):
                        documents.append([file, file.split('_')[1].split(': ')[0].split('.txt')[0]+'.'+self.load_document(os.path.join('../resources/jds', file))])
                logging.info('Titles and descriptions loaded')

            noc_embeddings = [[document[0], self.preprocess_embeddings(self.unicode_text(document[1]), self.embeddings)] for document in documents]
            with open(self.saved_ebeds_dir, 'wb') as f:
                pickle.dump(noc_embeddings, f)
        logging.info('Embeddings processed')
        return noc_embeddings


    @staticmethod
    def get_cos_distance(noc_embed, embed):
        return {noc_embed[n][0]: spatial.distance.cosine(noc_embed[n][1], embed) for n in range(len(noc_embed))}

    def process(self,text):
        text = text.lower().strip()
        processed_text = self.unicode_text(text.replace('\r\n', '.').replace('\r','.').replace('\n','.'))
        my_embedding = self.preprocess_embeddings(processed_text, self.embeddings)
        cos_distances = self.get_cos_distance(self.noc_embeddings, my_embedding)
        top_results = sorted(cos_distances.items(), key=lambda x: x[1])[0:3]
        top_names, top_codes, top_distance = [], [], []
        for item in top_results:
            splitted_names = item[0].split('_')
            top_codes.append(splitted_names[0])
            top_names.append(splitted_names[1].split('.txt')[0])
            top_distance.append(item[1])

        return top_codes, top_names, processed_text
