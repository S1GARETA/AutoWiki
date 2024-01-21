from django.contrib import admin

from .models import ForumPost, ForumComment

# Register your models here.

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'comments_count', 'auto', 'section', 'user', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'user', 'created_at')
    readonly_fields = ('created_at',)
