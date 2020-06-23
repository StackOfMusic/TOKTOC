from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, RedirectView

from .models import Article
from toktoc.core import data_preprocessing_sem, ir_model, select_date, sentiment_analysis, topic_modeling
from django.conf import settings

CORE_DIR = settings.BASE_DIR + '/core/'

class NewsListView(ListView):
    model = Article
    template_name = 'news_list.html'


class GraphView(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data()
        with open(CORE_DIR + 'topic_modeling_result_2019.txt', 'r') as f:
            result_context = f.read()
        context['topic_modeling'] = result_context

        with open(CORE_DIR + 'sem_average_1.txt', 'r') as f:
            result_context = f.read()
        context['sentiment_result1'] = result_context

        with open(CORE_DIR + 'sem_average_2.txt', 'r') as f:
            result_context = f.read()
        context['sentiment_result2'] = result_context

        return context


class ResultView(TemplateView):
    template_name = 'result.html'


class ModelView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        select_date.crawl_news()
        data_preprocessing_sem.data_preprocessing()
        ir_model.data_preprocessing()
        sentiment_analysis.sentiment_analysis()
        topic_modeling.topic_modeling()
        return super(ModelView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('home')
