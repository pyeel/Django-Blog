from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Category(models.Model):
    # Category 모델 -> models 모듈의 Model 클래스를 확장해서 만든 파이썬 클래스
    name = models.CharField(max_length=50, unique=True)
    # name 필드 -> CharField 클래스(문자를 담는 필드)
    # max_length=50 -> 최대 길이 50
    # unique=True -> 중복되는 값을 허용하지 않음, 동일한 이름의 카테고리를 만들 수 없음
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # slug 필드
    # - > SlugField 클래스(문자열을 URL에 사용 할 수 있는 형태로 변환해주는 필드)
    # -> 사람이 읽을 수 있는 텍스트로 고유 URL을 만들어주는 필드
    # -> Post 모델처럼 pk를 활용해 URL을 만들 수도 있지만, 카테고리는 포스트만큼 개수가 많지 않음
    #   그래서 카테고리의 이름을 URL에 사용
    # allow_unicode=True -> 한글을 slug로 변환할 수 있도록 설정
    # max_length=200 -> 최대 길이 200
    # unique=True -> 중복디ㅗ는 값을 허용하고 다른 카테고리가 동일한 slug를 가질 수 없음
    
    def __str__(self):
        # __str__ -> 클래스 자체의 내용을 출력하고 싶을 때 형식을 지정하는 메서드
        return self.name
        # name 필드의 값을 출력
        
    class Meta:
        verbose_name_plural = 'categories'

class Post(models.Model):
    # Post 모델 -> models 모듈의 Model 클래스를 확장해서 만든 파이썬 클래스
    title = models.CharField(max_length=30)
    # title 필드 -> CharField클래스(문자를 담는 필드), 최대 길이 30
    hook_text = models.CharField(max_length=100, blank=True)
    # hook_text 필드가 비어 있지 않을 떄는 hook_text 필드 값을 보여주도록 설정
    # CharField -> max_length = 100 -> hook_text 글자수 100자로 제한
    content = models.TextField()
    # content 필드 -> 문자열의 길이 제한이 없는 TextField를 사용
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # image 필드로 head_image 추가
    # upload_to -> 이미지를 저장할 폴더의 경로 규칙 지정
    # blog 폴더 아래 images폴더를 만들고, 연도폴더, 월폴더, 일폴더까지 내려간 위치에 저장되도록 설정
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    # file 필드로 file_upload 추가
    # upload_to -> 파일을 저장할 폴더의 경로 규칙 지정
    # blog폴더 아래 files폴더를 만들고, 연도폴더, 월폴더, 일폴더까지 내려간 위치에 저장되도록 설정
    created_at = models.DateTimeField(auto_now_add=True)
    # created_at 필드 -> 처음 레코드가 생성될 때
    # DateTimeField -> 월, 일, 시, 분, 초까지 기록할 수 있게 해주는 필드를 만들 때 사용
    # auto_now_add=True -> 현재 시각이 자동으로 저장됨.
    updated_at = models.DateTimeField(auto_now=True)
    # updated_at 필드 -> 다시 저장할 때
    # DateTImeField -> 월, 일, 시, 분, 초까지 기록 할 수 있게 해주는 필드를 만들 때 사용
    # auto_now=True -> 그 시점의 시각이 저장됨
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # author 필드 -> ForeignKey 클래스(다른 모델과의 연결을 의미하는 필드)
    # on_delete=models.SET_NULL -> 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트의 작성자명을 빈칸으로 설정(NULL로 설정)
    # on_delete=models.CASCADE -> 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트도 삭제되도록 설정
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # category 필드 -> ForeignKey 클래스 (다른 모델과의 연결을 의미하는 필드)
    # on_delete=models.SET_NULL -> 이 포스트의 카테고리가 데이터베이스에서 삭제되었을 때 이 포스트의 카테고리명을 빈칸으로 설정(NULL로 설정)
    # null=True -> category 필드가 비어 있어도 된다는 의미
    # blank=True -> category 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용
    # null=True, balnk=True 둘 다 지정하면 어떤 조건이든 값을 비워둘 수 있음.
    
    def __str__(self):
        # __stt__ -> 클래스 자체의 내용을 출력하고 싶을 때 형식을 지정하는 메서드
        return f'[{self.pk}]{self.title} :: {self.author}'
        # 장고의 모델을 만들면 기본적으로 pk필드 생성됨
        # pk -> 각 레코드에 대한 고유값
        # 첫번째 포스트 pk값 -> 1, 두번째 포스트 pk 값 -> 2
        # f-string 포맷 -> f'문자열 {변수} 문자열'
        # [{self.pk}]{self.title} -> [포스트 번호] 포스트 제목
        # :: {self.author} -> :: 포스트 목록에서 작성자 정보까지 출력
        
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    # f-string 포맷 -> f'문자열 {변수} 문자열'
    # /blog/{self.pk}/ -> /blog/포스트 번호/
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
        # 파일 경로를 제외하고 파일명만 출력
        
        
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]    
        # .의 위치를 이용해 확장자 찾기