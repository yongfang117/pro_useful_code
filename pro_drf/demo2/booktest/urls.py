from django.conf.urls import url
from . import views

urlpatterns = [
    url('^books/$', views.BooksView.as_view()),
    url('^books/(?P<pk>\d+)/$', views.BookView.as_view()),
    url('^heros/(?P<pk>\d+)/$', views.HeroView.as_view()),
]
