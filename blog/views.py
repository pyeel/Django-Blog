from django.shortcuts import render
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
    
def category_page(request, slug):
    if slug == 'no_category':
        # slug가 no_category라면
        category = '미분류'
        # category 변수에 '미분류'를 저장
        post_list = Post.objects.filter(category=None)
        # Post.objects.filter(category=None) -> 카테고리가 없는 Post 레코드를 가져옴
    else:
        category = Category.objects.get(slug=slug)
        # Category.objects.get(slug=slug) -> category_page()함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 가져와서 category 변수에 저장
        post_list = Post.objects.filter(category=category)
        # Post.objects.filter(category=category) -> category_page()함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 가져와서 category 변수에 저장
    
    return render(
        request,
        'blog/post_list.html', # 템플릿은 포스트 목록 페이지를 만들 때 사용했던 blog/post_list.html을 재사용
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            # 페이지의 오른쪽에 위치한 카테고리 목록을 만들기 위해 Category 모델의 모든 레코드를 가져옴
            'no_category_post_count': Post.objects.filter(category=None).count(),
            # 카테고리 카드 맨 아래에 미분류 포스트와 그 개수를 알려줌
            "category": category,
            # 페이지 타이틀 옆의 카테고리 이름을 알려줌.
        }
    )

class PostDetail(DetailView):
    model = Post # Post 모델에 대한 개별 페이지 생성
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        # get_context_data()에서 기존에 제공했던 기능을 context에 저장
        # super(PostDetail, self) -> PostDeatail 클래스의 부모 클래스인 ListView 클래스의 메서드를 호출
        context["categories"] = Category.objects.all()
        # Category.object.all() -> Category 모델의 모든 레코드를 가져옴
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        # Post.object.filter(category=None).count() -> 카테고리가 없는 Post 레코드의 개수를 가져옴
        return context