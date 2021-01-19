from django.shortcuts import render,HttpResponseRedirect, redirect
from django.shortcuts import render, get_object_or_404
from . forms import AddPost, CommentForm
from . models import Post, Comment
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse

# Create your views here.


#This Function Will show Post
def list_post(request):

    posts = Post.objects.all()
    return render(request, 'addandshow.html', { 'post':posts})


#This Function Will ADD Item
def add_show(request):
    if request.method == 'POST':
        fm = AddPost(request.POST)
        if fm.is_valid():
            fm.save()
            fm = AddPost()
            return HttpResponseRedirect('/list_post')

    else:
         fm = AddPost()
    posts = Post.objects.all()

    return render(request, 'update.html', {'form' : fm, 'post':posts, 'isAdd':True})



#This Fucntion used for Update/Edit Data

def update_data(request,id):
    if request.method == 'POST':
        pi = Post.objects.get(pk=id)
        fm = AddPost(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/list_post')
    else:
        pi = Post.objects.get(pk=id)
        fm = AddPost(instance=pi)
    

    return render(request, 'update.html', {'form':fm, 'isAdd': False})


#This Function Used for DELETE Item

def delete_data(request,id):
    if request.method == "POST":
        pi = Post.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/list_post')

def blog_post(request):
    posts = Post.objects.all()
    context = {
        "posts": posts,
        
    }
    return render(request, 'index.html', context)

def home(request):
    return render(request, 'login.html')

# This function is used to Post details.
def blog_detail(request, id):
    post = Post.objects.get(pk=id)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["content"],
                post=post
            )
            comment.save()
            form = CommentForm()

    comments = Comment.objects.filter(post=post)
    
    
    likes_connected = get_object_or_404(Post, id=id)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True

    data = {}
    data['number_of_likes'] = likes_connected.number_of_likes()
    data['post_is_liked'] = liked


    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "data":data
    }

    return render(request, "blog_detail.html", context)


# Login code

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/blog_post")

        else:
            messages.info(request, 'Invalid credentials')
            return redirect('/login')

    else:
        return render(request, 'login.html')

# Sign-up code
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Aready Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('User Created')
                return redirect('/login')
        else:
            messages.info(request, 'Password is not maching...')
            return redirect('register')
        return redirect('/')


    else:
        return render(request,'register.html')


def logout(request):
    auth.logout(request)

    return render(request,'login.html')
    # return HttpResponseRedirect('/')


# post_like code
def BlogPostLike(request, id):
    post = get_object_or_404(Post, id=id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect('/blog/'+str(id))