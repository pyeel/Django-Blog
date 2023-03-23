from django.urls import path
from . import views # 현재 폴더에 있는 views.py를 사용할 수 있게 가져오라는 의미

urlpatterns = [
    path('', views.index),
    # 입력된 URL이 'blog/'로 끝난다면 임포트한 view.py에 정의되어 있는 index()함수 실행
]
# urlpatters 리스트 -> URL과 그 RUL이 들어올 떄 어떻게 처리할지 명시