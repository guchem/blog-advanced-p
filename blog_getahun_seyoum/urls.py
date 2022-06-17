from django.contrib import admin
from django.urls import path
import blog.views as blog_view

urlpatterns = [
    path('', blog_view.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', blog_view.user_login, name='login'),
    path('logout/',blog_view.user_logout, name='logout'),
    path('register/',blog_view.register, name='register'),
    path('<str:username>', blog_view.blogs_by_user, name='user-blogs'),
    path('<int:pk>/', blog_view.blog_detail, name='blog-detail'),
    path('new/', blog_view.create_blog, name='create-blog'),
    path('<int:pk>/update/', blog_view.update_blog, name='blog-update'),
    path('<int:pk>/delete/', blog_view.delete_blog, name='blog-delete'),
    path('search/', blog_view.blog_search, name='blog-search'),


]
