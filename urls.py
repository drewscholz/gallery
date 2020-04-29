from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.directory, name='directory'),
    path('img_select/<str:img>/', views.select, name='img_select')
]
