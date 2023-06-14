from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

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

def new_comment(request, pk):
    if request.user.is_authenticated:
        # 로그인한 사용자만 댓글을 작성할 수 있도록 함.
        post = get_object_or_404(Post, pk=pk)
        # get_object_or_404(Post, pk=pk) -> pk값이 pk인 Post 레코드를 가져옴
        # post = Post.objects.get(pk=pk)를 사용할 수도 있지만, 해당하는 pk가 없는 경우 404 오류를 발생하도록 하기 위해
        # 장고가 제공하는 get_object_or_404() 기능 활용
        
        if request.method == 'POST': # POST 요청이 들어오먄
            comment_form = CommentForm(request.POST) # CommentForm에 POST 요청의 내용을 전달
            if comment_form.is_valid(): # CommentForm에 전달된 내용이 유효하다면
                comment = comment_form.save(commit=False)
                # comment_form에 저장된 데이터를 comment 변수에 저장
                # commit=False -> DB에 바로 저장하지 않고, comment_form에 담긴 정보로 Comment 인스턴스만 ㄱ ㅏ져옴
                # 이때 CommmentForm은 content 필드의 내용만 가지고 있기에 post와 author 필드를 추가로 저장해야 함
                comment.post = post # comment 변수에 post 변수를 저장
                comment.author = request.user # comment 변수에 로그인한 사용자를 저장
                comment.save() # comment 변수에 저장된 데이터를 DB에 저장
                return redirect(comment.get_absolute_url())
                # comment 변수에 저장된 데이터의 절대 경로로 리다이렉트
                # 해당 포스트의 상세 페이지에서 이 댓글이 작성되어 있는 위치로 브라우저가 이동
        else:
            return redirect(post.get_absolute_url())
            # comment 변수에 저장된 데이터의 절대 경로로 리다이렉트
            # 해당 포스트의 상세 페이지에서 이 댓글이 작성되어 있는 위치로 브라우저가 이동
    else:
        raise PermissionDenied
    # 비정상적인 방법으로 new_comment로 접근하려고 하거나, 로그인하지 않은 사용자가 댓글을 작성하려고 하면 오류 발생
        
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
        context['comment_form'] = CommentForm
        # 댓글 폼을 보여주기 위해 CommentForm 클래스의 인스턴스를 생성해서 comment_form 변수에 저장
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
            response = super(PostCreate, self).form_valid(form)
            # super(PostCreate, self).form_valid(form) -> PostCreate 클래스의 부모 클래스인 CreateView 클래스의 form_valid() 메서드를 호출
            # 태그와 관련된 작업을 하기 전에 CReateView의 form_valid() 결과값을 response 변수에 임시로 저장
            tags_str = self.request.POST.get('tags_str') #Post 방식으로 전달된 정보중 name='tags_str'인 input 값을 tags_str 변수에 저장
            if tags_str:
                tags_str = tags_str.strip() # tags_str 변수의 앞뒤 공백을 제거
                
                tags_str = tags_str.replace(',', ';') # tags_str 변수의 쉼표를 세미콜론으로 변경
                tags_list = tags_str.split(';') # 세미콜론을 기준으로 문자열을 분리해서 리스트로 만듦
                
                for t in tags_list:
                    t = t.strip() # 리스트의 각 요소의 앞뒤 공백을 제거
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    # Tag.objects.get_or_create(name=t) -> Tag 모델에서 name 필드의 값이 t인 레코드를 가져오거나 없으면 새로 생성
                    # get_or_create() 메서드는 튜플을 반환하므로 tag와 is_tag_created 변수에 각각 저장
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        # slugify() 함수를 사용해서 태그의 이름을 슬러그로 변환, allow_unicode=True -> 한글을 포함한 유니코드 문자를 허용
                        tag.save() # 슬러그를 저장
                    self.object.tags.add(tag) # Post 모델의 tags 필드에 태그를 추가, self.object는 이번에 새로 만든 포스트를 의미
            return response # 작업이 끝나면 response 변수에 담아두었던 CreateVuew의 form_valid() 결과값을 반환
        else:
            return redirect('/blog/')
            # 로그인하지 않은 사용자는 포스트를 작성할 수 없도록 blog/로 리다이렉트

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post # Post 모델을 사용한다고 선언
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    # Post 모델의 필드 중 어떤 필드를 입력받을지 지정
    
    template_name = 'blog/post_update_form.html'
    # 템플릿 파일을 blog/post_update_form.html로 지정
    
    def get_context_data(self, **kwargs): # get_context_data() 메서드를 사용해서 템플릿에 전달할 데이터를 추가
        context = super(PostUpdate, self).get_context_data()
        # get_context_data()를 이용하여 템플릿으로 추가 인자를 넘길 수 있음.
        # super(PostUpdate, self) -> PostUpdate 클래스의 부모 클래스인 UpdateView 클래스의 메서드를 호출
        if self.object.tags.exists(): # 수정하고자 하는 포스트에 태그가 존재하면
            tags_str_list = list() # 태그를 저장할 리스트 생성
            for t in self.object.tags.all(): # 수정하고자 하는 포스트에 연결된 태그를 모두 가져와서
                tags_str_list.append(t.name) # 태그의 이름을 리스트에 추가
            context['tags_str_default'] = "; ".join(tags_str_list) # 태그의 이름을 세미콜론으로 구분해서 문자열로 만들어서 템플릿에 전달
        return context # context 변수를 반환
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # 로그인한 사용자가 superuser 또는 staff 인지 확인
            # self.get_object() -> UpdateView 클래스의 메서드로 현재 수정하고자 하는 Post 객체를 가져옴(Post.object.get(pk=pk)와 동일)
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
            # *args 의미: 함수에 입력된 인자를 튜플 형태로 저장
            # **kwargs 의미: 함수에 입력된 인자를 딕셔너리 형태로 저장                                                                                      
        else:
            raise PermissionDenied
            # 권환이 없는 방문자가 타인의 포스트를 수정하려고 할 때 403 오류 메시지를 나타냄
            
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        # super(PostUpdate, self).form_valid(form) -> PostUpdate 클래스의 부모 클래스인 UpdateView 클래스의 form_vali() 메서드를 호출
        # 태그와 관련된 작업을 하기 전에 UpdateView의 form_valid() 결과값을 response 변수에 임시로 저장
        self.object.tags.clear() # 수정하고자 하는 포스트에 연결된 태그를 모두 삭제
        
        tags_str = self.request.POST.get('tags_str')
        # POST 방식으로 전달된 정보중 name='tags_str'인 input 값을 tags_str 변수에 저장
        if tags_str:
            tags_str = tags_str.strip() # tags_str 변수의 앞뒤 공백을 제거
            tags_str = tags_str.replace(',', ';') # tags_str 변수의 쉼표를 세미콜론으로 변경
            tags_list = tags_str.split(';') # 세미콜론을 기준으로 문자열을 분리해서 리스트로 만듦
            
            for t in tags_list: # 리스트의 각 요소를 반복ㅎ면서
                t = t.strip() # 리스트의 각 요소의 앞뒤 공백을 제거
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                # Tag.object.get_or_create(name=t) -> Tag 모델에서 name 필드의 값이 t인 레코드를 가져오거나 없으면 새로 생성
                # get_or_create() 메서드는 튜플을 반환하므로 tag와 is_tag_created 변수에 각각 저장
                if is_tag_created: # ㅅ ㅐ로 생성된 태그라면
                    tag.slug = slugify(t, allow_unicode=True)
                    # slugfy() 함수를 사용해서 태그의 이름을 슬러그로 변환, allow_unicode=True -> 한글을 포함한 유니코드 문자를 허용
                    tag.save() # 슬러그를 저장
                self.object.tags.add(tag) # Post 모델의 tags 필드에 태그를 추가, self.object는 이번에 새로 만든 포스트를 의미
                
        return response # 작업이 끝나면 response 변수에 담아두었던 UpdateView의 form_valid() 결과값을 반환
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    # 로그인되어 있지 않은 상태로 CommentUpdate 에 POST방식으로 정보를 보내는 상황을 막기 위해 LoginRequiredMixin을 포함시킴
    model = Comment # Comment 모델을 사용한다고 선언
    form_class = CommentForm # CommentForm 클래스를 사용한다고 선언
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # 로그인한 사용자가 superuser 또는 staff 인지 확인 -> 다른 경우 PermissinDenied 오류 발생
            # self.get_object() -> UpdateView 클래스의 메서드로 현재 수정하고자 하는 Comment 객체를 가져옴(Comment.object.get(pk=pk)와 동일)
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
            # super(CommentUpdate, self).dispatch(request, *args, **kwargs)
            # -> CommentUpdate 클래스의 상위 클래스인 UpdateView 클래스의 dispatch() 메서드를 호출
            # dispatch() -> 웹 사이틀 방문자의 요청이 GET인지 POST인지 판단하는 역할 수행
            # *args 의미: 함수에 입력된 인자를 튜플 형태로 저장
            # **kwargs 의미: 함수에 입력된 인자를 딕셔너리 형태로 저장
            
            