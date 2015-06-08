# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _,get_language
from itertools import islice, chain
from django.utils import simplejson
from django.template import Context, Template
from django.contrib.auth.decorators import user_passes_test

#from utils import *
from django.core.paginator import Paginator

from django.views.decorators.cache import cache_page

#MADDALEN
from django.http import HttpResponse
from django.shortcuts import render_to_response
from KULTURBIDEAK.kulturbideak_app.models import item
from KULTURBIDEAK.kulturbideak_app.models import path
from KULTURBIDEAK.kulturbideak_app.models import workspace_item
from django.contrib.auth.models import User
from KULTURBIDEAK.kulturbideak_app.forms import *
from KULTURBIDEAK.kulturbideak_app.models import *
from haystack.management.commands import update_index
from KULTURBIDEAK.settings import *

from django.utils.translation import ugettext as _

#from django.template.context_processors import csrf
#MADDALEN
#from haystack.forms import ModelSearchForm, HighlightedSearchForm
#from haystack.query import SearchQuerySet
#from haystack.views import SearchView, search_view_factory
#from KULTURBIDEAK.kulturbideak_app.models import item

#from array import array

import os
import subprocess
import sys

import urllib 
import tempfile

import datetime
import string


def get_tree(el_node):
    
    nodes = [el_node]
    if el_node.paths_next != "":
        for child_node_id in el_node.paths_next.split(","):
            nodes = nodes + get_tree(node.objects.filter(fk_item_id_id=child_node_id, fk_path_id_id=el_node.fk_path_id_id)[0])
    return nodes

