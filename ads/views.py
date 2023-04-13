from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.core.cache import cache
from .forms import AdvertForm, ResponseForm, Response_Receive_Form




class AdvertsList(ListView):
    model = Advert
    ordering = '-timeCreation'
    template_name = 'adverts_list.html'
    context_object_name = 'adverts'
    paginate_by = 10




class AdvertCreate(LoginRequiredMixin, CreateView):
    permission_required = ('ads.add_advert',)
    raise_exception = True
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_create.html'
    success_url = reverse_lazy('adverts_list')

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class AdvertUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('ads.change_advert',)
    raise_exception = True
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_edite.html'
    success_url = reverse_lazy('adverts_list')


class AdvertDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('ads.delete_advert',)
    raise_exception = True
    model = Advert
    template_name = 'advert_delete.html'
    success_url = reverse_lazy('adverts_list')


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'advert_index.html'
    context_object_name = 'advert'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'advert-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'advert-{self.kwargs["pk"]}', obj)

        return obj


class ResponseCreate(LoginRequiredMixin, CreateView):
    permission_required = ('ads.add_response',)
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    success_url = reverse_lazy('adverts_list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.responseAdvert_id = self.kwargs.get('pk')
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-timeCreation'
    template_name = 'response_list.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_list'] = \
            Response.objects.filter(responseAdvert__in=Advert.objects.filter(username_id=self.request.user))
        # context['filterset'] = self.filterset
        return context


class ResponseAdvert(ResponseList):
    model = Response
    template_name = 'response_advert_list.html'
    context_object_name = 'response_advert_list'

    def get_queryset(self):
        self.resp_Advert = get_object_or_404(Advert, id=self.kwargs['pk'])
        queryset = Response.objects.filter(responseAdvert=self.resp_Advert).order_by('-timeCreation')
        return queryset


class ResponseDetail(DetailView):
    model = Response
    template_name = 'response_index.html'
    context_object_name = 'response'


class ResponseUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('ads.change_response',)
    raise_exception = True
    form_class = Response_Receive_Form
    model = Response
    template_name = 'response_edite.html'
    success_url = reverse_lazy('response_list')


class ResponseDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('ads.delete_response',)
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response_list')


class AdvertsUserList(LoginRequiredMixin, ListView):
    model = Advert
    ordering = '-timeCreation'
    template_name = 'adverts_user_list.html'
    context_object_name = 'advert'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adverts_list'] = \
            Advert.objects.all().filter(username_id=self.request.user)

        return context

