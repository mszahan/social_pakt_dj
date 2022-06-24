from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:pk>/<slug:slug>', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('', views.image_list, name='image_list'),
    path('ranking/', views.image_ranking, name='image_ranking')
]