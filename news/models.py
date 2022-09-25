from django.db import models
from django.utils import timezone

from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    image = models.ImageField(default="category.png")
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name


# Create your models here.
class Post(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    image = models.ImageField(upload_to="images/", default="images/default.png")
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
    max_length=10, choices=options, default='published')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('-published',)
