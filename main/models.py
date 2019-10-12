from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.




class SecuredData(models.Model):
	#
	# Model of the secured data object
	#
	description = models.TextField() # description of the dat
	link = models.CharField(max_length=200) # hyper-reference to the data
	slug = models.CharField(max_length=16) # unique slag to access the data
	password = models.CharField(max_length=10) # password to access the data
	created = models.DateTimeField(default=timezone.now) # time of creation
	valid_until = models.DateTimeField() # expiry of the link
	visits = models.IntegerField(default=0) # counter of the visits
	is_file = models.BooleanField(default=True) # flag showing whether the data is file or URL

	@classmethod
	def create(cls, description, link, is_file):
		#
		# Extend model with create method
		#
		# generate unique slug and password
		slug = User.objects.make_random_password(length=16, allowed_chars="abcdefghjkmnpqrstuvwxyz")
		password = User.objects.make_random_password()
		# define create time and expiry
		created = timezone.now()
		valid_until = created + timezone.timedelta(hours=24)
		data = cls(description=description, link=link, slug=slug, password=password,
			   created=created, valid_until=valid_until, is_file=is_file)
		return data

	def __str__(self):
		if self.is_file:
			s = 'File: '
		else:
			s = 'URL: '
		s += self.created.strftime('%Y-%m-%d %H:%M:%S')
		return s


class UserInfo(models.Model):
	#
	# extension to the User to store User-Agent  
	#
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_agent = models.CharField(max_length=200)

# auto creation of the UserInfo object when a User is created
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
	if created:
		UserInfo.objects.create(user=instance)
