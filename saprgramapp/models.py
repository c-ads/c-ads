from django.db import models
from authentication.models import User


class Publication(models.Model):
    user_photo = models.ImageField(upload_to='photos/publications')  # Photo
    data = models.TextField(blank=True)  # Description under the photo
    date = models.DateTimeField(auto_now_add=True)  # Date of creation
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, default=None)

    class Meta:
        ordering = ['user']
        verbose_name = 'Publication'  # Change table name
        verbose_name_plural = 'Publications'

    def __str__(self):
        return str(self.user)


class Comments(models.Model):
    comment = models.TextField()  # Text of the comment
    # ID of the post that is commented by any user
    post = models.ForeignKey(Publication, on_delete=models.PROTECT, null=True, blank=True)
    # ID of user who made comments
    commenter = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['post']
        verbose_name = 'Comment'  # Change table name
        verbose_name_plural = 'Comments'
