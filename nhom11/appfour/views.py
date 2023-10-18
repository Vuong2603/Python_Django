from django.contrib.auth import decorators
from django.contrib.auth.models import User
from django.shortcuts import render
from appfour import admin
from appfour.forms import PostForm, UserForm,UserProfileForm, forms

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from appfour.models import Post
from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from .models import Draft, Post, Comment, UserProfileInfo
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import SearchForm
# Create your views here.
@login_required(login_url='/login')
def index(request):
    posts = Post.objects.order_by('-date')
    return render(request,'appfour/index.html', {'posts': posts})
    # else:
    #     return render(request,'appfour/login1.html', {})
def page1(request):
    return render(request,'appfour/page1.html')
def page2(request):
    return render(request,'appfour/page2.html')

@login_required 
def special(request):
    return HttpResponse('You are logged in !')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user .set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'appfour/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def register1(request):
    registered = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        portfolio_size = request.POST['portfolio_size']
        email = request.POST['email']
        image_post = request.POST['image_post']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.portfolio_size = portfolio_size
        user.save()
        profile = UserProfileInfo.objects.create(user=user,portfolio_size=portfolio_size,profile_pic=image_post)
        profile.save()
        registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'appfour/registration.html', {'registered': registered})
    # return HttpResponse("2222")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and fail!')
            print('Username: {} and Password {}'.format(username,password))
            return HttpResponse('invalid login details supplied!')
    else:
        return render(request,'appfour/login1.html',{})
        

def post(request):
    if request.user.is_superuser: 
        if request.method == 'POST':
            title = request.POST['title']
            body = request.POST['body']
            image_post = request.FILES['image_post']       
            post = Draft(title = title,body=body,image_post=image_post)
            post.save()
            return redirect('draft')
        else:
            return render(request,'appfour/post.html',{})
    else:
        # return HttpResponse("Chỉ có Admin mới được quyền truy cập !!!")
        # return render(request,'appfour/thongbao.html',{})
            response = HttpResponse()
            response.content = """
            <html>
            <head>
               <style>
                .notification {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    background-color: #f1f8e9;
                    border: 1px solid #c5e1a5;
                    border-radius: 4px;
                    color: #4caf50;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                .notification i {
                    margin-bottom: 10px;
                    font-size: 40px;
                }

                .notification p {
                    margin: 0;
                    margin-bottom: 20px;
                }

                .notification button {
                    padding: 10px 20px;
                    background-color: #4caf50;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
            </style>
            </head>
             <body>
            <div class="notification">
                <i class="fas fa-check-circle"></i>
                <p style="font-size: 32px;">Chỉ có Admin mới được quyền truy cập !</p>
                <button onclick="goBack()">OK</button>
            </div>

            <script>
                function goBack() {
                    window.history.back();
                }
            </script>
            </body>
            </html>
            """
            return response

def post_list(request):
    posts = Post.objects.order_by('-date')
    return render(request, 'appfour/blog.html', {'posts': posts})

def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = post.comments.all()
    # paginator = Paginator(comments, 2)  # Chia thành 10 comment trên mỗi trang

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
            # post = Post.objects.get(id=pk)
            # title = post.title
            user = request.user
            body = request.POST.get('comment')
            comment = Comment( post = post,user = user, body = body)
            comment.save()
            return redirect('index')
    return render(request, 'appfour/index.html', {})
    

def create_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        body = request.POST.get('body')

        if post_id and body:
            comment = Comment.objects.create(post_id=post_id, body=body)
            return JsonResponse({'success': True, 'comment': {'body': comment.body}})
    
    return JsonResponse({'success': False})

