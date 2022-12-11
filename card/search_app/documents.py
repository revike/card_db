from django_elasticsearch_dsl import Document, registries, fields

from main_app.models import Card, ProfileCard


@registries.registry.register_document
class CardOptionsDocument(Document):
    """New document cards"""
    card = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'series': fields.TextField(),
            'numbers': fields.TextField(),
            'release_data': fields.DateField(),
            'term': fields.IntegerField(),
            'end_activity': fields.DateField(),
            'amount': fields.FloatField(),
            'is_active': fields.BooleanField(),
            'overdue': fields.BooleanField(),
            'is_delete': fields.BooleanField()
        }
    )

    class Index:
        name = 'cards'
        settings = {'number_of_shards': 1, 'number_of_replicas': 1}

    class Django:
        model = ProfileCard
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone']
        related_models = [Card]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ProfileCard):
            return related_instance.card_set.all()