def editatu_ibilbidea(request):
    
    if 'id' in request.GET:
        id=request.GET['id']
    
        #lortu path-aren ezaugarriak
        ibilbidea = path.objects.get(id=id)
        titulua=ibilbidea.dc_title
        deskribapena=ibilbidea.dc_description
        irudia=ibilbidea.paths_thumbnail
        
        
        #path hasierak hartu
       # nodes = []
     #   path_starts = Node.objects.filter(prev=="")
     #   for path_start in path_starts:
     #       nodes = nodes + get_tree(path_start)
            
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id_id=id,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
            
        
        
        '''path_nodeak=[]
        for node in nodes:
         
            sarrera=str(node.fk_item_id_id)+";"+node.dc_title+";"+node.paths_thumbnail+";"+node.paths_prev+";"+node.paths_next
            path_nodeak+=[sarrera]
            # print "ERROA:"+sarrera'''
            
    
    
    return render_to_response('editatu_ibilbidea.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))



def erakutsi_item(request):
    
    
    if 'id' in request.GET:
        id=request.GET['id']
        
        item_tupla = item.objects.get(pk=id)
        titulua=item_tupla.dc_title
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.uri
        irudia=item_tupla.edm_object
        hornitzailea=item_tupla.edm_provider
        
        return render_to_response('item.html',{'id':id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea},context_instance=RequestContext(request))    

def login_egin_(request):
    """Erabiltzailea logeatzen du"""
    if request.POST:
        l=LoginForm(request.POST)
        if l.is_valid():
            cd=l.cleaned_data
            username = cd['erabiltzailea']
            password = cd['pasahitza']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return True
    return False



def logina(request):
    
    #!! Workspace bat sortu
    #Datu-basean: workspace eta usr_workspace taula eguneratu behar dira
    logina=LoginForm(request.POST)
   # return render_to_response('logina.html',{'logina':logina},context_instance=RequestContext(request))
    if logina.is_valid():
        login_egin_(request)
        return render_to_response('base.html',context_instance=RequestContext(request))
    else:
        logina=LoginForm()
        return render_to_response('logina.html',{'logina':logina},context_instance=RequestContext(request))
   
def handle_uploaded_file(f,izena):
    with open(MEDIA_ROOT+'/'+izena, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def itema_gehitu(request):
    
    itema=ItemGehituForm(request.POST, request.FILES)
    
    if itema.is_valid():
        #Datu-basean item-a gehitu
        
        azken_id = item.objects.latest('id').id
        azken_id += 1
        dc_title=request.POST['titulua']
        uri="uri_"+ str(azken_id)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        print request.POST
        edm_object=request.FILES['irudia'].name
        irudia_url=MEDIA_URL+edm_object
      
        dc_language=request.POST['hizkuntza']
        edm_language=request.POST['hizkuntza']
        if(dc_language==1):
            dc_language="Euskera"
            edm_language="Euskera"
        elif(dc_language==2):
            dc_language="Ingelesa"
            edm_language="Ingelesa"            
        else:
            dc_language="Gaztelania"
            edm_language="Gaztelania"
         
        
        dc_creator="Euskomedia" # ondoren logeatutako erabiltzailea jarri
        #Gaurko data hartu
        dc_date=datetime.datetime.now()
        #Irudia igo
        handle_uploaded_file(request.FILES['irudia'],edm_object)
        
        item_berria = item(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,dc_creator=dc_creator, dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url)
        item_berria.save()   
         
        #Haystack update_index EGIN!!!
        update_index.Command().handle()
         
        return render_to_response('base.html',{'mezua':"item berria gehitu da"},context_instance=RequestContext(request))
    else:
        itema=ItemGehituForm()
        return render_to_response('itema_gehitu.html',{'itema':itema},context_instance=RequestContext(request))
   

def erregistratu(request):
    
    print request.POST['erabIzena']
    if 'pasahitza' in request.POST:
        #Datu-basean erabiltzaile berria sartu
        print request.POST
        
        izena=request.POST['erabIzena']
        posta=request.POST['posta']
        pasahitza=request.POST['pasahitza']
         
        user = User.objects.create_user(izena, posta, pasahitza)
        
        return render_to_response('base.html',context_instance=RequestContext(request))
    else:
        return render_to_response('erregistratu.html',context_instance=RequestContext(request))    


def sortu_ibilbidea(request):
    
   
    fk_usr_id=1
        
    fk_workspace_id=1
    ws_item_zerrenda=workspace_item.objects.filter(fk_workspace_id=1)
   
   
    #azken_id = path.objects.latest('id').id
    # azken_id += 1
  
   
    
    # uri="uri_"+ str(azken_id)
    #dc_title="dc_title_"+ str(azken_id)
    # dc_subject="dc_subject_"+ str(azken_id)
    # dc_description="dc_description_"+ str(azken_id)
    # acces="acces_"+ str(azken_id)
    # lom_length=1
    #isdeleted=False
    #paths_status="public"
    #paths_thumbnail = "paths_thumbnail" + str(azken_id)
    #paths_iscloneable = True
   # tstamp =datetime.datetime.now()
    
    
    #ibilbide_berria = path(id=azken_id, 
    #fk_user_id_id=1,
    #uri=uri, 
    #dc_title=dc_title,
    #dc_subject=dc_subject,
    #dc_description=dc_description,
    #acces=acces,
    #lom_length=lom_length,
    #isdeleted=isdeleted,
    #paths_status=paths_status,
    #paths_thumbnail=paths_thumbnail,
    #paths_iscloneable=paths_iscloneable,
    #tstamp=tstamp )
    
    #ibilbide_berria.save()   
         
   
    
    return render_to_response('sortu_ibilbidea.html',{'ws_item_zerrenda': ws_item_zerrenda},context_instance=RequestContext(request))

def ajax_load_ws(request):
    
    fk_usr_id=request.POST['user_id']
        
    fk_workspace_id=request.POST['ws_id']
    ws_item_zerrenda=workspace_item.objects.filter(fk_workspace_id=fk_workspace_id)
    return render_to_response('workspace_items.xml', {'items': ws_item_zerrenda}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_lortu_paths_list(request):
    
    fk_usr_id=request.POST['user_id']
    
    user_path_zerrenda=path.objects.filter(fk_user_id_id=fk_usr_id)
    return render_to_response('ibilbide_lista.xml', {'paths': user_path_zerrenda}, context_instance=RequestContext(request), mimetype='application/xml')



def gorde_ibilbidea(request):

    #Haystack update_index EGIN!!!
    update_index.Command().handle()
    
    return render_to_response('base.html',{'mezua':"Ibilbide berria sortu da"},context_instance=RequestContext(request))
    
def ajax_workspace_item_gehitu(request):
    
    #0: unknown error; else: workspace item created;
    fk_usr_id=1
        
    request_answer= 0
    if request.is_ajax() and request.method == 'POST':
                 
        item_id=request.POST.get('item_id')
        fk_workspace_id=request.POST.get('fk_workspace_id')
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        thumbnail=request.POST.get('paths_thumbnail')
    
        #azken_id = workspace_item.objects.latest('id').id
        # azken_id += 1
        #fk_workspace_id_id = workspace.objects.filter(id=fk_workspace_id),
        
       
        ws_item_berria = workspace_item(fk_item_id_id=item_id,
                                        uri =uri,
                                        fk_workspace_id_id = fk_workspace_id,
                                        dc_source = dc_source,
                                        dc_title = dc_title,
                                        dc_description = dc_description,
                                        type = type,
                                        paths_thumbnail = thumbnail)
    
    
        ws_item_berria.save()
        request_answer = ws_item_berria.fk_item_id_id
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_workspace_item_borratu(request):
    request_answer= 0
    if request.is_ajax() and request.method == 'POST':
                 
        item_id=request.POST.get('item_id')
        #workspace_item.objects.filter(id=item_id).delete()
        workspace_item.objects.filter(fk_item_id_id=item_id).delete()
      
        request_answer = item_id
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_berria_gorde(request):
    
    request_answer= 0
    
    if request.is_ajax() and request.method == 'POST':
        
        fk_usr_id=1

        uri=request.POST.get('uri')
        dc_title=request.POST.get('dc_title')
        dc_subject=request.POST.get('dc_subject')
        dc_description=request.POST.get('dc_description')
        paths_thumbnail = request.POST.get('paths_thumbnail')
    
        #azken_id = path.objects.latest('id').id
        #azken_id += 1
      
        path_berria = path(fk_user_id_id = fk_usr_id,
                                        uri =uri,
                                        dc_title = dc_title,
                                        dc_subject = dc_subject,
                                        dc_description = dc_description,
                                        paths_thumbnail = paths_thumbnail)
    
    
        path_berria.save()
        request_answer = path_berria.id  
        
        #Haystack update_index EGIN!!!
        update_index.Command().handle()
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_eguneratu(request):
    
    request_answer =request.POST.get('path_id')

    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_node_gorde(request):
    
    request_answer= 0
    
    if request.is_ajax() and request.method == 'POST':
        
        
       
        fk_path_id_id=request.POST.get('path_id')
        fk_item_id_id=request.POST.get('item_id')
        print fk_item_id_id
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')     
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        paths_prev = request.POST.get('paths_prev')
        paths_next = request.POST.get('paths_next')
        paths_start = (int(request.POST.get('paths_start')) > 0)
    
        
      
        node_berria = node(#id=azken_id,
                           fk_item_id_id=fk_item_id_id,
                           uri =uri,
                           fk_path_id_id = fk_path_id_id,
                           dc_source = dc_source,   
                           dc_title = dc_title,
                           dc_description = dc_description,
                           type = type,
                           paths_thumbnail = paths_thumbnail,
                           paths_prev=paths_prev,
                           paths_next = paths_next,
                           paths_start = paths_start)
        
    
        node_berria.save()
        request_answer = node_berria.fk_item_id_id
        
        
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_node_eguneratu(request):
    
    request_answer= 0
    
    if request.is_ajax() and request.method == 'POST':
        
        
       
        fk_path_id_id=request.POST.get('path_id')
        fk_item_id_id=request.POST.get('item_id')
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')     
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        paths_prev = request.POST.get('paths_prev')
        paths_next = request.POST.get('paths_next')
        paths_start = (int(request.POST.get('paths_start')) > 0)
    
            
        nodea=node.objects.get(fk_item_id_id=fk_item_id_id,
                               fk_path_id_id = fk_path_id_id
                               )
      
        
        node_id=nodea.id
  
        node_eguneratua = node(id=node_id,
                           fk_item_id_id=fk_item_id_id,
                           uri =uri,
                           fk_path_id_id = fk_path_id_id,
                           dc_source = dc_source,   
                           dc_title = dc_title,
                           dc_description = dc_description,
                           type = type,
                           paths_thumbnail = paths_thumbnail,
                           paths_prev=paths_prev,
                           paths_next = paths_next,
                           paths_start = paths_start)
        
    
        node_eguneratua.save()
        request_answer = node_eguneratua.fk_item_id_id
        
        
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')
    
    
def kulturBideak(request):
    #return HttpResponse("Kaixo, kulturBideak Webgunean zaude.")
   
    return render_to_response('kulturBideak.html',{'galdera':'gako hitzak sartu'},context_instance=RequestContext(request))    
#def galdetu_wikipedia(request):
    # #print request.POST
    # if 'galdera' in request.POST:
    #     return erantzuna_lortu(request)
    #   if 'sparql' in request.POST:
    #      return erantzuna_lortu_sparql(request)
    # else:
    #     return render_to_response('galdetu.html',{'galdera':'Non jaio zen Ruper Ordorika?'})
    ##return  HttpResponse("Galdetu eta erantzuna jaso.")

def solr_erantzuna_lortu(request):
    
   
    galdera=request.POST['galdera']

    #solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)
    #erantzuna=pysolr.search(galdera)
    #erantzuna= erantzuna.communicate()[0]
    erantzuna="kaka"
   # print {'erantzuna': erantzuna}

    return render_to_response('kulturBideak.html',{'erantzuna': erantzuna},context_instance=RequestContext(request))

