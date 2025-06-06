from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import *

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class PostSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'

class AllLoginsSerializer(ModelSerializer):
	class Meta:
		model = AllLogins
		fields = '__all__'


class ProfileSerializer(ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'


class BrandSettingSerializer(ModelSerializer):
	class Meta:
		model = BrandSetting
		fields = '__all__'


class CommentSerializer(ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'

class LikePostSerializer(ModelSerializer):
	class Meta:
		model = LikePost
		fields = '__all__'

class NotificationSerializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = '__all__'

class VideoCountsSerializer(ModelSerializer):
	class Meta:
		model = VideoCounts
		fields = '__all__'

class FollowersCountSerializer(ModelSerializer):
	class Meta:
		model = FollowersCount
		fields = '__all__'

class OffTheBallVideoSerializer(ModelSerializer):
	class Meta:
		model = OffTheBallVideo
		fields = '__all__'

class VideoPositioningSerializer(ModelSerializer):
	class Meta:
		model = VideoPositioning
		fields = '__all__'

class VideoMarkingSerializer(ModelSerializer):
	class Meta:
		model = VideoMarking
		fields = '__all__'

class VideoAnticipationSerializer(ModelSerializer):
	class Meta:
		model = VideoAnticipation
		fields = '__all__'

class VideoPaceSerializer(ModelSerializer):
	class Meta:
		model = VideoPace
		fields = '__all__'

class VideoTacklingSerializer(ModelSerializer):
	class Meta:
		model = VideoTackling
		fields = '__all__'

class VideoVisionSerializer(ModelSerializer):
	class Meta:
		model = VideoVision
		fields = '__all__'

class VideoWorkRateSerializer(ModelSerializer):
	class Meta:
		model = VideoWorkRate
		fields = '__all__'

class VideoAggressionSerializer(ModelSerializer):
	class Meta:
		model = VideoAggression
		fields = '__all__'

class VideoCharismaSerializer(ModelSerializer):
	class Meta:
		model = VideoCharisma
		fields = '__all__'

class VideoBallProtectionSerializer(ModelSerializer):
	class Meta:
		model = VideoBallProtection
		fields = '__all__'

class VideoSpeedSerializer(ModelSerializer):
	class Meta:
		model = VideoSpeed
		fields = '__all__'

class VideoHeadingSerializer(ModelSerializer):
	class Meta:
		model = VideoHeading
		fields = '__all__'

class VideoFlairSerializer(ModelSerializer):
	class Meta:
		model = VideoFlair
		fields = '__all__'

class VideoJumpingReachSerializer(ModelSerializer):
	class Meta:
		model = VideoJumpingReach
		fields = '__all__'

class VideoShootingSerializer(ModelSerializer):
	class Meta:
		model = VideoShooting
		fields = '__all__'

class VideoTechniqueSerializer(ModelSerializer):
	class Meta:
		model = VideoTechnique
		fields = '__all__'

class VideoPassingSerializer(ModelSerializer):
	class Meta:
		model = VideoPassing
		fields = '__all__'

class VideoFinishingSerializer(ModelSerializer):
	class Meta:
		model = VideoFinishing
		fields = '__all__'

class VideoBallControlSerializer(ModelSerializer):
	class Meta:
		model = VideoBallControl
		fields = '__all__'

class VideoFreeKickSerializer(ModelSerializer):
	class Meta:
		model = VideoFreeKick
		fields = '__all__'

class VideoDribblingSerializer(ModelSerializer):
	class Meta:
		model = VideoDribbling
		fields = '__all__'

class VideoFootworkAndDistributionSerializer(ModelSerializer):
	class Meta:
		model = VideoFootworkAndDistribution
		fields = '__all__'

class VideoSavingOneOnOneSerializer(ModelSerializer):
	class Meta:
		model = VideoSavingOneOnOne
		fields = '__all__'

class VideoCommandingInDefenceSerializer(ModelSerializer):
	class Meta:
		model = VideoCommandingInDefence
		fields = '__all__'

class VideoSavingPenaltiesSerializer(ModelSerializer):
	class Meta:
		model = VideoSavingPenalties
		fields = '__all__'

class VideoConcentrationSerializer(ModelSerializer):
	class Meta:
		model = VideoConcentration
		fields = '__all__'

class VideoAgilitySerializer(ModelSerializer):
	class Meta:
		model = VideoAgility
		fields = '__all__'

class VideoCloseRangeShotStoppingAbilitySerializer(ModelSerializer):
	class Meta:
		model = VideoCloseRangeShotStoppingAbility
		fields = '__all__'

class VideoReflexesSerializer(ModelSerializer):
	class Meta:
		model = VideoReflexes
		fields = '__all__'

class ActivityLogSerializer(ModelSerializer):
	class Meta:
		model = ActivityLog
		fields = '__all__'