from django.contrib import admin

from .models import (
	Profile, Comment, BrandSetting, Post, LikePost, 
	VideoCounts, VideoFlair, OffTheBallVideo,
	VideoPositioning, VideoMarking, Code, Ads,
	VideoAnticipation, VideoPace, VideoTackling,
	VideoVision, VideoWorkRate, VideoAggression,
	VideoCharisma, VideoBallProtection,
	VideoSpeed, VideoHeading, VideoFlair,
	VideoJumpingReach, VideoShooting, VideoTechnique,
	VideoPassing, VideoFinishing, VideoBallControl,
	VideoFreeKick, VideoDribbling, VideoCrossing,
	FollowersCount,	Notification, VideoSavingOneOnOne,
	VideoCommandingInDefence, VideoFootworkAndDistribution,
	VideoSavingPenalties, VideoConcentration, VideoAgility,
	VideoCloseRangeShotStoppingAbility,	VideoReflexes, AllLogins, ActivityLog, LiveVideo
)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'profileimg', 'bio', 'location', 'phone_no', 'country_id', 'created_at']

class AllLoginsAdmin(admin.ModelAdmin):
	list_display = ['user', 'username', 'login_date', 'last_logged_out']

class ActivityLogAdmin(admin.ModelAdmin):
	list_display = ['user', 'activity', 'ip_address', 'url', 'user_agent', 'created_at']

admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(AllLogins, AllLoginsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(BrandSetting)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(VideoCounts)
admin.site.register(OffTheBallVideo)
admin.site.register(VideoPositioning)
admin.site.register(VideoMarking)
admin.site.register(VideoAnticipation)
admin.site.register(VideoPace)
admin.site.register(VideoTackling)
admin.site.register(VideoVision)
admin.site.register(VideoWorkRate)
admin.site.register(VideoAggression)
admin.site.register(VideoCharisma)
admin.site.register(VideoBallProtection)
admin.site.register(VideoSpeed)
admin.site.register(VideoHeading)
admin.site.register(VideoFlair)
admin.site.register(VideoJumpingReach)
admin.site.register(VideoShooting)
admin.site.register(VideoTechnique)
admin.site.register(VideoPassing)
admin.site.register(VideoFinishing)
admin.site.register(VideoBallControl)
admin.site.register(VideoFreeKick)
admin.site.register(VideoDribbling)
admin.site.register(VideoCrossing)
admin.site.register(FollowersCount)
admin.site.register(VideoReflexes)
admin.site.register(Notification)
admin.site.register(VideoSavingOneOnOne)
admin.site.register(VideoCommandingInDefence)
admin.site.register(VideoFootworkAndDistribution)
admin.site.register(VideoSavingPenalties)
admin.site.register(VideoConcentration)
admin.site.register(VideoAgility)
admin.site.register(VideoCloseRangeShotStoppingAbility)
admin.site.register(Code)
admin.site.register(LiveVideo)
admin.site.register(Ads)