from django.utils import timezone
from .models import Post, Item
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .forms import PostForm, ItemForm
from django.core.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.forms.models import BaseModelFormSet
from django.forms.models import modelform_factory, modelformset_factory


def post_list(request):
    """Shows all the projects"""
    if request.method == 'GET':
        posts = Post.objects.filter(author_id=request.user.id).order_by('-published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})
    elif request.method == 'POST':
        # create a new project: input the new name
        project_name = request.POST.get('project_name', '')
        # create_project input is not null
        if request.user.is_active:
            post = Post.objects.create(author_id=request.user.id,title=project_name)
            post.save()
            return redirect('blog.views.post_detail', pk=post.id)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        items_todo = Item.objects.filter(author_id=post.author_id,post=post,status=False).order_by('-added_date')
        items_done = Item.objects.filter(author_id=post.author_id,post=post,status=True).order_by('-added_date')
        return render(request, 'blog/post_detail.html', {'post': post, 'items_todo': items_todo, 'items_done': items_done})
    elif request.method == 'POST':
        #add new items abstract, remember to check whether the input is null
        new_items_abstract = request.POST.get('new_items_abstract', '')
        if request.user.is_active:
            item = Item.objects.create(author_id=post.author_id,post=post,abstract=new_items_abstract)
            form = ItemForm(request.POST, instance=item)
            return redirect('blog.views.post_detail', pk=post.pk)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)


    class BaseItemFormSet(BaseModelFormSet):
        # create BaseItemFormSet() to display all objects in the model 
        def __init__(self, *args, **kwargs):
            super(BaseItemFormSet, self).__init__(*args, **kwargs)

            #create filtering here whatever that suits you needs
            self.queryset = Item.objects.filter(author_id=post.author_id,post=post,status=False).order_by('-added_date')

    formset = modelformset_factory(Item, formset=BaseItemFormSet,form=ItemForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = formset(request.POST)
        if(formset.is_valid()):
            message = "Thank you"
        for form in formset:
            item = form.save(commit=False)
            item.author_id=post.author_id
            item.post = post
            print item
            item.save()
        else:
            message = "Something went wrong"
        return redirect('blog.views.post_detail', pk=post.pk)
        #return render_to_response('blog/post_edit.html', 
        #        {'message': message, 'post':post,},
        #        context_instance=RequestContext(request))
    else:
        return render_to_response('blog/post_edit.html',
                {'formset': formset()},
                context_instance=RequestContext(request))







