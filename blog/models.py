from django.db import models

# Create your models here.
class Post(models.Model):
    # Post 모델 -> models 모듈의 Model 클래스를 확장해서 만든 파이썬 클래스
    title = models.CharField(max_length=30)
    # title 필드 -> CharField클래스(문자를 담는 필드), 최대 길이 30
    content = models.TextField()
    # content 필드 -> 문자열의 길이 제한이 없는 TextField를 사용
    created_ad = models.DateTimeField()
    # created_at 필드 -> DateTimeField는 월, 일, 시, 분, 초까지 기록 할 수 있게 해주는 필드를 만들 때 사용
    # author : 추후 작성 예정