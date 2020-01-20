from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # url('^books/$', views.BooksView.as_view()),
    # url('^books/(?P<pk>\d+)/$', views.BookView.as_view()),

    # url('^books/$', views.BooksViewSet.as_view({'get': 'list', 'post': 'create'})),
    # url('^books/(?P<pk>\d+)/$', views.BooksViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # url('^books/hot/$', views.BooksViewSet.as_view({'get': 'hot'})),
    # url('^books/(?P<pk>\d+)/btitle/$', views.BooksViewSet.as_view({'get': 'btitle'}))
]

router = DefaultRouter()
router.register('books', views.BooksViewSet, base_name='books')
urlpatterns += router.urls
