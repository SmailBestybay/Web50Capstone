from django.urls import path
from . import views

app_name = 'ourtube'
urlpatterns = [
    path('', views.OurtubeTemplateView.as_view(), name='index'),
    path('feed/<int:feed_id>', views.FeedView.as_view(), name='feed'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('signup/', views.SignUpView.as_view(), name ='signup'),
]