from django import forms
from django.contrib import admin
from .models import Article

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):
    full_text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
