from django.urls import path

from blog import views

urlspatterns = [
    path('', views.post_list, name='post_link'),
    path('<int:id>', views.post_datail, name='post_detail'),
]
