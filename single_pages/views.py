from django.shortcuts import render
from blog.models import Post

# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    # Post 모델에서 최근 글 3개를 가져옴
    # order_by()는 정렬하는 메서드
    # -pk는 pk를 기준으로 내림차순 정렬
    # [:3]은 3개까지만 가져오는 것을 의미 -> 리스트 슬라이싱
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
            # 템플릿에 전달할 데이터를 사전형으로 정의
            # recent_posts 키에 recont_posts 변수를 할당
        }
    )
    
def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )