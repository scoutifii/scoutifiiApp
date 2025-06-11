import time
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse, HttpResponseServerError
from django.contrib.auth.models import User, auth
from django.core.cache import cache
from django.contrib import messages
from .models import (AllLogins, Profile, Post, Comment, Room, Messaging,
                      LikePost, Notification, VideoCounts, Ads,
                      FollowersCount, OffTheBallVideo, VideoPositioning, 
                      VideoMarking, VideoAnticipation, VideoPace, VideoTackling,
                      VideoVision, VideoWorkRate, VideoAggression, VideoCharisma, 
                      VideoBallProtection, VideoSpeed, VideoHeading, VideoJumpingReach,
                      VideoFlair, VideoShooting, VideoTechnique, VideoPassing, VideoFinishing,
                      VideoBallControl, VideoFreeKick, VideoDribbling, VideoCrossing,
                      VideoSavingOneOnOne, VideoCommandingInDefence, VideoFootworkAndDistribution,
                      VideoSavingPenalties, VideoConcentration, VideoAgility, VideoCloseRangeShotStoppingAbility,
                      VideoReflexes, ActivityLog, LiveVideo, BrandSetting, FaceRecognition)
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators import gzip
from django.urls import reverse
import random
import uuid
import json
import requests
import responses
from itertools import chain
from .helpers import send_forgot_password_mail
from django.db.models import Q, Count, F
from django.db.models.functions import Lower
from django.views import View
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from agora_token_builder import RtcTokenBuilder
from django.views.decorators.cache import cache_page
from kafka import KafkaProducer

# import face_recognition

url = 'dashboard.html'

@cache_page(60 * 10)    
def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username) 
        user_profile = Profile.objects.get(user=user_object)
        posts = Post.objects.all().order_by('-created_at')
        brand_setting = BrandSetting.objects.all()
        year = datetime.now().strftime("%Y")
    else:
        user_profile = Profile.objects.all()
        posts = Post.objects.all().order_by('-created_at') # Sorted by descending order
        brand_setting = BrandSetting.objects.all()
        year = datetime.now().strftime("%Y")

    context = {
        'posts':posts,
        'user_profile':user_profile,
        'brand_setting':brand_setting,
        'year':year,
    }

    return render(request, 'index.html', context)

