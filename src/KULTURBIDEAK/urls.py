from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic import TemplateView
#from django.views.generic import direct_to_template
from kulturbideak_app import views as ob_views
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
    url(r'^$', ob_views.hasiera),
    #url(r'search', SearchView(), name='haystack_search'), 
    url(r'cross_search', ob_views.cross_search),
    url(r'^login$', ob_views.logina),
    url(r'erregistratu$', ob_views.erregistratu),
    url(r'perfila_erakutsi', ob_views.perfila_erakutsi), 
    url(r'pasahitza_aldatu', ob_views.pasahitza_aldatu),     
    (r'irten/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'itema_gehitu$', ob_views.itema_gehitu),
    url(r'editatu_itema$', ob_views.editatu_itema),     
    url(r'sortu_ibilbidea$', ob_views.sortu_ibilbidea),
    url(r'erakutsi_item', ob_views.erakutsi_item),
    url(r'ajax_workspace_item_gehitu$', ob_views.ajax_workspace_item_gehitu),
    url(r'ajax_workspace_item_borratu$', ob_views.ajax_workspace_item_borratu),
    url(r'ajax_path_berria_gorde$', ob_views.ajax_path_berria_gorde),
    url(r'ajax_path_node_gorde$', ob_views.ajax_path_node_gorde),
    url(r'ajax_lortu_paths_list$', ob_views.ajax_lortu_paths_list),
    url(r'editatu_ibilbidea', ob_views.editatu_ibilbidea),
    url(r'ajax_path_eguneratu$', ob_views.ajax_path_eguneratu),
    url(r'ajax_path_node_eguneratu$', ob_views.ajax_path_node_eguneratu), 
    url(r'ajax_path_irudia_gorde_proba$', ob_views.ajax_path_irudia_gorde_proba),  
    url(r'ajax_path_irudia_gorde$', ob_views.ajax_path_irudia_gorde),
    url(r'ajax_path_irudia_eguneratu$', ob_views.ajax_path_irudia_eguneratu), 
    url(r'ajax_load_ws', ob_views.ajax_load_ws),    
    url(r'nire_itemak_erakutsi$', ob_views.nire_itemak_erakutsi), 
    url(r'nire_ibilbideak_erakutsi$', ob_views.nire_ibilbideak_erakutsi),
    url(r'itemak_hasiera$', ob_views.itemak_hasiera),
    url(r'ibilbideak_hasiera$', ob_views.ibilbideak_hasiera),
    url(r'hornitzaileak_hasiera$', ob_views.hornitzaileak_hasiera),
    url(r'nabigazio_item', ob_views.nabigazio_item),
    url(r'nabigatu', ob_views.nabigatu),
    url(r'botoa_eman_item', ob_views.botoa_eman_item),
    url(r'botoa_kendu_item', ob_views.botoa_kendu_item),   
    url(r'botoa_eman_path', ob_views.botoa_eman_path),
    url(r'botoa_kendu_path', ob_views.botoa_kendu_path), 
    url(r'ajax_egunekoa_aldatu_item',ob_views.ajax_egunekoa_aldatu_item),
    url(r'ajax_egunekoa_aldatu_path',ob_views.ajax_egunekoa_aldatu_path),
    url(r'ajax_egunekoak',ob_views.ajax_egunekoak),
    url(r'nabigazioa_hasi', ob_views.nabigazioa_hasi),
    url(r'ajax_lortu_most_voted_paths', ob_views.ajax_lortu_most_voted_paths),
    url(r'autoplay_hasieratik', ob_views.autoplay_hasieratik),
    url(r'autocomplete', ob_views.autocomplete),
    url(r'oaipmh_datubilketa',ob_views.oaipmh_datubilketa),
    url(r'hornitzaile_search',ob_views.hornitzaile_search),
    url(r'filtro_search',ob_views.filtro_search),
    url(r'admin_reset_user_password',ob_views.admin_reset_user_password),
    url(r'admin_hornitzaile_fitxa_editatu',ob_views.admin_hornitzaile_fitxa_editatu),
    url(r'admin_erabiltzaileak_kudeatu',ob_views.admin_erabiltzaileak_kudeatu), 
    url(r'admin_berriak_kudeatu',ob_views.admin_berriak_kudeatu),
    url(r'admin_eguneko_hornitzaileak_kudeatu',ob_views.admin_eguneko_hornitzaileak_kudeatu),
    url(r'admin_hornitzaile_bihurtu',ob_views.admin_hornitzaile_bihurtu),
    url(r'hornitzaile_fitxa_editatu',ob_views.hornitzaile_fitxa_editatu), 
    url(r'ajax_edit_arloa',ob_views.ajax_edit_arloa), 
    url(r'ajax_edit_where',ob_views.ajax_edit_where),
    url(r'ajax_edit_izena',ob_views.ajax_edit_izena), 
    url(r'ajax_edit_deskribapena',ob_views.ajax_edit_deskribapena), 
    url(r'ajax_edit_kokalekua',ob_views.ajax_edit_kokalekua), 
    url(r'ajax_hornitzaile_irudia_gorde',ob_views.ajax_hornitzaile_irudia_gorde),
    url(r'ajax_hornitzaile_argazkia_gorde',ob_views.ajax_hornitzaile_argazkia_gorde),
    url(r'ajax_edit_telefonoa',ob_views.ajax_edit_telefonoa),
    url(r'ajax_edit_emaila',ob_views.ajax_edit_emaila),
    url(r'ajax_edit_website',ob_views.ajax_edit_website), 
    url(r'ajax_edit_ordutegia',ob_views.ajax_edit_ordutegia), 
    url(r'fitxa_gorde',ob_views.fitxa_gorde),
    url(r'azkeneko_itemak',ob_views.azkeneko_itemak),
    url(r'azkeneko_ibilbideak',ob_views.azkeneko_ibilbideak),
    url(r'ezabatu_ibilbidea',ob_views.ezabatu_ibilbidea),
    url(r'ezabatu_itema',ob_views.ezabatu_itema),
    url(r'ajax_path_edizio_aukerak_aldatu',ob_views.ajax_path_edizio_aukerak_aldatu), 
    url(r'erab_form',ob_views.get_user),
    url(r'berria_form',ob_views.get_berria),
    
    
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
                               
    (r'^search/', include('haystack.urls')),
    
    #url(r'^rosetta/', include('rosetta.urls')),
    
 
    
      
)

#if 'rosetta' in settings.INSTALLED_APPS:
    # urlpatterns += patterns('',
    #url(r'^rosetta/', include('rosetta.urls')),
#)

