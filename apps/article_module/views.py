from django.db.models import Count
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView,UpdateView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .models import ArticleCategory, Article, ArticleComments
from .forms import CreateArticleForm,CommentForm,ArticleEditForm
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



# Create your views here.


class ArticlesView(ListView):
    template_name = 'article_module/articles_page.html'
    paginate_by = 2

    context_object_name = "article"
    model = Article
    ordering = ['-date_created',]

    def get_context_data(self,*args , **kwargs):
        context = super(ArticlesView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesView,self).get_queryset()
        query = query.filter(is_active=True)
        this_category = self.kwargs.get('category')
        if this_category is not None :
            query = query.filter(selected_categories__url__iexact=this_category)
        return query


class ArticleDetailView(DetailView):
    template_name = "article_module/article-detail.html"
    context_object_name = 'article'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        article = kwargs.get('object')
        comment : ArticleComments = ArticleComments.objects.filter(article_id=article.id,parent=None).order_by('-date_created').prefetch_related("parent_comment")
        context['comments'] = comment
        context['comment_count'] = ArticleComments.objects.annotate(comment_count=Count('article')).filter(article_id=article.id).count()
        return context
# def category_components(request):
#     main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,parent = None)
#     context = {
#         "main_categories" : main_categories
#     }
#     return render(request, "article_module/components/category_components.html", context)

def add_article_comment(request:HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        print(article_comment,article_id,parent_id)
        new_comment = ArticleComments(article_id=article_id, text=article_comment ,author_id=request.user.id, parent_id=parent_id)
        new_comment.save()

        context = {
            'comments': ArticleComments.objects.filter(article_id=article_id, parent=None).order_by(
                '-date_created'),
            'comments_count': ArticleComments.objects.filter(article_id=article_id).count(),
            'article': Article.objects.get(id=article_id),
            
        }
        # return HttpResponse("hello world ")
        return  render (request,'article_module/article-detail.html',context )
        # return JsonResponse({
        # 'status' : 'success' ,
        # 'response' : data
    # })

class CreateComment(CreateView):
    model=ArticleComments
    form_class=CommentForm
    template_name ='article_module/asd.html'
    success_url = "#"
    def post(self,request,*args, **kwargs):
        print(request.GET.get('article_id'))


def is_superuser_or_admin(user):
    return user.is_superuser 


class CreateArticle(UserPassesTestMixin,CreateView):
    
    model=Article
    form_class=CreateArticleForm
    template_name ='article_module/create_article.html'
    success_url = 'articles-list'

    def form_valid(self, form):

        form.instance.author = self.request.user
        form.instance.is_active=False
        # You can perform additional actions here if needed
        return super().form_valid(form)

    def test_func(self):
        return is_superuser_or_admin(self.request.user)


def UserArticles(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            user_articles=Article.objects.filter(author=request.user)
            print(user_articles)

            return render(request,"article_module/user_article.html",  {'articles': user_articles} )




class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'article_module/update_article.html'
    success_url = '/user-articles'



@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.delete()
    return redirect('article:user-articles')  