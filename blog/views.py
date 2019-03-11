from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from .models import Blog, BlogType
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.form import CommentForm

def home(request):
    return render(request, 'home.html')


def newhome(req):
    return render(req, 'new_home.html')


def game(erq):
    return render(erq, 'game.html')


def move(que):
    if que.method == 'POST':
        po = que.POST.get('searchInput')
        try:
            return redirect('http://mv.688ing.com/player?url=https:' + po)

        except:
            render(que, 'move.html')

    return render(que, 'move.html')


def about(req):
    return render(req, 'about.html')


def blog_list(request):
    context = {}
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list, 6)
    page_num = request.GET.get('page', 1)  # 得到page参数，默认为1
    page_of_blogs = paginator.get_page(page_num)  # 得到page 如果错误自动到第1页
    page_unmber = max(page_of_blogs.number - 2, 1)  # 中心坐标
    if page_unmber > len(page_of_blogs.paginator.page_range) - 4:
        page_unmber = len(page_of_blogs.paginator.page_range) - 4

    context['num'] = [page_unmber, page_unmber + 1, page_unmber + 2, page_unmber + 3, page_unmber + 4]
    context['page_of_blogs'] = page_of_blogs
    context['blog_ty'] = BlogType.objects.annotate(blog_count=Count('blog'))
    return render(request, 'list.html', context)


def blog_detail(request, blog_pk):  # 博客阅读页面
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)
    if not request.COOKIES.get('blog_%s_read_num' % blog_pk):
        blog.read_num += 1
        blog.save()
    context = {}
    context['blog'] = blog
    context['comments'] = comments
    context['blog_on'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog_next'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['comment_from'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk})
    response = render(request, 'blog_detai.html', context)  ####
    response.set_cookie('blog_%s_read_num' % blog_pk, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

    context['b'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_ty'] = BlogType.objects.all()
    return render(request, 'type_file.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('from', reversed('home')))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'er': '密码或账号不正确,请重新登录'})

    return render(request, 'login.html')


def registered(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        passwords = request.POST['passwords']
        emil = request.POST['emil']
        if User.objects.filter(username=name).exists():
            return render(request, 'registered.html', {'er_user': '用户以存在'})
        elif password != passwords:
            return render(request, 'registered.html', {'er_passwords': '两次密码不同'})
        elif len(passwords) < 6:
            return render(request, 'registered.html', {'er_password': '密码过于简单'})
        elif User.objects.filter(email=emil).exists():
            return render(request, 'registered.html', {'er_emil': '邮箱已存在'})
        else:
            user = User.objects.create_user(username=name, email=emil, password=password)
            user.save()
            user = authenticate(request, username=name, password=password)
            login(request, user)
            return render(request, 'home.html')
    else:
        return render(request, 'registered.html')


def bar(req):
    return render(req, 'bargrap.html')
