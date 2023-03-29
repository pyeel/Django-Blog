from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-pk')
    # order_by('pk') -> pk값의 역순으로 정렬
    # views.py에서 데이터베이스에 쿼리를 보내 원하는 레코드를 가져올 수 있음
    # 쿼리 : 데이터베이스의 데이터를 가져오거나 수정, 삭제하는 등의 행위를 하기 위한 요청
    
    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )
    # 장고가 기본으로 제공하는 render() 함수를 사용
    # -> 템플릿 폴더에서 blog 폴더의 index.html 파일을 찾아 방문자에게 전송

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    # Post.objects.get() -> ()안의 조건을 만족하는 Post 레코드를 가져오라는 의미
    # => Post 모델의 pk 필드 값이 single_post_page() 함수의 매개변수로 받은 pk와 같은 레코드를 가져오라는 의미
    # pk -> primary key의 약자, 각각의 레코드별로 고유의 값을 지정
    
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post' : post,
        }
        # 가져온 Post 레코드를 blog/single_post_page.html에 담아 렌더링
    )