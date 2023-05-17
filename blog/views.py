from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag

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
    
def tag_page(request, slug):
    # slug를 인자로 받아서 tag_page() 함수를 실행
    tag = Tag.objects.get(slug=slug)
    # Tag.objects.get(slug=slug) -> tag_page()함수의 인자로 받은 slug와 동일한 slug를 갖는 태그를 가져와서 tag 변수에 저장
    post_list = tag.post_set.all()
    # tag.post_set.all() -> tag 변수에 저장된 태그와 연결된 포스트를 가져옴
    return render(
        # render() 함수를 사용해서 태그 페이지를 만듦
        request,
        'blog/post_list.html', # 템플릿은 포스트 목록 페이지를 만들 때 사용했던 blog/post_list.html을 재사용
        {  
            'post_list': post_list,
            # 포스트 목록을 보여주기 위해 post_list 변수를 템플릿에 전달
            'tag': tag,
            # 페이지 타이틀 옆의 태그 이름을 알려줌
            'categories': Category.objects.all(),
            # 페이지의 오른쪽에 위치한 카테고리 목록을 만들기 위해 Category 모델의 모든 레코드를 가져옴
            'no_category_post_count': Post.objects.filter(category=None).count(),
            # 카테고리 카드 맨 아래에 미분류 포스트와 그 개수를 알려줌
        }
    )   
    
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
        
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post # Post 모델을 사용한다고 선언
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    # Post 모델의 필드 중 어떤 필드를 입력받을지 지정
    
    def test_func(self): # test_func() 메서드를 사용해서 로그인한 사용자가 superuser 또는 staff 인지 확인
        return self.request.user.is_superuser or self.request.user.is_staff
    
    
    def form_valid(self, form):
        current_user = self.request.user # 현재 로그인한 사용자를 가져옴
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # 로그인한 사용자가 superuser 또는 staff 인지 확인
            form.instance.author = current_user
            # form.instance.author = curret_user -> 현재 로그인한 사용자를 Post 모델의 author 필드에 저장
            return super(PostCreate, self).form_valid(form)
            # super(PostCreate, self).form_valid(form)
            # -> PostCreate 클래스의 부모 클래스인 CreateView 클래스의 form_valid() 메서드를 호출
        else:
            return redirect('/blog/')
            # 로그인하지 않은 사용자는 포스트를 작성할 수 없도록 blog/로 리다이렉트