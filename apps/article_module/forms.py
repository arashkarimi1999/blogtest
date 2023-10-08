from django import forms
from .models import ArticleCategory,Article,ArticleComments


class CreateArticleForm(forms.ModelForm):
    
    class Meta:
        model=Article
        fields = ["title",'slug','selected_categories','short_description','text','image']
        # fields='__all__'
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=ArticleCategory.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False  # Make it optional, remove this line if it should be required
    # )

class CommentForm(forms.ModelForm):
    
    class Meta:
        model=ArticleComments
        fields=["article","author","parent","text"]


class ArticleEditForm(forms.ModelForm):
    
    class Meta:
        model=Article
        fields = ["title",'slug','selected_categories','short_description','text','image']