from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Comment, Post, PostForm, CommentForm



class IndexView(generic.ListView):
    model = Post
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        postlist = Post.objects.all()
        realpostlist = []
        for post in postlist:
            if post.post_title != '':
                realpostlist.append(post)
        finalpostlist = realpostlist[-5:]
        finalpostlist.reverse()
        return finalpostlist
    
    #overrides the context getting argument to be passed to html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = PostForm()
        context['comment_form'] = CommentForm()
        return context
    
    #overrides the post func
    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST)
        comment_form = CommentForm(request.POST)

        if 'submit_post' in request.POST and post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect(request.path)
        if 'submit_comment' in request.POST and comment_form.is_valid():
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = comment_form.save(commit=False)
            comment.mother_post = post
            comment.post = post
            comment.save()
            return HttpResponseRedirect(request.path)

        


class DetailView(generic.DetailView):
    model = Post
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Post
    template_name = "polls/results.html"
    


def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        selected_choice = post.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Comment.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "post": post,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(post.id,)))
    
def results(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "polls/results.html", {"post":post})

# Create your views here.
