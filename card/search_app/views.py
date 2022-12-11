from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views import generic
from elasticsearch_dsl import Q

from search_app.documents import CardOptionsDocument


class SearchView(generic.ListView):
    """ElasticSearch view"""
    template_name = 'main_app/index.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        """Возвращает контекст для этого представления"""
        context = super().get_context_data(**kwargs)
        context['title'] = f'Поиск: {self.request.GET.get("search")}'
        return context

    def get_queryset(self):
        request_get = self.request.GET
        search = request_get.get('search')
        filters = request_get.getlist('filter')

        q = Q(
            'multi_match',
            query=search,
            fields=[
                'card.series', 'card.numbers', 'first_name', 'last_name',
                'email', 'phone'
            ],
            fuzziness='auto',
        )
        object_list = CardOptionsDocument.search().query()

        if search:
            object_list = object_list.query(q)

        if 'all' not in filters:
            if 'is_active' in filters:
                object_list = object_list.filter('match_phrase',
                                                 card__is_active=True)
            if 'not_is_active' in filters:
                object_list = object_list.filter('match_phrase',
                                                 card__is_active=False)
            if 'overdue' in filters:
                object_list = object_list.filter('match_phrase',
                                                 card__overdue=True)
            if 'not_overdue' in filters:
                object_list = object_list.filter('match_phrase',
                                                 card__overdue=False)

        return object_list.filter('match_phrase', card__is_delete=False)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
