from django.urls import path

from search_app.views import SearchView

app_name = 'search_app'

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
]
