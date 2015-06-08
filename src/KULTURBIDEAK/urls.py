from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from kulturbideak_app import views
from KULTURBIDEAK.kulturbideak_app.views import kulturBideak
from KULTURBIDEAK.kulturbideak_app.views import erakutsi_item
from KULTURBIDEAK.kulturbideak_app.views import logina
from KULTURBIDEAK.kulturbideak_app.views import erregistratu
from KULTURBIDEAK.kulturbideak_app.views import itema_gehitu
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
    #url(r'^kulturBideak/', include("haystack.urls")),
   # url(r'^$', include('haystack.urls')),
   # url(r'^$', SearchView(), name='haystack_search'),
    #url(r'^kulturBideak/', include("urls")),
    #url(r'^$',kulturBideak ),
    # url(r'^$', include('haystack.urls')),
    url(r'^$', SearchView(), name='haystack_search'), 
    url(r'^login', logina),
    url(r'^erregistratu', erregistratu),
    url(r'itema_gehitu$', itema_gehitu), 
    url(r'sortu_ibilbidea$', sortu_ibilbidea),
    url(r'^search/erakutsi_item', erakutsi_item),
    url(r'ajax_workspace_item_gehitu$', ajax_workspace_item_gehitu),
    url(r'ajax_workspace_item_borratu$', ajax_workspace_item_borratu),
    url(r'ajax_path_berria_gorde$', ajax_path_berria_gorde),
    url(r'ajax_path_node_gorde$', ajax_path_node_gorde),
    url(r'ajax_load_ws$', ajax_load_ws),
    url(r'ajax_lortu_paths_list$', ajax_lortu_paths_list),
    url(r'editatu_ibilbidea', editatu_ibilbidea),
    url(r'ajax_path_eguneratu$', ajax_path_eguneratu),
    url(r'ajax_path_node_eguneratu$', ajax_path_node_eguneratu),   
    (r'^search/', include('haystack.urls')),
    #url(r'^rosetta/', include('rosetta.urls')),
      
)

#if 'rosetta' in settings.INSTALLED_APPS:
    # urlpatterns += patterns('',
    #url(r'^rosetta/', include('rosetta.urls')),
#)

