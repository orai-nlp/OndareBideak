from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic import TemplateView
#from django.views.generic import direct_to_template
from kulturbideak_app import views
from KULTURBIDEAK.kulturbideak_app.views import kulturBideak
from KULTURBIDEAK.kulturbideak_app.views import hasiera
from KULTURBIDEAK.kulturbideak_app.views import erakutsi_item
from KULTURBIDEAK.kulturbideak_app.views import logina
from KULTURBIDEAK.kulturbideak_app.views import erregistratu
from KULTURBIDEAK.kulturbideak_app.views import itema_gehitu
from KULTURBIDEAK.kulturbideak_app.views import editatu_itema
from KULTURBIDEAK.kulturbideak_app.views import sortu_ibilbidea
from KULTURBIDEAK.kulturbideak_app.views import ajax_workspace_item_gehitu
from KULTURBIDEAK.kulturbideak_app.views import ajax_workspace_item_borratu
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_berria_gorde
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_node_gorde
from KULTURBIDEAK.kulturbideak_app.views import ajax_load_ws
from KULTURBIDEAK.kulturbideak_app.views import ajax_lortu_paths_list
from KULTURBIDEAK.kulturbideak_app.views import editatu_ibilbidea
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_eguneratu
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_node_eguneratu
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_irudia_gorde_proba
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_irudia_gorde
from KULTURBIDEAK.kulturbideak_app.views import ajax_path_irudia_eguneratu
from KULTURBIDEAK.kulturbideak_app.views import nire_itemak_erakutsi
from KULTURBIDEAK.kulturbideak_app.views import nire_ibilbideak_erakutsi
from KULTURBIDEAK.kulturbideak_app.views import perfila_erakutsi
from KULTURBIDEAK.kulturbideak_app.views import pasahitza_aldatu
from KULTURBIDEAK.kulturbideak_app.views import itemak_hasiera
from KULTURBIDEAK.kulturbideak_app.views import ibilbideak_hasiera
from KULTURBIDEAK.kulturbideak_app.views import hornitzaileak_hasiera
from KULTURBIDEAK.kulturbideak_app.views import nabigazio_item
from KULTURBIDEAK.kulturbideak_app.views import nabigatu
from KULTURBIDEAK.kulturbideak_app.views import botoa_eman_item
from KULTURBIDEAK.kulturbideak_app.views import botoa_kendu_item
from KULTURBIDEAK.kulturbideak_app.views import botoa_eman_path
from KULTURBIDEAK.kulturbideak_app.views import botoa_kendu_path
from KULTURBIDEAK.kulturbideak_app.views import nabigazioa_hasi
from KULTURBIDEAK.kulturbideak_app.views import ajax_lortu_most_voted_paths
from KULTURBIDEAK.kulturbideak_app.views import ajax_lortu_eguneko_itema
from KULTURBIDEAK.kulturbideak_app.views import cross_search
from KULTURBIDEAK.kulturbideak_app.views import autoplay_hasieratik
from KULTURBIDEAK.kulturbideak_app.views import autocomplete
from KULTURBIDEAK.kulturbideak_app.views import oaipmh_datubilketa
from KULTURBIDEAK.kulturbideak_app.views import hornitzaile_search
from KULTURBIDEAK.kulturbideak_app.views import filtro_search
from KULTURBIDEAK.kulturbideak_app.views import eguneko_itemak
from KULTURBIDEAK.kulturbideak_app.views import eguneko_itema_kendu
from KULTURBIDEAK.kulturbideak_app.views import eguneko_itema_gehitu
from KULTURBIDEAK.kulturbideak_app.views import hornitzaile_fitxa_editatu
#from KULTURBIDEAK.kulturbideak_app.views import brandy
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_arloa
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_where
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_izena
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_deskribapena
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_kokalekua
from KULTURBIDEAK.kulturbideak_app.views import ajax_hornitzaile_irudia_gorde
from KULTURBIDEAK.kulturbideak_app.views import ajax_hornitzaile_argazkia_gorde
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_telefonoa
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_emaila
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_website
from KULTURBIDEAK.kulturbideak_app.views import ajax_edit_ordutegia
from KULTURBIDEAK.kulturbideak_app.views import fitxa_gorde
from KULTURBIDEAK.kulturbideak_app.views import hornitzailea_ikusi
from KULTURBIDEAK.kulturbideak_app.views import ajax_lortu_eguneko_ibilbidea
from KULTURBIDEAK.kulturbideak_app.views import eguneko_ibilbideak
from KULTURBIDEAK.kulturbideak_app.views import azkeneko_itemak
from KULTURBIDEAK.kulturbideak_app.views import azkeneko_ibilbideak
from KULTURBIDEAK.kulturbideak_app.views import ezabatu_ibilbidea
from KULTURBIDEAK.kulturbideak_app.views import ezabatu_itema
from KULTURBIDEAK.kulturbideak_app.views import eguneko_ibilbidea_gehitu
from KULTURBIDEAK.kulturbideak_app.views import eguneko_ibilbidea_kendu

from django.contrib import admin

#MAddalen
from haystack.views import SearchView

from django.contrib.staticfiles import views
from django.conf.urls.static import static
 
#Hasieran patterns-etan hasieran string hutsaren ordez 'haystack.views' neukan

admin.autodiscover()


