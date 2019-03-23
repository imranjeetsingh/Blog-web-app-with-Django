from urllib.parse import quote_plus

from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .utils import get_read_time
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import PostForm
from .models import Post
from comments.models import Comment
from comments.forms import CommentForm
# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,"Invalid data")
    context = {
        "form":form,
    }
    return render(request, "post_form.html",context)

def post_detail(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    read_time = get_read_time(instance.get_markdown())
    print(read_time)
    # content_type = ContentType.objects.get_for_model(Post)
    # obj_id = instance.id
    comments = instance.comments 
    # comments =  Comment.objects.filter(content_type=content_type, object_id = obj_id)
    # print(comments)

    initial_data = {
        "content_type":instance.get_content_type,
        "object_id":instance.id
    }
    # print(initial_data.get("content_type"))
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            # print(parent_qs)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type=content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        # print(new_comment,created)
    context = {
        "instance":instance,
        "title" : "Detail",
        "share_string":share_string,
        "comments":comments,
        "comment_form":form
    }
    return render(request,"post_detail.html",context)

def post_list(request):
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                        Q(title__icontains=query)|
                        Q(content__icontains=query)|
                        Q(user__first_name__icontains=query)|
                        Q(user__last_name__icontains=query)
                        ).distinct()
    paginator = Paginator(queryset_list,4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    # print(page)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    # print(queryset)
    context = {
        "object_list": queryset,
        "title" : "Posts",
        "page_request_var":page_request_var,
        "today":timezone.now().date(),
    }
    return render(request,"post_list.html",context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,"successfully deleted the post")
    return redirect("posts:list")

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None , instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.error(request,"suceessfully Updated data")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title":instance.title,
        "instance":instance,
        "form":form
    }
    return render(request,"post_form.html",context)