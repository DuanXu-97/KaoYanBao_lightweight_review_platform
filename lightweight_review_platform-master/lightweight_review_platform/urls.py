"""lightweight_review_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views
from main_platform.views import WangEditor_uploadView,Thumbs_UpView,Thumbs_DownView,cancel_thumbsUpView,cancel_thumbsDownView,\
    AddTagtoQuesView,RemoveTagtoQuesView
from django.conf import settings
from django.views.static import serve


urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'', include('main_platform.urls', namespace='main_platform')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^login/$', views.UserLoginView.as_view(), name='login'),

    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),

    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),

    url(r'^usercenter/$', views.UserCenterView.as_view(), name='usercenter'),
  
    url(r'^upload_userpic/$', views.UploadImageView.as_view(),name='upload_userpic'),
  
    url(r'^userCenter_compile/$', views.UserCenterView.as_view(),name='user_center_compile'),

    url(r'^passwordChange/$', views.PasswordChangeView.as_view(), name='password_change'),

    url(r'^checkin/$', views.CheckinView.as_view(), name='check_in'),

    url(r'^memo/$', views.MemoView.as_view(), name='memo'),

    url(r'^initialTags/$', views.ActiveUserView.as_view(), name='weakness_chosen'),
  
    url(r'^initialTags_again/$', views.InitialTags_againView.as_view(), name='weakness_chosen_again'),    
  
    url(r'^ques/upload/$', WangEditor_uploadView.as_view(), name='upload_img'),

    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
  
    url(r'^thumbsUp/$',Thumbs_UpView.as_view(),name='thumbsUp'),   #点赞

    url(r'^thumbsDown/$',Thumbs_DownView.as_view(),name='thumbsDown'),   #点踩

    url(r'^cancel_thumbsUp/$',cancel_thumbsUpView.as_view(),name='cancel_thumbsUp'),   #取消点赞

    url(r'^cancel_thumbsDown/$',cancel_thumbsDownView.as_view(),name='cancel_thumbsDown'),  #取消点踩

    url(r'^addTagtoQues/$',AddTagtoQuesView.as_view(),name='addTagtoQues'),  #添加标签

    url(r'^removeTagtoQues/$',RemoveTagtoQuesView.as_view(),name='removeTagtoQues'), #删除标签





  
]
