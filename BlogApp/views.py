import os
import uuid
from django.http import JsonResponse
from django.shortcuts import redirect, render
from PersonalBlog import settings
from .models import BlogPost,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
import re
from django.core import serializers

@login_required(login_url="login")
def Home(request):
    blog = BlogPost.objects.first()
    context = {"Blog":blog,
               "User":request.user}
    return render(request,"BlogApp/home.html",context)

def create_vomit(request):
    if request.method == 'POST':
        user = request.user 
        title = request.POST.get('title', '')
        blog_image = request.FILES.get('blog_image', None)

        if blog_image:
            # Generate a unique filename for the image
            unique_filename = f'{uuid.uuid4().hex}_{blog_image.name}'
            
            # Save the image to the media directory with the unique filename
            media_root = settings.MEDIA_ROOT
            image_path = os.path.join(media_root, 'blog_images', unique_filename)
            with open(image_path, 'wb') as destination:
                for chunk in blog_image.chunks():
                    destination.write(chunk)
            
            # Create a new BlogPost instance with the unique filename
            blog_post = BlogPost(user=user, title=title, blog_image_url=f'media/blog_images/{unique_filename}')
            blog_post.save()

            # Return the newly created vomit data as JSON
            return JsonResponse({
                'message': 'Vomit created successfully',
                'title': blog_post.title,
                'blog_image_url': blog_post.blog_image_url,
            })
        else:
            return JsonResponse({'error': 'No image file provided'})

    return JsonResponse({'error': 'Invalid request method'})
    

def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            errors = form.errors
            context = {"Errors": errors}
            return render(request,"BlogApp/login.html",context)
    return render(request,"BlogApp/login.html")
            

def Search(request):
    if request.method == 'POST':
        search_term = request.POST.get('searchKeyword', '')
        Users = User.objects.filter(username__icontains=search_term)
        if Users:
            users_data = serializers.serialize('json', Users)
            return JsonResponse({
                'message': 'Vomit created successfully',
                'users': users_data,
            })
        else:
            return JsonResponse({'error': 'No Users Found'})
    return JsonResponse({'error': 'Invalid request method'})

def Register(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')

        errors = {}
        inputs = {}
        if not email:
            errors['email'] = 'This field is required'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = 'Invalid email format'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'This Email has already been registered'
        else: 
            inputs['email'] = email

        if not username:
            errors['username'] = 'This field is required'
        elif not re.match(r'^[a-zA-Z0-9._-]+$', username):
            errors['username'] = 'Invalid characters in username'
        else:
            inputs['username'] = username

        if not password:
            errors['password'] = 'This field is required'
        elif re.search(r'\b(OR|AND)\b', password, re.IGNORECASE):
            errors['password'] = 'Invalid characters in password'
        else:
            inputs['password'] = password

        if not re_password:
            errors['re_password'] = 'This field is required'
        elif password != re_password:
            errors['re_password'] = 'Passwords should match'
        else:
            inputs['re_password'] = re_password



        if not errors:
            user = User(email=email, username=username, password=make_password(password))
            user.save()
            login(request,user)
            return redirect('home')
        else:
            context = {
                'Errors': errors,
                'Inputs': inputs
            }
            return render(request, 'BlogApp/register.html', context)
            

    else:
        errors = {}
        errors['login'] = "Unknown error occured. Please try gain later"
        context = {
            'Errors': errors
        }
        return render(request, 'BlogApp/register.html', context)

def Logout_view(request):
    logout(request)
    return redirect('home')