from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.about_me),
    # 도메인 뒤에 아무것도 없는 경우 -> views.py에 있는 landing()함수 실행 -> 대문 페이지 표시
    path('', views.landing),
    # 도메인 뒤에 about_me/가 붙어 있을 경우 -> about_me()함수를 실행해 자기소개 페이지 표시
]
