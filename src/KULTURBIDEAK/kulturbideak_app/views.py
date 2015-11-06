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
from django.utils import timezone

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
            
            #nodes = nodes + get_tree(node.objects.filter(fk_item_id=child_node_id, fk_path_id=el_node.fk_path_id)[0])
            nodes = nodes + get_tree(node.objects.filter(fk_item_id__id=child_node_id, fk_path_id__id=el_node.fk_path_id.id)[0])
    return nodes


def hasiera(request):
    #EGUNEKO IBILBIDEAREN PARAMETROAK BIDALI BEHAR DIRA HEMEN
    #DB-an GALDERA EGIN EGUNEKO IBILBIDEA LORTZEKO
    #egunekoIbilbidea = path.objects.get(egunekoa=1)
   
    if(path.objects.filter(egunekoa=1)):
        
        egunekoIbilbidea = path.objects.get(egunekoa=1)
        #lortu path-aren ezaugarriak
    
        id=egunekoIbilbidea.id
        titulua=egunekoIbilbidea.dc_title
        gaia=egunekoIbilbidea.dc_subject
        deskribapena=egunekoIbilbidea.dc_description
        irudia=egunekoIbilbidea.paths_thumbnail
             
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id__id=id,paths_start=1)        
        #erroak = node.objects.filter(fk_path_id=egunekoIbilbidea,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
        #import pdb
        #pdb.set_trace()
    else:
        id=""
        titulua=""
        gaia=""
        deskribapena=""
        irudia=""                    
        nodes = []     
        
       
    return render_to_response('hasiera.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))

   
   
def itemak_hasiera(request):
    
    #Itemen hasierako pantailan erakutsi behar diren Itemen informazioa datu-basetik lortu eta pasa
    itemak=[]
    if(item.objects.filter(proposatutakoa=1)):
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK ITEMAK LORTZEKO   
        itemak=item.objects.filter(proposatutakoa=1)
        
       
    return render_to_response('itemak_hasiera.html',{'itemak':itemak},context_instance=RequestContext(request))
    

def ibilbideak_hasiera(request):
    
    #Ibilbideen hasierako pantailan erakutsi behar diren Ibilbideen informazioa datu-basetik lortu eta pasa
     
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK/IKUSIENA PATHA LORTZEKO   
    #DB-an GALDERA EGIN EGUNEKO IBILBIDEA LORTZEKO
    
    if(path.objects.filter(egunekoa=1)):
        
        egunekoIbilbidea = path.objects.get(egunekoa=1)
        #lortu path-aren ezaugarriak
    
        id=egunekoIbilbidea.id
        titulua=egunekoIbilbidea.dc_title
        gaia=egunekoIbilbidea.dc_subject
        deskribapena=egunekoIbilbidea.dc_description
        irudia=egunekoIbilbidea.paths_thumbnail
             
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=egunekoIbilbidea,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
    else:
        id=""
        titulua=""
        gaia=""
        deskribapena=""
        irudia=""                    
        nodes = []     
        
        
        
    return render_to_response('ibilbideak_hasiera.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))

def nabigazioa_hasi(request):
    
    if 'path_id' in request.GET:
        path_id=request.GET['path_id']
        
        momentukoPatha=path.objects.get(id=path_id)
        
        #Ibilbidearen Hasierak hartu
        hasieraNodoak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    
        
        #Hasierako nodo bat lortu
        momentukoNodea = node.objects.filter(fk_path_id=momentukoPatha, paths_start=1)[0]
        item_id=momentukoNodea.fk_item_id
        
        hurrengoak=momentukoNodea.paths_next
        aurrekoak=momentukoNodea.paths_prev
    
        hurrengoak_list=[]
        hasieraBakarra=0
        #node taulatik "hurrengoak" tuplak hartu 
        if(hurrengoak != ""):
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
        elif(hasieraNodoak.count()==1):       
            hurrengoak_list=hasieraNodoak.fk_item_id
        else:
            hasieraBakarra=0       
            hurrengoak_list=map(lambda x: x.fk_item_id,list(hasieraNodoak))
    
    
        hurrengoak=node.objects.filter(fk_path_id=momentukoPatha,fk_item_id__in=hurrengoak_list)
    
        aurrekoak_list=[]
        #node taulatik "aurrekoak" tuplak hartu
        if(aurrekoak != ""):
            aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
        aurrekoak=node.objects.filter(fk_path_id=momentukoPatha, fk_item_id__in=aurrekoak_list)
    
        #DB-an GALDERA EGIN MOMENTUKO ITEMA LORTZEKO
        momentukoItema = item.objects.get(id=item_id)  
    
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
        
        botatuDuPath=0
        if(votes_path.objects.filter(path=momentukoPatha,user_id=request.user)):
            botatuDuPath=1
        
        botatuDuItem=0
        if(votes_item.objects.filter(item=momentukoItema,user_id=request.user)):
            botatuDuItem=1
   
        #Momentuko Ibilbidea lortu
        momentukoIbilbidea=path.objects.get(id=path_id)
    
        botoKopuruaPath=momentukoIbilbidea.get_votes()
        botoKopuruaItem=momentukoItema.get_votes()
    
        return render_to_response('nabigazio_item.html',{'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    
    return False
        

def nabigazio_item(request):
    
    path_id=request.POST['path_id']
    item_id=request.POST['item_id']
    
    
    momentukoPatha=path.objects.get(id=path_id)
    momentukoItema=item.objects.get(id=item_id)
    #Ibilbidearen Hasierak hartu
    hasieraNodoak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    
    #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
    momentukoNodea = node.objects.get(fk_item_id=momentukoItema, fk_path_id=momentukoPatha) 
    
    hurrengoak=momentukoNodea.paths_next
    aurrekoak=momentukoNodea.paths_prev
    
    hurrengoak_list=[]
    hasieraBakarra=0
    #node taulatik "hurrengoak" tuplak hartu 
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    elif(hasieraNodoak.count()==1):       
        #hurrengoak_list=hasieraNodoak.fk_item_id
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
        hasieraBakarra=1
    else:
        hasieraBakarra=0       
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
    
    
    hurrengoak=node.objects.filter(fk_path_id=momentukoPatha,fk_item_id__id__in=hurrengoak_list)
    
    aurrekoak_list=[]
    #node taulatik "aurrekoak" tuplak hartu
    if(aurrekoak != ""):
        aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
    aurrekoak=node.objects.filter(fk_path_id=momentukoPatha, fk_item_id__id__in=aurrekoak_list)
    
      
    
    #path hasierak hartu
    nodes = [] 
    erroak = node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    for erroa in erroak:
        nodes = nodes + get_tree(erroa)
        
    botatuDuPath=0
    if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
        botatuDuPath=1
        
    botatuDuItem=0
    if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
        botatuDuItem=1
   
    #Momentuko Ibilbidea lortu
    momentukoIbilbidea=path.objects.get(id=path_id)
    
    botoKopuruaPath=momentukoIbilbidea.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()
    
    return render_to_response('nabigazio_item.html',{'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

def nabigatu(request):
     
    path_id=request.GET['path_id']
    item_id=request.GET['item_id']
    
    
    momentukoPatha=path.objects.get(id=path_id)
    momentukoItema=item.objects.get(id=item_id)
    #Ibilbidearen Hasierak hartu
    hasieraNodoak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    
    #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
    momentukoNodea = node.objects.get(fk_item_id=momentukoItema, fk_path_id=momentukoPatha) 
    
    hurrengoak=momentukoNodea.paths_next
    aurrekoak=momentukoNodea.paths_prev
    
    hurrengoak_list=[]
    hasieraBakarra=0
    #node taulatik "hurrengoak" tuplak hartu 
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    elif(hasieraNodoak.count()==1):       
        #hurrengoak_list=hasieraNodoak.fk_item_id
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
        hasieraBakarra=1
    else:
        hasieraBakarra=0       
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
    
   
    hurrengoak=node.objects.filter(fk_path_id=momentukoPatha,fk_item_id__id__in=hurrengoak_list)
    
    aurrekoak_list=[]
    #node taulatik "aurrekoak" tuplak hartu
    if(aurrekoak != ""):
        aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
    aurrekoak=node.objects.filter(fk_path_id=momentukoPatha, fk_item_id__id__in=aurrekoak_list)
    
      
    
    #path hasierak hartu
    nodes = [] 
    erroak = node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    for erroa in erroak:
        nodes = nodes + get_tree(erroa)
        
    botatuDuPath=0
    if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
        botatuDuPath=1
        
    botatuDuItem=0
    if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
        botatuDuItem=1
   
    #Momentuko Ibilbidea lortu
    momentukoIbilbidea=path.objects.get(id=path_id)
    
    botoKopuruaPath=momentukoIbilbidea.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()   
    
    
    return render_to_response('nabigazio_item.html',{'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))


def botoa_eman_path(request):
    
               
    path_id=request.GET['path_id']
    item_id=request.GET['item_id']
   
    path_tupla = path.objects.get(id=path_id)
    item_tupla = item.objects.get(id=item_id)
                   
    #botatu, request.user
    path_tupla.vote(request.user)
    
    #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
    momentukoNodea = node.objects.get(fk_item_id=item_tupla, fk_path_id=path_tupla) 
    
    hurrengoak=momentukoNodea.paths_next
    aurrekoak=momentukoNodea.paths_prev
    
    hurrengoak_list=[]
    #node taulatik "hurrengoak" tuplak hartu 
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    
    hurrengoak=node.objects.filter(fk_path_id=path_tupla,fk_item_id__id__in=hurrengoak_list)
    
    aurrekoak_list=[]
    #node taulatik "aurrekoak" tuplak hartu
    if(aurrekoak != ""):
        aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
    aurrekoak=node.objects.filter(fk_path_id=path_tupla, fk_item_id__id__in=aurrekoak_list)
    
   
    #DB-an GALDERA EGIN MOMENTUKO ITEMA LORTZEKO
    momentukoItema = item.objects.get(id=item_id)  
   
    #path hasierak hartu
    nodes = [] 
    erroak = node.objects.filter(fk_path_id=path_tupla,paths_start=1)
    for erroa in erroak:
        nodes = nodes + get_tree(erroa)
    
    botatuDuPath=0
    if(votes_path.objects.filter(path=path_tupla,user=request.user)):
        botatuDuPath=1
        
    botatuDuItem=0
    if(votes_item.objects.filter(item=item_tupla,user=request.user)):
        botatuDuItem=1
        
        
    botoKopuruaPath=path_tupla.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()
    
    return render_to_response('nabigazio_item.html',{'botoKopuruaItem':botoKopuruaItem,'botoKopuruaPath':botoKopuruaPath,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))


def botoa_kendu_path(request):
    
               
    path_id=request.GET['path_id']
    item_id=request.GET['item_id']
   
    path_tupla = path.objects.get(id=path_id)
    item_tupla= item.objects.get(id=item_id)           
    #botoa kendu
    path_tupla.unvote(request.user)
    
    #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
    momentukoNodea = node.objects.get(fk_item_id=item_tupla, fk_path_id=path_tupla) 
    
    hurrengoak=momentukoNodea.paths_next
    aurrekoak=momentukoNodea.paths_prev
    
    hurrengoak_list=[]
    #node taulatik "hurrengoak" tuplak hartu 
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    
    hurrengoak=node.objects.filter(fk_path_id=path_tupla,fk_item_id__in=hurrengoak_list)
    
    aurrekoak_list=[]
    #node taulatik "aurrekoak" tuplak hartu
    if(aurrekoak != ""):
        aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
    aurrekoak=node.objects.filter(fk_path_id=path_tupla, fk_item_id__in=aurrekoak_list)
    
   
    #DB-an GALDERA EGIN MOMENTUKO ITEMA LORTZEKO
    momentukoItema = item.objects.get(id=item_id)  
   
    #path hasierak hartu
    nodes = [] 
    erroak = node.objects.filter(fk_path_id=path_tupla,paths_start=1)
    for erroa in erroak:
        nodes = nodes + get_tree(erroa)
    
    botatuDuPath=0
    if(votes_path.objects.filter(path=path_tupla,user_id=request.user)):
        botatuDuPath=1
        
    botatuDuItem=0
    if(votes_item.objects.filter(item=item_tupla,user_id=request.user)):
        botatuDuItem=1
        
        
    botoKopuruaPath=path_tupla.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()
    
    return render_to_response('nabigazio_item.html',{'botoKopuruaItem':botoKopuruaItem,'botoKopuruaPath':botoKopuruaPath,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))



  
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
        
        #Django-ko auth_user-en gordetzen du erabiltailea
        erabiltzailea.save()
        #if cd["erabiltzaile_mota"]!='':
            #g=Group.objects.get(name=cd["erabiltzaile_mota"])
        #else:
            # g=Group.objects.get(name='editorea')
        # g.user_set.add(erabiltzailea)
        # g.save()
        #import pdb
        #pdb.set_trace()
        
        #Nire usr taulan gordetzen du erabiltzailea
        erab=usr(user=erabiltzailea)
        erab.save()
        
        #Erabiltzaileari workspace-a sortuko diogu       
        ws=workspace(fk_usr_id=erabiltzailea)
        ws.save()
        
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
    erabID=request.user.id
    erabiltzailea=User.objects.get(id=erabID)
    erabiltzailea.username = cd["username"]
    erabiltzailea.first_name=cd["izena"]
    erabiltzailea.last_name =cd["abizena"]
    erabiltzailea. email = cd["posta"]
    
    
    erabiltzailea.save()
    
    #erab=usr(user=erab_eguneratua)
    #erab.save()
    
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
 


def editatu_ibilbidea(request):
    
    if 'id' in request.GET:
        id=request.GET['id']
    
        #lortu path-aren ezaugarriak
        ibilbidea = path.objects.get(id=id)
        titulua=ibilbidea.dc_title
        gaia=ibilbidea.dc_subject
        deskribapena=ibilbidea.dc_description
        irudia=ibilbidea.paths_thumbnail
        
        
        #path hasierak hartu
       # nodes = []
     #   path_starts = Node.objects.filter(prev=="")
     #   for path_start in path_starts:
     #       nodes = nodes + get_tree(path_start)
            
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=ibilbidea,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
            
        
        
        '''path_nodeak=[]
        for node in nodes:
         
            sarrera=str(node.fk_item_id)+";"+node.dc_title+";"+node.paths_thumbnail+";"+node.paths_prev+";"+node.paths_next
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
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
        
        
        botatuDu=0
        if(votes_item.objects.filter(item=id,user_id=request.user.id)):
            botatuDu=1
        
        botoKopurua=item_tupla.get_votes()
        return render_to_response('item.html',{'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'id':id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    

def botoa_eman_item(request):
    
            
    item_id=request.GET['id']
    nondik=""
    if 'nondik' in request.GET:
        nondik=request.GET['nondik']
       
    
    item_tupla = item.objects.get(pk=item_id)                   
    #botatu, request.user
    item_tupla.vote(request.user)
        
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
        
    botatuDuItem=0
    if(votes_item.objects.filter(item_id=item_id,user_id=request.user.id)):
        botatuDuItem=1
            
    botoKopuruaItem=item_tupla.get_votes()
        
    if nondik=='nabigazioa':
        path_id=request.GET['path_id']
            
        #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
        momentukoNodea = node.objects.get(fk_item_id=item_id, fk_path_id=path_id) 
    
        hurrengoak=momentukoNodea.paths_next
        aurrekoak=momentukoNodea.paths_prev
    
        hurrengoak_list=[]
        #node taulatik "hurrengoak" tuplak hartu 
        if(hurrengoak != ""):
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    
        hurrengoak=node.objects.filter(fk_path_id=path_id,fk_item_id__in=hurrengoak_list)
    
        aurrekoak_list=[]
        #node taulatik "aurrekoak" tuplak hartu
        if(aurrekoak != ""):
            aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
        aurrekoak=node.objects.filter(fk_path_id=path_id, fk_item_id__in=aurrekoak_list)
    
        #DB-an GALDERA EGIN MOMENTUKO ITEMA LORTZEKO
        momentukoItema = item.objects.get(id=item_id)  
   
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=path_id,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
    
        botatuDuPath=0
        if(votes_path.objects.filter(path=path_id,user_id=request.user.id)):
            botatuDuPath=1
        
        botatuDuItem=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
            botatuDuItem=1
        
        #Momentuko Ibilbidea lortu
        momentukoIbilbidea=path.objects.get(id=path_id)
    
        botoKopuruaPath=momentukoIbilbidea.get_votes()
        botoKopuruaItem=momentukoItema.get_votes()
    
        return render_to_response('nabigazio_item.html',{'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

    else:
        return render_to_response('item.html',{'botoKopurua':botoKopuruaItem,'item':item_tupla,'id':id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    

    
def botoa_kendu_item(request):

       
    item_id=request.GET['id']
    
    nondik=""
    if 'nondik' in request.GET:
        nondik=request.GET['nondik']
      
     
     
    item_tupla = item.objects.get(pk=item_id)

    #botoa kendu
    item_tupla.unvote(request.user)
        
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
        
    botatuDuItem=0
    if(votes_item.objects.filter(item_id=item_id,user_id=request.user.id)):
        botatuDuItem=1
            
    botoKopuruaItem=item_tupla.get_votes()
    
    if nondik=='nabigazioa':
        path_id=request.GET['path_id']
            
        #DB-an GALDERA EGIN MOMENTUKO NODEA LORTZEKO
        momentukoNodea = node.objects.get(fk_item_id=item_id, fk_path_id=path_id) 
    
        hurrengoak=momentukoNodea.paths_next
        aurrekoak=momentukoNodea.paths_prev
    
        hurrengoak_list=[]
        #node taulatik "hurrengoak" tuplak hartu 
        if(hurrengoak != ""):
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    
        hurrengoak=node.objects.filter(fk_path_id=path_id,fk_item_id__in=hurrengoak_list)
    
        aurrekoak_list=[]
        #node taulatik "aurrekoak" tuplak hartu
        if(aurrekoak != ""):
            aurrekoak_list=map(lambda x: int(x),aurrekoak.split(","))
    
        aurrekoak=node.objects.filter(fk_path_id=path_id, fk_item_id__in=aurrekoak_list)
    
        #DB-an GALDERA EGIN MOMENTUKO ITEMA LORTZEKO
        momentukoItema = item.objects.get(id=item_id)  
   
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=path_id,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
    
        botatuDuPath=0
        if(votes_path.objects.filter(path=path_id,user_id=request.user.id)):
            botatuDuPath=1
        
        botatuDuItem=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
            botatuDuItem=1
        
        #Momentuko Ibilbidea lortu
        momentukoIbilbidea=path.objects.get(id=path_id)
    
        botoKopuruaPath=momentukoIbilbidea.get_votes()
        botoKopuruaItem=momentukoItema.get_votes()
    
        return render_to_response('nabigazio_item.html',{'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

    else:
        
        return render_to_response('item.html',{'botoKopurua':botoKopuruaItem,'item':item_tupla,'id':item_id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    


def editatu_itema(request):
     
    #Hasieran, Formularioa kargatzerakoan hemen'botoKopurua':botoKopurua sartuko da
    if 'id' in request.GET: 
        
        item_id=request.GET['id']
           
    itema=ItemEditatuForm(request.POST, request.FILES)
    
    #Editatu botoia sakatzerakoan hemendik sartuko da eta POST bidez bidaliko dira datuak
    if itema.is_valid():
        
        azken_id = item.objects.latest('id').id
        azken_id += 1
        item_id=request.POST['hidden_Item_id']
     
        dc_title=request.POST['titulua']
        uri="uri_"+ str(item_id)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['eskubideak']
        irudia_url=""
        if(request.FILES):
        
            edm_object=request.FILES['irudia'].name
            irudia_url=MEDIA_URL+ str(item_id)+edm_object #izen berekoak gainidatzi egingo dira bestela
      
        dc_language=request.POST['hizkuntza']
        edm_language=request.POST['hizkuntza']
        
        
        
       
        if(dc_language=="1"):
            dc_language="eu"
            edm_language="eu"
        elif(dc_language=="2"):
            dc_language="es"
            edm_language="es"            
        else:
            dc_language="en"
            edm_language="en"
         
        
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
            edm_object= str(item_id)+edm_object
            handle_uploaded_file(request.FILES['irudia'],edm_object)        
            item_berria = item(id=item_id,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
            #Item-a duten Ibilbideko nodoen argazkia ALDATU. node TAULAN, fk_item_id ALDAGAIA =item_id
            irudia_update=MEDIA_URL+edm_object              
            node.objects.filter(fk_item_id=item_id).update(paths_thumbnail=irudia_update)

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
        if(hizkuntza=="eu"):
            hizkuntza=1
            hizk="eu"
        elif(hizkuntza=="es"):
            hizkuntza=2
            hizk="es"
        else:
            hizkuntza=3
            hizk="en"
            
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.dc_date 
        viewAtSource=item_tupla.uri
        irudia=item_tupla.edm_object
        #hornitzailea=item_tupla.edm_provider
        hornitzailea=item_tupla.dc_creator
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'hizkuntza':hizkuntza})
        return render_to_response('editatu_itema.html',{'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'hizkuntza':hizk,'viewAtSource':viewAtSource},context_instance=RequestContext(request))
   


def handle_uploaded_file(f,izena):
    #Irudi fitxategia /uploads direktoriora igotzen du
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
    ibilbideak = path.objects.filter(fk_user_id=userID)
        
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
            irudia_url=MEDIA_URL+str(azken_id)+edm_object #izen berekoak gainidatzi egingo dira bestela
      
        dc_language=request.POST['hizkuntza']
        edm_language=request.POST['hizkuntza']
       
        if(dc_language=="1"):
            dc_language="eu"
            edm_language="eu"
        elif(dc_language=="2"):
            dc_language="es"
            edm_language="es"            
        else:
            dc_language="en"
            edm_language="en"
         
        
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
            edm_object=str(azken_id)+edm_object #izen berekoak gainidatzi egingo dira bestela
            handle_uploaded_file(request.FILES['irudia'],edm_object)
        
        latitude=request.POST['latitude']
        print latitude
        longitude=request.POST['longitude']
        print longitude
        item_berria = item(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
        item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        update_index.Command().handle(age=1)
         
        return render_to_response('base.html',{'mezua':"item berria gehitu da"},context_instance=RequestContext(request))
    else:
        # language==interface language
        
        if(request.LANGUAGE_CODE=="eu"):
            hizk=1
        elif(request.LANGUAGE_CODE=="es"):
            hizk=2
        else:
            hizk=3
        
        itema=ItemGehituForm(initial={'hizkuntza':hizk})
        non="itema_gehitu" #Mapako baimenak kontrolatzeko erabiliko da hau
        return render_to_response('itema_gehitu.html',{'itema':itema,'non':non},context_instance=RequestContext(request))
   

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
    #fk_user_id=1,
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
    
    #fk_usr_id=request.POST['user_id']
        
    #fk_workspace_id=request.POST['ws_id']
    #ws_item_zerrenda=workspace_item.objects.filter(fk_workspace_id=fk_workspace_id)
    
    workspacea=workspace.objects.get(fk_usr_id=request.user) 
    ws_item_zerrenda=workspace_item.objects.filter(fk_workspace_id=workspacea)
    return render_to_response('workspace_items.xml', {'items': ws_item_zerrenda}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_lortu_paths_list(request):
    
    fk_usr_id=request.POST['user_id']
    
    user_path_zerrenda=path.objects.filter(fk_user_id=fk_usr_id)
    
    return render_to_response('ibilbide_lista.xml', {'paths': user_path_zerrenda}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_lortu_most_voted_paths(request):
    
    #bozkatuenak lortu
    #votes_path:path,user
    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')[:5]
    
    if bozkatuenak_path_zerrenda:
        path_ids=[]
        for bozkatuena in bozkatuenak_path_zerrenda:
            path_ids = bozkatuena.path.id
    
    #hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    
        path_bozkatuenak=path.objects.filter(id__in=[path_ids]) 
    else:
        path_bozkatuenak=[]
    
    return render_to_response('ibilbide_bozkatuenak.xml', {'paths': path_bozkatuenak}, context_instance=RequestContext(request), mimetype='application/xml')

    
    

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
        #fk_workspace_id=request.POST.get('fk_workspace_id')
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        thumbnail=request.POST.get('paths_thumbnail')
    
        #workspace eta item objektuak pasa!
        #workspace=workspace.objects.get(fk_usr_id__id=request.user.id)   
        workspacea=workspace.objects.get(fk_usr_id=request.user)       
        itema=item.objects.get(id=item_id)
        
       
        ws_item_berria = workspace_item(fk_item_id=itema,
                                        uri =uri,
                                        fk_workspace_id = workspacea,
                                        dc_source = dc_source,
                                        dc_title = dc_title,
                                        dc_description = dc_description,
                                        type = type,
                                        paths_thumbnail = thumbnail)
    
    
        ws_item_berria.save()
        request_answer = ws_item_berria.fk_item_id
        #request_answer = ws_item_berria.id
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_workspace_item_borratu(request):
    request_answer= 0
    if request.is_ajax() and request.method == 'POST':
                 
        item_id=request.POST.get('item_id')
        workspacea=workspace.objects.get(fk_usr_id=request.user)
        itema=item.objects.get(id=item_id)
        
        workspace_item.objects.filter(fk_item_id=itema,fk_workspace_id = workspacea).delete()
      
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
      
      
        path_berria = path(fk_user_id = fk_usr_id,
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
       
        
        #Irudirik igotzen ez denean errorea ez emateko beharrezko da baldintza hau jartzea
        if(request.FILES):
        
            
            fileObject= request.FILES.get('file2')
            #irudiari id-a gehitzeko, izen berekoak gainidatzi ez daitezen
            # AZKEN PATH  ID-A + ERABILTZAILE IDa: request.POST['user_id']
           
            
            if(path.objects.count() > 0):
                azken_id = path.objects.latest('id').id
                azken_id += 1
            else:
                azken_id =1
            user_id =request.user.id
            fileName=str(user_id)+fileObject.name
            fileName=str(azken_id)+fileName
            
            #fileName=str(azken_id)+fileObject.name   
            print fileName
            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            request_answer = azken_id
    
    request_answer = 1    
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_irudia_eguneratu (request):

    #KONPONTZEKO
    request_answer= 0
    
    #import pdb
    #pdb.set_trace()
    print request.FILES
    print request.POST
    #print request.POST.FILES
    print request.GET
    
    if request.is_ajax() and request.method == 'POST':
       
        #Irudirik igotzen ez denean errorea ez emateko beharrezko da baldintza hau jartzea
        if(request.FILES):
        
 
            fileObject= request.FILES.get('file2')
            #irudiari id-a gehitzeko
            path_id=request.POST.get('path_id_h')
            user_id=request.user.id
            #fileName=str(path_id)+str(user_id)+fileObject.name
            fileName=str(user_id)+fileObject.name
           
           
    

            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            request_answer = path_id
    
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
        
        #irudiari id-a gehitzeko
        # ERABILBITZAILEAREN PATHEN ARTEAN AZKENA HARTZEKO ALDATU!!
                
        if(path.objects.count() > 0):
            azken_id = path.objects.latest('id').id
            azken_id += 1
        else:
            azken_id =1
        
        fk_usr_id=request.user.id
        uri=request.POST.get('uri')
        dc_title=request.POST.get('dc_title')
        dc_subject=request.POST.get('dc_subject')
        dc_description=request.POST.get('dc_description')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        ######paths_thumbnail=str(azken_id)+paths_thumbnail
       
        #fileObject= request.FILES.get('fileObject')
        #fileObject= request.GET.get('fileObject')
        #print fileObject
        ##
        paths_thumbnail_url=MEDIA_URL+str(azken_id)+str(fk_usr_id)+paths_thumbnail
        #paths_thumbnail_url=MEDIA_URL+paths_thumbnail
     
        #Irudia igo
        #handle_uploaded_file(request.FILES['irudia'],edm_object)
        #handle_uploaded_file(fileObject,paths_thumbnail)
        
        
        ###
        #user = usr.object.get(user=request.user)
      
        path_berria = path(fk_user_id = request.user,
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
    
    #erabiltzaileak ibilbidearen irudia eguneratu ez baldin badu zaharra hartu
    if paths_thumbnail=='':
                
        patha=path.objects.get(id=path_id)      
        paths_thumbnail_url=patha.paths_thumbnail 
    
    else:  
        
        #paths_thumbnail_url=MEDIA_URL+str(path_id)+str(fk_usr_id)+paths_thumbnail     
        paths_thumbnail_url=MEDIA_URL+str(fk_usr_id)+paths_thumbnail
     
  
      
    path_eguneratua = path(id=path_id,
                           fk_user_id = request.user,
                           dc_title = dc_title,
                           dc_subject = dc_subject,
                           dc_description = dc_description,
                           paths_thumbnail = paths_thumbnail_url,
                           tstamp = timezone.now(),
                           creation_date = timezone.now())
    
    
    path_eguneratua.save()
    request_answer = path_id 
        
    #Haystack update_index EGIN!!!
    update_index.Command().handle()
    
    

    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_path_node_gorde(request):
    
    request_answer= 0
    
    if request.is_ajax() and request.method == 'POST':
        
        
       
        fk_path_id=request.POST.get('path_id')
        fk_item_id=request.POST.get('item_id')
        
       
  
        fk_item_id=fk_item_id.replace("ws_box_","") #aldaketa
        
        patha=path.objects.get(id=fk_path_id)
        itema=item.objects.get(id=fk_item_id)

        
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')     
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        paths_prev = request.POST.get('paths_prev')
        paths_prev=paths_prev.replace("ws_box_","") #aldaketa
        paths_next = request.POST.get('paths_next')
        paths_next=paths_next.replace("ws_box_","") #aldaketa
        paths_start = (int(request.POST.get('paths_start')) > 0)
    
        
      
        node_berria = node(#id=azken_id,
                           fk_item_id=itema,
                           uri =uri,
                           fk_path_id = patha,
                           dc_source = dc_source,   
                           dc_title = dc_title,
                           dc_description = dc_description,
                           type = type,
                           paths_thumbnail = paths_thumbnail,
                           paths_prev=paths_prev,
                           paths_next = paths_next,
                           paths_start = paths_start)
        
    
        node_berria.save()
        request_answer = node_berria.fk_item_id
        
        
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_node_eguneratu(request):
    
    request_answer= 0
    
    if request.is_ajax() and request.method == 'POST':
        
        
       
        fk_path_id=request.POST.get('path_id')
        fk_item_id=request.POST.get('item_id')
        
        patha=path.objects.get(id=fk_path_id)
        itema=item.objects.get(id=fk_item_id)
        
        uri=request.POST.get('uri')
        dc_source=request.POST.get('dc_source')
        dc_title=request.POST.get('dc_title')     
        dc_description=request.POST.get('dc_description')
        type=request.POST.get('type')
        paths_thumbnail = request.POST.get('paths_thumbnail')
        paths_prev = request.POST.get('paths_prev')
        paths_prev=paths_prev.replace("pb_","") #aldaketa
        paths_next = request.POST.get('paths_next')
        paths_next=paths_next.replace("pb_","") #aldaketa
        paths_start = (int(request.POST.get('paths_start')) > 0)
    
            
        nodea=node.objects.get(fk_item_id__id= fk_item_id,
                               fk_path_id__id = fk_path_id                               
                               )
      
        
        node_id=nodea.id
        
        #Begiratu Narrazioa eguneratu behar den!
        if dc_description == 'undefined' :
            dc_description=nodea.dc_description
        
         
  
        node_eguneratua = node(id=node_id,
                           fk_item_id=itema,
                           uri =uri,
                           fk_path_id = patha,
                           dc_source = dc_source,   
                           dc_title = dc_title,
                           dc_description = dc_description,
                           type = type,
                           paths_thumbnail = paths_thumbnail,
                           paths_prev=paths_prev,
                           paths_next = paths_next,
                           paths_start = paths_start,
                           tstamp = timezone.now())
        
    
        node_eguneratua.save()
        request_answer = node_eguneratua.fk_item_id
        
        
       
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

