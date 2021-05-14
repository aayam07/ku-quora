from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib import messages
from .models import Profile
from blog.models import Post,Likes,Dislikes,Follow
User = get_user_model()
import json
from django.http import JsonResponse
# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        user = User.objects.filter(username = username).exists()
        if user:
            messages.error(request,'Error - ----  :( username already taken')
            return redirect('/account/')
        
        user = User.objects.filter(email = email).exists()
        if user:
            messages.error(request,'Error - ----  :( email already used')
            return redirect('/account/')
        
        if password1 != password2:
            messages.error(request,"Error - ----  :( password didn't match")
            return redirect('/account/')
        
        user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
        messages.success(request,"Success - ----  : ) Signed Up successfully")
        return redirect('/account/signin')
    
    return render(request,'account/signup.html',{})

def verify_account_view(request,token):
    userProfile = get_object_or_404(Profile,token=token)
    if userProfile:
        userProfile.is_verified = True
        userProfile.save()
        messages.success(request,f"account verified successfully")
        return redirect('/account/')
    else:
        messages.error(request,f"invalid token")
    return redirect('/account/')
        
def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user != None:
            login(request,user)
            print('logged in')
            return redirect('/')
        else:
            messages.error(request,f"user credentials didn't match")
            return redirect('/account/signin')
    return render(request,'account/signin.html',{})

def logout_view(request):
    logout(request)
    messages.success(request,f" : ) Logged out successfully")
    return redirect('/account/signin')



def profile_view(request,user_id):
    liked_post_ids = []
    liked_objs = Likes.objects.filter(user=request.user).all()
    for liked_obj in liked_objs:
        liked_post_ids.append(liked_obj.post.id)
        print(liked_obj.post.id)


    disliked_post_ids = []
    disliked_objs = Dislikes.objects.filter(user=request.user).all()

    for disliked_obj in disliked_objs:
        disliked_post_ids.append(disliked_obj.post.id)

    followers=0
    followings=0
    selfProfile = 1
    already_following = False
    if user_id == request.user.id:
        selfProfile = 1
        user = request.user
        posts = Post.objects.filter(user=request.user).all().order_by('-posted_on')
        followers = Follow.objects.filter(following=user).count()
        followings = Follow.objects.filter(follower=user).count()
       
    else:
        selfProfile = 0
        user = User.objects.get(id = user_id)
        posts = Post.objects.filter(user=user).all().order_by('-posted_on')
        followers = Follow.objects.filter(following=user).count()
        followings = Follow.objects.filter(follower=user).count()
        already_following = Follow.objects.filter(follower=request.user,following=user).exists()
        
    context = {
    'selfProfile' : selfProfile,
    'User':user,
    'posts':posts,
    'liked_posts_ids':liked_post_ids,
    'disliked_posts_ids':disliked_post_ids,
    'followers':followers,
    'followings':followings,
    'already_following':already_following
    }     
    
    return render(request,'account/profile.html',context)



def followings_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        following_id = data['followingId']
        following = User.objects.get(id=following_id)
        already_followed = Follow.objects.filter(following=following,follower=request.user).count()
        
        followers = Follow.objects.filter(following=following).count()
        followings = Follow.objects.filter(follower=following).count()
        
        if already_followed:
            Follow.objects.filter(following=following,follower=request.user).delete()
            print('unfollowed')

        else:
            Follow.objects.create(following=following,follower=request.user)
            print('followed')

        followers = Follow.objects.filter(following=following).count()
        followings = Follow.objects.filter(follower=following).count()
        response = {
            'followings':followings,
            'followers':followers
        }
        return JsonResponse(response)

def followings_list_view(request):

    return render(request,'account/followings.html',{})







