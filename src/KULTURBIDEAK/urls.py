from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
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
    (r'^search/', include('haystack.urls')),
    
    #url(r'^rosetta/', include('rosetta.urls')),
    
 
    
      
)

#if 'rosetta' in settings.INSTALLED_APPS:
    # urlpatterns += patterns('',
    #url(r'^rosetta/', include('rosetta.urls')),
#)

