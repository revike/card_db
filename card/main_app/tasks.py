from celery import shared_task
from django.utils.timezone import now
from main_app.models import Card
from main_app.utils import add_months


@shared_task(autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 10, 'countdown': 5})
def deactivate_card():
    """Deactivate card"""
    cards = Card.objects.filter(end_activity__lte=now())
    for i in cards:
        i.is_active=False
        i.overdue=True
        i.save()


@shared_task(autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 10, 'countdown': 60})
def generate_cards(term, score):
    """Generate cards"""
    end_activity = add_months(now(), term)
    series = 1000
    numbers = 1
    card_old = Card.objects.all().order_by('-pk').first()
    if card_old:
        series = int(card_old.series)
        numbers = int(card_old.numbers) + 1
        numbers, series = update_numbers_series(numbers, series)
    for _ in range(score):
        Card.objects.create(
            series=f'{series}',
            numbers=f'{numbers:08}',
            term=term,
            end_activity=end_activity,
        )
        numbers += 1
        numbers, series = update_numbers_series(numbers, series)


def update_numbers_series(numbers, series):
    """Update numbers and series"""
    if numbers == 99999999:
        numbers = 1
        series += 1
    return numbers, series
