"""django_blog_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog/', include('blog.urls')),
    # 방문자가 blog/로 접속 -> blog앱 폴더의 urls.py를 참조하도록 설정
    path('admin/', admin.site.urls),
    # 반문자가 서버 IP/admin/으로 접속 -> admin.site.urls에 정의된 내용을 찾아 처리
    path('', include('single_pages.urls')),
    # 도메인 뒤에 아무것도 붙어있지 않은 경우 -> single_pages 앱에서 처리
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)