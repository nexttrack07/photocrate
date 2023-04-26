from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

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
        ]
