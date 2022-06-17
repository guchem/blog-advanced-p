from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Blog
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')


def home(request):
    return render(request, 'layout.html', {'blogs': Blog.objects.all().order_by('-date_posted')})


def blogs_by_user(request, username):
    user = User.objects.get(username=username)
    blogs = Blog.objects.filter(author=user).order_by('-date_posted')
    return render(request,'user_blogs.html', {'blogs':blogs, 'username':username})


def blog_detail(request, pk):
    blog = Blog.objects.get(pk=pk)
    return render(request, 'blog_detail.html', {'blog':blog})


@login_required
def create_blog(request):
    if request.method=='POST':
        title = request.POST['title']
        content = request.POST['content']
        blog=Blog.objects.create(title=title, content=content, author=request.user)
        return redirect('blog-detail', blog.pk)
    return render(request, 'create_blog.html')


@login_required
def update_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.user==blog.author:
        if request.method=='POST':
            title = request.POST['title']
            content = request.POST['content']
            blog.title=title
            blog.content = content
            blog.save()
            return redirect('blog-detail', pk)
        return render(request, 'blog_update.html', {'blog': blog})
    return redirect('home')


@login_required
def delete_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if blog.author==request.user:
        blog.delete()
        messages.success(request, 'Blog Deleted successfully')
        return redirect('home')
    return redirect('-detail', pk)


def blog_search(request):
    if request.method=='POST':
        keyword = request.POST['keyword']
        if len(keyword)==0 or keyword.isspace():
            messages.warning(request, 'Please Type something to search')
            return redirect('home')
        blogs = Blog.objects.filter(title__contains=keyword).order_by('-date_posted')
        return render(request, 'layout.html', {'blogs':blogs, 'search_for':keyword})



