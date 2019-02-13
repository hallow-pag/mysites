from django.shortcuts import render_to_response, get_object_or_404,redirect,render
from .models import Blog, BlogType
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
def home(req):
    return render_to_response('home.html')
def newhome(req):
    return render_to_response( 'new_home.html')

def game(erq):
    return render_to_response('game.html')

def move(que):
    if que.method == 'POST':
        po =  que.POST.get('searchInput')
        try:
            return redirect('http://mv.688ing.com/player?url=https:' + po )
        except:
            return render_to_response('move.html')
        
    
    return render_to_response('move.html')
    
def about(req):
    return render_to_response('about.html')

def blog_list(request):
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list,10)
    page_num = request.GET.get('page',1) #得到page参数，默认为1
    page_of_blogs = paginator.get_page(page_num) #得到page 如果错误自动到第1页


    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blog_ty'] = BlogType.objects.all()
    return render_to_response('list.html', context)

def blog_detail(request, blog_pk):
    
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request,'article_de.html', context)

def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['b'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render_to_response('type_file.html', context)

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        # Return an 'invalid login' error message.
        return render(request,'er.html',{'er':'密码或账号不正确'})
    
def bar(req):
    return render(req, 'bargrap.html')
    