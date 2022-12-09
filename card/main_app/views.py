from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from main_app.forms import CardUpdateForm, CardCreateForm
from main_app.models import ProfileCard, Card, HistoryCard


class CardListView(generic.ListView):
    """Card list view"""
    template_name = 'main_app/index.html'
    model = ProfileCard
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список карт'
        return context

    def get_queryset(self):
        return self.model.objects.filter(card__is_delete=False)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardDetailView(generic.DetailView):
    """Card detail view"""
    template_name = 'main_app/card.html'
    model = ProfileCard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history_card = HistoryCard.objects.filter(card=self.object.card)
        context['history_card'] = history_card
        context['title'] = f'{self.object.card}'
        return context

    def get_queryset(self):
        return self.model.objects.filter(card__is_delete=False,
                                         card=self.kwargs['pk'])

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProfileCardUpdateView(generic.UpdateView):
    """Card profile update view"""
    template_name = 'main_app/card_update.html'
    model = ProfileCard
    form_class = CardUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изменить {self.object.card}'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardDeleteView(generic.DeleteView):
    """Card delete view"""
    template_name = 'main_app/card_delete.html'
    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить {self.object}'
        return context

    def delete(self, request, *args, **kwargs):
        card = self.get_object()
        if not card.is_delete:
            print('delete')
        return HttpResponseRedirect(reverse('main:list'))

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardCreateView(generic.CreateView):
    """Card create view"""
    template_name = 'main_app/card_create.html'
    model = Card
    form_class = CardCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сгенерировать карты'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
