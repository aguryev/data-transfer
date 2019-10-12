from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import SecuredData
from .utils import store_file


class StatisticsSerializer(serializers.Serializer):
	#
	# serializer for statistics
	#
	data = serializers.SerializerMethodField()

	def get_data(self, queryset):
		stat = {}
		for obj in queryset:
			if obj.visits > 0: # 
				date_string = obj.created.strftime('%Y-%m-%d')
				if not date_string in stat:
					stat[date_string] = {'files':0, 'links':0}
				if obj.is_file:
					stat[date_string]['files'] += 1
				else:
					stat[date_string]['links'] += 1

		return stat


class AddUrlSerializer(serializers.Serializer):
	#
	# serilizer for addition URL element
	#
	description = serializers.CharField()
	link = serializers.CharField()

	def create(self, validated_data):
		# create and save SecuredData object
		url_secured = SecuredData.create(
			description=validated_data['description'],
			link=validated_data['link'],
			is_file=False,
			)
		url_secured.save()
		return url_secured

class AddFileSerializer(serializers.Serializer):
	#
	# serilizer for addition URL element
	#
	description = serializers.CharField()
	file = serializers.FileField()

	def create(self, validated_data):
		# upload the file to a unique location 
		filename = User.objects.make_random_password() + '.'+ validated_data['file'].name.split('.')[-1]
		path = 'main/uploads/' + filename
		store_file(validated_data['file'], path)
		# define hyper-link
		link = '/'.join(['http:/', self.context['host'], 'download', filename])
		# create and save SecuredData object
		file_secured = SecuredData.create(
			description=validated_data['description'],
			link=link,
			is_file=True,
			)
		file_secured.save()
		return file_secured

class ResponseSerializer(serializers.ModelSerializer):
	#
	# serializer for response after addition data
	#
	class Meta:
		model = SecuredData
		fields = ('slug', 'password')

class AccessDataSerializer(serializers.ModelSerializer):
	#
	# serializer for access secured data
	#
	class Meta:
		model = SecuredData
		fields = ('slug', 'link')














