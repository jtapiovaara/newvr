from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from justchat import views

urlpatterns = ([
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('justchat/startchat/', views.startchat, name='startchat'),
    path('justchat/newchatbutton/', views.newchatbutton, name='newchatbutton'),
    path('justchat/newchat/create/', views.createnewchat, name='createnewchat'),
    path('justchat/getchat/<id>', views.getchat, name='getchat'),
    path('justchat/thischat/savechat/', views.savechat, name='savechat'),
    path('allyouneed/chat/thischat/upusergroup/', views.upusergroup, name='upusergroup'),
    path('justchat/thischat/deletechat/<id>', views.deletechat, name='deletechat'),
    path('justchat/tools/tools_demo/toggle_tools', views.toggle_tools, name='toggle_tools'),
    path('justchat/tools/tools_demo', views.tools_demo, name='tools_demo'),
    path('user-guide/', views.user_guide, name='user_guide'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
