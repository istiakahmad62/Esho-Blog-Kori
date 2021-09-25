from django.db import models
from django.utils.text import slugify


# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Author"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="post-images", null=True)
    date = models.DateField(blank=True, null=True, auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True) # if we add unique=true, don't nee {{db_index}}
    content = models.TextField() # screen shot -------------
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="posts") 
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Post"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