def comment_list(request):
    posts = Comment.objects.all() 
    return render(request, 'appfour/comment.html', {'posts': posts})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # author = request.POST.get('author')
        title = request.POST.get('title')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        # Cập nhật thông tin vào cơ sở dữ liệu
        # post.author = author
        post.title = title
        post.body = body
        if image:
            post.image_post = image
        post.save()
        return redirect('index')  # Chuyển hướng đến trang hiển thị danh sách các post

    return render(request, 'appfour/post_update.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # if request.method == 'POST':
    action = request.POST.get('action', '')
    if action == 'delete':
        post.delete()
        return redirect('index')  # Chuyển hướng đến trang hiển thị danh sách các post
    if action == 'cancel':
        return redirect('index')
    return render(request, 'appfour/post_delete.html', {'post': post})

def draft_view(request):
    if request.user.is_superuser: 
        drafts = Draft.objects.order_by('-date') 
 
        return render(request, 'appfour/draft.html', {'drafts': drafts})
    else:
        # return HttpResponse("Chỉ có Admin mới được quyền truy cập !!!")
        response = HttpResponse()
        response.content = """
            <html>
            <head>
               <style>
                .notification {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    background-color: #f1f8e9;
                    border: 1px solid #c5e1a5;
                    border-radius: 4px;
                    color: #4caf50;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                .notification i {
                    margin-bottom: 10px;
                    font-size: 40px;
                }

                .notification p {
                    margin: 0;
                    margin-bottom: 20px;
                }

                .notification button {
                    padding: 10px 20px;
                    background-color: #4caf50;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
            </style>
            </head>
             <body>
            <div class="notification">
                <i class="fas fa-check-circle"></i>
                <p style="font-size: 32px;">Chỉ có Admin mới được quyền truy cập !</p>
                <button onclick="goBack()">OK</button>
            </div>

            <script>
                function goBack() {
                    window.history.back();
                }
            </script>
            </body>
            </html>
            """
        return response

def draft(request, pk):
    draft = get_object_or_404(Draft, pk=pk)

    post = Post.objects.create(title=draft.title, date=draft.date, body=draft.body, image_post=draft.image_post)
    
    draft.delete()
    return redirect('index') 
    # return render(request, 'appfour/index.html', {})

def draft_update(request, pk):
    draft = get_object_or_404(Draft, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        draft.title = title
        draft.body = body
        if image:
            draft.image_post = image
        draft.save()
        return redirect('draft') 

    return render(request, 'appfour/draft_update.html', {'draft':draft})

def draft_delete(request, pk):
    draft = get_object_or_404(Draft, pk=pk)
    action = request.POST.get('action', '')
    if action == 'draft_delete':
        draft.delete()
        return redirect('draft')  
    if action == 'draft_cancel':
        return redirect('draft')
    return render(request, 'appfour/draft_delete.html', {'draft': draft})

def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        body = request.POST.get('body')
        comment.body = body
        comment.save()
        return redirect('index')

    return render(request, 'appfour/comment_update.html', {'comment':comment})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
  
    action = request.POST.get('action', '')
    if action == 'comment_delete':
        comment.delete()
        return redirect('index')  
    if action == 'comment_cancel':
        return redirect('index')
    return render(request, 'appfour/comment_delete.html', {'draft': comment})

def list_blog(request):
    if request.user.is_superuser: 
        posts = Post.objects.order_by('-date')
        return render(request,'appfour/list_blog.html', {'posts': posts})
    else:
        # return HttpResponse("Chỉ có Admin mới được quyền truy cập !!!")
        response = HttpResponse()
        response.content = """
            <html>
            <head>
               <style>
                .notification {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    background-color: #f1f8e9;
                    border: 1px solid #c5e1a5;
                    border-radius: 4px;
                    color: #4caf50;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                .notification i {
                    margin-bottom: 10px;
                    font-size: 40px;
                }

                .notification p {
                    margin: 0;
                    margin-bottom: 20px;
                }

                .notification button {
                    padding: 10px 20px;
                    background-color: #4caf50;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
            </style>
            </head>
             <body>
            <div class="notification">
                <i class="fas fa-check-circle"></i>
                <p style="font-size: 32px;">Chỉ có Admin mới được quyền truy cập !</p>
                <button onclick="goBack()">OK</button>
            </div>

            <script>
                function goBack() {
                    window.history.back();
                }
            </script>
            </body>
            </html>
            """
        return response

def search(request):
    if request.user.is_superuser: 
        form = SearchForm(request.GET)
        posts = []
    
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            posts = Post.objects.filter(title__icontains=search_query)

        context = {
            'form': form,
            'posts': posts
        }
    
        return render(request, 'appfour/list_blog.html', context)
    else:
        response = HttpResponse()
        response.content = """
            <html>
            <head>
               <style>
                .notification {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    background-color: #f1f8e9;
                    border: 1px solid #c5e1a5;
                    border-radius: 4px;
                    color: #4caf50;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                .notification i {
                    margin-bottom: 10px;
                    font-size: 40px;
                }

                .notification p {
                    margin: 0;
                    margin-bottom: 20px;
                }

                .notification button {
                    padding: 10px 20px;
                    background-color: #4caf50;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
            </style>
            </head>
             <body>
            <div class="notification">
                <i class="fas fa-check-circle"></i>
                <p style="font-size: 32px;">Chỉ có Admin mới được quyền truy cập !</p>
                <button onclick="goBack()">OK</button>
            </div>

            <script>
                function goBack() {
                    window.history.back();
                }
            </script>
            </body>
            </html>
            """
        return response