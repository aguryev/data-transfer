from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import FileResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import UploadFileForm, UploadUrlForm, AccessForm
from .models import SecuredData
from .utils import store_file
from .serializers import StatisticsSerializer, AddUrlSerializer, AddFileSerializer, ResponseSerializer, AccessDataSerializer


# Create your views here.


#
# API views
#

class StatisticsView(APIView):
	#
	# secured endpoint view for statistics
	#
	permission_classes = [IsAuthenticated]

	def get(self, request):
		# build queryset of items that have been visited at least once
		queryset = SecuredData.objects.filter(visits__gt=0).order_by('created')
		serializer = StatisticsSerializer(queryset)
		return Response(serializer.data['data'])

class AddUrlView(CreateAPIView):
	#
	# secured endpoint view for adding URL
	#
	permission_classes = [IsAuthenticated]
	serializer_class = AddUrlSerializer

	def perform_create(self, serializer):
		return serializer.save()

	def create(self, request, *args, **kwargs):
		# serializer for creation
		create_serializer = AddUrlSerializer(data=request.data)
		create_serializer.is_valid()
		instance = self.perform_create(create_serializer)
		# serializer for response
		response_serializer = ResponseSerializer(instance)

		return Response(response_serializer.data)

class AddFileView(CreateAPIView):
	#
	# secured endpoint view for adding file
	#
	permission_classes = [IsAuthenticated]
	serializer_class = AddFileSerializer

	def perform_create(self, serializer):
		return serializer.save()

	def create(self, request, *args, **kwargs):
		# serializer for creation
		create_serializer = AddFileSerializer(data=request.data, context={'host':request.headers['Host']})
		create_serializer.is_valid()
		instance = self.perform_create(create_serializer)
		# serializer for response
		response_serializer = ResponseSerializer(instance)

		return Response(response_serializer.data)

class AccessDataView(RetrieveAPIView):
	#
	# open endpoint view to access secured data
	#
	lookup_fields = ('slug', 'password')
	queryset = SecuredData.objects.all()
	serializer_class = AccessDataSerializer

	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(
			queryset,
			slug=self.kwargs['slug'], 
			password=self.kwargs['password'],
			)
		return obj

#
# Regular views
#

class LoginView(FormView):
	#
	# Login view
	#
	success_url = '/upload/'
	form_class = AuthenticationForm
	template_name = 'login.html'
	
	def form_valid(self, form):
		login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)

def upload(request):
	#
	# add data view
	#
	if request.user.is_authenticated:
		# process POST request
		if request.method == 'POST':
			# url-form posted
			if 'url' in request.POST: 
				form = UploadUrlForm(request.POST)
			# file-form posted
			else: 
				form = UploadFileForm(request.POST, request.FILES)
			# form validation
			if form.is_valid():
				# store URL
				if 'url' in request.POST:
					secured_data = SecuredData.create(
						description=form.cleaned_data.get('description'),
						link=form.cleaned_data.get('url'),
						is_file=False,
						)
				# store file
				else:
					# upload the file to a unique location
					filename = User.objects.make_random_password() + '.'+ form.cleaned_data.get('file').name.split('.')[-1]
					path = 'main/uploads/' + filename
					store_file(form.cleaned_data.get('file'), path)
					# define hyper-link
					link = '/'.join(['http:/', request.headers['host'], 'download', filename])
					# create and save SecuredData object
					secured_data = SecuredData.create(
						description=form.cleaned_data.get('description'),
						link=link,
						is_file=True,
						)
				secured_data.save()

				return render(request=request,
							  template_name='success.html',
							  context={'data':secured_data, 'host':request.headers['host']})
		# process GET request
		file_form = UploadFileForm()
		url_form = UploadUrlForm()
		return render(request=request,
					  template_name='upload.html',
					  context={'file_form':file_form, 'url_form':url_form})
	# prevent unauthorized request 
	else:
		return redirect('/')



def unique_slug(request, unique_slug):
	#
	# access data view
	#
	# check link expiry
	data = get_object_or_404(SecuredData, slug=unique_slug, valid_until__gte=timezone.now())

	# process POSt request
	if request.method == 'POST':
		form = AccessForm(request.POST)
		if form.is_valid():
			# check whether the password matches the slug
			if form.cleaned_data.get('password') == data.password:
				# update correct redirect counter
				data.visits += 1
				data.save()
				return redirect(data.link)
			# incorrect password
			else:
				form = AccessForm()
				return render(request=request,
							  template_name='download.html',
							  context={'form':form, 'data':data, 'try_again':True})
	# process GET request
	form = AccessForm()
	return render(request=request,
				  template_name='download.html',
				  context={'form':form, 'data':data})

def download(request, file_name):
	#
	# downlod secured file
	#
	return FileResponse(open('main/uploads/' + file_name, 'rb'))
