from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from .models import Post,Comment
from .forms import EmailPostForm, CommentForm, SearchForm

def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    #Paginator
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',context={
        'posts':posts,
        'tag': tag
    })

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

def post_detail(request,year,month,day,slug):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=slug,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)
    #Список комментарией к этому посту
    comments = post.comments.filter(active=True)
    #Создание формы для комментариев
    user = request.user
    if not request.user.is_authenticated:
        form = None
        user = None
    form = CommentForm()
    #Список схожих постов для рекомендации
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', context={
        'post':post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'user':user,
    })

def post_share(request, post_id):
    #Извлекаем пост по id
    post = get_object_or_404(Post, id = post_id,
                                   status = Post.Status.PUBLISHED)
    sent = False
    user = False

    if request.method == 'POST':
        data = request.POST.copy()
        if 'name' not in request.POST:
            data['name'] = request.user
            data['email'] = request.user.email
        form = EmailPostForm(data)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} порекомендовал вам запись: {post.title}"
            message = f"Посмотри запись: '{post.title}' \nпо ссылке - {post_url}\n\n" \
                      f"От {cd['name']} ({cd['email']})"
            send_mail(subject, message, 'busipac@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        if request.user.is_authenticated:
            user = True
            user = request.user
            user_email = request.user.email
            form = EmailPostForm(initial={'name':user,'email':user_email})
    return render(request, 'blog/post/share.html',context={
        'post': post,
        'form': form,
        'sent': sent,
        'user': user
    })

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status=Post.Status.PUBLISHED)
    comment = None
    
    data = {'name':request.user.id,
            'email':request.user.email,
            'body':request.POST['body']}
    
    form = CommentForm(data=data)
    print(form)
    if form.is_valid():
        print('asdadasdadaddas')
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query)
                                              ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', context={
        'form': form,
        'query': query,
        'results': results
    })