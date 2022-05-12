from django.views import generic
from . import models
from django.http import Http404


class ArticlesListView(generic.ListView):
    paginate_by = 5
    model = models.Article
    template_name = 'articles/articles_list.html'
    context_object_name = 'articles'
    ordering = ['-pub_date']
    queryset = models.Article.objects.select_related('author').filter(status=True)


class ArticleDetailView(generic.DetailView):
    model = models.Article
    template_name = 'articles/article_details.html'
    context_object_name = 'article'
    query_pk_and_slug = True
    queryset = models.Article.objects.select_related('author').filter(status=True)

    def get_object(self, queryset=None):
        try:
            return self.queryset.get(**self.kwargs)
        except self.model.DoesNotExist:
            raise Http404()
