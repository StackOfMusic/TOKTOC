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
        data_dir = settings.BASE_DIR + '/core/' + year_dict[i + 1] + '_sem/'
        data = {}
        for month in range(end_month[i]):
            for j in range(100):
                if i == 0 and month == 9 and j > 96:
                    break
                name = str(month + 1) + '_' + str(j)
                full_path = data_dir + name + '.txt'
                with open(full_path, "rb") as f:
                    data[name] = [pickle.load(f)]

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
