from django.contrib import admin
from .models import ArticleCategory, Article , ArticleComments


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'parent', 'is_active']
    list_editable = ['is_active', 'url', 'parent']



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active','author']
    list_editable = ['is_active' ]
    prepopulated_fields = {"slug": ['title',]}

    def save_model(self, request, obj:Article , form, change):
        if not change :
            obj.author = request.user
        return super().save_model(request,obj,form,change)

@admin.register(ArticleComments)
class ArticleCommentsAdmin(admin.ModelAdmin):
    pass
