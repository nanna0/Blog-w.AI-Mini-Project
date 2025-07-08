from django.db import models
from account.models import User 


class Posts(models.Model):  # 대문자로 변경
    STATUS_CHOICES = [
        ('draft', '임시'),
        ('published', '공개'),
        ('private', '비공개'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['-created_at']


class Comment(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"

    class Meta:
        ordering = ['-created_at']


class Attachment(models.Model):
    posts = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return f"{self.file.name}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_like')
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 중복 좋아요 방지

    def __str__(self):
        return f"{self.user.username} ❤️ {self.post.title}"