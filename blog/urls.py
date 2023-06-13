from django.urls import path
from . import views # 현재 폴더에 있는 views.py를 사용할 수 있게 가져오라는 의미

urlpatterns = [
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    # /blog/update_post/정수/ 형태의 URL -> views.py의 PostUpdate 클래스 이용
    path('create_post/', views.PostCreate.as_view()),
    # /blog/create_post/ 형태의 URL -> views.py의 PostCreate 클래스 이용
    path('tag/<str:slug>/', views.tag_page),
    # /blog/tag/태그이름/ 형태의 URL -> views.py의 tag_page() 함수 이용
    path('category/<str:slug>/', views.category_page),
    # /blog/category/카테고리이름/ 형태의 URL -> views.py의 category_page() 함수 이용
    path('<int:pk>/new_comment/', views.new_comment),
    # /blog/정수/new_comment/ 형태의 URL -> views.py의 new_comment() 함수 이용
    path('<int:pk>/', views.PostDetail.as_view()),
    # /blog/정수/ 형태의 URL -> PostDetail 클래스 이용
    path('', views.PostList.as_view()),
    # URL 끝이 /blog/일 떄는 PostList클래스로 처리
]
# urlpatters 리스트 -> URL과 그 URL이 들어올 떄 어떻게 처리할지 명시