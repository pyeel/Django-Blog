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
