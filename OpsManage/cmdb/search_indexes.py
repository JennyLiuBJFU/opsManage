
from haystack import indexes


# 修改此处，为你自己的model
from cmdb.models import Asset


# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class AssetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #
    # asset_name = indexes.CharField(model_attr='asset_name')  # 创建一个author字段
    #
    # asset_type = indexes.CharField(model_attr='asset_type')  # 创建一个pub_date字段
    #
    # manage_ip = indexes.CharField(model_attr='manage_ip')

    def get_model(self):
        # 修改此处，为你自己的model
        return Asset

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
