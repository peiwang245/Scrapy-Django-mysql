"""building URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

import os
os.path.dirname(os.path.dirname(os.path.abspath('.')))
from django.conf.urls import url, include
from django.contrib import admin
from BuildingPlat import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import  re_path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home),
    url(r'mdeditor/', include('mdeditor.urls')),#MD富文本编辑器
    re_path(r'^tinymce/', include('tinymce.urls')),#HTML富文本编辑器
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
