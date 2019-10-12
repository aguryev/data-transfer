"""netguru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views


app_name = 'task'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('upload/', views.upload, name='upload'),
    path('download/<file_name>', views.download, name='download'),
    path('<unique_slug>', views.unique_slug, name='unique_slug'),
    path('api/statistics/', views.StatisticsView.as_view(), name='api-statistics'),
    path('api/add-url/', views.AddUrlView.as_view(), name='api-add-url'),
    path('api/add-file/', views.AddFileView.as_view(), name='api-add-file'),
    path('api/get-data/<slug>/<password>', views.AccessDataView.as_view(), name='api-access-data'),   
]
