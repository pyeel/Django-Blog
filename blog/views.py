# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

# Create your views here.
class PostList(ListView): # ListView 클래스를 상속해서 PostList 클래스 생성
    model = Post
    ordering = '-pk' # pk값의 역순으로 정렬

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        # get_context_data()에서 기존에 제공했던 기능을 context에 저장
        # super(PostList, self) -> PostList 클래스의 부모 클래스인 ListViex 클래스의 메서드를 호출
        context['categories'] = Category.objects.all()
        # Category.objects.all() -> Category 모델의 모든 레코드를 가져옴
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        # Post.objects.filter(category=None).count() -> 카테고리가 없는 Post 레코드의 개수를 가져옴
        return context
    
#def index(request):
#   posts = Post.objects.all().order_by('-pk')
    # order_by('pk') -> pk값의 역순으로 정렬
    # views.py에서 데이터베이스에 쿼리를 보내 원하는 레코드를 가져올 수 있음
    # 쿼리 : 데이터베이스의 데이터를 가져오거나 수정, 삭제하는 등의 행위를 하기 위한 요청
    
#    return render(
#        request,
#        'blog/index.html',
#        {
#            'posts': posts,
#        }
 #   )
    # 장고가 기본으로 제공하는 render() 함수를 사용
    # -> 템플릿 폴더에서 blog 폴더의 index.html 파일을 찾아 방문자에게 전송

class PostDetail(DetailView):
    model = Post # Post 모델에 대한 개별 페이지 생성
    # Post.objects.get() -> ()안의 조건을 만족하는 Post 레코드를 가져오라는 의미
    # => Post 모델의 pk 필드 값이 single_post_page() 함수의 매개변수로 받은 pk와 같은 레코드를 가져오라는 의미
    # pk -> primary key의 약자, 각각의 레코드별로 고유의 값을 지정
    
#    return render(
#        request,
#        'blog/single_post_page.html',
#        {
#            'post' : post,
#        }
#        # 가져온 Post 레코드를 blog/single_post_page.html에 담아 렌더링
##     )