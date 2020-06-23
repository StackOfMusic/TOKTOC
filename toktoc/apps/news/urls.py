from django.urls import path
from .views import ResultView, NewsListView, GraphView, ModelView


app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('graph/', GraphView.as_view(), name='graph'),
    path('result/', ResultView.as_view(), name='result'),
    path('ir_module/', ModelView.as_view(), name='model'),
]