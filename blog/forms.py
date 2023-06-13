from .models import Comment # models.py에서 Comment 모델을 가져옴
from django import forms # django의 forms를 가져옴

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # Comment 모델을 사용
        fields = ('content',) # content 필드만 사용
        # sxclude = ('post', 'author', 'created_at'm 'modified_at'. )
        # fields -> 사용할 필드를 지정
        # exclude -> 사용하지 않을 필드를 지정