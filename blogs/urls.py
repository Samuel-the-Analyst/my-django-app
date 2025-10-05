from django.urls import path
from .views import PostListView, PostView, UserPostListView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('user/<str:username>/', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostView.as_view(), name="post"),
    path('post/new/', PostCreateView.as_view(), name="create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),
    path('about/', views.About, name="about"),
]