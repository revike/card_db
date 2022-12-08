from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view"""
    template_name = 'main_app/index.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
