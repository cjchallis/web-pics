"""web_pics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url

from review import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^testing$', views.testing, name = 'testing'),
    url(r'^pics()/$', views.view_dir, name = 'root_pic'),
    url(r'^pics/(.+)/$', views.view_dir, name = 'view_dir'),
    url(r'^deletion_list$', views.del_list, name = 'del_list'),
    url(r'^run_deletion$', views.run_del, name = 'run_del'),
    url(r'^chatbooks$', views.chatbooks, name = 'chatbooks'),
    url(r'(.+)/next$', views.nxt, name = 'next'),
    url(r'(.+)/previous$', views.prev, name = 'prev'), 
    url(r'(.+)/(KP|DL|CH)$', views.modify, name = 'modify'),
    url(r'(.+)', views.view_img, name='view_img'),
    # url(r'^admin/', include(admin.site.urls)),
]

