from django.shortcuts import render,redirect,get_object_or_404
from .models import Stream,Post,Tag,Likes,Dislikes
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
import json

@login_required(login_url='signin')
def index_view(request):


    # stream_objs = Stream.objects.filter(user=request.user)
    
    # stream_objs_ids = []

    # for obj in stream_objs:
    #     stream_objs_ids.append(obj.id)
    
    # posts = Post.objects.filter(id__in=stream_objs_ids).all().order_by('-posted_on')

    # print(posts)
    liked_post_ids = []
    liked_objs = Likes.objects.filter(user=request.user).all()
    for liked_obj in liked_objs:
        liked_post_ids.append(liked_obj.post.id)
        print(liked_obj.post.id)


    disliked_post_ids = []
    disliked_objs = Dislikes.objects.filter(user=request.user).all()

    for disliked_obj in disliked_objs:
        disliked_post_ids.append(disliked_obj.post.id)
    

    posts = Post.objects.all().order_by('-posted_on')
    context = {
        'posts':posts,
        'liked_posts_ids':liked_post_ids,
        'disliked_posts_ids':disliked_post_ids
    }

    return render(request,'blog/index.html',context)



@login_required
def create_post_view(request):
    user = request.user
    tags_objs = []
    title = request.POST.get('title')
    body = request.POST.get('body')
    tags = request.POST.get('tags')
    tags_list = list(tags.split(' '))

    print(tags_list)
    for tag in tags_list:
        t, created = Tag.objects.get_or_create(title=tag)
        tags_objs.append(t)
    
    p, created = Post.objects.get_or_create(title=title,body=body,user=user)
    p.tags.set(tags_objs)
    return redirect('/')

@login_required
def post_detail_view(request,post_id):
    liked_post_ids = []
    liked_objs = Likes.objects.filter(user=request.user).all()
    for liked_obj in liked_objs:
        liked_post_ids.append(liked_obj.post.id)
        print(liked_obj.post.id)
    disliked_post_ids = []
    disliked_objs = Dislikes.objects.filter(user=request.user).all()

    for disliked_obj in disliked_objs:
        disliked_post_ids.append(disliked_obj.post.id)
    post = get_object_or_404(Post,id = post_id)

    context = {
        'post':post,
        'liked_posts_ids':liked_post_ids,
        'disliked_posts_ids':disliked_post_ids
    }
    return render(request,'blog/post_detail.html',context)


@login_required
def tags_post_view(request,tag_slug):
    liked_post_ids = []
    liked_objs = Likes.objects.filter(user=request.user).all()
    for liked_obj in liked_objs:
        liked_post_ids.append(liked_obj.post.id)
        print(liked_obj.post.id)
    disliked_post_ids = []
    disliked_objs = Dislikes.objects.filter(user=request.user).all()
    for disliked_obj in disliked_objs:
        disliked_post_ids.append(disliked_obj.post.id)
    tag = get_object_or_404(Tag,slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted_on')
    context = {
        'posts':posts,
        'tag':tag,
         'liked_posts_ids':liked_post_ids,
        'disliked_posts_ids':disliked_post_ids
    }
    return render(request,'blog/tag_post.html',context)

@login_required
def like_post_view(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)
        current_likes = post.likes
        current_dislikes = post.dislikes

        disliked = Dislikes.objects.filter(user=user,post=post).count()
        liked = Likes.objects.filter(user=user,post=post).count()

        if liked:
            Likes.objects.filter(user=user,post=post).delete()
            current_likes -= 1

        if disliked:
            Dislikes.objects.filter(user=user,post=post).delete()
            current_dislikes -= 1

        # if not disliked:
        #     Dislikes.objects.create(user-user,post=post)
        #     current_dislikes += 1

        if not liked:
            like = Likes.objects.create(user=user,post=post)
            current_likes += 1
      
            
            
        post.likes = current_likes
        post.dislikes = current_dislikes
        post.save()
        response = {
            'current_dislikes':current_dislikes,
            'current_likes':current_likes
        }
        print('likes : ',post.likes)
        print('dislikes : ',post.dislikes)
        return JsonResponse(response)
    return redirect('/')

@login_required
def dislike_post_view(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)
        current_likes = post.likes
        current_dislikes = post.dislikes

        liked = Likes.objects.filter(user=user,post=post).count()
        disliked = Dislikes.objects.filter(user=user,post=post).count()

        if disliked:
            Dislikes.objects.filter(user=user,post=post).delete()
            current_dislikes -= 1
        if liked:
            Likes.objects.filter(user=user,post=post).delete()
            current_likes -= 1
        if not disliked:
            Dislikes.objects.create(user=user,post=post)
            current_dislikes += 1

        post.likes = current_likes
        post.dislikes=current_dislikes
        post.save()
        print('likes : ',post.likes)
        print('dislikes : ',post.dislikes)
        response = {
            'current_dislikes':current_dislikes,
            'current_likes':current_likes,

        }
        return JsonResponse(response)