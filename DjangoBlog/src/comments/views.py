from django.shortcuts import render,get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404

@login_required #(login_url='/login/')
def comment_delete(request,id):
    # obj = get_object_or_404(Comment,id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404
    if request.user != obj.user:
        response = HttpResponse("You don't have permission to do this.")
        response.status_code = 403
        return response

    if request.method =="POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request,"Comment was deleted successfully")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object":obj,
    }
    return render(request,"confirm_delete.html",context)

def comment_thread(request,id):
    # obj = get_object_or_404(Comment, id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent
    # print(obj)
    
    content_object = obj.content_object
    content_id = obj.object_id
    initial_data = {
        "content_type":obj.content_type,
        "object_id":obj.object_id
    }
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
        # return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {
        "comments":obj,
        "form":form,
    }
    return render(request, "comment_thread.html", context)