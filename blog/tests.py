from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
class TestView(TestCase): #TestCase 클래스를 상속받는 'TestView' 클래스 생성
    def setUp(self): # TestCase의 초기 데이터베이스 상태를 정의하는 메서드
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        # username이 'trump' 이고 password가 'somepassword' 인 User 객체 생성
        self.user_biden = User.objects.create_user(username='biden', password='somepassword')
        # username이 'trump' 이고 password가 'somepassword' 인 User 객체 생성
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        # programming 카테고리 생성
        self.category_mugic = Category.objects.create(name='music', slug='mugic')
        # music 카테고리 생성
        
        self.post_001 = Post.objects.create(
            title='첫 번쨰 포스트입니다.',
            content='Hello World. We are the world.',
            category = self.category_programming, # programming 카테고리를 지정
            author = self.user_trump,
        )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category = self.category_mugic, # music 카테고리를 지정
            author = self.user_biden,
        )
       
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category가 없을 수도 있죠.',
            author = self.user_biden,
        )
        
    def category_card_test(self, soup): # 카테고리 카드를 테스트하는 메서드
        categories_card = soup.find('div', id='categories-card')
        # id가 categorues-card인 div 태그를 찾아서 categories_card 변수에 할당
        self.assertIn('Categories', categories_card.text)
        # assertIn() 메서드를 사용하여 'Categories'라는 문구가 categories_card.text에 포함되어 있는지 확인
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        # asertIn() 메서드를 사용하여 programming 카테고리의 이름과 포스트 개수가 categories_card.text에 포함되어 있는지 확인
        self.assertIn(f'{self.category_mugic.name} ({self.category_mugic.post_set.count()})', categories_card.text)
        # assertIn() 메서드를 사용하여 music 카테고리의 이름과 포스트 개수가 categories_card.text에 포함되어 있는지 확인
        self.assertIn(f'미분류 (1)', categories_card.text)
        # assertIn() 메서드를 사용하여 미분류 카테고리의 이름과 포스트 개수가 categories_card.text에 포함되어 있는지 확인
        
    def navbar_test(self, soup):
        # 1.4 내비게이션 바가 있다.
        navbar = soup.nav
        # 1.5 Blog, About Me라는 문구가 내비게이션 바에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        
        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        home_htn = navbar.find('a', text='Home')
        self.assertEqual(home_htn.attrs['href'], '/')
        
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')
        
    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3) # Post 객체가 3개인지 확인
        
        response = self.client.get('/blog/') # /blog/로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200) # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser') # BeautifulSoup 객체 생성
        
        self.navbar_test(soup) # navbar_text() 메서드를 사용하여 내비게이션 바가 있는지 확인
        self.category_card_test(soup) # category_card_test() 메서드를 사용하여 카테고리 카드가 있는지 확인
        
        main_area = soup.find('div', id='main-area') # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertNotIn("아직 게시물이 없습니다", main_area.text) # assertNoIn() 메서드를 사용하여 '아직 게시물이 없습니다'라는 문구가 main_area.text에 포함되어 있지 않은짛 ㅘㄱ인
        
        post_001_card = main_area.find('div', id='post-1') # id가 post=1인 div 태그를 찾아서 post_001_card 변수에 할당
        self.assertIn(self.post_001.title, post_001_card.text) # assertIn() 메서드를 사용하여 post_001.title이 post_001_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_001.category.name, post_001_card.text) # assertIn() 메서드를 사용하여 post_001.Category이 post_002_card.text에 포함되어 있는지 확인
        
        post_002_card = main_area.find('div', id='post-2') # id가 post-2인 div 태그를 찾아서 post_002_card 변수에 할당
        self.assertIn(self.post_002.title, post_002_card.text) # assertIn() 메서드를 사용하여 post_002.title이 post_002_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_002.category.name, post_002_card.text) # assertIn() 메서드를 사용하여 post_002.category.name이 post_002_card.text에 포함되어 있는지 확인
        
        post_003_card = main_area.find('div', id='post-3') # id가 post-3인 div 태그를 찾아서 post_003_card 변수에 할당
        self.assertIn('미분류', post_003_card.text) # assertIn() 메서드를 사용하여 '미분류'라는 문구가 post_003_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_003.title, post_003_card.text) # assertIn() 메서드를 사용하여 post_003.category.name이 post_003_card.text에 포함되어 있는지 확인
    
        self.assertIn(self.user_trump.username.upper(), main_area.text) # assertIn() 메서드를 사용하여 self.user_trump.username.upper()이 main_area.text에 포함되어 있는지 확인
        self.assertIn(self.user_biden.username.upper(), main_area.text) # assertIn() 메서드를 사용하여 self.user_biden.username.upper()이 main_area.text에 포함되어 있는지 확인
        
        # 포스트가 없는 경우   
        Post.objects.all().delete() # Post 객체를 모두 삭제
        self.assertEqual(Post.objects.count(), 0) # Post 객체가 0개인지 확인
        response = self.client.get('/blog/') # /blog/로 GET 요청을 보냄
        soup = BeautifulSoup(response.content, 'html.parser') # BeautifulSoup 객체 생성
        main_area = soup.find('div', id='main-area') # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn("아직 게시물이 없습니다", main_area.text) # assertIn() 메서드를 사용하여 '아직 게시물이 없습니다'라는 문구가 main_area.text에 포함되어 있는지 확인 

    def test_post_detail(self): 
        # 1. 첫 번쨰 포스트의 url이 '/blog/1/'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(status_code: 200).                                                                                                                                                                                   
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # assertEqual? 첫 번째 인자와 두 번째 인자가 같은지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        # html.parser? HTML 문서를 파싱하는 파서
        # 파싱? 문서를 읽어서 문법적인 오류를 찾고, 문서를 구조적으로 분석하는 것
        # BeautifulSoup 객체? 파싱된 문서를 다루기 위한 객체
        # response.content? 요청에 대한 응답의 본문
        
        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)
        # 2.2. 포스트 목록 페이지와 똑같은 카테고리 카드가 있다.
        self.category_card_test(soup)
        
        # 2.3. 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)
        # 2.4. 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)
        # assertIn? 첫 번째 인자가 두 번째 인자에 포함되어 있는지 확인
        
        # 2.5. 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)
        
        # 2.6. 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)