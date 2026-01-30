from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from .utils import get_group


class SignUpView(CreateView):
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        group_common = get_group('common')
        self.object.groups.add(group_common)
        return response


def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')


@login_required
def user_profile(request):
    context = {
        'is_author': request.user.groups.filter(name='authors').exists()
    }
    return render(request, 'sign/profile.html', context)


@login_required
def author_group(request):
    group_author = get_group('authors')
    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(group_author)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def common_group(request):
    group_common = get_group('common')
    if not request.user.groups.filter(name='common').exists():
        request.user.groups.add(group_common)
    return redirect(request.META.get('HTTP_REFERER'))
