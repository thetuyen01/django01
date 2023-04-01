from django.urls import path
from .import views
app_name = 'chatapp'
urlpatterns = [
    path('getMessages/<int:id>/', views.getMessages, name='getMessages'),
    path('', views.home, name='home'),
    path('message/<int:id>', views.messa, name='message'),
    path('send/', views.send, name='send'),
]