urlpatterns = patterns('',
    #url(r'rosetta/', include('rosetta.urls')),              
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'uploads/(?P<path>.*)$', views.serve),
    url(r'uploads/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
   #url(r'^$', SearchView(), name='haystack_search'),
    url(r'^$', hasiera),
    #url(r'brandy', brandy),
    url(r'eguneko_itema_gehitu',eguneko_itema_gehitu),  
    #url(r'search', SearchView(), name='haystack_search'), 
    url(r'cross_search', cross_search),
    url(r'login', logina),
    url(r'erregistratu$', erregistratu),
    url(r'perfila_erakutsi', perfila_erakutsi), 
    url(r'pasahitza_aldatu', pasahitza_aldatu),     
    (r'irten/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'itema_gehitu$', itema_gehitu),
    url(r'editatu_itema$', editatu_itema),     
    url(r'sortu_ibilbidea$', sortu_ibilbidea),
    url(r'erakutsi_item', erakutsi_item),
    url(r'ajax_workspace_item_gehitu$', ajax_workspace_item_gehitu),
    url(r'ajax_workspace_item_borratu$', ajax_workspace_item_borratu),
    url(r'ajax_path_berria_gorde$', ajax_path_berria_gorde),
    url(r'ajax_path_node_gorde$', ajax_path_node_gorde),
    url(r'ajax_lortu_paths_list$', ajax_lortu_paths_list),
    url(r'editatu_ibilbidea', editatu_ibilbidea),
    url(r'ajax_path_eguneratu$', ajax_path_eguneratu),
    url(r'ajax_path_node_eguneratu$', ajax_path_node_eguneratu), 
    url(r'ajax_path_irudia_gorde_proba$', ajax_path_irudia_gorde_proba),  
    url(r'ajax_path_irudia_gorde$', ajax_path_irudia_gorde),
    url(r'ajax_path_irudia_eguneratu$', ajax_path_irudia_eguneratu), 
    url(r'ajax_load_ws', ajax_load_ws),    
    url(r'nire_itemak_erakutsi$', nire_itemak_erakutsi), 
    url(r'nire_ibilbideak_erakutsi$', nire_ibilbideak_erakutsi),
    url(r'itemak_hasiera$', itemak_hasiera),
    url(r'ibilbideak_hasiera$', ibilbideak_hasiera),
    url(r'hornitzaileak_hasiera$', hornitzaileak_hasiera),
    url(r'nabigazio_item', nabigazio_item),
    url(r'nabigatu', nabigatu),
    url(r'botoa_eman_item', botoa_eman_item),
    url(r'botoa_kendu_item', botoa_kendu_item),   
    url(r'botoa_eman_path', botoa_eman_path),
    url(r'botoa_kendu_path', botoa_kendu_path), 
    url(r'nabigazioa_hasi', nabigazioa_hasi),
    url(r'ajax_lortu_most_voted_paths', ajax_lortu_most_voted_paths),
    url(r'ajax_lortu_eguneko_itema', ajax_lortu_eguneko_itema),   
    url(r'autoplay_hasieratik', autoplay_hasieratik),
    url(r'autocomplete', autocomplete),
    url(r'oaipmh_datubilketa',oaipmh_datubilketa),
    url(r'hornitzaile_search',hornitzaile_search),
    url(r'filtro_search',filtro_search),
    url(r'eguneko_itemak',eguneko_itemak),
    url(r'eguneko_itema_kendu',eguneko_itema_kendu),
    url(r'hornitzaile_fitxa_editatu',hornitzaile_fitxa_editatu), 
    url(r'ajax_edit_arloa',ajax_edit_arloa), 
    url(r'ajax_edit_where',ajax_edit_where),
    url(r'ajax_edit_izena',ajax_edit_izena), 
    url(r'ajax_edit_deskribapena',ajax_edit_deskribapena), 
    url(r'ajax_edit_kokalekua',ajax_edit_kokalekua), 
    url(r'ajax_hornitzaile_irudia_gorde',ajax_hornitzaile_irudia_gorde),
    url(r'ajax_hornitzaile_argazkia_gorde',ajax_hornitzaile_argazkia_gorde),
    url(r'ajax_edit_telefonoa',ajax_edit_telefonoa),
    url(r'ajax_edit_emaila',ajax_edit_emaila),
    url(r'ajax_edit_website',ajax_edit_website), 
    url(r'ajax_edit_ordutegia',ajax_edit_ordutegia), 
    url(r'fitxa_gorde',fitxa_gorde),
    url(r'hornitzailea_ikusi',hornitzailea_ikusi),
    url(r'ajax_lortu_eguneko_ibilbidea',ajax_lortu_eguneko_ibilbidea),
    url(r'eguneko_ibilbideak',eguneko_ibilbideak),
    url(r'azkeneko_itemak',azkeneko_itemak),
    url(r'azkeneko_ibilbideak',azkeneko_ibilbideak),
    url(r'ezabatu_ibilbidea',ezabatu_ibilbidea),
    url(r'ezabatu_itema',ezabatu_itema),
    url(r'eguneko_ibilbidea_gehitu',eguneko_ibilbidea_gehitu),
    url(r'eguneko_ibilbidea_kendu',eguneko_ibilbidea_kendu),
            
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
                               
    (r'^search/', include('haystack.urls')),
    
    #url(r'^rosetta/', include('rosetta.urls')),
    
 
    
      
)

#if 'rosetta' in settings.INSTALLED_APPS:
    # urlpatterns += patterns('',
    #url(r'^rosetta/', include('rosetta.urls')),
#)

