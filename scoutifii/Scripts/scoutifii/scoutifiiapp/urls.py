from django.contrib import admin
from django.urls import path
from . import views
from .views import PostAPIView
import uuid


urlpatterns = [ 
    # Path to render index page
	path('', views.index, name='index'),
    # Path to render Dashboard / Home page
	path('dashboard', views.dashboard, name='dashboard'),
    # Path to render signup page
	path('signup', views.signup, name='signup'),
    # Path to render login page
    path('login', views.login, name='login'),
    # Path to render logout
    path('logout', views.logout, name='logout'),
    # Path to render user account page
    path('settings', views.settings, name='settings'),
    # Path to render profile page
    path('profile/<str:pk>', views.profile, name='profile'),
    # Path to render post page
    path('user-post/<int:id>', views.user_post, name='user-post'),
    # Path to render like post
    path('like/<uuid:id>', views.like_post, name='like_post'),
    path('delete-post/<str:pk>', views.delete_post, name='delete-post'),
    path('change-password/<token>', views.change_password, name='change-password'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('autosuggest', views.autosuggest, name='autosuggest'),
    path('watchqv=<str:pk>', views.watch, name='watch'),
    path('flair/<uuid:id>', views.video_flair, name='flair'),
    path('positioning/<uuid:id>', views.video_positioning, name='positioning'),
    path('marking/<uuid:id>', views.video_marking, name='marking'),
    path('anticipation/<uuid:id>', views.video_anticipation, name='anticipation'),
    path('off-the-ball/<uuid:id>', views.video_offtheball, name='off-the-ball'),
    path('tackling/<uuid:id>', views.video_tackling, name='tackling'),
    path('vision/<uuid:id>', views.video_vision, name='vision'),
    path('speed/<uuid:id>', views.video_speed, name='speed'),
    path('heading/<uuid:id>', views.video_heading, name='heading'),
    path('jumping-reach/<uuid:id>', views.video_jumping_reach, name='jumping-reach'),
    path('work-rate/<uuid:id>', views.video_work_rate, name='work-rate'),
    path('aggression/<uuid:id>', views.video_aggression, name='aggression'),
    path('charisma/<uuid:id>', views.video_charisma, name='charisma'),
    path('ball-protection/<uuid:id>', views.video_ball_protection, name='ball-protection'),
    path('passing/<uuid:id>', views.video_passing, name='passing'),
    path('technique/<uuid:id>', views.video_technique, name='technique'),
    path('shooting/<uuid:id>', views.video_shooting, name='shooting'),
    path('finishing/<uuid:id>', views.video_finishing, name='finishing'),
    path('ball-controll/<uuid:id>', views.video_ball_control, name='ball-controll'),
    path('free-kick/<uuid:id>', views.video_free_kick, name='free-kick'),
    path('dribbling/<uuid:id>', views.video_dribbling, name='dribbling'),
    path('crossing/<uuid:id>', views.video_crossing, name='crossing'),
    path('pace/<uuid:id>', views.video_pace, name='pace'),
    path('notifications', views.show_notifications, name='notifications'),
    path('delete-notification/<int:pk>', views.delete_notifications, name='delete-notification'),
    path('user-comments/<uuid:id>', views.user_comments, name='user-comments'),
    path('report', views.report, name='report'),
    path('view-log', views.view_log, name='log'),
    path('get_comments_by_post/<uuid:id>', views.get_comments_by_post, name='get_comments_by_post'),
    path('get_no_of_likes/<uuid:pk>', views.get_no_of_likes, name='get_no_of_likes'),
    path('live-stream', views.live_stream, name='live-stream'),
    path('follower/<str:pk>', views.follower, name='follower'),
    path('get_token/', views.get_token, name='get_token'),
    path('<str:pk>/follower', views.follower, name='follower'),
    path('<str:pk>/following', views.following, name='following'),
    path('create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('create-ads', views.create_ads, name='create-ads'),
    path('face-recognition', views.face_recognition, name='face-recognition'),
    path('postview', PostAPIView.as_view(), name='post-view'),
]