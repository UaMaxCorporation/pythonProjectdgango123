from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .models import Post, PostPoint
from django.views.generic import ListView
from .models import Comment, User
from .forms import CommentForm, PostForm,PostPointForm, UserCreateForm
from taggit.models import Tag
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import CommentForm,  PostForm
from django.shortcuts import redirect


def sign_up(request):
    user_form=UserCreateForm()
    if request.method == 'POST':
        user_form=UserCreateForm(request.POST)
        if user_form.is_valid():
            new_user=User.objects.create_user(**user_form.cleaned_data)
            new_user.save()
            login(request, authenticate(username=user_form.cleaned_data['username'],
                                        password=user_form.cleaned_data['password']))
            return redirect('blog:post_list')
    return render(request,'registration/sign_up.html',
                                {'user_form':user_form})

@login_required
def post_point_delete(request, post_point_id):
    try:
        post_point=get_object_or_404(PostPoint,id=post_point_id)
        post_point.delete()
        return redirect('blog:post_point_list',post_id=post_point.post.id)
    except Post.DoesNotExist:
        return redirect('blog:post_list')


@login_required
def post_point_edit(request, post_point_id):
    post_point = get_object_or_404(PostPoint, id=post_point_id)
    post = get_object_or_404(Post, id=post_point.post.id)
    post_point_edit_form = PostPointForm(instance=post_point)
    if request.method == 'POST':
        post_point_edit_form = PostPointForm(request.POST, request.FILES,
                                             instance=post_point)
        if post_point_edit_form.is_valid():
            post_point_edit_form.save()
    return render(request, 'blog/account/post_point_edit.html',
                  {'form': post_point_edit_form,
                   'post_point': post_point,
                   'post': post})




@login_required
def post_point_add(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostPointForm()

    if request.method == 'POST':
        form = PostPointForm(request.POST,
                             request.FILES)
        if form.is_valid():
            post_point = form.save(commit=False)
            post_point.post = post
            post_point.save()

    return render(request, 'blog/account/post_point_add.html', {'form': form,
                                                                'post': post})

@login_required
def post_point_list(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    post_points = PostPoint.objects.filter(
        post=post)
    return render(request,
                  'blog/account/post_points.html',
                  {'post': post,
                   'post_points': post_points})


@login_required
def post_delete(request, post_id):
    try:
        post = get_object_or_404(Post,
                                 id=post_id)
        post.delete()
        return redirect('blog:dashboard')
    except Post.DoesNotExist:
        return redirect('blog:dashboard')

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_edit_form = PostForm(instance=post)
    if request.method == 'POST':
        post_edit_form = PostForm(request.POST, request.FILES, instance=post)
        if post_edit_form.is_valid():
            post_edit_form.save()
    return render(request,
                  'blog/account/post_edit.html',
                  {'form': post_edit_form,
                   'post': post})
@login_required
def post_add(request):
    user=request.user
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=user
            print(post)
            post.save()
            for tag in form.cleaned_data['tags']:
                post.tags.add(tag)
    else:
        form=PostForm()

    return render(request, 'blog/account/post_add.html',{'form':form})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/account/login.html', {'form': form})

class PostListViev(ListView):
    queryset=Post.objects.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'


@login_required
def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:

        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


def post_detail(request, year, month, day, post):
    post_object = get_object_or_404(Post, slug=post, status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    post_points = PostPoint.objects.filter(post=post_object)

    comments = post_object.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment(post=post_object, name=cd['name'], email=cd['email'], body=cd['body'])
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids=post_object.tags.values_list('id', flat=True)
    similar_posts=Post.objects.filter(tags__in=post_tags_ids,status='published').exclude(id=post_object.id)


    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]



    return render(request, 'blog/post/detail.html', {'post': post_object,
                                                     'post_points': post_points,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     })

@login_required
def dashboard(request):
    user=request.user
    posts_pub=Post.objects.filter(author=user,status='published')
    posts_draft=Post.objects.filter(author=user,status='draft')
    return render(request,'blog/account/dashboard.html',{'posts_pub':posts_pub,
                                                         'posts_draft':posts_draft})


