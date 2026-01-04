from django_filters import FilterSet, CharFilter
from .models import Post


class PostFilter(FilterSet):
    author_name = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'time_in': ['gt'],
        }
