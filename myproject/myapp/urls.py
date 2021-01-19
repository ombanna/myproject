from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('blog_post',views.blog_post,name="blog_post"),
    path("blog/<int:id>", views.blog_detail, name="blog"),
    path("<int:id>", views.blog_detail, name="blog_detail"),
    path('addpost',views.add_show,name="addpost"),
    path('list_post',views.list_post,name="list_post"),
    path('delete/<int:id>',views.delete_data,name="deletedata"),
    path('update/<int:id>',views.update_data,name="updatedata"),
    path('blogpost_like/<int:id>', views.BlogPostLike, name="blogpost_like"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    
]
