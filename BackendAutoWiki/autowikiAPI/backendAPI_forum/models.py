from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from backendAPI_user.models import CustomUser
from backendAPI_auto.models import Auto, Instruction, Section

# Create your models here.

class ForumPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок поста")
    content = models.TextField(verbose_name="Содержание поста")
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, null=True, blank=True)
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comments_count = models.PositiveIntegerField(default=0, verbose_name="Ответов")

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Содержание комментария")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

@receiver(post_save, sender=ForumComment)
def update_comments_count(sender, instance, created, **kwargs):
    if created:
        instance.post.comments_count = instance.post.comments.count()
        instance.post.save()