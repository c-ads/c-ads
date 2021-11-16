from __future__ import unicode_literals
from django.db import models


class Users(models.Model):
    objects = None
    login = models.CharField(max_length=25)  # You can add verbose_name='...' to change tha name of column
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/avatar', blank=True)
    email = models.EmailField(max_length=40)
    cookies = models.TextField(default='')
    description = models.TextField(default='', blank=True)
    age = models.IntegerField(default='18', blank=True)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Користувач'  # Change table name
        verbose_name_plural = 'Користувачі'
        ordering = ['-login']  # Filter the table


# Use user ID to understand which post rely on which user
# Use ForeignKey connection between Users model and this
class Posts(models.Model):
    objects = None
    user_photos = models.ImageField(upload_to='photos/users')  # Photo
    data = models.TextField(blank=True)  # Description under the photo
    date = models.DateTimeField(auto_now_add=True)  # Date of creation
    user_id = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['user_id']
        verbose_name = 'Пост'  # Change table name
        verbose_name_plural = 'Пости'

    def __str__(self):
        return str(self.user_id)


# Use ID if the post to understand which comment rely on which post
# Use ForeignKey connection between Posts model and this
# Also using the id of commenter import the photo of commenter from Users model
class Comments(models.Model):
    objects = None
    comment = models.TextField()  # Text of the comment
    # ID of the post that is commented by any user
    post_id = models.ForeignKey(Posts, on_delete=models.PROTECT, null=True, blank=True)
    # ID of user who made comments
    commenter = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['post_id']
        verbose_name = 'Коментар'  # Change table name
        verbose_name_plural = 'Коментарі'
