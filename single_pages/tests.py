from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self): # 테스트 시작 전 실행
        self.client = Client() # Client 인스턴스 생성
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        # User 인스턴스 생성
        # create_user()는 password를 암호화해서 저장
        
    def test_landing(self):
        # landing 페이지를 가져오는 테스트
        post_001 = Post.objects.create(
            # Post 인스턴스 생성
            title='첫 번째 포스트',
            content='첫 번째 포스트입니다.',
            author=self.user_trump
        )
        
        post_002 = Post.objects.create(
            title='두 번째 포스트',
            content='두 번째 포스트입니다.',
            author=self.user_trump
        )
        
        post_003 = Post.objects.create(
            title='세 번째 포스트',
            content='세 번째 포스트입니다.',
            author=self.user_trump
        )
        
        post_004 = Post.objects.create(
            title='네 번째 포스트',
            content='네 번째 포스트입니다.',
            author=self.user_trump
        )
        
        response = self.client.get('')
        # client 인스턴스의 get() 메서드를 사용해 '/' URL에 접근
        self.assertEqual(response.status_code, 200)
        # statuse_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # response.content를 html.parser를 사용해 soup에 저장
        
        body = soup.body
        # soup에서 body 부분만 가져옴
        self.assertNotIn(post_001.title, body.text)
        # post_001의 title이 body에 없는지 확인
        self.assertIn(post_002.title, body.text)
        # post_002의 title이 body에 없는지 확인
        self.assertIn(post_003.title, body.text)
        # post_003의 title이 body에 없는지 확인
        self.assertIn(post_004.title, body.text)
        # post_004의 title이 body에 없는지 확인