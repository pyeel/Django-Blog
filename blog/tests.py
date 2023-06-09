from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment

# Create your tests here.
class TestView(TestCase): #TestCase 클래스를 상속받는 'TestView' 클래스 생성
    def setUp(self): # TestCase의 초기 데이터베이스 상태를 정의하는 메서드
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        # username이 'trump' 이고 password가 'somepassword' 인 User 객체 생성
        self.user_biden = User.objects.create_user(username='biden', password='somepassword')
        # username이 'trump' 이고 password가 'somepassword' 인 User 객체 생성
        self.user_biden.is_staff = True
        # user_biden의 is_staff 속성을 True로 변경
        # biden에게 스태프 권한 부여 / trump는 일반 사용자로 지정
        self.user_biden.save() # 변경사항을 저장
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        # programming 카테고리 생성
        self.category_music = Category.objects.create(name='music', slug='music')
        # music 카테고리 생성
        
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        # name이 '파이썬 공부'이고 slug가 '파이썬-공부'인 Tag 객체 생성
        self.tag_python = Tag.objects.create(name='python', slug='python')
        # name이 'python'이고 slug가 'python'인 Tag 객체 생성
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')
        # name이 'hello'이고 slug가 'hello'인 Tag 객체 생성
        
        self.post_001 = Post.objects.create(
            title='첫 번쨰 포스트입니다.',
            content='Hello World. We are the world.',
            category = self.category_programming, # programming 카테고리를 지정
            author = self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello) # post_001에 tag_hello를 추가
        
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category = self.category_music, # music 카테고리를 지정
            author = self.user_biden,
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category가 없을 수도 있죠.',
            author = self.user_biden,
        )
        self.post_003.tags.add(self.tag_python_kor) # post_003에 tag_python_kor를 추가
        self.post_003.tags.add(self.tag_python) # post_003에 tag_python을 추가
         
        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_biden,
            content='첫 번째 댓글입니다. '
        )
    
    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        # self.tag_hello.get_absolute_url() 메서드를 사용하여 tag_hello의 절대 경로를 가져옴
        self.assertEqual(response.status_code, 200) # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser') # BeautifulSoup 객체 생성
        
        # 다른 함수에서 사용한 함수를 재활용, self.navber_test(), self.category_card_test()
        self.navbar_test(soup) # navbar_test() 메서드를 사용하여 내비게이션 바가 있는지 확인
        self.category_card_test(soup) # category_card_test() 메서드를 사용하여 카테고리 카드가 있는지 확인
        
        self.assertIn(self.tag_hello.name, soup.h1.text) # tag_hello의 name이 h1 태그의 text에 포함되어 있는지 확인
        
        main_area = soup.find('div', id='main-area') # id가 main_area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn(self.tag_hello.name, main_area.text) # tag_hello의 name이 main_area.text에 포함되어 있는지 확인
        self.assertIn(self.post_001.title, main_area.text) # post_001의 title이 main_area.text에 포함되어 있는지 확인
        self.assertNotIn(self.post_002.title, main_area.text) # post_002의 title이 main_area.text에 포함되어 있지 않은지 확인
        self.assertNotIn(self.post_003.title, main_area.text) # post_003의 title이 main_area.text에 포함되어 있지 않은지 확인
        
    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        # self.category_programming.get_absolute_url() 메서드를 사용하여 programming 카테고리의 절대 경로를 가져옴
        # self.client.get() 메서드를 사용하여 programming 카테고리의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200) # status_code가 200인지 확인
        
        soup = BeautifulSoup(response.content, 'html.parser') # BeautifulSoup 객체 생성
        # html.parser를 사용하여 response.content를 파싱
        # parser는 html 문서를 파싱하는 방법을 의미
        # 파싱이란 문서를 읽어서 문법적인 오류를 찾고, 문서의 구조를 분석하는 것을 의미
        self.navbar_test(soup) # navber_test() 메서드를 사용하여 내비게이션 바가 있는지 확인
        self.category_card_test(soup) # category_card_test() 메서드를 사용하여 카테고리 카드가 있는지 확인
        
        self.assertIn(self.category_programming.name, soup.find('h1').text)
        # assertIn() 메서드를 사용하여 programming 카테고리의 이름이 h1 태그의 text에 포함되어 있는지 확인
        # assertIn() 메서드는 첫 번째 인자에 있는 값이 두 번째 인자에 있는 값에 포함되어 있는지 확인
        
        main_area = soup.find('div', id='main-area') # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn(self.category_programming.name, main_area.text)
        # assertIn() 메서드를 사용하여 programming 카테고리의 이름이 main_area.text에 포함되어 있는지 확인하고, 이 카테고리에 해당하는 포스트만 노출되어 있는지 확인
        self.assertIn(self.post_001.title, main_area.text)
        # assertIn() 메서드를 사용하여 post_001의 title이 main_area.text에 포함되어 있는지 확인
        self.assertNotIn(self.post_002.title, main_area.text)
        # assertNoIn() 메서드를 사용하여 post_002의 title이 main_area.text에 포함되어 있지 않은지 확인 -> 메인 영역에 존재해서는 안됨.
        self.assertNotIn(self.post_003.title, main_area.text)
        # assertNoIn() 메서드를 사용하여 post_003의 title이 main_area.text에 포함되어 있지 않은지 확인 -> 메인 영역에 존재해서는 안됨.
        
    def category_card_test(self, soup): # 카테고리 카드를 테스트하는 메서드
        categories_card = soup.find('div', id='categories-card')
        # id가 categorues-card인 div 태그를 찾아서 categories_card 변수에 할당
        self.assertIn('Categories', categories_card.text)
        # assertIn() 메서드를 사용하여 'Categories'라는 문구가 categories_card.text에 포함되어 있는지 확인
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        # asertIn() 메서드를 사용하여 programming 카테고리의 이름과 포스트 개수가 categories_card.text에 포함되어 있는지 확인
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
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
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text) # assertIn() 메서드를 사용하여 post_001.author.username(대문자로 변경)이 post_001_card.text에 포함되어 있는지 확인
        self.assertIn(self.tag_hello.name, post_001_card.text) # tag_hello.name이 post_001_card.text에 포함되어 있는지 확인
        self.assertNotIn(self.tag_python.name, post_001_card.text) # tag_python.name이 post_001_card.text에 포함되어 있지 않은지 확인
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text) # tag_python_kor.name이 post_001_card.text에 포함되어 있지 않은지 확인
        
        post_002_card = main_area.find('div', id='post-2') # id가 post-2인 div 태그를 찾아서 post_002_card 변수에 할당
        self.assertIn(self.post_002.title, post_002_card.text) # assertIn() 메서드를 사용하여 post_002.title이 post_002_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_002.category.name, post_002_card.text) # assertIn() 메서드를 사용하여 post_002.category.name이 post_002_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text) # assertIn() 메서드를 사용하여 post_002.author.username(대문자로 변경)이 post_001_card.text에 포함되어 있는지 확인
        self.assertNotIn(self.tag_hello.name, post_002_card.text) # tag_hello.name이 post_002_card.text에 포함되어 있는지 확인
        self.assertNotIn(self.tag_python.name, post_002_card.text) # tag_python.name이 post_002_card.text에 포함되어 있지 않은지 확인
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text) # tag_python_kor.name이 post_002_card.text에 포함되어 있지 않은지 확인
        
        post_003_card = main_area.find('div', id='post-3') # id가 post-3인 div 태그를 찾아서 post_003_card 변수에 할당
        self.assertIn('미분류', post_003_card.text) # assertIn() 메서드를 사용하여 '미분류'라는 문구가 post_003_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_003.title, post_003_card.text) # assertIn() 메서드를 사용하여 post_003.category.name이 post_003_card.text에 포함되어 있는지 확인
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text) # assertIn() 메서드를 사용하여 post_003.author.username(대문자로 변경)이 post_001_card.text에 포함되어 있는지 확인
        self.assertNotIn(self.tag_hello.name, post_003_card.text) # tag_hello.name이 post_003_card.text에 포함되어 있는지 확인
        self.assertIn(self.tag_python.name, post_003_card.text) # tag_python.name이 post_003_card.text에 포함되어 있지 않은지 확인
        self.assertIn(self.tag_python_kor.name, post_003_card.text) # tag_python_kor.name이 post_003_card.text에 포함되어 있지 않은지 확인
        
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
        
        self.assertIn(self.tag_hello.name, post_area.text) # tag_hello.name이 post_area.text에 포함되어 있는지 확인
        self.assertNotIn(self.tag_python.name, post_area.text) # tag_python.name이 post_area.text에 포함되어 있지 않은지 확인
        self.assertNotIn(self.tag_python_kor.name, post_area.text) # tag_python_kor.name이 post_area.text에 포함되어 있지 않은지 확인
    
        # comment area
        comments_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 domments_area 변수에 할당
        comment_001_area = comments_area.find('div', id='comment-1')
        # id가 comment-1인 div 태그를 찾아서 comment_001_area 변수에 할당
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        # comment_001의 author.username이 comment_001_area.text에 포함되어 있는지 확인
        self.assertIn(self.comment_001.content, comment_001_area.text)
        # comment_001의 content가 comment_001_area.text에 포함되어 있는지 확인
        
    def test_create_post(self):
        # 로그인하지 않으면 status code가 200이면 안된다.
        response = self.client.get('/blog/create_post/')
        # '/blog/create_post/'로 GET 요청을 보냄
        self.assertNotEqual(response.status_code, 200)
        # assertEqual? 첫 번째의 인자와 두 번째 인자가 같은지 확인
        
        # staff가 아닌 trump가 로그인을 한다.
        self.client.login(username='trump', password='somepassword')
        # username이 trump이고 password가 somepassword인 사용자로 로그인
        response = self.client.get('/blog/create_post/')
        # '/blog/create_post/'로 GET 요청을 보냄
        self.assertNotEqual(response.status_code, 200)
        # trump는 staff가 아니므로 status_code가 200이 아니어야 함.
        
        # staff인 biden으로 로그인한다.
        self.client.login(username='biden', password='somepassword')
        # username이 biden이고 password가 somepassword인 사용자로 로그인
        response = self.client.get('/blog/create_post/')
        # '/blog/create_post/'로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # assertEqual? 첫 번째의 인자와 두 번째 인자가 같은지 확인
        # status_code? 응답의 상대 코드
        # 200? 요청이 성공적으로 되었음을 의미
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        self.assertEqual('Create Post - Blog', soup.title.text)
        # 웹 브라우저의 타이틀은 'Create Post - Blog'로 되어 있어야 함.
        main_area = soup.find('div', id='main-area')
        # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn('Create New Post', main_area.text)
        # 메인 영역에는 'Create New Post'라는 문구가 있어야 함.
        
        tag_str_input = main_area.find('input', id='id_tags_str')
        # id가 id_tags_str인 input 태그를 찾아서 tag_str_input 변수에 할당
        self.assertTrue(tag_str_input)
        # tag_str_input이 존재하는지 확인
        
        self.client.post( # '/blog/create_post/'로 POST 요청을 보냄
            '/blog/create_post/',
            {
                'title': "Post Form 만들기",
                'content': "Post Form 페이지를 만듭시다.",
                'tags_str': 'new tag; 한글 태그, python'
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        # Post 객체가 4개인지 확인
        last_post = Post.objects.last()
        # Post 객체 중 가장 마지막 객체를 last_post 변수에 할당
        self.assertEqual(last_post.title, "Post Form 만들기")
        # last_post의 title이 'Post Form 만들기'인지 확인
        self.assertEqual(last_post.author.username, 'biden')
        # last_post의 author의 username이 biden인지 확인
        
        self.assertEqual(last_post.tags.count(), 3)
        # last_post의 tags의 개수가 3개인지 확인
        self.assertTrue(Tag.objects.get(name='new tag'))
        # name이 'new tag'인 Tag 객체가 존재하는지 확인
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        # name이 '한글 태그'인 Tag 객체가 존재하는지 확인
        self.assertEqual(Tag.objects.count(), 5)
        # Tag 객체가 5개인지 확인
        
    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'
        # 수정할 포스트는 setUp()함수에서 미리 만들어둔 self.post_003
        # 포스트 수정 페이지의 URL형태는 '/blog/update_post/포스트의 pk/'
        
        # 로그인하지 않는 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)
        # 기존 포스트 작성자(biden)만 접근 가능해야 함.
        # 로그인을 하지 않는 경우 status code가 200이 아니어야 함.
        
        # 로그인을 했지만 작성자(biden)가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        # 방문자가 로그인하긴 했지만 포스트 작성자가 아닌 사람이 접근하면 권한이 없음을 나타내는 403 오류가 발생하는지 테스트
        
        # 작성자(biden)가 접근하는 경우
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # htnl.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        self.assertEqual('Edit Post - Blog', soup.title.text) # 웹 브라우저의 타이틀은 'Edit Post - Blog'로 되어 있어야 함,
        main_area = soup.find('div', id='main-area') # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn('Edit Post', main_area.text) # 메인 영역에는 'Edit Post'라는 문구가 있어야 함.
        
        tag_str_input = main_area.find('input', id='id_tags_str') # id가 id_tags_str인 input 태그를 찾아서 tag_str_input 변수에 할당
        self.assertTrue(tag_str_input) # tag_str_input()이 존재하는지 확인
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])
        # tag_str_input의 value 속성에 '파이썬 공부; python'이 포함되어 있는지 확인
        
        
        # 위의 3개 코드가 확인되면 title, content, category를 모두 다음과 같이 수정한 다음 POST 방식으로 update_post_url에 전송
        response = self.client.post(
            update_post_url,
            {
                'title': '세 번째 포스트를 수정했습니다.',
                'content': '안녕 세계? 우리는 하나!',
                'category': self.category_music.pk,
                # 외래키(ForeignKey)인 category는 category_music의 pk를 명시하여 전송
                'tags_str': '파이썬 공부; 한글 태그, some tag'
            },
            follow=True
            # follow=True 옵션을 사용하면 POST 요청에 대한 응답을 받은 후에 자동으로 GET 요청을 보냄
        )
        soup =  BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        main_area = soup.find('div', id='main-area')
        # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        # main_area에 '세 번째 포스트를 수정했습니다.'라는 문구가 있는지 확인
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        # main_area에 '안녕 세계? 우리는 하나!'라는 문구가 있는지 확인
        self.assertIn(self.category_music.name, main_area.text)
        # main_area에 category_music의 name이 있는지 확인
        self.assertIn('파이썬 공부', main_area.text)
        # main_area에 '파이썬 공부'라는 문구가 있는지 확인
        self.assertIn('한글 태그', main_area.text)
        # main_area에 '한글 태그'라는 문구가 있는지 확인
        self.assertIn('some tag', main_area.text)
        # main_area에 'some tag'라는 문구가 있는지 확인
        self.assertNotIn('python', main_area.text)
        # main_area에 'python'라는 문구가 없는지 확인
        
    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        # setUp() 함수에 이미 댓글이 하나 있는 상태에서 시작 -> Comment 객체가 1개인지 확인
        self.assertEqual(self.post_001.comment_set.count(), 1)
        # 이 댓글을 self.post_001에 달려 있는 댓글 -> post_001의 comment_set의 개수가 1개인지 확인
        
        # 로그인하지 않은 상태
        
        response = self.client.get(self.post_001.get_absolute_url())
        # post_001이 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확이
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        self.assertIn('Log in and leave a comment', comment_area.text)
        # 로그인하지 않은 상태 -> comment_area에서 'Log in and leave a comment'라는 문구가 있는지 확인
        self.assertFalse(comment_area.find('form', id='comment-form'))
        # 로그인하지 않은 상태 -> comment_area에 id가 comment-form인 form 태그가 없는지 확인
        
        # 로그인한 상태
        
        self.client.login(username='biden', password='somepassword')
        # username이 biden이고 password가 somepassword인 사용자로 로그인
        response = self.client.get(self.post_001.get_absolute_url())
        # post_001의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        self.assertNotIn('Log in and leave a comment', comment_area.text)
        # 로그인한 상태 -> comment_area에 'Log in and leave a comment'라는 문구가 없는지 확인
        
        comment_form = comment_area.find('form', id='comment-form')
        # id가 comment-form인 form 태그를 찾아서 comment-form 변수에 할당
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        # comment_form에 id가 id_content인 textarea 태그가 있는지 확인
        response = self.client.post(
            # POST 방식으로 댓글 내용을 서버에 전송하고, 그 요청 결과를 response에 담음.
            self.post_001.get_absolute_url() + 'new_comment/',
            # post_001의 절대 경로에 'new_comment/'를 추가
            {
                'content': "바이든의 댓글입니다.",
            },
            follow=True
            # follow=True 옵션을 사용하면 POST 요청에 대한 응답을 받은 후에 자동으로 GET 요청을 보냄
        )
        
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인

        self.assertEqual(Comment.objects.count(), 2)
        # 댓글이 원래 1개였는데 response = self.client.post() 부분에서 추가됨 -> Comment 객체가 2개인지 확인
        self.assertEqual(self.post_001.comment_set.count(), 2)
        # self.post_001에는 댓글이 1개였음 -> post_001의 comment_set의 개수가 2개인지
        new_comment = Comment.objects.last()
        # 마지막으로 생성된 comment를 가져옴 -> Comment 객체 중 가장 마지막 객체를 new_comment 변수에 할당
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        self.assertIn(new_comment.post.title, soup.title.text)
        # POST방식으로 서버에 요청해 comment가 달린 포스트의 상세 페이지가 리다이렉트됨.
        # -> new_comment의 post의 title이 웹 브라우저 탭 타이틀에 나타남
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        # id가 comment-{new_comment.pk}인 div 태그를 찾아서 new_comment_div 변수에 할당
        self.assertIn('biden', new_comment_div.text)
        # 새로 만든 comment의 내용과 작성자가 나타남 -> new_commnt_div에 biden이라는 문구가 있는지 확인
        self.assertIn('바이든의 댓글입니다.', new_comment_div.text)
        # new_comment_div에 '바이든의 댓글입니다.'라는 문구가 있는지 확인
        
    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            # 다른 사람이 작성한 댓글이 있어야 함 -> Comment 객체를 생성하고 comment_by_trump 변수에 할당
            post = self.post_001, # post_001에 달린 댓글이므로 post_001을 할당
            author = self.user_trump, # user_trump이 작성한 댓글이므로 user_trump를 할당
            content = '트럼프의 댓글입니다.'
        )
        response = self.client.get(self.post_001.get_absolute_url())
        # 로그인하지 않은 상태에서 댓글이 2개 있는 self.post_001 페이지를 열어봄
        # -> post_001의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment_area인 div 태그를 찾아서 comment_area 변수에 할당
        # 댓글 영역에 수정 버튼이 둘 다 보이지 않아야 하므로
        # 수정 버튼의 id는 comment-해당 comment의 pk-update-btn 형식으로 만들어짐
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        # 로그인하지 않은 상태 -> 수정 버튼이 보이지 않아야 함
        # comment_area에 id가 comment-1-update-btn인 a 태그가 없는지 확인
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        # comment_area에 id가 comment-2-update-btn인 a 태그가 없는지 확인
        
        # 로그인한 상태
        self.client.login(username='biden', password='somepassword')
        # biden으로 로그인
        response = self.client.get(self.post_001.get_absolute_url())
        # post_001의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만ㄷ름
        
        comment_area = soup.find('div', id='comment-area')
        # 바이든으로 로그인했으므로, 트럼프가 작성한 댓글에 대한 수정 버튼은 보이지 않아야 함.
        # 바이든이 작성한 self.comment_001에 대한 수정버튼은 나타나야 함.(수정버튼 -> edit 표시)
        # 수정 버튼에 있는 href속성(링그 경로) -> blog/update_comment/해당 comment의 pk/
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        # comment_area에 id가 comment-2-update-btn인 a 태그가 없는지 확인
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        # comment_area에 id가 comment-1-update-btn인 a 태그를 찾아서 comment_001_update_btn 변수에 할당
        self.assertIn('edit', comment_001_update_btn.text)
        # comment_001_update_btn에 'edit'라는 문구가 있는지 확인
        self.assertEqual(comment_001_update_btn['href'], f'/blog/update_comment/1/')
        # comment_001_update_btn의 href 속성이 '/blog/update_comment/1/'인지 확인
        
        self.assertIn('edit', comment_001_update_btn.text)
        # comment_001_update_btn에 'edit'라는 문구가 있는지 확인
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        # comment_001_update_btn의 href 속성이 '/blog/update_comment/1/'인지 확인
        
        response = self.client.get('/blog/update_comment/1/')
        # <edit>버튼을 클릭하면 댓글을 수정하는 폼이 있는 페이지로 넘어감
        # -> '/blog/update_comment/1/'로 GET 요청을 본냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        self.assertEqual('Edit Comment - Blog', soup.title.text)
        # 웹 브라우저의 타이틀은 'Edit Comment - Blog'로 되어 있어야 함.
        update_comment_form = soup.find('form', id='comment-form')
        # id가 update-comment-form인 form 태그를 찾아서 comment_form 변수에 할당
        content_textarea = update_comment_form.find('textarea', id='id_content')
        # id가 id_content인 textarea태그를 찾아서 content_textarea 변수에 할당
        self.assertIn(self.comment_001.content, content_textarea.text)
        # 폼 안에는 id="id_content"인 textarea가 있어야 하고, 그 안에는 수정하기 전의 comment내용이 담겨 있어야 함.
        # content_textarea에 self.comment_001의 content가 있는지 확인
        
        response = self.client.post(
            # 이 폼의 content내용을 수정하고 <submit>버튼을 클릭하면 해당 댓글이 수정됨.
            # 이 부분을 self.client.post로 구현
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': '바이든의 댓글을 수정합니다.'
            },
            follow=True
            # POST 방식으로 서버에 내용을 보내는 방식으로 요청
            # CommentUpdate 클래스에서 내용이 처리된 후 해당 comment 의 절대 겨올로 리다이렉트됨.
        )
        
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만ㄷ름
        comment_001_div = soup.find('div', id='comment-1')
        # id가 comment-1인 div 태그를 찾아서 comment_001_div 변수에 할당
        self.assertIn('바이든의 댓글을 수정합니다', comment_001_div.text)
        # comment_001_div에 '바이든의 댓글을 수정합니다'라는 문구가 있는지 확인
        self.assertIn('Updated: ', comment_001_div.text)
        # 수정된 댓글은 수정된 내용으로 변경되어 있어야 하고,
        # 수정되었을 때는 댓글에 'Updated: '라는 문구가 추가되어 있어야 함.
        # comment_001_div에 'Updated: '라는 문구가 있는지 확인
        
    def test_delete_comment(self):
        comment_by_trump = Comment.objects.create( # 트럼프라는 이름으로 댓글 작성
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.',
        )
        # 이미 setUp() 함수에서 self.post_001에 바이든이라는 이름을 댓글을 작성해 두었음. -> 총 2개의 댓글이 있음.
                
        self.assertEqual(Comment.objects.count(), 2)
        # Comment 객체가 2개 있는지 확인
        self.assertEqual(self.post_001.comment_set.count(), 2)
        # self.post_001의 댓글은 2개이므로, self.post_001.comment_set.count()는 2가 되어야 함.
        
        # 로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        # post_001의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        # comment_area에 id가 comment-1-delete-btn인 a 태그가 없는지 확인
        self.assertFalse(comment_area.find('a', id='comment-2-delete-btn'))
        # comment_area에 id가 comment-2-delete-btn인 a 태그가 없는지 확인
                
        # 트럼프(trump)로 로그인한 상태
        self.client.login(username='trump', password='somepassword')
        # 트럼프로 로그인
        response = self.client.get(self.post_001.get_absolute_url())
        # post_001의 절대 경로로 GET 요청을 보냄
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        # 트럼프로 로그인했기 때문에 댓글영역(comment-area)에는 바이든이 작성한 self.comment_001에 대한 <delete>버튼은 없어야 함.
        # 반면, pk=2인 댓글(트럼프 작성)에는 <delete>버튼이 있어야 함.
        # 이 버튼은 곧바로 지우는 버튼이 아니라 정말로 지울 것인지 한 번 더 물어보는 모달을 나타내기 위한 버튼임.
        
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        # comment_area에 id가 comment-1-delete-btn인 a 태그가 없는지 확인
        comment_002_delete_modal_btn = comment_area.find(
            'a', id='comment-2-delete-modal-btn'
        ) # comment_area에 id가 comment-2-delete-modal-btn인 a 태그를 찾아서 comment_002_delete_modal_btn 변수에 할당        
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        # comment_002_delete_modal_btn에 'delete'라는 문구가 있는지 확인
        self.assertEqual(
            comment_002_delete_modal_btn['data-target'],
            '#deleteCommentModal-2'
        ) # comment_002_delete_modal_btn의 data-target 속성값이 '#deleteCommentModal-2'인지 확인
        
        # 삭제를 할지 재차 물어보는 모달에는 'Are You Sure?'라는 문구와 함께 <delete>버튼이 있어야 함.
        # 이 버튼의 링크는 '/blog/delete_comment/삭제할 comment의 pk/'로 되어 있어야 함.
        
        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        # id가 deleteCommentModal-2인 div 태그를 찾아서 delete_comment_modal_002 변수에 할당
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        # delete_comment_modal_002에 'Are You Sure?'라는 문구가 있는지 확인
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        # delete_comment_modal_002에 a 태그를 찾아서 really_delete_btn_002 변수에 할당
        self.assertIn('Delete', really_delete_btn_002.text)
        # really_delete_btn_002에 'Delete'라는 문구가 있는지 확인
        self.assertEqual(
            really_delete_btn_002['href'],
            '/blog/delete_comment/2/'
        ) # really_delete_btn_002의 href 속성값이 '/blog/delete_comment/2/'인지 확인
        
        # 실제로 <delete>버튼을 클릭하면 댓글이 삭제되고 self.post_001의 페이지로 리다이렉트 됨.
        # 이 페이지에는 더 이상 트럼프가 작성한 댓글이 존재하지 않고, 댓글의 개수도 1로 줄어드는 것을 확인할 수 있음.
        
        response = self.client.get('/blog/delete_comment/2/', follow=True)
        # '/blog/delete_comment/2/'로 GET 요청을 보냄. follow=True 옵션을 주어서 리다이렉트된 페이지를 받아옴.
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        self.assertIn(self.post_001.title, soup.title.text)
        # soup.title.text에 self.post_001.title이 있는지 확인
        comment_area = soup.find('div', id='comment-area')
        # id가 comment-area인 div 태그를 찾아서 comment_area 변수에 할당
        self.assertNotIn('트럼프의 댓글입니다.', comment_area.text)
        # comment_area에 '트럼프의 댓글입니다.'라는 문구가 없는지 확인
        
        self.assertEqual(Comment.objects.count(), 1)
        # Comment.objects.count()가 1인지 확인
        self.assertEqual(self.post_001.comment_set.count(), 1)
        # self.post_001.comment_set.count()가 1인지 확인
        
    def test_search(self):
        post_about_python = Post.objects.create(
            # Post 객체를 생성하고 post_about_python 변수에 할당
            title = '파이썬에 대한 포스트입니다.',
            content = 'Hello World. We are the world.',
            author = self.user_trump
        )
        
        response = self.client.get('/blog/search/파이썬/')
        # '/blog/search/파이썬/'으로 GET 요청을 보냄
        # 검색어를 서버에 전달하는 URL을 '/blog/search/검색어/'로 설정
        self.assertEqual(response.status_code, 200)
        # status_code가 200인지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # html.parser를 사용하여 response.content를 BeautifulSoup 객체로 만듦
        
        main_area = soup.find('div', id='main-area')
        # id가 main-area인 div 태그를 찾아서 main_area 변수에 할당
        
        self.assertIn('Search: 파이썬 (2)', main_area.text)
        # main_area에 'Search: 파이썬 (2)'라는 문구가 있는지 확인
        # (2)는 검색 결과에 해당하는 포스트가 총 2개라는 의미
        self.assertNotIn(self.post_001.title, main_area.text)
        # main_area에 self.post_001.title이 없는지 확인
        # title, tags에 모두 '파이썬'이 포함되어있지 않음 -> 검색 결과에 나와서는 안됨
        self.assertNotIn(self.post_002.title, main_area.text)
        # main_area에 self.post_002.title이 없는지 확인
        # title, tags에 모두 '파이썬'이 포함되어있지 않음 -> 검색 결과에 나와서는 안됨
        self.assertIn(self.post_003.title, main_area.text)
        # main_area에 self.post_003.title이 있는지 확인
        # title에 '파이썬'이 포함되어있지 않으나 tags에 '파이썬 공부'인 태그가 있음 -> 검색 결과에 나와야 함
        self.assertIn(post_about_python.title, main_area.text)
        # main_area에 post_about_python.title이 있는지 확인