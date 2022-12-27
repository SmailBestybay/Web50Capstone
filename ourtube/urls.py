from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:feed_id>', views.feed, name='feed'),
    path('search/', views.search_view, name='search'),
    # path('search/<str:search_channel>', views.search_view, name='search'),
]