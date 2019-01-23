
from django.contrib import admin
from django.urls import path,include
from blog import views

urlpatterns = [

   
    path('<int:blog_pk>',views.blog_detail,name='article_detail'),
    path('b/<int:blog_type_pk>',views.blogs_with_type,name='blog_type_pk'),
    path('game',views.game,name='game'),
    path('move', views.move, name='move'),
    path('about',views.about,name='about'),
    path('login/',views.my_view,name='login'),
    path('', views.blog_list, name='list'),
    path('bargrap',views.bar,name='bar'),
    ]
