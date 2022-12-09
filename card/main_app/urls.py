from django.urls import path

from main_app.views import CardListView, CardDetailView, CardDeleteView, \
    ProfileCardUpdateView, CardCreateView

app_name = 'main_app'

urlpatterns = [
    path('', CardListView.as_view(), name='cards'),
    path('<int:pk>/', CardDetailView.as_view(), name='card'),
    path('delete/<int:pk>/', CardDeleteView.as_view(), name='card_delete'),
    path('create/', CardCreateView.as_view(), name='card_create'),
    path('update/<int:pk>/', ProfileCardUpdateView.as_view(),
         name='card_update'),
]