@login_required(login_url='login')
@cache_page(60 * 10)
def dashboard(request):
    user_object = User.objects.get(username=request.user.username) #getting object of currently logged in user
    user_profile = Profile.objects.get(user=user_object) #use the object to get the user profile
   
    brand_setting = BrandSetting.objects.all()
    
    year = datetime.now().strftime("%Y")

    # assign two empty lists, list to contain all logged in user is following
    user_following_list = [] # List that will contain users the logged in user is following
    feed = [] # List that will contain the posts that the logged in user is following
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    # append to the feed list
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user_prof=usernames)
        feed.append(feed_lists)


    # convert to a feed list and pass it to posts under context
    feed_list = list(chain(*feed))
    random.shuffle(feed)
    
    # user suggestions
    all_users = User.objects.all()
    user_following_all = []

    for obj in user_following:
        user_list = User.objects.get(username=obj.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    # list of all we are not following and is not myself
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    num_of_followers = len(suggestions_username_profile_list)
    token = str(uuid.uuid4())  

    context = {
        'user_profile': user_profile, 
        'posts': feed_list,
        'brand_setting': brand_setting,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
        'year': year,
        'num_of_followers': num_of_followers,
        'token': token
    }

    return render(request, url, context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            if User.objects.filter(email__iexact=email).exists():
                messages.info(request, 'Email Exists')
                return redirect('signup')
            elif User.objects.filter(username__iexact=username).exists():
                messages.info(request, 'Username Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                """#create a profile object for new user"""
                otp=random.randint(10000,99999)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, otp=otp)
                new_profile.save()
                return redirect('login')
                
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
     return redirect('index')
 
def track_login_attempts(request, username):
    attempts = cache.get(f'login_attempts_{username}', 0)
    cache.set(f'login_attempts_{username}', attempts + 1, 60 * 60)
    return attempts + 1     

def login(request):
    if request.user.is_authenticated:
        return redirect('settings')
    else:
        ip_address = request.META['REMOTE_ADDR']
        host       = request.META['SERVER_NAME']
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            attempts = track_login_attempts(request, username)
            
            if attempts > 3:
                # Handle too many login attempts
                return render(request, "too_many_attempts.html") 
            
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    cache.delete(f'login_attempts_{username}') 
                    AllLogins.objects.create(user=request.user, username=request.user.username, ip_address=ip_address, server=host)
                    return redirect('dashboard')
                else:
                    messages.info(request, 'Account Deactivated')
            else:
                messages.info(request, 'Invalid username OR password')
                return redirect('login')
            
        return redirect('index')

@login_required(login_url='login')       
def logout(request):    
    AllLogins.objects \
    .filter(user_id=request.user.pk, login_date__startswith=timezone.now().date()) \
    .update(last_logged_out=timezone.now())
    auth.logout(request)
    return redirect('index')

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        if request.FILES.get('profileimg') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            phone_no = request.POST['phone_no']
            country_id = request.POST['country_id']
            profile_type_data = request.POST['profile_type_data']
            birth_date = request.POST['birth_date']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.phone_no = phone_no
            user_profile.country_id = country_id
            user_profile.profile_type_data = profile_type_data
            user_profile.birth_date = birth_date
            user_profile.save()
        if request.FILES.get('profileimg') != None:
            image = request.FILES.get('profileimg')
            bio = request.POST['bio']
            location = request.POST['location']
            phone_no = request.POST['phone_no']
            country_id = request.POST['country_id']
            profile_type_data = request.POST['profile_type_data']
            birth_date = request.POST['birth_date']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.phone_no = phone_no
            user_profile.country_id = country_id
            user_profile.profile_type_data = profile_type_data
            user_profile.birth_date = birth_date
            user_profile.save()

            return redirect('dashboard')

    brand_setting = BrandSetting.objects.all()

    context = {
        'brand_setting': brand_setting,
        'user_profile': user_profile,
        'profiles': profiles
    }
        
    return render(request, 'settings.html', context)

@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')
    user_post_length = len(user_posts)
    brand_setting = BrandSetting.objects.all()

    follower = request.user.username # someone is following
    user = pk  # Someone that's being followed
    # if this is in our database, these means the user is already following
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Following'
        Profile.objects.update(status=1)
    else:
        button_text = 'Follow'
        Profile.objects.update(status=0)

    # len() is the integer for calculating numbers
    user_followers = len(FollowersCount.objects.filter(user=user))
    user_following = len(FollowersCount.objects.filter(follower=follower))

    year = datetime.now().strftime("%Y")

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers':user_followers,
        'user_following':user_following,
        'brand_setting':brand_setting,
        'year':year
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follower(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    brand_setting = BrandSetting.objects.all()
    user = pk
    user_followers = len(FollowersCount.objects.filter(user=user))
    user_followers_list = list(FollowersCount.objects.filter(user=user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_followers_list':user_followers_list,
        'user_followers':user_followers,
        'brand_setting':brand_setting
    }

    return render(request, 'follower.html', context)

@login_required(login_url='login')
def following(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    brand_setting = BrandSetting.objects.all()
    follower = pk
    user_following = len(FollowersCount.objects.filter(follower=follower))
    user_following_list = list(FollowersCount.objects.filter(follower=follower))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_following_list':user_following_list,
        'user_following':user_following,
        'brand_setting':brand_setting
    }

    return render(request, 'following.html', context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower'] # Person that's following someone else
        user = request.POST['user'] # Person that's being followed
        profile = request.POST.get('profile_id')

        # check if the currently logged in user is already following this user and tries to unfollow
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
            # if person is not following yet and is trying to follow this person
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user, profile_id=profile)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def change_password(request, token):    
    try:
        profile_obj = Profile.objects.filter(forgot_password_token=token).first()

        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password_confirm')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found')
                return redirect(f"change_password/{token}")

            if new_password != confirm_password:
                messages.info(request, 'Password Not Matching')
                return redirect(f"change_password/{token}")
            
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')

        context = {"user_id": profile_obj.user.id}

    except Exception as e:
        raise e.info()
    
    return render(request, 'change_password.html', context)

def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Username not found')
                return redirect('forgot-password')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forgot_password_token = token
            profile_obj.save()
            send_forgot_password_mail(user_obj, token)
            messages.success(request, 'An email is sent')
            return redirect('forgot-password')
    except Exception as e:
        raise e.info()
    return render(request, 'forgot_password.html')

@login_required(login_url='login')
def search(request):
    brand_setting = BrandSetting.objects.all()
    user_object = User.objects.get(username=request.user.username) #getting object of currently logged in user
    user_profile = Profile.objects.get(user=user_object) 
    if request.method == 'POST':
        searched = request.POST['q']
        username_object = User.objects.filter(username__icontains=searched)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

        context = {
            'user_profile':user_profile, 
            'username_profile_list': username_profile_list,
            'brand_setting':brand_setting
        }

    return render(request, 'search.html', context)

def autosuggest(request):
    if 'term' in request.GET: 
        search_term = request.GET.get('term')       
        users = User.objects.filter(
            Q(first_name__icontains=search_term) | 
            Q(last_name__icontains=search_term) |
            Q(username__icontains=search_term)
        )
        payload = []
        for obj in users:
            user_json = {}
            user_json = obj.first_name + " " + obj.last_name
            payload.append(user_json)
    
    return JsonResponse(payload, safe=False)

@login_required(login_url='login')
def delete_post(request, pk):
    if request.user.is_staff | request.user.id:
        post = Post.objects.filter(id=pk)
        post.delete()
        messages.success(request, 'Post Deleted Successfully')
    else:
        messages.info(request, 'You have no permission to delete!')

    return redirect('dashboard')
  
@login_required(login_url='login')
def user_post(request, id):
    if request.method == 'POST':
        user = request.user.pk
        user_obj = request.user.username
        video = request.FILES.get('video_upload')
        video_name = request.POST['video_name']
        category_type = request.POST['category_type']
        profile = request.POST['profile_id'] 
        uuid = request.POST.get('uuid', '')     

        new_post = Post.objects.create(user_id=user, uuid=uuid, user_prof=user_obj, profile_id=profile, video=video, video_name=video_name, category_type=category_type)
        new_post.save()
        return HttpResponseRedirect(reverse('dashboard'))
    else:
            
        return render(request, url)

@login_required(login_url='login')
def like_post(request, id):
    username = request.user.username   # getting username of the currently logged in user
    userid = request.user.pk
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id') 

    # getting the entire object of the post
    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username, user_id=userid).first()

    # Prevent user from liking their own posts
    if post.user_id == request.user.id:
        raise PermissionDenied
        # messages.info(request, 'You cannot like your own post')
    # if user has not liked any post
    elif like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username, user_id=userid, profile_id=profile)
        new_like.save()

        post.no_of_likes = post.no_of_likes+1
        post.save()

        return redirect('dashboard')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()

        return redirect('dashboard')

@login_required(login_url='login')
def video_flair(request, id):
    username = request.user.username   # getting username of the currently logged in user
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    # getting the entire object of the post
    post = Post.objects.get(id=post_id)

    flair_filter = VideoFlair.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's flair any post
    elif flair_filter == None:
        new_flair = VideoFlair.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_flair.save()

        post.no_of_flair = post.no_of_flair+1
        post.save()
        return redirect('dashboard')
    else:
        flair_filter.delete()
        post.no_of_flair = post.no_of_flair-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_positioning(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    positioning_filter = VideoPositioning.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's positioning 
    elif positioning_filter == None:
        new_positioning = VideoPositioning.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_positioning.save()

        post.no_of_positioning = post.no_of_positioning+1
        post.save()
        return redirect('dashboard')
    else:
        positioning_filter.delete()
        post.no_of_positioning = post.no_of_positioning-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_marking(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    marking_filter = VideoMarking.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's marking 
    elif marking_filter == None:
        new_marking = VideoMarking.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_marking.save()

        post.no_of_marking = post.no_of_marking+1
        post.save()
        return redirect('dashboard')
    else:
        marking_filter.delete()
        post.no_of_marking = post.no_of_marking-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_anticipation(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    anticipation_filter = VideoAnticipation.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's anticipation 
    elif anticipation_filter == None:
        new_anticipation = VideoAnticipation.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_anticipation.save()

        post.no_of_anticipation = post.no_of_anticipation+1
        post.save()
        return redirect('dashboard')
    else:
        anticipation_filter.delete()
        post.no_of_anticipation = post.no_of_anticipation-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_offtheball(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    off_the_ball_filter = OffTheBallVideo.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's off_the_ball 
    elif off_the_ball_filter == None:
        new_off_the_ball = OffTheBallVideo.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_off_the_ball.save()

        post.no_of_off_the_ball = post.no_of_off_the_ball+1
        post.save()
        return redirect('dashboard')
    else:
        off_the_ball_filter.delete()
        post.no_of_off_the_ball = post.no_of_off_the_ball-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_tackling(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    tackling_filter = VideoTackling.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's tackling 
    elif tackling_filter == None:
        new_tackling = VideoTackling.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_tackling.save()

        post.no_of_tackling = post.no_of_tackling+1
        post.save()
        return redirect('dashboard')
    else:
        tackling_filter.delete()
        post.no_of_tackling = post.no_of_tackling-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_vision(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    vision_filter = VideoVision.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's vision for the ball 
    elif vision_filter == None:
        new_vision = VideoVision.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_vision.save()

        post.no_of_vision = post.no_of_vision+1
        post.save()
        return redirect('dashboard')
    else:
        vision_filter.delete()
        post.no_of_vision = post.no_of_vision-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_speed(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    speed_filter = VideoSpeed.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's speed on the ball 
    elif speed_filter == None:
        new_speed = VideoSpeed.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_speed.save()

        post.no_of_speed = post.no_of_speed+1
        post.save()
        return redirect('dashboard')
    else:
        speed_filter.delete()
        post.no_of_speed = post.no_of_speed-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_heading(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    heading_filter = VideoHeading.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's heading of the ball 
    elif heading_filter == None:
        new_heading = VideoHeading.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_heading.save()

        post.no_of_heading = post.no_of_heading+1
        post.save()
        return redirect('dashboard')
    else:
        heading_filter.delete()
        post.no_of_heading = post.no_of_heading-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_jumping_reach(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    jumping_reach_filter = VideoJumpingReach.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's jumping_reach of the ball 
    elif jumping_reach_filter == None:
        new_jumping_reach = VideoJumpingReach.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_jumping_reach.save()

        post.no_of_jumping_reach = post.no_of_jumping_reach+1
        post.save()
        return redirect('dashboard')
    else:
        jumping_reach_filter.delete()
        post.no_of_jumping_reach = post.no_of_jumping_reach-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_work_rate(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    work_rate_filter = VideoWorkRate.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's work rate of the ball 
    elif work_rate_filter == None:
        new_work_rate = VideoWorkRate.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_work_rate.save()

        post.no_of_work_rate = post.no_of_work_rate+1
        post.save()
        return redirect('dashboard')
    else:
        work_rate_filter.delete()
        post.no_of_work_rate = post.no_of_work_rate-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_aggression(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    aggression_filter = VideoAggression.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's aggression on the ball 
    elif aggression_filter == None:
        new_aggression = VideoAggression.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_aggression.save()

        post.no_of_aggression = post.no_of_aggression+1
        post.save()
        return redirect('dashboard')
    else:
        aggression_filter.delete()
        post.no_of_aggression = post.no_of_aggression-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_charisma(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    charisma_filter = VideoCharisma.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's charisma on the ball 
    elif charisma_filter == None:
        new_charisma = VideoCharisma.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_charisma.save()

        post.no_of_charisma = post.no_of_charisma+1
        post.save()
        return redirect('dashboard')
    else:
        charisma_filter.delete()
        post.no_of_charisma = post.no_of_charisma-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_ball_protection(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    ball_protection_filter = VideoBallProtection.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's on the ball protection 
    elif ball_protection_filter == None:
        new_ball_protection = VideoBallProtection.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_ball_protection.save()

        post.no_of_ball_protection = post.no_of_ball_protection+1
        post.save()
        return redirect('dashboard')
    else:
        ball_protection_filter.delete()
        post.no_of_ball_protection = post.no_of_ball_protection-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_shooting(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    shooting_filter = VideoShooting.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's shooting of the ball 
    elif shooting_filter == None:
        new_shooting = VideoShooting.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_shooting.save()

        post.no_of_shooting = post.no_of_shooting+1
        post.save()
        return redirect('dashboard')
    else:
        shooting_filter.delete()
        post.no_of_shooting = post.no_of_shooting-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_technique(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    technique_filter = VideoTechnique.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's technique on the ball 
    elif technique_filter == None:
        new_technique = VideoTechnique.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_technique.save()

        post.no_of_technique = post.no_of_technique+1
        post.save()
        return redirect('dashboard')
    else:
        technique_filter.delete()
        post.no_of_technique = post.no_of_technique-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_passing(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    passing_filter = VideoPassing.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's passing rate of the ball
    elif passing_filter == None:
        new_passing = VideoPassing.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_passing.save()

        post.no_of_passing = post.no_of_passing+1
        post.save()
        return redirect('dashboard')
    else:
        passing_filter.delete()
        post.no_of_passing = post.no_of_passing-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_finishing(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    finishing_filter = VideoFinishing.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's passing rate of the ball
    elif finishing_filter == None:
        new_passing = VideoFinishing.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_passing.save()

        post.no_of_finishing = post.no_of_finishing+1
        post.save()
        return redirect('dashboard')
    else:
        finishing_filter.delete()
        post.no_of_finishing = post.no_of_finishing-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_ball_control(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    ball_control_filter = VideoBallControl.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's passing rate of the ball
    elif ball_control_filter == None:
        new_bal_control = VideoBallControl.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_bal_control.save()

        post.no_of_ball_control = post.no_of_ball_control+1
        post.save()
        return redirect('dashboard')
    else:
        ball_control_filter.delete()
        post.no_of_ball_control = post.no_of_ball_control-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_free_kick(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    free_kick_filter = VideoFreeKick.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's free kick on the ball
    elif free_kick_filter == None:
        new_free_kick = VideoFreeKick.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_free_kick.save()

        post.no_of_free_kick = post.no_of_free_kick+1
        post.save()
        return redirect('dashboard')
    else:
        free_kick_filter.delete()
        post.no_of_free_kick = post.no_of_free_kick-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_dribbling(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    dribbling_filter = VideoDribbling.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's dribbling skills of the ball
    elif dribbling_filter == None:
        new_free_kick = VideoDribbling.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_free_kick.save()

        post.no_of_dribbling = post.no_of_dribbling+1
        post.save()
        return redirect('dashboard')
    else:
        dribbling_filter.delete()
        post.no_of_dribbling = post.no_of_dribbling-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_crossing(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    crossing_filter = VideoCrossing.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's crossing style of the ball
    elif crossing_filter == None:
        new_crossing = VideoCrossing.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_crossing.save()

        post.no_of_crossing = post.no_of_crossing+1
        post.save()
        return redirect('dashboard')
    else:
        crossing_filter.delete()
        post.no_of_crossing = post.no_of_crossing-1
        post.save()
        return redirect('dashboard')

@login_required(login_url='login')
def video_pace(request, id):
    username = request.user.username
    post_id = request.POST.get('post_id')
    profile = request.POST.get('profile_id')
    user_id = request.user.pk

    post = Post.objects.get(id=post_id)
    pace_filter = VideoPace.objects.filter(post_id=post_id, username=username, user_id=user_id).first()

    if post.user_id == request.user.id:
        raise PermissionDenied
    # if user has not voted player's pace style of the ball
    elif pace_filter == None:
        new_pace = VideoPace.objects.create(post_id=post_id, username=username, user_id=user_id, profile_id=profile)
        new_pace.save()

        post.no_of_pace = post.no_of_pace+1
        post.save()
        return redirect('dashboard')
    else:
        pace_filter.delete()
        post.no_of_pace = post.no_of_pace-1
        post.save()
        return redirect('dashboard')

def watch(request, pk):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username) 
        user_profile = Profile.objects.get(user=user_object) 
        post = Post.objects.get(id=pk)
        video = get_object_or_404(Post, id=pk)
        post_lists = Post.objects.filter(id=pk)
        view_count = VideoCounts.objects.filter(post_id=post).count()
        brand_setting = BrandSetting.objects.all()
        year = datetime.now().strftime("%Y")
   
        ip_address = request.META.get('REMOTE_ADDR')
        if post.user_id == request.user.id:
            messages.info(request, 'Access denied')
            return redirect('dashboard')
        else:
            if not VideoCounts.objects.filter(post=video, session=request.session.session_key):
                views = VideoCounts(post=video, ip_address=ip_address, session=request.session.session_key, user_id=request.user.pk)
                views.save()
    else:
        post_lists = Post.objects.filter(id=pk)
        post = Post.objects.get(id=pk)
        view_count = VideoCounts.objects.filter(post_id=post).count()
        brand_setting = BrandSetting.objects.all() 
        user_profile = Profile.objects.all()
        year = datetime.now().strftime("%Y")

    context = {
        'posts':post,
        'view_count':view_count,
        'postLists':post_lists,
        'brand_setting': brand_setting,
        'user_profile': user_profile,
        'year': year
    }

    return render(request, 'watch.html', context)

@login_required(login_url='login')
def show_notifications(request):
    user_object = User.objects.get(username=request.user.username) 
    user_profile = Profile.objects.get(user=user_object)   
    brand_setting = BrandSetting.objects.all()
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    notifications.update(is_seen=True)
    year = datetime.now().strftime("%Y")

    context = {
        'notifications': notifications,
        'user_profile': user_profile,
        'brand_setting': brand_setting,
        'year':year
    }

    return render(request, 'notifications.html', context)

@login_required(login_url='login')
def delete_notifications(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('dashboard')

def count_notifications(request):
    count_notifications = None
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
    return {'count_notifications': count_notifications}

@login_required(login_url='login')
def user_comments(request, id):
    if request.method == 'POST':
        user = request.user.pk
        user_obj = request.user.username
        body = request.POST.get('comment_body')
        profile = request.POST.get('profile_id')
        post = request.POST.get('post_id')

        user_post = Post.objects.get(id=id)

        if user_post.user_id == request.user.id:
            messages.info(request, 'Access denied')
            return     
        else:
            
            Comment.objects.create(post_id=post, user_id=user, user_prof=user_obj, profile_id=profile, comment_body=body)
        
        return HttpResponseRedirect(reverse('dashboard'))
    else:
            
        return render(request, url)

@login_required(login_url='login')
def live_stream(request):
    user_object = User.objects.get(username=request.user.username) 
    user_profile = Profile.objects.get(user=user_object)
    brand_setting = BrandSetting.objects.all()
    year = datetime.now().strftime("%Y")
    request.POST.get('profile_id')
    request.user.pk

    # data = json.loads(request.body)
    # LiveVideo.objects.create(
    #     user_id=data['user'], 
    #     profile_id=data['profile'], 
    #     channel_name=data['channel_name'], 
    #     uid=data['UID']
    # )
    context = {
        'user_profile': user_profile,
        'brand_setting': brand_setting,
        'year': year
    }
    return render(request, 'live.html', context)
    
@login_required(login_url='login')
def report(request):
    user_object = User.objects.get(username=request.user.username) 
    user_profile = Profile.objects.get(user=user_object)   
    brand_setting = BrandSetting.objects.all()
    if request.method == 'POST':
        from_date=request.POST.get("from_date")
        to_date=request.POST.get("to_date")
        
        list_weekly_users = AllLogins.objects.filter(login_date__range=(from_date, to_date)).distinct().count()
        
        context = {
            'weekly_users': list_weekly_users,
            'user_profile': user_profile,
            'brand_setting': brand_setting
        }

        return render(request, 'report.html', context)
    
    else:
        active_users = Profile.objects.all().count()
        total_posts = Post.objects.all().count()
        user_object = User.objects.get(username=request.user.username) 
        user_profile = Profile.objects.get(user=user_object)   
        brand_setting = BrandSetting.objects.all()
        logins = AllLogins.objects.values('user').annotate(num_logins=Count('user_id')).filter(login_date__startswith=timezone.now().date())
        daily_users= len(logins)
        year = datetime.now().strftime("%Y")

        # Using Group by in django
        most_viewed_videos = VideoCounts.objects.values("post_id", "post__video_name") \
            .annotate(most_watched=Count('post_id')) \
            .order_by('post_id')[:10]
        data = []

        for item in most_viewed_videos:
            data.append([item["post_id"], item["post__video_name"]])


        post_dataset = Post.objects.all() \
            .values('user_prof', 'profile_id__country_id') \
            .annotate(num_posts=Count('video_name')) \
            .annotate(num_users=Count('user_prof')) \
            .annotate(num_countries=Count('profile_id__country_id')) \
            .order_by('user_prof')
        posts = list()
        country_data = list()
        users_data_series = list()

        for obj in post_dataset:
            posts.append(obj['user_prof'])
            users_data_series.append(obj['num_users'])
            country_data.append(obj['num_countries'])

        users_series = {
            'name': 'Users',
            'data': users_data_series
        }
        country_series = {
            'name': 'Countries',
            'data': country_data
        }

        user_posts_chart = {
            'chart': {'type': 'column'},
            'title': {'text': ' User Posts by Country'},
            'xAxis': {
                'categories': posts,
                'accessibility': {
                    'description': 'Posts by Category'
                    }
                },
            'yAxis': {
                'title': {
                    'text': 'No of Posts by User'
                    },
                'accessibility': {
                    'description': 'No of Posts by User'
                    }
                },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                    },
                'cursor': 'pointer'
                },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
                },
            'series': [users_series, country_series],
        }
        user_posts_by_country = json.dumps(user_posts_chart)

        dataset = Profile.objects \
            .values('country_id') \
            .annotate(profile_type_user_count=Count('country_id', filter=Q(profile_type_data='user')), 
                profile_type_player_count=Count('country_id', filter=Q(profile_type_data='player')),
                profile_type_agent_count=Count('country_id', filter=Q(profile_type_data='agent')),
                profile_type_coach_count=Count('country_id', filter=Q(profile_type_data='coach'))) \
            .order_by('country_id')
        countries = list()
        user_data_series = list()
        player_data_series = list()
        agent_data_series = list()
        coach_data_series = list()

        for obj in dataset:
            countries.append(obj['country_id'])
            user_data_series.append(obj['profile_type_user_count'])
            player_data_series.append(obj['profile_type_player_count'])
            agent_data_series.append(obj['profile_type_agent_count'])
            coach_data_series.append(obj['profile_type_coach_count'])
        
        user_series = {
            'name': 'User',
            'data': user_data_series
        }
        player_series = {
            'name': 'Player',
            'data': player_data_series
        }
        agent_series = {
            'name': 'Agent',
            'data': agent_data_series
        }
        coach_series = {
            'name': 'Coach',
            'data': coach_data_series
        }
        
        column_chart = {
            'chart': {'type': 'column'},
            'title': {'text': 'User by Country'},
            'xAxis': {'categories': countries},
            'yAxis': {'title': {
                        'text': 'All Profile Statistics'
                        }
                     },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                    }
                },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
                },
            'series': [user_series, player_series, agent_series, coach_series],
        }
        profile_data = json.dumps(column_chart)


        category_data = Post.objects \
            .values('user_id__username') \
            .annotate(football_count=Count('user_id__username', filter=Q(category_type='football'))) \
            .order_by('user_id__username')
        countries = list()
        football_data_series = list()

        for obj in category_data:
            countries.append(obj['user_id__username'])
            football_data_series.append(obj['football_count'])
        
        football_series = {
            'name': 'Football',
            'data': football_data_series
        }
        
        category_chart = {
            'chart': {'type': 'column'},
            'title': {'text': 'Category Type by Country'},
            'xAxis': {'categories': countries},
            'yAxis': {'title': {
                        'text': 'All Category Statistics'
                        }
                     },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                    }
                },
            'tooltip': {
                'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
                },
            'series': [football_series],
        }
        posts_by_category = json.dumps(category_chart)
        
        return render(request, 'report.html', 
            {'active_users': active_users,
             'total_posts': total_posts, 
             'user_profile': user_profile,
             'brand_setting': brand_setting,
             'daily_users': daily_users, 
             'chart': profile_data, 
             'posts_by_user': user_posts_by_country,
             'year': year,
             'most_viewed_videos': data,
             'posts_by_category': posts_by_category,
            })

@login_required(login_url='login')
def view_log(request):
    log_list = ActivityLog.objects.all()
    user_object = User.objects.get(username=request.user.username) 
    user_profile = Profile.objects.get(user=user_object)   
    brand_setting = BrandSetting.objects.all()

    context = {
        'log_list': log_list,
        'user_profile': user_profile,
        'brand_setting': brand_setting
    }

    return render(request, 'view_logs.html', context)

def get_comments_by_post(post_id):
    post_details = Post.objects.get(pk=post_id)
    
    comments = Comment.objects.filter(post_id=post_details.id)

    return JsonResponse({"comments":list(comments.values())})

def get_no_of_likes(pk):
    like_post_counter = Post.objects.filter(id=pk)
    data = []

    for obj in like_post_counter:
        data = json.dumps(obj.no_of_likes)

    return JsonResponse({'data':data}, safe=False)

@login_required(login_url='login')
def follower(request, pk):
    user_object = User.objects.get(username=request.user.username) 
    user_profile = Profile.objects.get(user=user_object)
    brand_setting = BrandSetting.objects.all()
    user_followers_list = FollowersCount.objects.filter(follower=request.user.username)

    context = {
        'followers': user_followers_list,
        'user_profile': user_profile,
        'brand_setting': brand_setting
    }

    return render(request, 'follower.html', context)

def list_users_post_viewers(request, pk):
    viewers_list = VideoCounts.objects.filter(id = pk, user_id=request.user.id)
    
    context = {
        'viewers': viewers_list
    }
    
    return  render(request, '', context)

# For video streaming
def get_token(request):
    app_id = 'cf3600b52a1849aba17cc3d3080275fecd'
    app_certificate = '53daeddb2f414fd089140f22bf673d02'
    channel_name = request.GET.get('channel')
    uid = request.user.id   # or use random.randint(1,230)
    expiration_time_in_seconds = 3600 * 24 # to expire in 24 hours
    current_time_stamp = int(time.time())
    privilege_expired_ts = current_time_stamp + expiration_time_in_seconds
    role = request.user.is_staff
    
    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
    token_context = {
        'token': token,
        'uid': uid
    }
    
    return JsonResponse(token_context, safe=False)

def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)
    return JsonResponse({'message':'Room Created'})


@login_required(login_url='login')
def create_ads(request):
    if request.method == 'POST':
        location = request.POST['location']
        age = request.POST['age']
        gender = request.POST['gender']
        profile = request.POST['profile_id'] 
        daily_budget = request.POST['daily_budget']
        duration = request.POST['duration']  
        tax = request.POST['tax']  
        total_payment = request.POST['total_payment']
        payment = request.POST['payment_method']

        new_ad = Ads.objects.create(location=location, age=age, gender=gender, profile_id=profile, daily_budget=daily_budget, duration=duration, tax=tax, total_payment=total_payment, payment_method=payment)
        new_ad.save()
        
        brand_setting = BrandSetting.objects.all()
        user_object = User.objects.get(username=request.user.username) 
        user_profile = Profile.objects.get(user=user_object) 

    context = {
        'brand_setting': brand_setting,
        'user_profile': user_profile,
    }
        
    return render(request, 'ads.html', context)

def my_likes(request):
    """ Read data from the database using pandas"""
    df = pd.read_sql_query('SELECT no_of_likes FROM post', settings)
    
    # Prepare data
    likes_data = df.dropna()
    
class PostAPIView(APIView):
    """docstring for PostAPIView"""
    def get(self, request):
        posts = Post.objects.all()
        
        return responses([self.formatPost(p) for p in posts])

    def formatPost(self, post):
        comments = requests.get("http://127.0.0.1:5001/posts/id/comments" %post.id).json()
        return {
            'id': id,
            'profile': profile,
            'user': user,
            'user_prof': user_prof,
            'video': video,
            'video_name': video_name,
            'slug': slug,
            'category_type': category_type,
            'comments': comments
        }
        
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        # Produce message to Kafka topic
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('post_saved', value=f'Post {pk} saved'.encode('UTF-8'))

        return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
        # Produce message to Kafka topic
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('post_updates', value=f'Post {pk} updated'.encode('UTF-8'))

        return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()

        # Produce message to Kafka topic
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('post_deleted', value=f'Post {pk} deleted'.encode('UTF-8'))
        return Response(status=204)

def face_recognition(request):
    if request.method == 'POST':
        image = request.FILES['image']
        face_encodings = face_recognition.face_encodings(image)

        for face_encoding in face_encodings:
            face_model = FaceRecognition.objects.filter(face_encoding=face_encoding).first()

            context = {
                'name': face_model.name
            }

            if face_model:
                return render(request, 'face_recognition.html', context)


