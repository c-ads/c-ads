from django.contrib import admin
from .models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'email')  # columns that you can see in admin panel table
    search_fields = ('login', 'email')


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'date')  # columns that you can see in admin panel table
    search_fields = ('user_id', 'date')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'commenter')  # columns that you can see in admin panel table
    search_fields = ('post_id',)


# At first you need to register model and than class
admin.site.register(Users, UsersAdmin)  # Register model and class for changing
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments, CommentsAdmin)
# Register your models here.
