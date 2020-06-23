import pandas as pd
from textblob import TextBlob
from django.conf import settings


def sentiment_analysis():
    year_dict = {
        1: '2019',
        2: '2020',
    }
    end_month = [12, 5]

    sem_average = []

    for i in range(2):
        data_dir = settings.BASE_DIR + '/core/' + year_dict[i + 1] + '_sem/'

        data = pd.read_pickle(data_dir + 'corpus.pkl')

        pol = lambda x: TextBlob(x).sentiment.polarity
        #sub = lambda x: TextBlob(x).sentiment.subjectivity

        data['polarity'] = data['transcript'].apply(pol)
        #data['subjectivity'] = data['transcript'].apply(sub)

        sem_avg = []
        for month in range(end_month[i]):
            total_sem = 0.0
            data_num = 100
            if month + 1 == 10:
                data_num = 97
            for file_iter in range(100):
                if month + 1 == 10 and file_iter > 96:
                    break
                key = str(month + 1) + '_' + str(file_iter)
                total_sem += data['polarity'][key]

            sem_avg.append(total_sem / data_num)

        sem_average.append(sem_avg)

    with open('sem_average_0.txt', 'w') as f:
        data = sem_average[0]
        f.write(data)

    with open('sem_average_1.txt', 'w') as f:
        data = sem_average[1]
        f.write(data)
