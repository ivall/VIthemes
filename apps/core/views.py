from django.contrib.auth.decorators import login_required
from django.db.models import Count, When
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Theme, Vote
from .forms import CreateThemeForm
from .utils.utils import get_form_errors
from django.db import models


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        themes = Theme.objects.filter(approved=True)
        popular_themes = themes.annotate(
            num_of_true_vote_type=models.Count(
                models.Case(When(vote__choice='upvote', then=1), output_field=models.IntegerField())
            ),
            num_of_false_vote_type=models.Count(
                models.Case(When(vote__choice='downvote', then=1), output_field=models.IntegerField())
            ),
            difference=models.F('num_of_true_vote_type') - models.F('num_of_false_vote_type')
        ).order_by('-difference')
        context['themes'] = themes
        context['popular_themes'] = popular_themes
        return context


class MyThemes(LoginRequiredMixin, TemplateView):
    template_name = 'my_themes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        themes = Theme.objects.filter(user=self.request.user)
        context['themes'] = themes
        return context


class CreateThemeView(LoginRequiredMixin, FormView):
    template_name = 'create_theme.html'
    login_url = '/users/discord/login'
    form_class = CreateThemeForm

    def form_invalid(self, form):
        errors = get_form_errors(form)
        for error in errors:
            messages.add_message(self.request, messages.ERROR, error)
        return super(CreateThemeView, self).form_invalid(form)

    def form_valid(self, form):
        theme = form.save(commit=False)
        theme.user = self.request.user
        theme.save()
        self.success_url = f'/themes/{theme.uuid}'
        messages.add_message(self.request, messages.SUCCESS, 'Motyw został dodany, oczekuje on teraz na zatwierdzenie.')
        return super(CreateThemeView, self).form_valid(form)


class ThemeView(TemplateView):
    template_name = 'theme_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = get_object_or_404(Theme, uuid=self.kwargs.get('theme_uuid'))
        if self.request.user.is_authenticated:
            user_vote = Vote.objects.filter(theme=theme, user=self.request.user).first()
        else:
            user_vote = None
        context['theme'] = theme
        context['vote'] = user_vote
        return context


class VoteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        vote_type = request.POST.get('vote_type')
        theme = get_object_or_404(Theme, uuid=kwargs.get('theme_uuid'))
        check_vote = Vote.objects.filter(user=request.user, theme=theme).first()
        if check_vote and check_vote.choice == vote_type:
            check_vote.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Głos został usunięty')
            return redirect(f'/themes/{theme.uuid}')
        elif check_vote:
            check_vote.delete()
        vote = Vote(
            user=self.request.user,
            theme=theme,
            choice=vote_type
        )
        vote.save()
        messages.add_message(self.request, messages.SUCCESS, 'Głos został dodany')
        return redirect(f'/themes/{theme.uuid}')


class SearchView(View):
    def get(self, request, *args, **kwargs):
        theme_name = request.GET.get('name')
        if not theme_name:
            return redirect('/')
        themes = Theme.objects.filter(name__icontains=theme_name, approved=True)
        return render(request, "search.html", {"themes": themes})


class PanelView(PermissionRequiredMixin, TemplateView):
    template_name = 'panel.html'
    permission_required = 'is_admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        themes = Theme.objects.filter(approved=False)
        context['themes'] = themes
        return context


class ApproveThemeView(PermissionRequiredMixin, View):
    permission_required = 'is_admin'

    def post(self, request, *args, **kwargs):
        approve_type = request.POST.get('approved')
        theme_uuid = request.POST.get('theme_uuid')
        if approve_type is None or not theme_uuid:
            return redirect('/panel')
        theme = get_object_or_404(Theme, uuid=theme_uuid)
        if approve_type == 'approve':
            theme.approved = True
            theme.save()
            return redirect('/panel')
        else:
            theme.delete()
            return redirect('/panel')


@login_required
def edit(request, theme_uuid=None, template_name='create_theme.html'):
    if theme_uuid:
        theme = get_object_or_404(Theme, uuid=theme_uuid)
        if theme.user != request.user and not request.user.is_admin:
            return HttpResponseForbidden()
    else:
        theme = Theme(user=request.user)

    form = CreateThemeForm(request.POST or None, instance=theme)
    if request.POST and form.is_valid():
        theme = form.save(commit=True)
        success_url = f'/themes/{theme.uuid}'
        messages.add_message(request, messages.SUCCESS, 'Motyw został edytowany.')
        return redirect(success_url)
    elif request.POST and not form.is_valid():
        errors = get_form_errors(form)
        for error in errors:
            messages.add_message(request, messages.ERROR, error)

    return render(request, template_name, {
        'form': form
    })
