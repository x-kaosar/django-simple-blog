from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django_countries.fields import CountryField


User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='user.svg')
    bio = models.TextField(max_length=50000,null=True, blank=True)
    birthday = models.DateField(null=True,blank=True)
    phone = models.CharField(max_length=11,null=True, blank=True)
    company = models.CharField(max_length=100,null=True, blank=True)
    country = CountryField(null=True,blank_label='Select Country')
    address = models.CharField(max_length=200,null=True, blank=True)
    website = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    post    = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    description = RichTextField(null=True,max_length=1000)
    tags = models.ManyToManyField(Tag)
    category = models.ManyToManyField(Category)
    # comment_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    featured = models.BooleanField()
    slug = models.SlugField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def content(self):
        if len(self.description) > 50:
            return f"{str(self.description)[:50]}..."
        else:
            return f"{str(self.description)}"

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.title)
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + "-" + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('post-details', kwargs={
            'slug':self.slug
        })

    
    def get_update_url(self):
        return reverse('post-update', kwargs={
            'slug':self.slug
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'slug':self.slug
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-date_created')

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

