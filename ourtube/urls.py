from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feed/<int:feed_id>/', views.feed, name='feed'),
    path('search/', views.search_view, name='search'),
    path('join_or_create_feed/', views.join_or_create_feed, name='join_or_create_feed'),
    # path('search/<str:search_channel>', views.search_view, name='search'),
]