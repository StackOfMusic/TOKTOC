import pandas as pd
import pickle
from gensim import matutils, models
import scipy.sparse
from nltk import word_tokenize, pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from django.conf import settings
import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')


def nouns_adj(text):
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ' or pos[:2] == 'NNP'
    tokenized = word_tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
    return ' '.join(nouns_adj)


def topic_modeling():
    year_dict = {
        1: '2019',
        2: '2020',
    }

    for i in range(2):
        print(year_dict[i + 1] + 'results---------------------------------------')
        data_dir = settings.BASE_DIR + '/core/' + year_dict[i + 1] + '/'

        #data = pd.read_pickle(data_dir + 'dtm.pkl')
        data_clean = pd.read_pickle(data_dir + 'data_clean.pkl')

        data_nouns_adj = pd.DataFrame(data_clean.transcript.apply(nouns_adj))

        cnva = CountVectorizer(stop_words='english', max_df=.8)
        data_cnva = cnva.fit_transform(data_nouns_adj.transcript)
        data_dtmna = pd.DataFrame(data_cnva.toarray(), columns=cnva.get_feature_names())
        data_dtmna.index = data_nouns_adj.index

        tdm = data_dtmna.transpose()

        sparse_counts = scipy.sparse.csr_matrix(tdm)
        corpusna = matutils.Sparse2Corpus(sparse_counts)

        #cv = pickle.load(open(data_dir + "cv.pkl", "rb"))
        id2wordna = dict((v, k) for k, v in cnva.vocabulary_.items())

        ldana = models.LdaModel(corpus=corpusna, id2word=id2wordna, num_topics=12, passes=80)

        for i in range(12):

            with open('topic_modeling_result', 'w') as f:
                data = ldana.print_topics()[i]
                f.write(data)

        #corpus_transformed = ldana[corpusna]
        #print(list(zip([a for [(a,b)] in corpus_transformed], data_dtmna.index)))
