from django.contrib import admin

from .models import Author, Comment, Post, Tag


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    prepopulated_fields = {
        "slug" : ("title", ),
    }
    list_filter = ('author', 'tags',)
    list_display = ('title', 'author', 'date',)

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
