from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin


@admin.register(models.Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    prepopulated_fields = {'slug': ('name',), }

@admin.register(models.Post)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug',)
    prepopulated_fields = {'slug': ('title',), }


# admin.site.register(models.Category)

# class PostModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     list_display = ('title', 'id', 'status', 'slug',)
#     prepopulated_fields = {'slug': ('title',), }
#     summernote_fields = ('content',)

# admin.site.register(models.Post, PostModelAdmin)