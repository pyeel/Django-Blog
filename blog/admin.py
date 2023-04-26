from django.contrib import admin
from .models import Post, Category

# Register your models here.
admin.site.register(Post)
# 관리자 페이지에 Post 모델 등록

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    # Category 모델의 name필드에 값이 입력되었을 때 자동으로 slug필드에 값이 입력되도록 함
    # slug 필드는 URL에서 사용되는 필드이므로 name필드의 값이 변경되면 slug필드의 값도 변경되어야 함
    # prepopulated_fields 옵션을 사용하면 name필드의 값이 변경되면 slug필드의 값도 자동으로 변경됨
    
admin.site.register(Category, CategoryAdmin)
# CategoryAdmin 클래스를 사용하여 Category 모델을 관리자 페이지에 등록