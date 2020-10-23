import tqdm
import pickle
from nltk.corpus import stopwords
from scipy import spatial
import logging
from pymagnitude import *
from src.Compare import Compare


class CompareJD(Compare):
    def get_noc_embeddings(self):
        documents = []
        if os.path.exists('../resources/saved_noc_embeddings_glove.6B.{}.pkl'.format(self.model_version)):
            noc_embeddings = pickle.load(open('../resources/saved_noc_embeddings_glove.6B.{}.pkl'.format(self.model_version), 'rb'))
        else:
            for file in os.listdir('../resources/jds'):
                if not file.endswith('.DS_Store'):
                    documents.append([file, self.load_document(os.path.join('../resources/jds', file))])
            logging.info('Documents loaded')

            noc_embeddings = [[document[0], self.preprocess_embeddings(self.unicode_text(document[1]), self.embeddings)] for document in documents]
            with open('../resources/saved_noc_embeddings_glove.6B.300d.pkl', 'wb') as f:
                pickle.dump(noc_embeddings, f)
        logging.info('Embeddings processed')
        return noc_embeddings

    def process(self, jd_text):
        my_embedding = self.preprocess_embeddings(self.unicode_text(jd_text.replace('\n', '.')), self.load_embeddings_mg())
        cos_distances = self.get_cos_distance(self.noc_embeddings, my_embedding)
        top_results = sorted(cos_distances.items(), key=lambda x: x[1])[0:3]
        top_names, top_codes, top_distance = [], [], []
        for item in top_results:
            splitted_names = item[0].split('_')
            top_codes.append(splitted_names[0])
            top_names.append(splitted_names[1].split('.txt')[0])
            top_distance.append(item[1])

        return top_codes, top_names


def main():
    top_codes, top_names = process('../resources/myjd.txt')
    print(list(zip(top_codes, top_names)))


if __name__ == '__main__':
    main()
