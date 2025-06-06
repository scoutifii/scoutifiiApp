from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
import uuid
import math
import random
from django.core.validators import RegexValidator, FileExtensionValidator
from django.conf import settings
from scoutifiiapp.JWT import generate
from django.urls import reverse
from scoutify2.fileUploadChecker import ContentTypeRestrictedFileField


class AllLogins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    login_date = models.DateTimeField(auto_now_add=True)
    last_logged_out = models.DateTimeField()
    ip_address = models.CharField(max_length=100, default=0, blank=True)
    server = models.CharField(max_length=100, default=0, blank=True)

    class Meta:
        db_table = "all_logins"

    def __str__(self):
        return str(self.user) + ':' + str(self.login_date)

class Profile(models.Model):
    PROFILE_TYPES = (("user",'User'), ("player",'Player'), ("coach",'Coach'), ("agent", 'Agent'))
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile') #Foreign key of currently logged in user
    id_user = models.IntegerField() #Primary key of profile
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-user.png', validators= [FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    location = models.CharField(max_length=100, blank=True)
    phone_no = models.CharField(validators=[mobile_num_regex], max_length=13, default=0, blank=False)
    forgot_password_token = models.CharField(max_length=100)
    country_id = CountryField()
    profile_type_data = models.CharField(default="user", max_length=10)
    birth_date = models.DateField(null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = "profile"
    
    def __str__(self):
        return self.user.username

class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "code"

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]  #List comprehension'''
        code_items = []

        for x in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)

