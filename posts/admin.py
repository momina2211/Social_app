from django.contrib import admin
from posts.models import Tag,Post,Comment,Notification,Vote
# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Vote)

