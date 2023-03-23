from django.db import models

# Create your models here.
class Post(models.Model):
    # Post 모델 -> models 모듈의 Model 클래스를 확장해서 만든 파이썬 클래스
    title = models.CharField(max_length=30)
    # title 필드 -> CharField클래스(문자를 담는 필드), 최대 길이 30
    content = models.TextField()
    # content 필드 -> 문자열의 길이 제한이 없는 TextField를 사용
    created_at = models.DateTimeField(auto_now_add=True)
    # created_at 필드 -> 처음 레코드가 생성 될 때
    # DateTImeField -> 월, 일, 시, 분, 초까지 기록 할 수 있게 해주는 필드를 만들 때 사용
    # auto_now_add=True -> 현재 시각이 자동으로 저장됨
    updated_at = models.DateTimeField(auto_now=True)
    # updated_at 필드 -> 다시 저장할 때
    # DateTImeField -> 월, 일, 시, 분, 초까지 기록 할 수 있게 해주는 필드를 만들 때 사용
    # auto_now=True -> 그 시점의 시각이 저장됨
    
    def __str__(self):
        return f'[{self.pk}]{self.title}'
        # 장고의 모델을 만들면 기본적으로 pk필드 생성됨
        # pk -> 각 레코드에 대한 고유값
        # 첫번째 포스트 pk값 -> 1, 두번째 포스트 pk 값 -> 2
        # f-string 포맷 -> f'문자열 {변수} 문자열'
        # [{self.pk}]{self.title} -> [포스트 번호] 포스트 제목