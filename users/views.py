from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.db.models import Count
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from articles.models import Like


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next')
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                # Добавляем пользователя на лайки, которые он поставил, являясь анонимом
                Like.objects.filter(session_key=session_key).update(user=user)
                # Получаем дубликаты, на которых пользователь уже ставил лайк
                duplicates = Like.objects.filter(user=user)\
                                         .values_list('article', flat=True)\
                                         .alias(duplicate=Count('article'))\
                                         .filter(duplicate__gt=1)
                if duplicates:
                    Like.objects.filter(article__in=duplicates,
                                        session_key=session_key).delete()
            messages.success(self.request,
                             f'{user.username}, Вы вошли в аккаунт!')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context
    

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)
            if session_key:
                Like.objects.filter(session_key=session_key).update(user=user)
            messages.success(self.request,
                             f'{user.username}, Вы успешно зарегистрировалась!')
        return HttpResponseRedirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Личный кабинет обновлен!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        return context


@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Вы вышли из аккаунта!')
    auth.logout(request)
    return redirect(reverse('main:index'))
