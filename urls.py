from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.directory, name='directory'),
    path('select/<str:img>/', views.select, name='select'),
    path('page/<str:page>/', views.page, name='page')
]