class BrandSetting(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_title = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=100)
    brand_logo = models.ImageField(upload_to='brand_images', validators= [FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    favicon_icon = models.ImageField(upload_to='brand_images', validators= [FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    brand_footer = models.CharField(max_length=1000)
    brand_slogan = models.CharField(max_length=50, null=True)
    about = models.TextField()
    google_analytics = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    website = models.URLField()
    location = models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "brand_setting"

    def __str__(self):
        return self.brand_name

class Post(models.Model):
    POST_CATEGORY = (("football",'Football'), ("netball",'Netball'), ("basketball",'Basketball'), ("volleyball",'Volleyball'), ("athletics",'Athletics'), ("boxing",'Boxing'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_prof = models.CharField(max_length=100, blank=True, null=True)
    video = ContentTypeRestrictedFileField(upload_to='player_videos/%Y/%m/%d', blank=False, content_types=['video/mp4', 'video/mkv',],max_upload_size=20971520)
    video_name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    category_type = models.CharField(choices=POST_CATEGORY, max_length=50, null=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_views = models.IntegerField(default=0)
    no_of_flair = models.IntegerField(default=0)
    no_of_off_the_ball = models.IntegerField(default=0)
    no_of_positioning = models.IntegerField(default=0)
    no_of_marking = models.IntegerField(default=0)
    no_of_anticipation = models.IntegerField(default=0)
    no_of_pace = models.IntegerField(default=0)
    no_of_tackling = models.IntegerField(default=0)
    no_of_vision = models.IntegerField(default=0)
    no_of_work_rate = models.IntegerField(default=0)
    no_of_aggression = models.IntegerField(default=0)
    no_of_charisma = models.IntegerField(default=0)
    no_of_ball_protection = models.IntegerField(default=0)
    no_of_speed = models.IntegerField(default=0)
    no_of_heading = models.IntegerField(default=0)
    no_of_jumping_reach = models.IntegerField(default=0)
    no_of_shooting = models.IntegerField(default=0)
    no_of_technique = models.IntegerField(default=0)
    no_of_passing = models.IntegerField(default=0)
    no_of_finishing = models.IntegerField(default=0)
    no_of_ball_control = models.IntegerField(default=0)
    no_of_free_kick = models.IntegerField(default=0)
    no_of_dribbling = models.IntegerField(default=0)
    no_of_crossing = models.IntegerField(default=0)
    no_of_concentration = models.IntegerField(default=0)
    no_of_agility = models.IntegerField(default=0)
    no_of_reflexes = models.IntegerField(default=0)
    no_of_saving_penalties = models.IntegerField(default=0)
    no_of_footwork_and_distribution = models.IntegerField(default=0)
    no_of_commanding_in_defence = models.IntegerField(default=0)
    no_of_saving_one_on_one = models.IntegerField(default=0)
    no_of_handling = models.IntegerField(default=0)
    no_of_aerial_ability = models.IntegerField(default=0)
    no_of_close_range_shot_stopping_ability = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post"

    def __str__(self):
        return f"{self.user}, {self.profile.country_id}"

    
    def simplify(self):
        magnitude_dict={0:'', 1:'K', 2:'M', 3:'B'}
        num=math.floor(self)
        magnitude=0
        while num>=1000.0:
            magnitude+=1
            num=num/1000.0
        return(f'{math.floor(num*100.0)/100.0} {magnitude_dict[magnitude]}')

    def human_format(self):
        units = ['', 'K', 'M', 'G', 'T', 'P']
        k = 1000.0
        magnitude = int(math.floor(math.log(self, k)))
        return '%.2f%s' % (self / k**magnitude, units[magnitude])
        

    def timeAgo(self):
        now = timezone.now()        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) + "s"            
            else:
                return str(seconds) + "seconds"            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"            
            else:
                return str(minutes) + "minutes"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"
            else:
                return str(hours) + "hours"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days <= 6:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"
            else:
                return str(days) + "days"

        # 1 week to 4 weeks
        if diff.days >= 7 and diff.days < 31:
            weeks= math.floor(diff.days/7)
        
            if weeks == 1:
                return str(weeks) + "week"
            else:
                return str(weeks) + "weeks"

        ''' 1 month to 12 month '''
        if diff.days >= 31 and diff.days < 365:
            months= math.floor(diff.days/31)            

            if months == 1:
                return str(months) + "month"
            else:
                return str(months) + "months"

        ''' 1 year to unlimited years'''
        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "y"
            else:
                return str(years) + "years"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    user_prof = models.CharField(max_length=50, blank=True, default=None)
    comment_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return '%s - %s' % (self.post.video_name, self.comment_body)

    def get_comments_by_post(self):
        return Comment.objects.filter(post=self).order_by('created_at')

    def timeAgo(self):
        now = timezone.now()        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "s"            
            else:
                return str(seconds) + "seconds"            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"            
            else:
                return str(minutes) + "minutes"


        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"
            else:
                return str(hours) + "hours"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days <= 6:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"
            else:
                return str(days) + "days"

        # 1 week to 4 weeks
        if diff.days >= 7 and diff.days < 31:
            weeks= math.floor(diff.days/7)
        
            if weeks == 1:
                return str(weeks) + "week"
            else:
                return str(weeks) + "weeks"

        ''' 1 month to 12 month '''
        if diff.days >= 31 and diff.days < 365:
            months= math.floor(diff.days/31)            

            if months == 1:
                return str(months) + "month"
            else:
                return str(months) + "months"

        ''' 1 year to unlimited years'''
        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "y"
            else:
                return str(years) + "years"

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "like_post"

    def __str__(self):
        return self.username

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1,'Like'), (2,'Comment'), (3,'Follow'), (4, 'Voted'), (5, 'Viewed'))

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user", null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profiles", default='')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


    class Meta:
        db_table = "notifications"

    def __str__(self):
        return f"{self.post}"

    def timeAgo(self):
        now = timezone.now()        
        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "s"            
            else:
                return str(seconds) + "seconds"            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"            
            else:
                return str(minutes) + "minutes"


        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"
            else:
                return str(hours) + "hours"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days <= 6:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"
            else:
                return str(days) + "days"

        # 1 week to 4 weeks
        if diff.days >= 7 and diff.days < 31:
            weeks= math.floor(diff.days/7)
        
            if weeks == 1:
                return str(weeks) + "week"
            else:
                return str(weeks) + "weeks"

        ''' 1 month to 12 month '''
        if diff.days >= 31 and diff.days < 365:
            months= math.floor(diff.days/31)            

            if months == 1:
                return str(months) + "month"
            else:
                return str(months) + "months"

        ''' 1 year to unlimited years'''
        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "y"
            else:
                return str(years) + "years"

class VideoCounts(models.Model):
    post = models.ForeignKey(Post, related_name='video_counts', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(max_length=15, default="127.0.0.1")
    session = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, related_name='video_counts', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "video_counts"

    def __str__(self):
        return f'{0} in {1} post'.format(self.ip_address, self.post.video_name)

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="followers_count")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "followers_count"

    def __str__(self):
        return self.user

class OffTheBallVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "off_the_ball"

    def __str__(self):
        return self.username

class VideoPositioning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "positioning"

    def __str__(self):
        return self.username

class VideoMarking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "marking"

    def __str__(self):
        return self.username
         
class VideoAnticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "anticipation"

    def __str__(self):
        return self.username

class VideoPace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pace"

    def __str__(self):
        return self.username

class VideoTackling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tackling"

    def __str__(self):
        return self.username

class VideoVision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vision"

    def __str__(self):
        return self.username

class VideoWorkRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "work_rate"

    def __str__(self):
        return self.username

class VideoAggression(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "aggression"

    def __str__(self):
        return self.username

class VideoCharisma(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "charisma"

    def __str__(self):
        return self.username

class VideoBallProtection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ball_protection"

    def __str__(self):
        return self.username

class VideoSpeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "speed"

    def __str__(self):
        return self.username

class VideoHeading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "heading"

    def __str__(self):
        return self.username

class VideoFlair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "flair"

    def __str__(self):
        return self.username

class VideoJumpingReach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "jumping_reach"

    def __str__(self):
        return self.username

class VideoShooting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shooting"

    def __str__(self):
        return self.username

class VideoTechnique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "technique"

    def __str__(self):
        return self.username

class VideoPassing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "passing"

    def __str__(self):
        return self.username

class VideoFinishing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "finishing"

    def __str__(self):
        return self.username

class VideoBallControl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ball_control"

    def __str__(self):
        return self.username

class VideoFreeKick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "free_kick"

    def __str__(self):
        return self.username

class VideoDribbling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dribbling"

    def __str__(self):
        return self.username

class VideoCrossing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "crossing"

    def __str__(self):
        return self.username

class VideoSavingOneOnOne(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saving_one_on_one"

    def __str__(self):
        return self.username

class VideoCommandingInDefence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "commanding_in_defence"

    def __str__(self):
        return self.username

class VideoFootworkAndDistribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "footwork_and_distribution"

    def __str__(self):
        return self.username

class VideoSavingPenalties(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saving_penalties"

    def __str__(self):
        return self.username

class VideoConcentration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "concentration"

    def __str__(self):
        return self.username

class VideoAgility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agility"

    def __str__(self):
        return self.username

class VideoCloseRangeShotStoppingAbility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "close_range_shot_stopping_ability"

    def __str__(self):
        return self.username

class VideoReflexes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reflexes"

    def __str__(self):
        return self.username

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=100, null=True)
    activity = models.CharField(max_length=1000)
    ip_address = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "activity_log"

    def __str__(self):
        return '%s - %s' % (self.activity, self.created_at) 

    # JSON
    def get_data(self):
        return {
            'user': self.user_id,
            'username': self.username,
            'activity': self.activity,
            'ip_address': self.ip_address,
            'url': self.url,
            'user_agent': self.user_agent,
            'created_at': self.created_at,
        }

class LiveVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    uid = models.CharField(max_length=200, null=True)
    channel_name = models.CharField(max_length=200, null=True)
    live_date = models.DateTimeField(auto_now_add=True)
    live_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'live_video'

    def __str__(self):
        return f"{self.user}, {self.live_date}" 

class Messaging(models.Model):
    message_body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messaging'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.created_by}'

class Room(models.Model):
    WAITING = 'Waiting'
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    CHOICES_STATUS = {
        (WAITING,'Waiting'),
        (ACTIVE,'Active'),
        (CLOSED, 'Closed'),
    } 
    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    messages = models.ManyToManyField(Messaging, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.client} {self.uuid}'


class Ads(models.Model):
    MOBILEMONEY = 'MobileMoney'
    VISA = 'Visa'
    PAYMENT_STATUS = {
        (MOBILEMONEY,'MobileMoney'),
        (VISA,'Visa'),
    }
    REGIONAL = 'Regional'
    LOCAL = 'Local'
    LOCATION_STATUS = {
        (REGIONAL,'Regional'),
        (LOCAL,'Local'),
    }
    ALL = 'All'
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_STATUS = {
        (ALL, 'All'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    }
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=20, choices=LOCATION_STATUS, default=LOCAL)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, choices=GENDER_STATUS, default=ALL)
    daily_budget = models.CharField(max_length=10, null=True)
    duration = models.IntegerField(null=True)
    tax = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    total_payment = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_STATUS, default=MOBILEMONEY)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'scoutifii_ad'
        ordering = ('-created_at',)


class FaceRecognition(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    face_encoding = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'face_recognition'
        ordering = ('-created_at',)