from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.views.generic import DetailView
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count, Q
from .models import Post,Author, PostView
from .forms import PostForm,CommentForm,UserForm,UserInfoForm,PasswordChangingForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView


def get_category_count():
    queryset = Post \
    .objects \
    .values('category__name') \
    .annotate(Count('category__name'))
    return queryset
def get_tags():
    queryset = Post.objects.values('tags__name').annotate(Count('tags__name'))
    return queryset
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)
        ).distinct()
        context = {
            'queryset':queryset
        }
        return render(request, 'search_result.html',context)

def home(request):
    posts = Post.objects.all()
    latest_posts = Post.objects.order_by('-date_created')[0:3]
    get_category = get_category_count()
    get_tag = get_tags()

    page = request.GET.get('page')
    paginator = Paginator(posts,4)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'object_list':posts,
        'latest_post':latest_posts,
        'get_categories':get_category,
        'get_tags':get_tag,
        'posts':posts,
    }
    return render(request, 'blog.html',context)

def post(request,slug):
    post = get_object_or_404(Post,slug=slug)
    latest_posts = Post.objects.order_by('-date_created')[0:3]
    get_category = get_category_count()
    get_tag = get_tags()

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            send_mail(
                str(form.instance.user)+' commented in your post',
                str(form.instance.content),
                settings.EMAIL_HOST_USER,
                [post.author.user.email],
                fail_silently=False,
            )
            return redirect(reverse('post-details', kwargs={
                'slug':post.slug
            }))

    context = {
        'form':form,
        'post':post,
        'latest_post':latest_posts,
        'get_categories':get_category,
        'get_tags':get_tag,
    }
    return render(request, 'post.html',context)


def post_create(request):
    form = PostForm()
    author = get_author(request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-details', kwargs={
                'slug':form.instance.slug
            }))
    context = {'form':form}
    return render(request, 'create_post.html', context)


def post_update(request,slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-details', kwargs={
                'slug':form.instance.slug
            }))
    context = {'form':form,'post':post}
    return render(request, 'update_post.html', context)


def post_delete(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    context = {'post':post}
    return render(request, 'post_delete.html', context)


def setting(request, username):
    user = User.objects.get(username=username)
    form = UserForm(instance=user)
    auth_form = request.user.author
    info_form = UserInfoForm(instance=auth_form)

    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        info_form = UserInfoForm(request.POST,request.FILES,instance=auth_form)

        if form.is_valid():
            form.save()
            info_form.save()
            return redirect(reverse('setting', kwargs={
                'username':request.user
            }))

        if info_form.is_valid():
            info_form.save()
            return redirect(reverse('setting', kwargs={
                'username':request.user
            }))

    context = {'user':user,'form':form,'info_form':info_form}
    return render(request, 'account_settings.html',context)


def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.POST,request.user)
        if form.is_valid():
            form.save()
            return HttpResponse("Password Changed")
    context = {'form':form}
    return render(request,'password_change.html',context)

'''def password_change(request):
    form = PasswordChangeView()

    context = {'form':form}
    return render(request,'password_change.html',context)'''