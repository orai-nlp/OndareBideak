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

##### LOGIN ETA ERREGISTRO FUNTZIOAkK #####  

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
        return render_to_response('base.html',{'mezua':"Ongi etorri Kulturbideak sistemara"},context_instance=RequestContext(request))
    else:
        logina=LoginForm()
        return render_to_response('logina.html',{'logina':logina},context_instance=RequestContext(request))
  
 
def erregistratu(request):
    """Erabiltzaile bat sisteman erregistratzen du"""
   
    erabiltzailea_form=CreateUserForm()
    #bilaketa_form=Bilaketa_arrunta_F()
    
    if 'Erabiltzailea_gehitu' in request.POST:       
        erabiltzailea_form=CreateUserForm(request.POST)
        if erabiltzailea_form.is_valid():
            cd=erabiltzailea_form.cleaned_data
            
            if db_erregistratu_erabiltzailea(cd):
               
                new_user = authenticate(username=cd["username"],password=cd["password"],email=cd["posta"])
                #return redirect("/search")
                return render_to_response('base.html',{'mezua':"Kulturbideak sisteman Erregistaru zara"},context_instance=RequestContext(request))
   
        else:
            #return render_to_response("izena_eman.html",{"bilaketa":bilaketa_form,"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
            return render_to_response("erregistratu.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
    return render_to_response("erregistratu.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))

def db_erregistratu_erabiltzailea(cd):
    """Erabiltzaile bat erregistratzen du"""
   
    try:
        
        #erabiltzailea=usr.objects.create_user(cd["username"], cd["posta"], cd["password"])
        erabiltzailea=User.objects.create_user(cd["username"], cd["posta"], cd["password"])
        erabiltzailea.first_name=cd['izena']
        erabiltzailea.last_name=cd['abizena']
        erabiltzailea.save()
        #if cd["erabiltzaile_mota"]!='':
            #g=Group.objects.get(name=cd["erabiltzaile_mota"])
        #else:
            # g=Group.objects.get(name='editorea')
        # g.user_set.add(erabiltzailea)
        # g.save()
        
        return True
    except Exception as a:
        print "datu-basean ez da ondo erregistratu"
        print a
        #erabiltzailea.delete()
        #g.delete()
        return False



def db_erregistratu_erabiltzailea_Iker(cd):
    """Erabiltzaile bat erregistratzen du"""
    try:
        erabiltzailea=Erabiltzaileak.objects.create_user(cd["username"], cd["posta"], cd["password"])
        erabiltzailea.first_name=cd['izena']
        erabiltzailea.last_name=cd['abizena']
        erabiltzailea.save()
        if cd["erabiltzaile_mota"]!='':
            g=Group.objects.get(name=cd["erabiltzaile_mota"])
        else:
            g=Group.objects.get(name='editorea')
        g.user_set.add(erabiltzailea)
        g.save()
        
        return True
    except Exception as a:
        print a
        #erabiltzailea.delete()
        #g.delete()
        return False
 
 
def perfila_erakutsi(request):
    """Erabiltzaile baten perfila erakutsi eta editatzeko aukera ematen du"""
    
    """Datu-basetik kargatzen dira datuak"""
    erabID=request.user.id
    erabiltzaile_tupla= User.objects.get(id=erabID)
    izena=erabiltzaile_tupla.first_name
    abizena=erabiltzaile_tupla.last_name
    username=erabiltzaile_tupla.username
    posta=erabiltzaile_tupla.email
    #password=erabiltzaile_tupla.password
    erabiltzailea_form=UserProfileForm(initial={'izena':izena,'abizena': abizena, 'username': username, 'posta':posta})
        
   
    #erabiltzailea_form=UserProfileForm()
    #bilaketa_form=Bilaketa_arrunta_F()
    
    if 'Erabiltzailea_eguneratu' in request.POST:       
        erabiltzailea_form=UserProfileForm(request.POST)
        if erabiltzailea_form.is_valid():
            cd=erabiltzailea_form.cleaned_data
            
            if db_eguneratu_erabiltzailea(cd,request):
               
                #new_user = authenticate(username=cd["username"],password=cd["password"],email=cd["posta"])
                #return redirect("/search")
                return render_to_response('base.html',{'mezua':"Zure erabiltzaile Perfila eguneratu duzu"},context_instance=RequestContext(request))
   
        else:
            return render_to_response("perfila_erakutsi.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
    return render_to_response("perfila_erakutsi.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))

def db_eguneratu_erabiltzailea(cd,request):
    
    """Erabiltzaile baten perfila erakutsi eta editatzeko aukera ematen du"""
    userID=request.user.id

    erab_eguneratua = User(id=userID,
                           username = cd["username"],
                           first_name=cd["izena"],
                           last_name =cd["abizena"],
                           email = cd["posta"])
    
    
    erab_eguneratua.save()
    
    return True


def pasahitza_aldatu(request):
    
    """Erabiltzaileari pasahitza aldatzeko aukera ematen dio"""
    
    pasahitza_aldatu_form=ChangePasswordForm()
    
    if 'Pasahitza_aldatu' in request.POST:       
        pasahitza_aldatu_form=ChangePasswordForm(request.POST)
        if pasahitza_aldatu_form.is_valid():
            cd=pasahitza_aldatu_form.cleaned_data
            
            if db_pasahitza_aldatu(cd,request):
               
                #new_user = authenticate(username=cd["username"],password=cd["password"],email=cd["posta"])
                #return redirect("/search")
                return render_to_response('base.html',{'mezua':"Zure Pasahitza aldatu da"},context_instance=RequestContext(request))
   
        else:
            return render_to_response("pasahitza_aldatu.html",{"erabiltzailea":pasahitza_aldatu_form},context_instance=RequestContext(request))
    return render_to_response("pasahitza_aldatu.html",{"erabiltzailea":pasahitza_aldatu_form},context_instance=RequestContext(request))

def db_pasahitza_aldatu(cd,request):
    
    """Erabiltzaileari pasahitza aldatzeko aukera ematen dio"""

    erabID=request.user.id
    
    erabiltzaile_tupla= User.objects.get(id=erabID)
    #User.objects.filter(id=erabID).update(password = cd["password"])
    erabiltzaile_tupla.set_password(cd['password'])                   

    erabiltzaile_tupla.save()
    
    return True

##### BUKATU LOGIN ETA ERREGISTRO FUNTZIOAkK #####  
 

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
        gaia=ibilbidea.dc_subject
        print gaia
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
            
    
    
    return render_to_response('editatu_ibilbidea.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))



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
        #hornitzailea=item_tupla.edm_provider
        hornitzailea=item_tupla.dc_creator
        
        return render_to_response('item.html',{'id':id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea},context_instance=RequestContext(request))    


def editatu_itema(request):
     
    #Hasieran, Formularioa kargatzerakoan hemen sartuko da
    if 'id' in request.GET: 
        
        item_id=request.GET['id']
           
    itema=ItemEditatuForm(request.POST, request.FILES)
    
    #Editatu botoia sakatzerakoan hemendik sartuko da eta POST bidez bidaliko dira datuak
    if itema.is_valid():
        
        azken_id = item.objects.latest('id').id
        azken_id += 1
        item_id=request.POST['hidden_Item_id']
     
        dc_title=request.POST['titulua']
        uri="uri_"+ str(azken_id)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['eskubideak']
        irudia_url=""
        if(request.FILES):
        
            edm_object=request.FILES['irudia'].name
            irudia_url=MEDIA_URL+edm_object
      
        dc_language=request.POST['hizkuntza']
        edm_language=request.POST['hizkuntza']
        
        print "dc_language"
        print dc_language
       
        if(dc_language=="1"):
            dc_language="Euskera"
            edm_language="Euskera"
        elif(dc_language=="2"):
            dc_language="Gaztelania"
            edm_language="Gaztelania"            
        else:
            dc_language="Ingelesa"
            edm_language="Ingelesa"
         
        
        #dc_creator="Euskomedia" # ondoren logeatutako erabiltzailea jarri
        #edm_provider="Euskomedia" # ondoren logeatutako erabiltzailea jarri
        
        #username-a ez da errepikatzen datu-basean, beraz, id bezala erabili dezakegu 
        dc_creator= request.user.username # ondoren logeatutako erabiltzailea jarri
        edm_provider= request.user.username # ondoren logeatutako erabiltzailea jarri
        #Gaurko data hartu
        dc_date=datetime.datetime.now()
                
        edm_country="Euskal Herria"
       
        if(irudia_url!=""):
            #Irudia igo
            handle_uploaded_file(request.FILES['irudia'],edm_object)        
            item_berria = item(id=item_id,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
        else:
            #Datu-basean irudi zaharra mantendu
            item_tupla = item.objects.get(pk=item_id)
            irudia_url=item_tupla.edm_object
            item_berria = item(id=item_id,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
   
        
        item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        update_index.Command().handle(age=1)
         
        return render_to_response('base.html',{'mezua':"itema editatu da",'nondik':"editatu_itema",'irudia':irudia_url,'titulua':dc_title,'herrialdea':edm_country,'hornitzailea':edm_provider,'eskubideak':edm_rights,'urtea':dc_date},context_instance=RequestContext(request))
    
    else:
        #Hasieran hemendik sartuko da eta Datu-basetik kargatuko dira itemaren datuak
        item_tupla = item.objects.get(pk=item_id)
        titulua=item_tupla.dc_title
        deskribapena=item_tupla.dc_description
        gaia=item_tupla.dc_subject
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.uri
        irudia=item_tupla.edm_object
        #hornitzailea=item_tupla.edm_provider
        hornitzailea=item_tupla.dc_creator
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'hizkuntza':hizkuntza})
        return render_to_response('editatu_itema.html',{'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'viewAtSource':viewAtSource},context_instance=RequestContext(request))
   


def handle_uploaded_file(f,izena):
    with open(MEDIA_ROOT+'/'+izena, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def nire_itemak_erakutsi(request):
    
    #userID=request.POST['user_id']
    userName=request.user.username
    itemak = item.objects.filter(dc_creator=userName)
  
    return render_to_response('nire_itemak.html',{'itemak':itemak},context_instance=RequestContext(request))
   


def nire_ibilbideak_erakutsi(request):
    
    userID=request.user.id
    #userName=request.user.username
    print "userID:"
    print userID
    ibilbideak = path.objects.filter(fk_user_id_id=userID)
        
    return render_to_response('nire_ibilbideak.html',{'ibilbideak':ibilbideak},context_instance=RequestContext(request))
   
   
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
        edm_rights=request.POST['eskubideak']
        irudia_url=""
        if(request.FILES):
            edm_object=request.FILES['irudia'].name
            irudia_url=MEDIA_URL+edm_object
      
        dc_language=request.POST['hizkuntza']
        edm_language=request.POST['hizkuntza']
       
        if(dc_language=="1"):
            dc_language="Euskera"
            edm_language="Euskera"
        elif(dc_language=="2"):
            dc_language="Gaztelania"
            edm_language="Gaztelania"            
        else:
            dc_language="Ingelesa"
            edm_language="Ingelesa"
         
        
        #dc_creator="Euskomedia" # ondoren logeatutako erabiltzailea jarri
        #edm_provider="Euskomedia" # ondoren logeatutako erabiltzailea jarri
        
        #username-a ez da errepikatzen datu-basean, beraz, id bezala erabili dezakegu 
        dc_creator= request.user.username # ondoren logeatutako erabiltzailea jarri
        edm_provider= request.user.username # ondoren logeatutako erabiltzailea jarri
        #Gaurko data hartu
        dc_date=datetime.datetime.now()
                
        edm_country="Euskal Herria"
        if(irudia_url!=""):
            #Irudia igo
            handle_uploaded_file(request.FILES['irudia'],edm_object)
        
        item_berria = item(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
        item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        update_index.Command().handle(age=1)
         
        return render_to_response('base.html',{'mezua':"item berria gehitu da"},context_instance=RequestContext(request))
    else:
        itema=ItemGehituForm()
        return render_to_response('itema_gehitu.html',{'itema':itema},context_instance=RequestContext(request))
   
'''
def erregistratu(request):
    
    
    if 'pasahitza' in request.POST:
        #Datu-basean erabiltzaile berria sartu
       
        
        izena=request.POST['erabIzena']
        posta=request.POST['posta']
        pasahitza=request.POST['pasahitza']
         
        user = User.objects.create_user(izena, posta, pasahitza)
        
        return render_to_response('base.html',context_instance=RequestContext(request))
    else:
        return render_to_response('erregistratu.html',context_instance=RequestContext(request))    

'''
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
    #fk_usr_id=1
        
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
'''
def ajax_path_berria_gorde(request):
    
    request_answer= 0
    print request.GET
    if request.is_ajax() and request.method == 'POST':
        
        fk_usr_id=1

        uri=request.POST.get('uri')
        dc_title=request.POST.get('dc_title')
        dc_subject=request.POST.get('dc_subject')
        dc_description=request.POST.get('dc_description')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        
        ##fileObject= request.FILES.get('fileObject')
        print paths_thumbnail
        print dc_title
        ##
        paths_thumbnail_url=MEDIA_URL+paths_thumbnail
        print paths_thumbnail_url
        #Irudia igo
        #handle_uploaded_file(request.FILES['irudia'],edm_object)
        ##handle_uploaded_file(fileObject,paths_thumbnail)
        
        
        ###
      
      
        path_berria = path(fk_user_id_id = fk_usr_id,
                                        uri =uri,
                                        dc_title = dc_title,
                                        dc_subject = dc_subject,
                                        dc_description = dc_description,
                                        paths_thumbnail = paths_thumbnail_url)
    
    
        path_berria.save()
        request_answer = path_berria.id  
        
        #Haystack update_index EGIN!!!
        update_index.Command().handle()
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')
'''

def ajax_path_irudia_gorde (request):

    request_answer= 0
    
    #import pdb
    #pdb.set_trace()
    print request.FILES
    #print request.POST.FILES
    #print request.GET
    
    if request.is_ajax() and request.method == 'POST':
       
        fileObject= request.FILES.get('file2')
        #print fileObject
        #fileObject= request.POST.get('formdata')
        #fileName= request.GET.get('name')
        #print fileName
        # fileObject= request.GET.get('fileObject')
        #fileName = request.GET.get('fileName')
       
        #fileName="mm"
       
        

        handle_uploaded_file(fileObject,fileObject.name)
        request_answer = 1
        
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')




def ajax_path_irudia_gorde_proba (request):

    request_answer= 0
    
    #import pdb
    #pdb.set_trace()
    print request.FILES
    #print request.POST.FILES
    #print request.GET
    
    if request.is_ajax() and request.method == 'POST':
       
        fileObject= request.FILES.get('file')
        print fileObject
        #fileObject= request.POST.get('formdata')
        #fileName= request.GET.get('name')
        #print fileName
        # fileObject= request.GET.get('fileObject')
        #fileName = request.GET.get('fileName')
       
        #fileName="mm"
       
        

        handle_uploaded_file(fileObject,fileObject.name)
        request_answer = 1
        
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_berria_gorde(request):
    
    request_answer= 0
  
    if request.is_ajax() and request.method == 'POST':
        
        #fk_usr_id=1
        
        fk_usr_id=request.user.id
        uri=request.POST.get('uri')
        dc_title=request.POST.get('dc_title')
        dc_subject=request.POST.get('dc_subject')
        dc_description=request.POST.get('dc_description')
        paths_thumbnail = request.POST.get('paths_thumbnail')
       
        #fileObject= request.FILES.get('fileObject')
        #fileObject= request.GET.get('fileObject')
        #print fileObject
        ##
        paths_thumbnail_url=MEDIA_URL+paths_thumbnail
     
        #Irudia igo
        #handle_uploaded_file(request.FILES['irudia'],edm_object)
        #handle_uploaded_file(fileObject,paths_thumbnail)
        
        
        ###
      
      
        path_berria = path(fk_user_id_id = fk_usr_id,
                                        uri =uri,
                                        dc_title = dc_title,
                                        dc_subject = dc_subject,
                                        dc_description = dc_description,
                                        paths_thumbnail = paths_thumbnail_url)
    
    
        path_berria.save()
        request_answer = path_berria.id  
        
        #Haystack update_index EGIN!!!
        update_index.Command().handle()
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_eguneratu(request):
    
        
    path_id=request.POST.get('path_id')
    fk_usr_id=request.user.id
    dc_title=request.POST.get('dc_title')
    dc_subject=request.POST.get('dc_subject')
    dc_description=request.POST.get('dc_description')
    paths_thumbnail = request.POST.get('paths_thumbnail')
     
    paths_thumbnail_url=MEDIA_URL+paths_thumbnail
     
       
      
    path_eguneratua = path(id=path_id,
                           fk_user_id_id = fk_usr_id,
                           dc_title = dc_title,
                           dc_subject = dc_subject,
                           dc_description = dc_description,
                           paths_thumbnail = paths_thumbnail_url)
    
    
    path_eguneratua.save()
    request_answer = path_id 
        
    #Haystack update_index EGIN!!!
    update_index.Command().handle()
    
    

    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_node_gorde(request):
    
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

