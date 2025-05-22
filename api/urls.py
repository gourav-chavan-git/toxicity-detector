from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check-toxicity/', views.check_toxicity, name='check_toxicity'),
    path('clean-comment/', views.clean_comment, name='clean_comment'),
    path('generate-wordcloud/', views.wordcloud_view, name='generate_wordcloud'),
]



