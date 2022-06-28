from django.contrib import admin

from .models import (
    Author,
    Post,
    Tag,
    Category,
    Comment,
    PostView,

)


admin.site.register(Author)
admin.site.register(PostView)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
