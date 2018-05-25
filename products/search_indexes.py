from haystack import indexes
from .models import ProductInfo


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ProductInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()