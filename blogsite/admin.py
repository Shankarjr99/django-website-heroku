from django.contrib import admin
from .models import contact
from .models import post,Comment

# Register your models here.

admin.site.register(contact)
admin.site.register(post)
admin.site.register(Comment)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'body', 'post', 'created_on', 'active')
#     list_filter = ('active', 'created_on')
#     search_fields = ('name', 'email', 'body')
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)
