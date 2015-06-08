import datetime
from haystack import indexes
from KULTURBIDEAK.kulturbideak_app.models import item
from KULTURBIDEAK.kulturbideak_app.models import path


class itemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    dc_title = indexes.CharField(model_attr='dc_title')
    dc_subject = indexes.CharField(model_attr='dc_subject')
    dc_description = indexes.CharField(model_attr='dc_description')
    dc_creator = indexes.CharField(model_attr='dc_creator')
    dc_language = indexes.CharField(model_attr='dc_language')
    edm_provider= indexes.CharField(model_attr='edm_provider')
    edm_country= indexes.CharField(model_attr='edm_country')
    edm_type= indexes.CharField(model_attr='edm_type')
    edm_rights= indexes.CharField(model_attr='edm_rights')
    edm_year= indexes.CharField(model_attr='edm_year')
    edm_object = indexes.CharField(model_attr='edm_object')
    uri = indexes.CharField(model_attr='uri')
    dc_publisher = indexes.CharField(model_attr='dc_publisher')
    dc_contributor = indexes.CharField(model_attr='dc_contributor')
    dc_type = indexes.CharField(model_attr='dc_type')
    dc_format = indexes.CharField(model_attr='dc_format')
    dc_identifier = indexes.CharField(model_attr='dc_identifier')
    dc_source = indexes.CharField(model_attr='dc_source')
    item_id = indexes.CharField(model_attr='id')
    
    def get_model(self):
        return item

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
    
class pathIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    path_id = indexes.CharField(model_attr='id')
    path_uri = indexes.CharField(model_attr='uri')
    path_dc_title = indexes.CharField(model_attr='dc_title')
    path_dc_subject = indexes.CharField(model_attr='dc_subject')
    path_dc_description = indexes.CharField(model_attr='dc_description')
    path_lom_length = indexes.CharField(model_attr='lom_length')
    path_thumbnail = indexes.CharField(model_attr='paths_thumbnail')
    
    def get_model(self):
        return path

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
   
