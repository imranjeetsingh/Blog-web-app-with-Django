from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from .forms import PostForm
from .models import Post
# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,"Invalid data")
    context = {
        "form":form,
    }
    return render(request, "post_form.html",context)

def post_detail(request,id=None):
    instance = get_object_or_404(Post,id=id)
    context = {
        "instance":instance,
        "title" : "Detail"
    }
    return render(request,"post_detail.html",context)

def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title" : "List"
    }
    return render(request,"post_list.html",context)

def post_delete(request, id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,"successfully deleted the post")
    return redirect("posts:list")

def post_update(request, id=None):
    instance = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None, instance=instance)
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