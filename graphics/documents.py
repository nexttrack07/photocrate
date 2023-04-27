from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import field

from graphics.models import Graphic


@registry.register_document
class GraphicDocument(Document):
    class Index:
        name = "graphics"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Graphic
        fields = [
            "desc",
            "url",
            "created_at",
            "updated_at",
        ]

    category_id = field.Keyword()

    def prepare_category_id(self, instance):
        return instance.category_id.id

    def __str__(self):
        return self.desc
