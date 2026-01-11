from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Выберите автора'
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']
        labels = {
            'author': 'Автор',
            'title': 'Название',
            'text': 'Содержание',
        }
