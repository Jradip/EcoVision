"""
URL configuration for eco_vision_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from eco_vision_api_edu_app.views import PredictImageView
from eco_vision_api_bank_app.views import WasteBankListView,TrashCanListView
from eco_vision_api_leader_board_app.views import LeaderboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eco_vision_api_auth_app.urls')),
    path('predict/', PredictImageView.as_view(), name='predict'),
    path('waste-banks/', WasteBankListView.as_view(), name='waste_bank'),
    path('trash-cans/', TrashCanListView.as_view(), name='trash_can'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]