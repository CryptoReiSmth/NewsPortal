from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
from django.forms import DateInput
from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )

    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Позже даты',
        widget=DateInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []
