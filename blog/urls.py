from django.urls import path
from . import views # 현재 폴더에 있는 views.py를 사용할 수 있게 가져오라는 의미

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    # 만약 /blog/ 뒤에 정수 (int) 형태의 값이 붙는 URL이라면 blog/views.py의 single_post_page() 함수에 정으된 대로 처리
    # <int:pk> -> 정수 형태의 값을 pk라는 변수로 담아 single_post_page() 함수로 전달
#    path('', views.index),
    # 입력된 URL이 'blog/'로 끝난다면 임포트한 view.py에 정의되어 있는 index()함수 실행
]
# urlpatters 리스트 -> URL과 그 RUL이 들어올 떄 어떻게 처리할지 명시