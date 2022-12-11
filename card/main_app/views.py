from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from main_app.forms import CardUpdateForm, CardCreateForm
from main_app.models import ProfileCard, Card, HistoryCard
from main_app.tasks import generate_cards


class CardListView(generic.ListView):
    """Card list view"""
    template_name = 'main_app/index.html'
    model = ProfileCard
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список карт'
        return context

    def get_queryset(self):
        return self.model.objects.filter(card__is_delete=False).select_related(
            'card')

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
                                         card=self.kwargs[
                                             'pk']).select_related('card')

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
        update = 'активировать'
        if self.object.card.is_active:
            update = 'деактивировать'
        context['title'] = f'{update} {self.object.card}'
        return context

    def get_queryset(self):
        return self.model.objects.filter(card__is_delete=False,
                                         card=self.kwargs[
                                             'pk']).select_related('card')

    def form_valid(self, form):
        data = form.data
        card = self.get_object()
        if not card.card.is_active:
            card.card.is_active = True
        else:
            card.card.is_active = False
        card.phone = data['phone']
        card.first_name = data['first_name']
        card.last_name = data['last_name']
        card.email = data['email']
        card.save()
        card.card.save()
        return HttpResponseRedirect(
            reverse('main:card_update', kwargs={'pk': self.kwargs['pk']}))

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardDeleteView(generic.DeleteView):
    """Card delete view"""
    template_name = 'main_app/card_delete.html'
    model = Card
    success_url = reverse_lazy('main:cards')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удалить {self.object}'
        return context

    def get_queryset(self):
        return self.model.objects.filter(id=self.kwargs['pk'])

    def form_valid(self, request, *args, **kwargs):
        card = self.get_object()
        if not card.is_delete:
            card.is_delete = True
            card.is_active = False
            card.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CardCreateView(generic.CreateView):
    """Card create view"""
    template_name = 'main_app/card_create.html'
    model = Card
    form_class = CardCreateForm
    success_url = reverse_lazy('main:cards')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сгенерировать карты'
        return context

    def form_valid(self, form):
        data = form.data
        term = int(data['term'])
        score = int(data['score'])
        generate_cards.delay(term, score)
        return HttpResponseRedirect(reverse('main:cards'))

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
