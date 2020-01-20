from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books/$', views.BooksView.as_view()),
    url(r'^books/(?P<pk>\d+)/$', views.BookView.as_view()),
]

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('books', views.BookModelViewSet, base_name='books')
# urlpatterns += router.urls
