import datetime
from haystack import indexes
from KULTURBIDEAK.kulturbideak_app.models import item
from KULTURBIDEAK.kulturbideak_app.models import path


class itemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/indexes/kulturbideak_app/item_text.txt')
    dc_title = indexes.CharField(model_attr='dc_title')
    dc_subject = indexes.CharField(model_attr='dc_subject')
    dc_description = indexes.CharField(model_attr='dc_description')
    dc_creator = indexes.CharField(model_attr='dc_creator')
    dc_language = indexes.CharField(model_attr='dc_language')
    dc_date = indexes.CharField(model_attr='dc_date')
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
    proposatutakoa = indexes.BooleanField(model_attr='proposatutakoa')
    egunekoa = indexes.BooleanField(model_attr='egunekoa')
    aberastua = indexes.BooleanField(model_attr='aberastua')
    ob_language = indexes.CharField(model_attr='ob_language')
    ob_thumbnail = indexes.CharField(model_attr='ob_thumbnail')
    #item_user_id = indexes.CharField(model_attr='fk_ob_user')
    item_user_id =indexes.EdgeNgramField(use_template=True,template_name='search/indexes/kulturbideak_app/item_user.txt')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='dc_title')
    #item_autocomp = indexes.EdgeNgramField(model_attr='dc_title')
    #content_auto = indexes.EdgeNgramField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text.txt')
    
    
    # LANGUAGE FIELDS:
    text_eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_eu.txt')
    #title_eu=indexes.CharField()
    #description_eu=indexes.CharField()
    #subject_eu=indexes.CharField()
    
    text_eu2es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_eu2es.txt')
    #title_eu2es=indexes.CharField()
    #description_eu2es=indexes.CharField()
    #subject_eu2es=indexes.CharField()
    
    text_eu2en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_eu2en.txt')
    #title_eu2en=indexes.CharField()
    #description_eu2en=indexes.CharField()
    #subject_eu2en=indexes.CharField()
    
    
    text_es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_es.txt')
    #title_es=indexes.CharField()
    #description_es=indexes.CharField()
    #subject_es=indexes.CharField()
    
    text_es2eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_es2eu.txt')
    #title_es2eu=indexes.CharField()
    #description_es2eu=indexes.CharField()
    #subject_es2eu=indexes.CharField()
    
    text_es2en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_es2en.txt')
    #title_es2en=indexes.CharField()
    #description_es2en=indexes.CharField()
    #subject_es2en=indexes.CharField()
    
    
    text_en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_en.txt')
    #title_en=indexes.CharField()
    #description_en=indexes.CharField()
    #subject_en=indexes.CharField()
    
    text_en2eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_en2eu.txt')
    #title_en2eu=indexes.CharField()
    #description_en2eu=indexes.CharField()
    #subject_en2eu=indexes.CharField()
    
    text_en2es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/item_text_en2es.txt')
    #title_en2es=indexes.CharField()
    #description_en2es=indexes.CharField()
    #subject_en2es=indexes.CharField()
    
    
    def get_model(self):
        return item

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()
    
    
class pathIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True , template_name='search/indexes/kulturbideak_app/path_text.txt')
    path_id = indexes.CharField(model_attr='id')
    #path_fk_user_id = indexes.CharField(model_attr='fk_user_id')
    path_fk_user_id =indexes.EdgeNgramField(use_template=True,template_name='search/indexes/kulturbideak_app/path_user.txt')  
    path_uri = indexes.CharField(model_attr='uri')
    path_dc_title = indexes.CharField(model_attr='dc_title')
    path_dc_subject = indexes.CharField(model_attr='dc_subject')
    path_dc_description = indexes.CharField(model_attr='dc_description')
    path_lom_length = indexes.CharField(model_attr='lom_length')
    path_thumbnail = indexes.CharField(model_attr='paths_thumbnail')
    language = indexes.CharField(model_attr='language')
    path_creation_date  = indexes.DateField(model_attr='creation_date')
    path_proposatutakoa = indexes.BooleanField(model_attr='proposatutakoa')
    path_egunekoa = indexes.BooleanField(model_attr='egunekoa')
    acces =  indexes.CharField(model_attr='acces')
    
     # We add this for autocomplete.
    #path_autocomp = indexes.EdgeNgramField(model_attr='dc_title')
    
    # LANGUAGE FIELDS:
    text_eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_eu.txt')
       
    text_eu2es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_eu2es.txt')
     
    text_eu2en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_eu2en.txt')
           
    text_es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_es.txt')
       
    text_es2eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_es2eu.txt')
    
    text_es2en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_es2en.txt')
     
    text_en= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_en.txt')
      
    text_en2eu= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_en2eu.txt')
   
    text_en2es= indexes.CharField(use_template=True, template_name='search/indexes/kulturbideak_app/path_text_en2es.txt')
  
    
    def get_model(self):
        return path

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()
   

#site.register(item, itemIndex)
#site.register(path, pathIndex)
