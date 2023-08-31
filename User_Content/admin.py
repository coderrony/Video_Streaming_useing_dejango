from django.contrib import admin
from .models import Category, UploadContent, Comment

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    # it's mean this slug field fill automatic when create  category_name
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ['category_name', 'slug']


admin.site.register(Category, CategoryAdmin)

admin.site.register(UploadContent)
admin.site.register(Comment)
