from django.views.generic import ListView, TemplateView

from .models import Article


class NewsListView(ListView):
    model = Article
    template_name = 'news_list.html'


class GraphView(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data()


class ResultView(TemplateView):
    template_name = 'result.html'
