import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from django.conf import settings


def clean_text_round1(text):
    text = text.lower()
    text = re.sub('[.,\'\"()’”“—–:\-\[\]]', '', text)
    text = re.sub('\n', '', text)
    return text


def data_preprocessing():
    year_dict = {
        1: '2019',
        2: '2020',
    }
    end_month = [12, 5]

    pd.set_option('max_colwidth', 150)

    for i in range(2):
        data = {}
        data_dir = settings.BASE_DIR + '/core/' + year_dict[i + 1] + '/'
        for j in range(end_month[i]):
            name = data_dir + str(j + 1) + '.txt'
            with open(name, "rb") as f:
                data[j + 1] = [pickle.load(f)]

        data_df = pd.DataFrame.from_dict(data).transpose()
        data_df.columns = ['transcript']
        data_df = data_df.sort_index()

        round1 = lambda x: clean_text_round1(x)

        data_clean = pd.DataFrame(data_df.transcript.apply(round1))

        data_df.to_pickle(data_dir + "corpus.pkl")

        cv = CountVectorizer(stop_words='english')
        data_cv = cv.fit_transform(data_clean.transcript)
        data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_dtm.index = data_clean.index

        data_dtm.to_pickle(data_dir + "dtm.pkl")
        data_clean.to_pickle(data_dir + 'data_clean.pkl')
        pickle.dump(cv, open(data_dir + "cv.pkl", "wb"))

