# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _,get_language
from itertools import islice, chain
from django.utils import simplejson
from django.template import Context, Template
from django.utils import timezone
from django.core.mail import send_mail

#from utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

#MADDALEN
from django.http import HttpResponse
from django.shortcuts import render_to_response
from KULTURBIDEAK.kulturbideak_app.models import item
from KULTURBIDEAK.kulturbideak_app.models import path
from KULTURBIDEAK.kulturbideak_app.models import node
from KULTURBIDEAK.kulturbideak_app.models import workspace_item
from django.contrib.auth.models import User,Group
from KULTURBIDEAK.kulturbideak_app.forms import *
from KULTURBIDEAK.kulturbideak_app.models import *
from haystack.management.commands import update_index
from KULTURBIDEAK.settings import *

from django.utils.translation import ugettext as _


from KULTURBIDEAK.kulturbideak_app.search_indexes import itemIndex
from KULTURBIDEAK.kulturbideak_app.search_indexes import pathIndex
from db_views import db_add_itemcomment,db_add_pathcomment,db_register, db_update_profile
from haystack.query import SQ, SearchQuerySet

import simplejson as json
import getopt
import tempfile

from  haystack.inputs import Not
from haystack.inputs import Raw
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
from oaiharvestandstore_django import oaiharveststore
import re
import random

nodeLoadError=""

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))



def get_tree(el_node):
    
    
    nodes = [el_node]
    
    if el_node.paths_next != "":
        for child_node_id in el_node.paths_next.split(","):
            
            #nodes = nodes + get_tree(node.objects.filter(fk_item_id=child_node_id, fk_path_id=el_node.fk_path_id)[0])
            try:
                nodes = nodes + get_tree(node.objects.filter(fk_item_id__id=child_node_id, fk_path_id__id=el_node.fk_path_id.id)[0])
            except Exception as nodeLoadError:
                print node.objects.filter(fk_item_id__id=child_node_id, fk_path_id__id=el_node.fk_path_id.id)
                print child_node_id, el_node.fk_path_id.id
                nodeLoadError="Node "+child_node_id+" could not be loaded"
    return nodes

def brandy(request):
    
    return render_to_response('index_brandy.html',context_instance=RequestContext(request))
 

def hasiera(request):
  
    #DB-an GALDERA EGIN EGUNEKO IBILBIDEAK LORTZEKO
    egunekoIbilbideak=[]
    egunekoIbilbideak = path.objects.filter(egunekoa=1)
    '''
    if(path.objects.filter(egunekoa=1)):
        
        egunekoIbilbideak = path.objects.filter(egunekoa=1)
     
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
    '''
    
    #Kontadoreko kopuruak lortu datu-basetik
    #Itemak
    itemKop = item.objects.count()
    #Ibilbideak
    ibilbideKop = path.objects.count()   
    #Hornitzaileak
    hornitzaileKop = hornitzailea.objects.count()
    #Erabiltzaileak
    erabiltzaileKop = usr.objects.count()
    #return render_to_response('hasiera.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))
    return render_to_response('index_brandy.html',{'itemKop':itemKop,'ibilbideKop':ibilbideKop,'hornitzaileKop':hornitzaileKop,'erabiltzaileKop':erabiltzaileKop,'egunekoIbilbideak':egunekoIbilbideak},context_instance=RequestContext(request))

   
   
def itemak_hasiera(request):
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK ITEMAK LORTZEKO 
    #Itemen hasierako pantailan erakutsi behar diren Itemen informazioa datu-basetik lortu eta pasa
    itemak=[]
    itemak=item.objects.order_by('-edm_year')
    paginator = Paginator(itemak, 26)
    
   
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
    page = request.GET.get('page')
    try:
        itemak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        itemak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        itemak = paginator.page(paginator.num_pages)
    
    #Proposatutakoak
    ##if(item.objects.filter(proposatutakoa=1)):
        ##itemak=item.objects.filter(proposatutakoa=1)
        
    #Egunekoak
    eguneko_itemak=[]
    eguneko_itemak=item.objects.filter(egunekoa=1)
    
    #Azkenak
    azken_itemak=[]
    azken_itemak=item.objects.order_by('-edm_year')[:10]
    
    #Bozkatuenak
    item_bozkatuenak=[]
    bozkatuenak_item_zerrenda= votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')[:10]
    if bozkatuenak_item_zerrenda:
        item_ids=[]
        for bozkatuena in bozkatuenak_item_zerrenda:
            id = bozkatuena.item.id
            item_ids.append(id)
       
        item_bozkatuenak=item.objects.filter(id__in=item_ids) 
    
    non="fitxaE"  
    return render_to_response('itemak_hasiera.html',{'non':non,'itemak':itemak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak},context_instance=RequestContext(request))
    
def eguneko_itemak(request):
    itemak=[]
    itemak=item.objects.filter(egunekoa=1)
    
    paginator = Paginator(itemak, 26)
    
   
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
    page = request.GET.get('page')
    try:
        itemak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        itemak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        itemak = paginator.page(paginator.num_pages)
    
    #Proposatutakoak
    ##if(item.objects.filter(proposatutakoa=1)):
        ##itemak=item.objects.filter(proposatutakoa=1)
        
       
    return render_to_response('eguneko_itemak.html',{'itemak':itemak},context_instance=RequestContext(request))

def azkeneko_itemak(request):
    
    azkenekoak=[]
    azkenekoak=item.objects.order_by('-dc_date')[:5]

    return render_to_response('azkeneko_itemak.html',{'azkenekoak':azkenekoak},context_instance=RequestContext(request))

def azkeneko_ibilbideak(request):
    
    azkenekoak=[]
    azkenekoak=path.objects.order_by('-creation_date')[:5]

    return render_to_response('azkeneko_ibilbideak.html',{'azkenekoak':azkenekoak},context_instance=RequestContext(request))

def eguneko_ibilbideak(request):
    ibilbideak=[]
    ibilbideak=path.objects.filter(egunekoa=1)
    
    paginator = Paginator(ibilbideak, 26)
    
   
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
    page = request.GET.get('page')
    try:
        ibilbideak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ibilbideak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ibilbideak = paginator.page(paginator.num_pages)

    return render_to_response('eguneko_ibilbideak.html',{'ibilbideak':ibilbideak},context_instance=RequestContext(request))


def hornitzaile_fitxa_editatu(request):
    
        #INPLEMENTATU
    non="fitxaE"
    user_id=request.user.id
    hornitzaile =hornitzailea.objects.get(fk_user__id=user_id)
    return render_to_response('hornitzaile_fitxa_editatu.html',{'non':non,"hornitzailea":hornitzaile},context_instance=RequestContext(request))
    #return render_to_response('proposal.html',{'non':non,"hornitzailea":hornitzaile},context_instance=RequestContext(request))

def eguneko_itema_kendu(request):
    
    item_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    
    
    item.objects.filter(id=item_id).update(egunekoa = 0,proposatutakoa=1)   

    #GURI ALDAKETAREN BERRI EMAN?
    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko item hau kendu du (id): "+str(item_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko itemetan aldaketak', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        
        '''
        uri =randomword(10); 
    
        '''

        itemak=[]
        itemak=item.objects.order_by('-edm_year')
    
        paginator = Paginator(itemak, 26)
    
   
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
        page = request.GET.get('page')
        try:
            itemak = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            itemak = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            itemak = paginator.page(paginator.num_pages)
    
        #Egunekoak
        eguneko_itemak=[]
        eguneko_itemak=item.objects.filter(egunekoa=1)
    
        #Azkenak
        azken_itemak=[]
        azken_itemak=item.objects.order_by('-edm_year')[:10]
    
        #Bozkatuenak
        item_bozkatuenak=[]
        bozkatuenak_item_zerrenda= votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')[:10]
        if bozkatuenak_item_zerrenda:
            item_ids=[]
            for bozkatuena in bozkatuenak_item_zerrenda:
                id = bozkatuena.item.id
                item_ids.append(id)
       
            item_bozkatuenak=item.objects.filter(id__in=item_ids) 
    
        non="fitxaE"  
        return render_to_response('itemak_hasiera.html',{'non':non,'itemak':itemak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak},context_instance=RequestContext(request))

    elif(nondik=="bilaketa"):
        print "bilaketa orritik"
        # Helburu hizkuntza guztietan burutuko du bilaketa
        hizkuntza=request.GET['hizkRadio']   
        galdera=request.GET['search_input']
    
        #FILTROAK
        hizkuntzakF=request.GET['hizkuntzakF']
        hizkF=[] 
        hornitzaileakF=request.GET['hornitzaileakF']
        horniF=[]
        motakF=request.GET['motakF']
        motaF=[]
        ordenakF=request.GET['ordenakF']
        ordenaF=[]
        lizentziakF=request.GET['lizentziakF']
        lizentziaF=[]  
        besteakF=request.GET['besteakF']
        besteaF=[]
    
        items=[]
        paths=[]
        search_models_items = [item]
        search_models_paths = [path]
        bilaketa_filtroak=1
    
    
        #FILTROAK PRESTATU
        hEu="ez"
        hEs="ez"
        hEn="ez"
        if hizkuntzakF != "":       
            hizkF=hizkuntzakF.split(',')
            for h in hizkF:
                if(h=="eu"):
                    hEu="eu"
                if(h=="es"):
                    hEs="es"
                if(h=="en"):
                    hEn="en"
                
        horniEkm="ez"
        horniArrunta="ez"
        if hornitzaileakF != "":       
            horniF=hornitzaileakF.split(',')
            for h in horniF:
                if(h=="EuskoMedia"):
                    horniEkm="EuskoMedia"
                if(h=="herritarra"):
                    horniArrunta="herritarra"
        
        motaT="ez"
        motaS="ez"
        motaV="ez"  
        motaI="ez"  
        if motakF != "":       
            motaF=motakF.split(',')
            for m in motaF:
                if(m=="testua"):
                    motaT="TEXT"
                if(m=="audioa"):
                    motaS="SOUND"
                if(m=="bideoa"):
                    motaV="VIDEO"
                if(m=="irudia"):
                    motaI="IMAGE"
    
        oData="ez"
        oData2="ez"
        oBoto="ez"
        if ordenakF != "":       
            ordenaF=ordenakF.split(',')
            for o in ordenaF:
                if(o=="data"):
                    oData="data"
                if(o=="dataAsc"):
                    oData2="dataAsc"
                if(o=="botoak"):
                    Boto="botoak"
    
        lLibre="ez"
        lCommons="ez"
        lCopy="ez"
        if lizentziakF !="":
            lizentziaF=lizentziakF.split(',')
            for l in lizentziaF:
                if(l=="librea"):
                    lLibre="librea"
                if(l=="creativeCommons"):
                    lCommons="creativeCommons"
                if(l=="copyRight"):
                    lCopy="copyRight"
    
    
        bEgun="ez"
        bProp="ez"
        bWikify="ez"
        bIrudiBai="ez"
        bIrudiEz="ez"
        if besteakF != "":       
            besteaF=besteakF.split(',')
            for b in besteaF:
                if(b=="egunekoa"):
                    bEgun="egunekoa"
                if(b=="proposatutakoa"):
                    bProp="proposatutakoa"
                if(b=="wikifikatua"):
                    bWikify="wikifikatua"
                if(b=="irudiaDu"):
                    bIrudiBai="irudiaDu"
                if(b=="irudiaEzDu"):
                    bIrudiEz="irudiaEzDu"
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS
            #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                print "Motaren arabera filtratu"
                print items.count()
                print motaT
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])  
                print items.count()
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
               
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS
            paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
       
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
       
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
                
        elif hizkuntza == 'es':
       
            items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):             
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
 
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
      
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    aths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
        elif hizkuntza == 'en':
       
            items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
                    print "DATA GORAKA"
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
     
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
            
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
    
    
        #PAGINATOR ITEMS
        paginator = Paginator(items, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
    
        
    
        #PAGINATOR PATHS
        paginator = Paginator(paths, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
    
    
        z="i"
        return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    else:
        print "nondik ba?"
        
        
       

def eguneko_itema_gehitu(request):
    
    item_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    
    print "eguneko_itema_gehitu"
    item.objects.filter(id=item_id).update(egunekoa = 1)   

    #GURI ALDAKETAREN BERRI EMAN?
    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko item hau gehitu du (id): "+str(item_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko itemetan aldaketak', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        itemak=[]
        itemak=item.objects.order_by('-edm_year')
        paginator = Paginator(itemak, 26)
    
   
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
        page = request.GET.get('page')
        try:
            itemak = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            itemak = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            itemak = paginator.page(paginator.num_pages)
    
       
        #Egunekoak
        eguneko_itemak=[]
        eguneko_itemak=item.objects.filter(egunekoa=1)
    
        #Azkenak
        azken_itemak=[]
        azken_itemak=item.objects.order_by('-edm_year')[:10]
    
        #Bozkatuenak
        item_bozkatuenak=[]
        bozkatuenak_item_zerrenda= votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')[:10]
        if bozkatuenak_item_zerrenda:
            item_ids=[]
            for bozkatuena in bozkatuenak_item_zerrenda:
                id = bozkatuena.item.id
                item_ids.append(id)
       
            item_bozkatuenak=item.objects.filter(id__in=item_ids) 
    
        non="fitxaE"  
        return render_to_response('itemak_hasiera.html',{'non':non,'itemak':itemak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak},context_instance=RequestContext(request))

    elif(nondik=="bilaketa"):
        print "bilaketa orritik"
        # Helburu hizkuntza guztietan burutuko du bilaketa
        hizkuntza=request.GET['hizkRadio']   
        galdera=request.GET['search_input']
    
        #FILTROAK
        hizkuntzakF=request.GET['hizkuntzakF']
        hizkF=[] 
        hornitzaileakF=request.GET['hornitzaileakF']
        horniF=[]
        motakF=request.GET['motakF']
        motaF=[]
        ordenakF=request.GET['ordenakF']
        ordenaF=[]
        lizentziakF=request.GET['lizentziakF']
        lizentziaF=[]  
        besteakF=request.GET['besteakF']
        besteaF=[]
    
        items=[]
        paths=[]
        search_models_items = [item]
        search_models_paths = [path]
        bilaketa_filtroak=1
    
    
        #FILTROAK PRESTATU
        hEu="ez"
        hEs="ez"
        hEn="ez"
        if hizkuntzakF != "":       
            hizkF=hizkuntzakF.split(',')
            for h in hizkF:
                if(h=="eu"):
                    hEu="eu"
                if(h=="es"):
                    hEs="es"
                if(h=="en"):
                    hEn="en"
                
        horniEkm="ez"
        horniArrunta="ez"
        if hornitzaileakF != "":       
            horniF=hornitzaileakF.split(',')
            for h in horniF:
                if(h=="EuskoMedia"):
                    horniEkm="EuskoMedia"
                if(h=="herritarra"):
                    horniArrunta="herritarra"
        
        motaT="ez"
        motaS="ez"
        motaV="ez"  
        motaI="ez"  
        if motakF != "":       
            motaF=motakF.split(',')
            for m in motaF:
                if(m=="testua"):
                    motaT="TEXT"
                if(m=="audioa"):
                    motaS="SOUND"
                if(m=="bideoa"):
                    motaV="VIDEO"
                if(m=="irudia"):
                    motaI="IMAGE"
    
        oData="ez"
        oData2="ez"
        oBoto="ez"
        if ordenakF != "":       
            ordenaF=ordenakF.split(',')
            for o in ordenaF:
                if(o=="data"):
                    oData="data"
                if(o=="dataAsc"):
                    oData2="dataAsc"
                if(o=="botoak"):
                    Boto="botoak"
    
        lLibre="ez"
        lCommons="ez"
        lCopy="ez"
        if lizentziakF !="":
            lizentziaF=lizentziakF.split(',')
            for l in lizentziaF:
                if(l=="librea"):
                    lLibre="librea"
                if(l=="creativeCommons"):
                    lCommons="creativeCommons"
                if(l=="copyRight"):
                    lCopy="copyRight"
    
    
        bEgun="ez"
        bProp="ez"
        bWikify="ez"
        bIrudiBai="ez"
        bIrudiEz="ez"
        if besteakF != "":       
            besteaF=besteakF.split(',')
            for b in besteaF:
                if(b=="egunekoa"):
                    bEgun="egunekoa"
                if(b=="proposatutakoa"):
                    bProp="proposatutakoa"
                if(b=="wikifikatua"):
                    bWikify="wikifikatua"
                if(b=="irudiaDu"):
                    bIrudiBai="irudiaDu"
                if(b=="irudiaEzDu"):
                    bIrudiEz="irudiaEzDu"
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS
            #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                print "Motaren arabera filtratu"
                print items.count()
                print motaT
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])  
                print items.count()
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
               
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS
            paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
       
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
       
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
                
        elif hizkuntza == 'es':
       
            items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):             
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
 
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
      
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    aths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
        elif hizkuntza == 'en':
       
            items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
                    print "DATA GORAKA"
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
     
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
            
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
    
    
        #PAGINATOR ITEMS
        paginator = Paginator(items, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
    
        
    
        #PAGINATOR PATHS
        paginator = Paginator(paths, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
    
    
        z="i"
        return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    else:
        print "nondik ba?"
        
        
#EGUNEKO IBILBIDEA KUDEATZEKO BI FUNTZIO
def eguneko_ibilbidea_gehitu(request):
    
    path_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    
    print "eguneko_itema_gehitu"
    path.objects.filter(id=path_id).update(egunekoa = 1)   

    #GURI ALDAKETAREN BERRI EMAN?    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko ibilbide hau gehitu du (id): "+str(path_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko ibilbidetan aldaketak', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        paths=[]
        paths=path.objects.order_by('-creation_date')
        paginator = Paginator(paths, 26)
    
   
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
        
        
        #Egunekoak
        eguneko_ibilbideak=[]
        eguneko_ibilbideak=path.objects.filter(egunekoa=1)
    
        #Azkenak
        azken_ibilbideak=[]
        azken_ibilbideak=path.objects.order_by('-creation_date')[:10]
    
        #Bozkatuenak
        ibilbide_bozkatuenak=[]
        bozkatuenak_ibilbide_zerrenda= votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')[:10]
        if bozkatuenak_ibilbide_zerrenda:
            path_ids=[]
            for bozkatuena in bozkatuenak_ibilbide_zerrenda:
                id = bozkatuena.path.id
                path_ids.append(id)
       
            ibilbide_bozkatuenak=path.objects.filter(id__in=path_ids) 
    
        non="fitxaE"  
    
    
       
        return render_to_response('ibilbideak_hasiera.html',{'non':non,'paths':paths,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak},context_instance=RequestContext(request))
    elif(nondik=="bilaketa"):
        print "bilaketa orritik"
        # Helburu hizkuntza guztietan burutuko du bilaketa
        hizkuntza=request.GET['hizkRadio']   
        galdera=request.GET['search_input']
    
        #FILTROAK
        hizkuntzakF=request.GET['hizkuntzakF']
        hizkF=[] 
        hornitzaileakF=request.GET['hornitzaileakF']
        horniF=[]
        motakF=request.GET['motakF']
        motaF=[]
        ordenakF=request.GET['ordenakF']
        ordenaF=[]
        lizentziakF=request.GET['lizentziakF']
        lizentziaF=[]  
        besteakF=request.GET['besteakF']
        besteaF=[]
    
        items=[]
        paths=[]
        search_models_items = [item]
        search_models_paths = [path]
        bilaketa_filtroak=1
    
    
        #FILTROAK PRESTATU
        hEu="ez"
        hEs="ez"
        hEn="ez"
        if hizkuntzakF != "":       
            hizkF=hizkuntzakF.split(',')
            for h in hizkF:
                if(h=="eu"):
                    hEu="eu"
                if(h=="es"):
                    hEs="es"
                if(h=="en"):
                    hEn="en"
                
        horniEkm="ez"
        horniArrunta="ez"
        if hornitzaileakF != "":       
            horniF=hornitzaileakF.split(',')
            for h in horniF:
                if(h=="EuskoMedia"):
                    horniEkm="EuskoMedia"
                if(h=="herritarra"):
                    horniArrunta="herritarra"
        
        motaT="ez"
        motaS="ez"
        motaV="ez"  
        motaI="ez"  
        if motakF != "":       
            motaF=motakF.split(',')
            for m in motaF:
                if(m=="testua"):
                    motaT="TEXT"
                if(m=="audioa"):
                    motaS="SOUND"
                if(m=="bideoa"):
                    motaV="VIDEO"
                if(m=="irudia"):
                    motaI="IMAGE"
    
        oData="ez"
        oData2="ez"
        oBoto="ez"
        if ordenakF != "":       
            ordenaF=ordenakF.split(',')
            for o in ordenaF:
                if(o=="data"):
                    oData="data"
                if(o=="dataAsc"):
                    oData2="dataAsc"
                if(o=="botoak"):
                    Boto="botoak"
    
        lLibre="ez"
        lCommons="ez"
        lCopy="ez"
        if lizentziakF !="":
            lizentziaF=lizentziakF.split(',')
            for l in lizentziaF:
                if(l=="librea"):
                    lLibre="librea"
                if(l=="creativeCommons"):
                    lCommons="creativeCommons"
                if(l=="copyRight"):
                    lCopy="copyRight"
    
    
        bEgun="ez"
        bProp="ez"
        bWikify="ez"
        bIrudiBai="ez"
        bIrudiEz="ez"
        if besteakF != "":       
            besteaF=besteakF.split(',')
            for b in besteaF:
                if(b=="egunekoa"):
                    bEgun="egunekoa"
                if(b=="proposatutakoa"):
                    bProp="proposatutakoa"
                if(b=="wikifikatua"):
                    bWikify="wikifikatua"
                if(b=="irudiaDu"):
                    bIrudiBai="irudiaDu"
                if(b=="irudiaEzDu"):
                    bIrudiEz="irudiaEzDu"
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS
            #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
               
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS
            paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
       
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
       
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
                
        elif hizkuntza == 'es':
       
            items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):             
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
 
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
      
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    aths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
        elif hizkuntza == 'en':
       
            items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
                    print "DATA GORAKA"
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
     
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
            
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
    
    
        #PAGINATOR ITEMS
        paginator = Paginator(items, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
    
        
    
        #PAGINATOR PATHS
        paginator = Paginator(paths, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
    
    
        z="p"
        return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    else:
        print "nondik ba?"

def eguneko_ibilbidea_kendu(request):
    
    path_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    

    
    path.objects.filter(id=path_id).update(egunekoa = 0,proposatutakoa=1)   

    #GURI ALDAKETAREN BERRI EMAN?
    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko ibilbide hau kendu du (id): "+str(path_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko ibilbideetan aldaketak', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
       
        paths=[]
        paths=path.objects.order_by('-creation_date')
        paginator = Paginator(paths, 26)

   
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
    
        #Egunekoak
        eguneko_ibilbideak=[]
        eguneko_ibilbideak=path.objects.filter(egunekoa=1)
    
        #Azkenak
        azken_ibilbideak=[]
        azken_ibilbideak=path.objects.order_by('-creation_date')[:10]
    
        #Bozkatuenak
        ibilbide_bozkatuenak=[]
        bozkatuenak_ibilbide_zerrenda= votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')[:10]
        if bozkatuenak_ibilbide_zerrenda:
            path_ids=[]
            for bozkatuena in bozkatuenak_ibilbide_zerrenda:
                id = bozkatuena.path.id
                path_ids.append(id)
       
            ibilbide_bozkatuenak=path.objects.filter(id__in=path_ids) 
    
        non="fitxaE"  

        return render_to_response('ibilbideak_hasiera.html',{'non':non,'paths':paths,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak},context_instance=RequestContext(request))
    elif(nondik=="bilaketa"):
        print "bilaketa orritik"
        # Helburu hizkuntza guztietan burutuko du bilaketa
        hizkuntza=request.GET['hizkRadio']   
        galdera=request.GET['search_input']
    
        #FILTROAK
        hizkuntzakF=request.GET['hizkuntzakF']
        hizkF=[] 
        hornitzaileakF=request.GET['hornitzaileakF']
        horniF=[]
        motakF=request.GET['motakF']
        motaF=[]
        ordenakF=request.GET['ordenakF']
        ordenaF=[]
        lizentziakF=request.GET['lizentziakF']
        lizentziaF=[]  
        besteakF=request.GET['besteakF']
        besteaF=[]
    
        items=[]
        paths=[]
        search_models_items = [item]
        search_models_paths = [path]
        bilaketa_filtroak=1
    
    
        #FILTROAK PRESTATU
        hEu="ez"
        hEs="ez"
        hEn="ez"
        if hizkuntzakF != "":       
            hizkF=hizkuntzakF.split(',')
            for h in hizkF:
                if(h=="eu"):
                    hEu="eu"
                if(h=="es"):
                    hEs="es"
                if(h=="en"):
                    hEn="en"
                
        horniEkm="ez"
        horniArrunta="ez"
        if hornitzaileakF != "":       
            horniF=hornitzaileakF.split(',')
            for h in horniF:
                if(h=="EuskoMedia"):
                    horniEkm="EuskoMedia"
                if(h=="herritarra"):
                    horniArrunta="herritarra"
        
        motaT="ez"
        motaS="ez"
        motaV="ez"  
        motaI="ez"  
        if motakF != "":       
            motaF=motakF.split(',')
            for m in motaF:
                if(m=="testua"):
                    motaT="TEXT"
                if(m=="audioa"):
                    motaS="SOUND"
                if(m=="bideoa"):
                    motaV="VIDEO"
                if(m=="irudia"):
                    motaI="IMAGE"
    
        oData="ez"
        oData2="ez"
        oBoto="ez"
        if ordenakF != "":       
            ordenaF=ordenakF.split(',')
            for o in ordenaF:
                if(o=="data"):
                    oData="data"
                if(o=="dataAsc"):
                    oData2="dataAsc"
                if(o=="botoak"):
                    Boto="botoak"
    
        lLibre="ez"
        lCommons="ez"
        lCopy="ez"
        if lizentziakF !="":
            lizentziaF=lizentziakF.split(',')
            for l in lizentziaF:
                if(l=="librea"):
                    lLibre="librea"
                if(l=="creativeCommons"):
                    lCommons="creativeCommons"
                if(l=="copyRight"):
                    lCopy="copyRight"
    
    
        bEgun="ez"
        bProp="ez"
        bWikify="ez"
        bIrudiBai="ez"
        bIrudiEz="ez"
        if besteakF != "":       
            besteaF=besteakF.split(',')
            for b in besteaF:
                if(b=="egunekoa"):
                    bEgun="egunekoa"
                if(b=="proposatutakoa"):
                    bProp="proposatutakoa"
                if(b=="wikifikatua"):
                    bWikify="wikifikatua"
                if(b=="irudiaDu"):
                    bIrudiBai="irudiaDu"
                if(b=="irudiaEzDu"):
                    bIrudiEz="irudiaEzDu"
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS
            #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
               
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS
            paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
       
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
       
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
                
        elif hizkuntza == 'es':
       
            items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):             
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
 
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
      
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
           
                if bIrudiBai=="irudiaDu":             
                    aths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
        elif hizkuntza == 'en':
       
            items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            if(hornitzaileakF != ""):
                if(horniEkm=="ekm"):
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
                else:
                    items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
            #Mota filtroa, edm_type=SOUND
            if(motakF != ""):
                items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
            #Ordena Filtroa
            bozkatuenak_item_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                if(oData2 == "dataAsc"):
                    print "DATA GORAKA"
                    #items = items.order_by('-dc_date')
                    items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                    items_ids=[]
                    for itema in items:
                        id = itema.item_id
                        items_ids.append(id)
                    #Ordena mantentzen du??                        
                    items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
            #Lizentziak filtroa
            if lizentziakF !="":  
                if  lLibre=="librea":
                    items=items.filter(edm_rights='librea')
                if lCommons=="creativeCommons":
                    items=items.filter(edm_rights='creativeCommons')
                if lCopy=="copyRight":
                    items=items.filter(edm_rights='copyRight')                
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(wikifikatua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):
           
                if(horniEkm=="ekm"):
                
                    hornitzaileakF=hornitzaileakF+"ekm"
                    hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                    hornitzaile_erab=User.objects.get(username='ekm')
                    paths = paths.filter(path_fk_user_id=hornitzaile_erab)
                else:      
                        
                    items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
     
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azkarragoa            
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                    paths_ids=[]
                    for patha in paths:
                        id = patha.path_id
                        paths_ids.append(id)
                    #Ordena mantentzen du??                        
                    paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
      
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    paths=paths.filter(path_egunekoa=1)
                if bProp == "proposatutakoa":
                    paths=paths.filter(path_proposatutakoa=1)
            
                if bIrudiBai=="irudiaDu":             
                    paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
    
    
        #PAGINATOR ITEMS
        paginator = Paginator(items, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
    
        
    
        #PAGINATOR PATHS
        paginator = Paginator(paths, 26)    
        type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
        page = request.GET.get('page')
        try:
            paths = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paths = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paths = paginator.page(paginator.num_pages)
    
    
        z="p"
        return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    else:
        print "nondik ba?"
        
        

     
def ibilbideak_hasiera(request):
    
    #Ibilbideen hasierako pantailan erakutsi behar diren Ibilbideen informazioa datu-basetik lortu eta pasa
     
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK/IKUSIENA PATHA LORTZEKO   
    #DB-an GALDERA EGIN EGUNEKO IBILBIDEA LORTZEKO
    paths=[]
    paths=path.objects.order_by('-creation_date')
    
    paginator = Paginator(paths, 26)
    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        paths = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paths = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paths = paginator.page(paginator.num_pages)
    
    #Egunekoak
    eguneko_ibilbideak=[]
    eguneko_ibilbideak=path.objects.filter(egunekoa=1)
    
    #Azkenak
    azken_ibilbideak=[]
    azken_ibilbideak=path.objects.order_by('-creation_date')[:10]
    
    #Bozkatuenak
    ibilbide_bozkatuenak=[]
    bozkatuenak_ibilbide_zerrenda= votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')[:10]
    if bozkatuenak_ibilbide_zerrenda:
        path_ids=[]
        for bozkatuena in bozkatuenak_ibilbide_zerrenda:
            id = bozkatuena.path.id
            path_ids.append(id)
       
        ibilbide_bozkatuenak=item.objects.filter(id__in=path_ids) 
    
    non="fitxaE"  
    
    return render_to_response('ibilbideak_hasiera.html',{'non':non,'paths':paths,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak},context_instance=RequestContext(request))

    '''
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
    '''

def hornitzaileak_hasiera(request):
    print "hornitzaileak_hasiera"
    hornitzaileak=hornitzailea.objects.all()
    return render_to_response('hornitzaileak_hasiera.html',{'hornitzaileak':hornitzaileak},context_instance=RequestContext(request))
    
def hornitzailea_ikusi(request):
   
    non="fitxaI"
    id=request.GET['id']
    hornitzaile=hornitzailea.objects.get(fk_user__id=id)
    print non
    return render_to_response('hornitzailea_ikusi.html',{'non':non,'hornitzailea':hornitzaile},context_instance=RequestContext(request))
    
def autocomplete(request):
    
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:4]
    #suggestions = [result.item_id for result in sqs]
    
    #suggestions = [result.dc_title for result in sqs]
    
    # html ETIKETEN GARBIKETA EGIN HEMEN
    suggestions=[]
    for result in sqs:
        titulua = result.dc_title
        titulua = titulua.replace("<div class=\"titulu_es\">", " ")
        titulua = titulua.replace("</div>", " ")
        titulua = titulua.replace("<div class=\"titulu_en\">", " ")
        #titulua = titulua.replace("</div>", " ")
        titulua = titulua.replace("<div class=\"titulu_eu\">", " ")
        #titulua = titulua.replace("</div>", " ")
        titulua = titulua.replace("<div class=\"titulu_lg\">", " ")
        suggestions.append(titulua)
    
    
    #print suggestions
    suggestions_id = [result.item_id for result in sqs]
    suggestions_img = [result.edm_object for result in sqs]
    #suggestions_src = [result.edm_provider for result in sqs]
    suggestions_src=[]
    for result in sqs:
        if result.edm_provider == "herritarra" or result.edm_provider == "Herritarra" :
            src=result.dc_creator
            suggestions_src.append(src)
        else:
            src=result.edm_provider
            suggestions_src.append(src)
    
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions,
        'results_id': suggestions_id,
        'results_img':suggestions_img,
        'results_src':suggestions_src
    })
    print the_data
    return HttpResponse(the_data, content_type='application/json')





def cross_search(request):
    print "cross_search"
    #Defektuz itemen orria erakusteko
    z="i"
    # Helburu hizkuntza guztietan burutuko du bilaketa
    if(request.POST):
        hizkuntza=request.POST['hizkRadio']   
        galdera=request.POST['search_input']
    
    if(request.GET):
        hizkuntza=request.GET['hizkRadio']   
        galdera=request.GET['search_input']
        #zein paginator den
        z=request.GET['z']
  
    items=[]
    paths=[]
    search_models_items = [item]
    search_models_paths = [path]
    
    #egiteko: hizkuntza edozein dela ere, galdera hutsunea bada, item guztiak erakutsi
    
    if hizkuntza == 'eu':
     
        #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)
        items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)
        print "CROSS_SEARCH"
        print items.count()
        paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
 
    elif hizkuntza == 'es':
       
        #items = itemIndex.objects.filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera))
        #paths = pathIndex.objects.filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera))
       
        items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
        paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
    
    
        
    elif hizkuntza == 'en':
        
        #items = itemIndex.objects.filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera))
        #paths = pathIndex.objects.filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera))

        items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)

    
    #PAGINATOR ITEMS
    paginator = Paginator(items, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    
    
    
    
    #PAGINATOR PATHS
    paginator = Paginator(paths, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        paths = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paths = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paths = paginator.page(paginator.num_pages)
    
    
    
    bilaketa_filtroak=1
    return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))


def hornitzaile_search(request):
    # Hornitzaile jakin baten item eta ibilbide guztiak bilatuko dira
    #username
    hornitzaile_izena=request.GET['h']
    #Erab id
    hornitzaile_id=request.GET['h_id']
    #zein paginator den
    z=request.GET['z']
  
    galdera=""
    hizkuntza="eu"
    horniF=[]
    horniF.append(hornitzaile_izena)
   
    items=[]
    paths=[]
    search_models_items = [item]
    search_models_paths = [path]
    
    #Hornitzaileak taula gehitzen ditugunean agian hau aldatuko da
    hornitzaile_erab=User.objects.get(username=hornitzaile_izena)
    
    #Itemak erabiltzaileekin lotzean hau aldatu
    #items = SearchQuerySet().all().filter(fk_ob_user__id=hornitzaile_id).models(*search_models_items) 
    items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
    #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_erab).models(*search_models_paths)
    paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)

    
  
    #PAGINATOR ITEMS
    paginator = Paginator(items, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    
        
    
    #PAGINATOR PATHS
    paginator = Paginator(paths, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        paths = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paths = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paths = paginator.page(paginator.num_pages)
    
    
    #HORNITZAILEAREN FITXA 
    #user_id=request.user.id
    hornitzaile = hornitzailea.objects.get(fk_user__id=hornitzaile_erab.id)
   
    geoloc_longitude=0.0
    geoloc_latitude=0.0
    geoloc_longitude=hornitzaile.geoloc_longitude
    geoloc_latitude=hornitzaile.geoloc_latitude
    
    bilaketa_filtroak=1
    return render_to_response('cross_search.html',{'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzaile,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))

def filtro_search(request):
    
   
    # Helburu hizkuntza guztietan burutuko du bilaketa
    hizkuntza=request.GET['hizkRadio']   
    galdera=request.GET['search_input']
    z=request.GET['z']
    if 'hornitzailea' in request.GET:
        hornitzaile_izena=request.GET['hornitzailea']
    else:
        hornitzaile_izena=""
    
    
    hizkuntzakF=request.GET['hizkuntzakF']
    hizkF=[] 
    hornitzaileakF=request.GET['hornitzaileakF']
    horniF=[]
    motakF=request.GET['motakF']
    motaF=[]
    ordenakF=request.GET['ordenakF']
    ordenaF=[]
    lizentziakF=request.GET['lizentziakF']
    lizentziaF=[]  
    besteakF=request.GET['besteakF']
    besteaF=[]
    
    items=[]
    paths=[]
    search_models_items = [item]
    search_models_paths = [path]
    bilaketa_filtroak=1
    
    
    #FILTROAK PRESTATU
    hEu="ez"
    hEs="ez"
    hEn="ez"
    if hizkuntzakF != "": 
        hizkF=hizkuntzakF.split(',')
        print "split hizkuntzakF"
        print hizkF
        for h in hizkF:
            print h
            if(h=="eu"):
                hEu="eu"
            if(h=="es"):
                hEs="es"
            if(h=="en"):
                hEn="en"
                
    horniEkm="ez"
    horniArrunta="ez"
    if hornitzaileakF != "":       
        horniF=hornitzaileakF.split(',')
        for h in horniF:
            if(h=="EuskoMedia"):
                horniEkm="EuskoMedia"
            if(h=="herritarra"):
                horniArrunta="herritarra"
        
    motaT="ez"
    motaS="ez"
    motaV="ez"  
    motaI="ez"  
    if motakF != "":       
        motaF=motakF.split(',')
        for m in motaF:
            if(m=="testua"):
                motaT="TEXT"
            if(m=="audioa"):
                motaS="SOUND"
            if(m=="bideoa"):
                motaV="VIDEO"
            if(m=="irudia"):
                motaI="IMAGE"
    
    oData="ez"
    oData2="ez"
    oBoto="ez"
    if ordenakF != "":       
        ordenaF=ordenakF.split(',')
        for o in ordenaF:
            if(o=="data"):
                oData="data"
            if(o=="dataAsc"):
                oData2="dataAsc"
            if(o=="botoak"):
                oBoto="botoak"
    
    lLibre="ez"
    lCommons="ez"
    lCopy="ez"
    if lizentziakF !="":
        lizentziaF=lizentziakF.split(',')
        for l in lizentziaF:
            if(l=="librea"):
                lLibre="librea"
            if(l=="creativeCommons"):
                lCommons="creativeCommons"
            if(l=="copyRight"):
                lCopy="copyRight"
    
    
    bEgun="ez"
    bProp="ez"
    bWikify="ez"
    bIrudiBai="ez"
    bIrudiEz="ez"
    if besteakF != "":       
        besteaF=besteakF.split(',')
        for b in besteaF:
            if(b=="egunekoa"):
                bEgun="egunekoa"
            if(b=="proposatutakoa"):
                bProp="proposatutakoa"
            if(b=="wikifikatua"):
                bWikify="wikifikatua"
            if(b=="irudiaDu"):
                bIrudiBai="irudiaDu"
            if(b=="irudiaEzDu"):
                bIrudiEz="irudiaEzDu"
    
    #GALDERA BOTA
    if hizkuntza == 'eu':
        #ITEMS
        #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
        if (galdera ==""):
            print "galdera null"
            items = SearchQuerySet().all().models(*search_models_items)  
           
            
            print items.count() 
        else:
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            if(horniEkm=="ekm"):
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
            else:
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
        #Mota filtroa, edm_type=SOUND
        if(motakF != ""):
            print "Motaren arabera filtratu"
            print items.count()
            print motaT
            items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])  
            print items.count()
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
            if(oData2 == "dataAsc"):
                print "DATA GORAKA"
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                items_ids=[]
                for itema in items:
                    id = itema.item_id
                    items_ids.append(id)
                #Ordena mantentzen du??                        
                items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
        #Lizentziak filtroa
        if lizentziakF !="":  
            if  lLibre=="librea":
                items=items.filter(edm_rights='librea')
            if lCommons=="creativeCommons":
                items=items.filter(edm_rights='creativeCommons')
            if lCopy=="copyRight":
                items=items.filter(edm_rights='copyRight')                
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=1)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(wikifikatua=1)
            if bIrudiBai=="irudiaDu":             
                #import pdb
                #pdb.set_trace()             
                #self.searchqueryset.exclude(edm_object = None ) hau egiten du behekoak
                items=items.filter(edm_object = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
        #PATHS
        paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa TXUKUNDUUUU
        if(hornitzaileakF != ""):
            
            '''
            if(horniEkm=="herritarra"):
                #Hornitzaileak diren erabiltzaileak hartu
                paths = paths.exclude(path_fk_user_id__in=hornitzaile_erab)
            else:
                
                paths = paths.filter(path_fk_user_id__in=hornitzaile_erab)
            '''
           
            if(horniEkm=="ekm"):
                
                hornitzaileakF=hornitzaileakF+"ekm"
                hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                hornitzaile_erab=User.objects.get(username='ekm')
                paths = paths.filter(path_fk_user_id=hornitzaile_erab)
            else:      
                        
                items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
        #Mota filtroa,IBILBIDEETAN EZ DAGO MOTA
        #if(motakF != ""):
            #paths = paths
        #Ordena Filtroa
        bozkatuenak_path_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                paths = paths.order_by('-path_creation_date')
            if(oData2 == "dataAsc"):
                paths = paths.order_by('path_creation_date')              
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                paths_ids=[]
                for patha in paths:
                    id = patha.path_id
                    paths_ids.append(id)
                #Ordena mantentzen du??                        
                paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
        #Lizentziak filtroa,IBILBIDEETAN EZ DAGO LIZENTZIA
        #if lizentziakF !="": 
            #paths = paths
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                paths=paths.filter(path_egunekoa=1)
            if bProp == "proposatutakoa":
                paths=paths.filter(path_proposatutakoa=1)
            #if bWikify=="wikifikatua":
                #paths = paths
            if bIrudiBai=="irudiaDu":             
                paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
                
    elif hizkuntza == 'es':
       
        items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            if(horniEkm=="ekm"):
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
            else:
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
        #Mota filtroa, edm_type=SOUND
        if(motakF != ""):
            items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
            if(oData2 == "dataAsc"):
                print "DATA GORAKA"
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                items_ids=[]
                for itema in items:
                    id = itema.item_id
                    items_ids.append(id)
                #Ordena mantentzen du??                        
                items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
        #Lizentziak filtroa
        if lizentziakF !="":  
            if  lLibre=="librea":
                items=items.filter(edm_rights='librea')
            if lCommons=="creativeCommons":
                items=items.filter(edm_rights='creativeCommons')
            if lCopy=="copyRight":
                items=items.filter(edm_rights='copyRight')                
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=1)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(wikifikatua=1)
            if bIrudiBai=="irudiaDu":             
                #import pdb
                #pdb.set_trace()             
                #self.searchqueryset.exclude(edm_object = None ) hau egiten du behekoak
                items=items.filter(edm_object = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
        paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa TXUKUNDUUUU
        if(hornitzaileakF != ""):
            
            '''
            if(horniEkm=="arrunta"):
                #Hornitzaileak diren erabiltzaileak hartu
                paths = paths.exclude(path_fk_user_id__in=hornitzaile_erab)
            else:
                
                paths = paths.filter(path_fk_user_id__in=hornitzaile_erab)
            '''
           
            if(horniEkm=="ekm"):
                
                hornitzaileakF=hornitzaileakF+"ekm"
                hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                hornitzaile_erab=User.objects.get(username='ekm')
                paths = paths.filter(path_fk_user_id=hornitzaile_erab)
            else:      
                        
                items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
        #Mota filtroa,IBILBIDEETAN EZ DAGO MOTA
        #if(motakF != ""):
            #paths = paths
        #Ordena Filtroa
        bozkatuenak_path_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                paths = paths.order_by('-path_creation_date')
            if(oData2 == "dataAsc"):
                paths = paths.order_by('path_creation_date')              
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                paths_ids=[]
                for patha in paths:
                    id = patha.path_id
                    paths_ids.append(id)
                #Ordena mantentzen du??                        
                paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
        #Lizentziak filtroa,IBILBIDEETAN EZ DAGO LIZENTZIA
        #if lizentziakF !="": 
            #paths = paths
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                paths=paths.filter(path_egunekoa=1)
            if bProp == "proposatutakoa":
                paths=paths.filter(path_proposatutakoa=1)
            #if bWikify=="wikifikatua":
                #paths = paths
            if bIrudiBai=="irudiaDu":             
                paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    elif hizkuntza == 'en':
        print "radio hizk en"
        items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            if(horniEkm=="ekm"):
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta,"ekm"])
            else:
                items = items.filter(edm_provider__in=[horniEkm,horniArrunta])
        #Mota filtroa, edm_type=SOUND
        if(motakF != ""):
            items = items.filter(edm_type__in=[motaT,motaS,motaV,motaI])       
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
            if(oData2 == "dataAsc"):
                print "DATA GORAKA"
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
    
                items_ids=[]
                for itema in items:
                    id = itema.item_id
                    items_ids.append(id)
                #Ordena mantentzen du??                        
                items=bozkatuenak_item_zerrenda.filter(id__in=items_ids)                
        #Lizentziak filtroa
        if lizentziakF !="":  
            if  lLibre=="librea":
                items=items.filter(edm_rights='librea')
            if lCommons=="creativeCommons":
                items=items.filter(edm_rights='creativeCommons')
            if lCopy=="copyRight":
                items=items.filter(edm_rights='copyRight')                
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=1)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(wikifikatua=1)
            if bIrudiBai=="irudiaDu":             
                #import pdb
                #pdb.set_trace()             
                #self.searchqueryset.exclude(edm_object = None ) hau egiten du behekoak
                items=items.filter(edm_object = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
        paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa TXUKUNDUUUU
        if(hornitzaileakF != ""):
            
            '''
            if(horniEkm=="herritarra"):
                #Hornitzaileak diren erabiltzaileak hartu
                paths = paths.exclude(path_fk_user_id__in=hornitzaile_erab)
            else:
                
                paths = paths.filter(path_fk_user_id__in=hornitzaile_erab)
            '''
           
            if(horniEkm=="ekm"):
                
                hornitzaileakF=hornitzaileakF+"ekm"
                hornitzaile_erab=User.objects.get(username__in=hornitzaileakF)
                hornitzaile_erab=User.objects.get(username='ekm')
                paths = paths.filter(path_fk_user_id=hornitzaile_erab)
            else:      
                        
                items = items #.exclude(path_fk_user_id=hornitzaile_erab)
       
        #Mota filtroa,IBILBIDEETAN EZ DAGO MOTA
        #if(motakF != ""):
            #paths = paths
        #Ordena Filtroa
        bozkatuenak_path_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                paths = paths.order_by('-path_creation_date')
            if(oData2 == "dataAsc"):
                paths = paths.order_by('path_creation_date')              
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
    
                paths_ids=[]
                for patha in paths:
                    id = patha.path_id
                    paths_ids.append(id)
                #Ordena mantentzen du??                        
                paths=bozkatuenak_path_zerrenda.filter(id__in=paths_ids)  
        
        #Lizentziak filtroa,IBILBIDEETAN EZ DAGO LIZENTZIA
        #if lizentziakF !="": 
            #paths = paths
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                paths=paths.filter(path_egunekoa=1)
            if bProp == "proposatutakoa":
                paths=paths.filter(path_proposatutakoa=1)
            #if bWikify=="wikifikatua":
                #paths = paths
            if bIrudiBai=="irudiaDu":             
                paths=paths.filter(path_thumbnail = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                paths=paths.exclude(path_thumbnail = Raw("[* TO *]"))
    
    
    
    #PAGINATOR ITEMS
    paginator = Paginator(items, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    
        
    
    #PAGINATOR PATHS
    paginator = Paginator(paths, 26)    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
    
    page = request.GET.get('page')
    try:
        paths = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paths = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paths = paginator.page(paginator.num_pages)
    
    
    if hornitzaile_izena:
       
        hornitzaile = hornitzailea.objects.get(fk_user__username=hornitzaile_izena)
        return render_to_response('cross_search.html',{'hornitzailea':hornitzaile,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkuntzakF':hizkF,'horniF':hornitzaileakF,'motaF':motakF,'ordenaF':ordenakF,'lizentziaF':lizentziakF,'besteaF':besteakF},context_instance=RequestContext(request))
    else:
        return render_to_response('cross_search.html',{'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkuntzakF,'horniF':hornitzaileakF,'motaF':motakF,'ordenaF':ordenakF,'lizentziaF':lizentziakF,'besteaF':besteakF},context_instance=RequestContext(request))

def nabigazioa_hasi(request):
    
    print "nabigazioa_hasi"
    if 'path_id' in request.GET:
        path_id=request.GET['path_id']
        
        momentukoPatha=path.objects.get(id=path_id)
        
        #Ibilbidearen Hasierak hartu
        hasieraNodoak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
    
        
        #Hasierako nodo bat lortu
        momentukoNodea = node.objects.filter(fk_path_id=momentukoPatha, paths_start=1)[0]
        item_id=momentukoNodea.fk_item_id.id
        
        hurrengoak=momentukoNodea.paths_next
        aurrekoak=momentukoNodea.paths_prev
    
        hurrengoak_list=[]
        hasieraBakarra=0
        #node taulatik "hurrengoak" tuplak hartu 
        if(hurrengoak != ""):
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
        elif(hasieraNodoak.count()==1):
          
            hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
            hasieraBakarra=1
        else:
            hasieraBakarra=0       
            hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
            
    
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
        botatuDuItem=0
        if not request.user.is_anonymous():
            if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
                botatuDuPath=1           
            if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
                botatuDuItem=1
   
        #Momentuko Ibilbidea lortu
        momentukoIbilbidea=path.objects.get(id=path_id)
    
        botoKopuruaPath=momentukoIbilbidea.get_votes()
        botoKopuruaItem=momentukoItema.get_votes()
    
        autoplay=0
        
        #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
        pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
        itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=momentukoItema)
        
        #LORTU IBILBIDEAREN KOMENTARIOAK
        comments = momentukoPatha.get_comments()    
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        
        #Ezkerreko zutabea ez erakusteko
        non="fitxaE"
        return render_to_response('ibilbidea.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    
    return False
        

def autoplay_hasieratik(request):
    
   
    if 'path_id' in request.GET:
       
        
        path_id=request.GET['path_id']        
        momentukoPatha=path.objects.get(id=path_id)
        
        #Ibilbidearen Hasierak hartu
        nodes = [] 
        erroak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
  
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
        
        #Autonabigaziorako orrien path-ak sortu
        autoplaypages=[]
        for nodoa in nodes:
           
            #id=nodoa.id
            nodoID_str=str(nodoa.fk_item_id.id)
            path_id_str=str(path_id)
            
            #nodoID_str=map(lambda x: str(x),nodoa.id)
            #path_id_str=map(lambda x: str(x),path_id)
                    
            berria = 'nabigatu?path_id='+path_id_str+'&item_id='+nodoID_str;
            print berria
          
            autoplaypages.append(berria)
                      
        #
        
        #Hasierako nodo bat lortu
        momentukoNodea = node.objects.filter(fk_path_id=momentukoPatha, paths_start=1)[0]
        item_id=momentukoNodea.fk_item_id.id
        
        hurrengoak=momentukoNodea.paths_next
        aurrekoak=momentukoNodea.paths_prev
    
        hurrengoak_list=[]
        hasieraBakarra=0
        #node taulatik "hurrengoak" tuplak hartu 
        if(hurrengoak != ""):
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
        elif(erroak.count()==1):
          
            hurrengoak_list=map(lambda x: x.fk_item_id.id,list(erroak))
            hasieraBakarra=1
        else:
            hasieraBakarra=0       
            hurrengoak_list=map(lambda x: x.fk_item_id.id,list(erroak))
            
    
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
        botatuDuItem=0
        if not request.user.is_anonymous():
            if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
                botatuDuPath=1           
            if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
                botatuDuItem=1
   
        #Momentuko Ibilbidea lortu
        momentukoIbilbidea=path.objects.get(id=path_id)
    
        botoKopuruaPath=momentukoIbilbidea.get_votes()
        botoKopuruaItem=momentukoItema.get_votes()
    
        autoplay=1
        offset=0
        autoplaypage=autoplaypages[0]
        
        #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
        pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
        itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=momentukoItema)
        
    
        #LORTU IBILBIDEAREN KOMENTARIOAK
        comments = momentukoPatha.get_comments()    
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        
        #MORE LIKE THIS
        mlt=[]    
        mlt = SearchQuerySet().more_like_this(momentukoItema) 
        mlt = mlt[:10]
      
        
        return render_to_response('nabigazio_item_berria.html',{"mlt":mlt,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'offset':offset,'autoplay':autoplay,'autoplaypage':autoplaypage,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    
 
def nabigazio_item(request):
    
 
    if request.GET:
        #Ibilbideak.html-tik ikusi botoia sakatzean
        path_id=request.GET['path_id']
        item_id=request.GET['item_id']
    
    if request.POST:
        #nabigazio item batetik hurrengora edota aurrekora pasatzean
        path_id=request.POST['path_id']
        item_id=request.POST['item_id']
    
    
    #print "path_id"
    #print path_id
    #print "item_id"
    #print item_id
    
    momentukoPatha=path.objects.get(id=path_id)
    momentukoItema=item.objects.get(id=item_id)
    
    
    #KOMENTARIOA IDATZI DA  -IBILBIDEAK        
    if not request.user.is_anonymous() and "submit_comment" in request.POST: # make a comment
       
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            db_add_pathcomment(comment_form, momentukoPatha, request.user)
            comment_form = CommentForm()
    #Komentario bati erantzun baldin badio
    if not request.user.is_anonymous() and "submit_comment_parent" in request.POST: # make a comment
        comment_parent_form = CommentParentForm(request.POST)
        if comment_parent_form.is_valid():
            db_add_pathcomment(comment_parent_form, momentukoPatha, request.user)
            comment_parent_form = CommentParentForm()

    
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
    botatuDuItem=0
    if not request.user.is_anonymous():
        if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
            botatuDuPath=1           
        if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
            botatuDuItem=1
   
    #Momentuko Ibilbidea lortu
    momentukoIbilbidea=path.objects.get(id=path_id)
    
    botoKopuruaPath=momentukoIbilbidea.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()
    
    autoplay=0
    
    #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
    pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
    itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
    
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=momentukoItema)
    
    
    #LORTU IBILBIDEAREN KOMENTARIOAK
    comments = momentukoPatha.get_comments()    
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
    
    #MORE LIKE THIS
    mlt=[]    
    mlt = SearchQuerySet().more_like_this(momentukoItema) 
    mlt = mlt[:10]
 
    
    return render_to_response('nabigazio_item_berria.html',{"mlt":mlt,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

def nabigatu(request):
     
    
    path_id=request.GET['path_id']
    item_id=request.GET['item_id']
   
    if 'autoplay' in request.GET:
        autoplay=request.GET['autoplay']
    else:
        autoplay='0'
        
    if 'offset' in request.GET:
        offset=request.GET['offset']
       
    if(autoplay == '1'):
        
       
        momentukoPatha=path.objects.get(id=path_id)
        
        #Ibilbidearen Hasierak hartu
        nodes = [] 
        erroak= node.objects.filter(fk_path_id=momentukoPatha,paths_start=1)
  
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
        
        #Autonabigaziorako orrien path-ak sortu
        autoplaypages=[]
        for nodoa in nodes:
           
            nodoID_str=str(nodoa.fk_item_id.id)
            path_id_str=str(path_id)
                    
            berria = 'nabigatu?path_id='+path_id_str+'&item_id='+nodoID_str;
           
            autoplaypages.append(berria)
    
       
        path_len=len(autoplaypages)
        path_len_ken=path_len-1
        if int(offset) == path_len_ken:            
            autoplay=0
            autoplaypage=autoplaypages[path_len_ken]
        else:
            autoplay=1
            offset=int(offset)+1
            autoplaypage=autoplaypages[offset]
         
    else:
        autoplay=0
    
    
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
    botatuDuItem=0
    if not request.user.is_anonymous():
        if(votes_path.objects.filter(path=momentukoPatha,user=request.user)):
            botatuDuPath=1
        if(votes_item.objects.filter(item=momentukoItema,user=request.user)):
            botatuDuItem=1
   
    #Momentuko Ibilbidea lortu
    momentukoIbilbidea=path.objects.get(id=path_id)
    
    botoKopuruaPath=momentukoIbilbidea.get_votes()
    botoKopuruaItem=momentukoItema.get_votes()   
    
    
    
    #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
    pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
    itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
    
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=momentukoItema)
    
    
    #LORTU IBILBIDEAREN KOMENTARIOAK
    comments = momentukoPatha.get_comments()    
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
 
    #MORE LIKE THIS
    mlt=[]    
    mlt = SearchQuerySet().more_like_this(momentukoItema) 
    mlt = mlt[:10]
 
    
    
    if(autoplay == 1):
        non="fitxaE"
        return render_to_response('nabigazio_item_berria.html',{"mlt":mlt,"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'offset':offset,'autoplay':autoplay,'autoplaypage':autoplaypage,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))

    else:
        non="fitxaE"
        return render_to_response('nabigazio_item_berria.html',{"mlt":mlt,"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))


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
    
    #Momentuko Ibilbidea lortu
    momentukoPatha=path.objects.get(id=path_id)
    
    #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
    pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
    itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
    
    
    
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=momentukoItema)
    
    
    #LORTU IBILBIDEAREN KOMENTARIOAK
    comments = momentukoPatha.get_comments()    
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
 
    #Ezkerreko zutabea ez erakusteko
    non="fitxaE"
    #return render_to_response('nabigazio_item.html',{"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'botoKopuruaItem':botoKopuruaItem,'botoKopuruaPath':botoKopuruaPath,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'momentukoPatha':path_tupla,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    return render_to_response('ibilbidea.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'botoKopuruaItem':botoKopuruaItem,'botoKopuruaPath':botoKopuruaPath,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'momentukoPatha':path_tupla,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))


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
    
    #Momentuko Ibilbidea lortu
    momentukoPatha=path.objects.get(id=path_id)
    
    #QR kodeak sortzeko , ibilbidea eta momentuko nodoarena     
    pathqrUrl="http://ondarebideak.org/nabigazioa_hasi?path_id="+str(path_id)
    itemqrUrl="http://ondarebideak.org/erakutsi_item?id="+str(item_id)
   
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=momentukoItema)
    
    
    #LORTU IBILBIDEAREN KOMENTARIOAK
    comments = momentukoPatha.get_comments()    
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
   
   
    #Ezkerreko zutabea ez erakusteko
    non="fitxaE"
    return render_to_response('ibilbidea.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'botoKopuruaItem':botoKopuruaItem,'botoKopuruaPath':botoKopuruaPath,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'momentukoPatha':path_tupla,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak, 'aurrekoak':aurrekoak},context_instance=RequestContext(request))



  
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

def db_oaipmh_bilketa(cd):
    """ oai-pmh baseURL batetik abiatuta itemak EDM formatuan jetsi eta metadatuak datu-basean gorde"""
    
    baseurl=cd['baseurl']
    #baseurl adibidea : http://euskonews.oai.euskomedia.org/
    wikify=cd['wikify']
    
    
 
    # -c temporalak sortzen dira /tmp karpetan 
    #collection="/home/maddalen/OAI-PMH_COLLECTION/"
    #collection="/tmp/tmpOAQvFR"
    collection = tempfile.mkdtemp() 
    
  
    if oaiharveststore(collection, baseurl, wikify):
     
        return True
    else:
        return False

@user_passes_test(lambda u: u.groups.filter(name='hornitzailea').exists())
def oaipmh_datubilketa(request):
    
    oaipmhform=OaipmhForm()
    
    if 'oaipmh_bilketa' in request.POST: 
        oaipmh_form=OaipmhForm(request.POST)
        if oaipmh_form.is_valid():
            cd=oaipmh_form.cleaned_data
            baseurl=cd['baseurl']
            mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"OAI Url-a"+str(baseurl)+"\n"+"Bidali mezua hornitzaileari: "+str(request.user.email)
            send_mail('OndareBideak - Itemak inportatzeko eskaera', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
            return render_to_response('base.html',{'mezua':"Zure eskaera jaso dugu. Itemen bilketa prest dagoenean jasoko duzu posta elektroniko bat."},context_instance=RequestContext(request))
           
            '''
            if db_oaipmh_bilketa(cd):
               
                return render_to_response('base.html',{'mezua':"Itemak ondo biltegiratu dira"},context_instance=RequestContext(request))
            else:
                return render_to_response('base.html',{'errore_mezua':"ERROREA: Itemak EZ DIRA ondo biltegiratu"},context_instance=RequestContext(request))
            '''
        else:
                return render_to_response("oaipmh_datubilketa.html",{"oaipmhform":oaipmhform},context_instance=RequestContext(request)) 
    return render_to_response("oaipmh_datubilketa.html",{"oaipmhform":oaipmhform},context_instance=RequestContext(request)) 
 
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
                
                
                #IF Hornitzailea izan nahi badu
                if cd["hornitzailea"]:
                    return render_to_response('base.html',{'mezua':"Kulturbideak sisteman Erregistratu zara. Momentu honetan erabiltzaile arrunt bezala zaude erregistratuta. Hornitzaile izateko eskaera bideratuta dago. Zure posta elektronikoan mezu bat jasoko duzu hornitzaile izateko baimena eskuratzen duzunean. Edozein zalantza jarri gurekin kontaktuan: ondarebideak@elhuyar.com"},context_instance=RequestContext(request)) 
                else:
                    return render_to_response('base.html',{'mezua':"Kulturbideak sisteman Erregistratu zara"},context_instance=RequestContext(request))
   
        else:
            #return render_to_response("izena_eman.html",{"bilaketa":bilaketa_form,"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
            return render_to_response("erregistratu.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
    return render_to_response("erregistratu.html",{"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))

def db_erregistratu_erabiltzailea(cd):
    """Erabiltzaile bat erregistratzen du"""
   
    try:
        
        erabiltzailea=User.objects.create_user(cd["username"], cd["posta"], cd["password"])
        erabiltzailea.first_name=cd['izena']
        erabiltzailea.last_name=cd['abizena']
        
        #Django-ko auth_user-en gordetzen du erabiltailea
        erabiltzailea.save()
       
        #Hornitzaile bezala erregistratu nahi baldin badu
        if cd["hornitzailea"]:
            hornitzaile_izena=cd["honitzaile_izena"]
            mezua="Hornitzailearen izena:"+str(hornitzaile_izena)+".\n"+"Ondorengoa egin datu-basean: update auth_user_groups set group_id=3 where user_id="+str(erabiltzailea.id)+"\n"+"Bidali mezua hornitzaileari: "+str(erabiltzailea.email)
            send_mail('OndareBideak - Hornitzaile izateko eskaera', mezua, 'm.lopezdelacalle@elhuyar.com',['m.lopezdelacalle@elhuyar.com'], fail_silently=False)
            
            #Hornitzailearen fitxa (hutsa) sortuko dugu datu-basean
            hornitzaile_fitxa=hornitzailea(fk_user=erabiltzailea,izena=hornitzaile_izena)
            hornitzaile_fitxa.save()
            #group = Group.objects.get(name='hornitzailea') 
            #group.user_set.add(erabiltzailea)     
         
        #Hasieran beti 'arrunta' bezala erregistratu   
        group = Group.objects.get(name='herritarra') 
        group.user_set.add(erabiltzailea)     
            
       
        
        
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

def ezabatu_itema(request):
    if 'id' in request.GET:
        id=request.GET['id']
        #Ibilbidea ezabatu
        item.objects.filter(id=id).delete()
        
        #votes_item
        votes_item.objects.filter(item__id=id).delete()
        #itemComment
        itemComment.objects.filter(itema__id=id).delete()
        
        return render_to_response('base.html',{'mezua':"Kultur Itema ezabatu da"},context_instance=RequestContext(request))
    
 
def ezabatu_ibilbidea(request):
    if 'id' in request.GET:
        id=request.GET['id']
        #Ibilbidea ezabatu
        path.objects.filter(id=id).delete()
        
        #votes_item
        votes_path.objects.filter(path__id=id).delete()
        #itemComment
        pathComment.objects.filter(patha__id=id).delete()
        
        
        return render_to_response('base.html',{'mezua':"Ibilbidea ezabatu da"},context_instance=RequestContext(request))
    

def editatu_ibilbidea(request):
    
    if 'id' in request.GET:
        id=request.GET['id']
    
        #lortu path-aren ezaugarriak
        ibilbidea = path.objects.get(id=id)
        titulua=ibilbidea.dc_title
        gaia=ibilbidea.dc_subject
        deskribapena=ibilbidea.dc_description
        irudia=ibilbidea.paths_thumbnail
        #hizkuntza=ibilbidea.language
        
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
     
    if request.POST:
        #KOMENTARIOA IDATZI DA
        id=request.POST['id']
        item_tupla = item.objects.get(pk=id)
        
        if not request.user.is_anonymous() and "submit_comment" in request.POST: # make a comment
        
            print "MAKE COMMENT"
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                db_add_itemcomment(comment_form, item_tupla, request.user)
                comment_form = CommentForm()
        #Komentario bati erantzun baldin badio
        if not request.user.is_anonymous() and "submit_comment_parent" in request.POST: # make a comment
            comment_parent_form = CommentParentForm(request.POST)
            if comment_parent_form.is_valid():
                db_add_itemcomment(comment_parent_form, item_tupla, request.user)
                comment_parent_form = CommentParentForm()

        
        
    if request.GET:
        #ITEMA BISITATU NAHI DA 
        if 'id' in request.GET:
            id=request.GET['id']        
            item_tupla = item.objects.get(pk=id)
            
   
    herrialdea=item_tupla.edm_country
    hizkuntza=item_tupla.dc_language
    kategoria=item_tupla.dc_type
    eskubideak=item_tupla.edm_rights
    urtea=item_tupla.edm_year 
    viewAtSource=item_tupla.edm_isshownat
    irudia=item_tupla.edm_object
    hornitzailea=item_tupla.edm_provider
    #hornitzailea=item_tupla.dc_creator
    geoloc_longitude=item_tupla.geoloc_longitude
    geoloc_latitude=item_tupla.geoloc_latitude
       
        
    botatuDu=0
    botoKopurua=0
    if(votes_item.objects.filter(item=id,user_id=request.user.id)):
        botatuDu=1   
        botoKopurua=item_tupla.get_votes()
        
    #MORE LIKE THIS
   #print "MORE LIKE THIS KALKULATZEN" 
    mlt=[] 
    #search_models_items=[item]
    #mlt = SearchQuerySet().more_like_this(item_tupla)
    mlt = SearchQuerySet().more_like_this(item_tupla)
    #print mlt.count()
    #print "MORE LIKE THIS KALKULATZEN BUKATU DU" 
    mlt = mlt[:10]
   
          
    #print mlt.count() # 5        
    #print mlt[0].object.dc_title
        
    #QR-a sortzeko
    qrUrl="http://ondarebideak.org/erakutsi_item?id="+id
        
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
    #LORTU ITEMAREN KOMENTARIOAK
    comments = item_tupla.get_comments()
      
    comment_form = CommentForm() 
    comment_parent_form = CommentParentForm()
    print "item.html deitu baino lehen"
    
    non="fitxaE"

    return render_to_response('item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'id':id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    




def botoa_eman_item(request):
    
    non="fitxaE"
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
    

    #MORE LIKE THIS
    mlt=[]    
    mlt = SearchQuerySet().more_like_this(item_tupla) 
    mlt = mlt[:10]
      
    
    #QR-a sortzeko
    qrUrl="http://ondarebideak.org/erakutsi_item?id="+item_id
    
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
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
        
        
    
        return render_to_response('nabigazio_item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

    else:
      
        return render_to_response('item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopurua':botoKopuruaItem,'item':item_tupla,'id':id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    

    
def botoa_kendu_item(request):
    
    non="fitxaE"
       
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
    
    #MORE LIKE THIS
    mlt=[]    
    mlt = SearchQuerySet().more_like_this(item_tupla) 
    mlt = mlt[:10]
    
    #QR-a sortzeko
    qrUrl="http://ondarebideak.org/erakutsi_item?id="+item_id
    
    #Itema erabiltzen duten path-ak lortu
    itemPaths=node.objects.filter(fk_item_id=item_tupla)
    
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
    
        return render_to_response('nabigazio_item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

    else:
     
        return render_to_response('item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopurua':botoKopuruaItem,'item':item_tupla,'id':item_id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    




def editatu_itema(request):
     
    print "editatu itema"
    #Hasieran, Formularioa kargatzerakoan hemen'botoKopurua':botoKopurua sartuko da
    if 'id' in request.GET: 
        
        item_id=request.GET['id']
    
        
    itema=ItemEditatuForm(request.POST, request.FILES)
    
    #Editatu botoia sakatzerakoan hemendik sartuko da eta POST bidez bidaliko dira datuak
    if itema.is_valid():
        print "IS VALID"
        erabiltzailea=request.user
        irudi_izena_random =randomword(10);
        
        #azken_id = item.objects.latest('id').id
        #azken_id += 1
        item_id=request.POST['hidden_Item_id']
        print "item_id"
        print item_id 
        
        dc_title=request.POST['titulua']
        uri="uri_"+ str(item_id)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['eskubideak']
        irudia_url=""
        if(request.FILES):
        
            edm_object=request.FILES['irudia'].name
            print "irudia"
            print edm_object
            irudia_url=MEDIA_URL+ str(irudi_izena_random)+edm_object #izen berekoak gainidatzi egingo dira bestela
      
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
         
        
        #username-a ez da errepikatzen datu-basean, beraz, id bezala erabili dezakegu 
        dc_creator= request.user.username # ondoren logeatutako erabiltzailea jarri
        edm_provider= request.user.username # ondoren logeatutako erabiltzailea jarri
        #Gaurko data hartu
        dc_date=datetime.datetime.now()
        edm_year=datetime.datetime.now()
        edm_country="Euskal Herria"
        
        
        if request.POST['latitude']:
            latitude=request.POST['latitude']
        else:
            item_db=item.objects.get(id=item_id)
            latitude=item_db.geoloc_latitude
        if request.POST['longitude']:
            longitude=request.POST['longitude']
        else:
            item_db=item.objects.get(id=item_id)
            longitude=item_db.geoloc_longitude
       
        if(irudia_url!=""):
            #Irudia igo
            edm_object= str(irudi_izena_random)+edm_object
            handle_uploaded_file(request.FILES['irudia'],edm_object)
            #item.objects.filter(id=item_id).update(egunekoa = 0,proposatutakoa=1)         
            #item_berria = item(id=item_id,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
            item.objects.filter(id=item_id).update(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
            
            #Item-a duten Ibilbideko nodoen argazkia ALDATU. node TAULAN, fk_item_id ALDAGAIA =item_id
            irudia_update=MEDIA_URL+edm_object              
            node.objects.filter(fk_item_id=item_id).update(paths_thumbnail=irudia_update)

        else:
            #Datu-basean irudi zaharra mantendu
            item_tupla = item.objects.get(pk=item_id)
            irudia_url=item_tupla.edm_object
            #item_berria = item(id=item_id,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country)
            item.objects.filter(id=item_id).update(fk_ob_user=erabiltzailea,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,edm_year=edm_year,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
   
        
        #item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        #update_index.Command().handle(age=1)
        non="fitxaE"
        item_obj=item.objects.get(id=item_id)
        return render_to_response('base.html',{'non':non,'item':item_obj,'mezua':"itema editatu da",'nondik':"editatu_itema",'hizkuntza':dc_language,'irudia':irudia_url,'titulua':dc_title,'herrialdea':edm_country,'hornitzailea':edm_provider,'eskubideak':edm_rights,'urtea':dc_date,'geoloc_latitude':latitude,'geoloc_longitude':longitude},context_instance=RequestContext(request))
    
        #return render_to_response('base.html',{'non':non,'mezua':"itema editatu da",'nondik':"editatu_itema",'hizkuntza':dc_language,'irudia':irudia_url,'titulua':dc_title,'herrialdea':edm_country,'hornitzailea':edm_provider,'eskubideak':edm_rights,'urtea':dc_date,'geoloc_latitude':latitude,'geoloc_longitude':longitude},context_instance=RequestContext(request))
    
    else:
        #Hasieran hemendik sartuko da eta Datu-basetik kargatuko dira itemaren datuak
        print "hasiera editatu"
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
        
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
        
        non="itema_editatu" #Mapako baimenak kontrolatzeko erabiliko da hau
       
       
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'hizkuntza':hizkuntza})
        return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'hizkuntza':hizk,'viewAtSource':viewAtSource},context_instance=RequestContext(request))
   


def handle_uploaded_file(f,izena):
    #Irudi fitxategia /uploads direktoriora igotzen du
    with open(MEDIA_ROOT+'/'+izena, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def nire_itemak_erakutsi(request):
    
    userName=request.user.username
    userID=request.user.id
    itemak=[]
    itemak = item.objects.filter(fk_ob_user__id=userID).order_by('-edm_year')
    #PAGINATOR
    paginator = Paginator(itemak, 26)

    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
     
    page = request.GET.get('page')
    try:
        itemak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        itemak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        itemak = paginator.page(paginator.num_pages)
    non="fitxaE"
    return render_to_response('nire_itemak.html',{'non':non,'itemak':itemak},context_instance=RequestContext(request))
   


def nire_ibilbideak_erakutsi(request):
    
    userID=request.user.id
    ibilbideak=[]
    ibilbideak = path.objects.filter(fk_user_id__id=userID).order_by('-creation_date')
        
    #PAGINATOR
    paginator = Paginator(ibilbideak, 26)

    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
     
    page = request.GET.get('page')
    try:
        ibilbideak = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ibilbideak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ibilbideak = paginator.page(paginator.num_pages)
    non="fitxaE"
    return render_to_response('nire_ibilbideak.html',{'non':non,'paths':ibilbideak},context_instance=RequestContext(request))
   
   
def itema_gehitu(request):
    
    itema=ItemGehituForm(request.POST, request.FILES)
    
    if itema.is_valid():
        #Datu-basean item-a gehitu
        irudi_izena_random =randomword(10); 
        #azken_id = item.objects.latest('id').id
        #azken_id += 1
        erabiltzailea=request.user
        dc_title=request.POST['titulua']
        uri="uri_"+ str(irudi_izena_random)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['eskubideak']
        irudia_url=""
        if(request.FILES):
            edm_object=request.FILES['irudia'].name
            irudia_url=MEDIA_URL+str(irudi_izena_random)+edm_object #izen berekoak gainidatzi egingo dira bestela
      
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
         
        
        #DC_CREATOR Vs. EDM_PROVIDER       
        #username-a ez da errepikatzen datu-basean, beraz, id bezala erabili dezakegu 
        dc_creator= request.user.username 
        
        #BEGIRATU EA HORNITZAILEA DEN EDO EZ. EZ BADA:Herritarra balioa eman edm_providerri, bestela Hornitzailea
        #erab_id=request.user.id         
        if( User.objects.filter(id=request.user.id, groups__name='hornitzailea').exists()):
            hornitzaile=hornitzailea.objects.get(fk_user=request.user)
            edm_provider=hornitzaile.izena
        else:
            edm_provider= "herritarra"
        
     
        #Gaurko data hartu
        dc_date=datetime.datetime.now()  
        edm_year=datetime.datetime.now()  
        edm_country="Euskal Herria"
        
        if(irudia_url!=""):
            #Irudia igo
            edm_object=str(irudi_izena_random)+edm_object #izen berekoak gainidatzi egingo dira bestela
            handle_uploaded_file(request.FILES['irudia'],edm_object)
        
        latitude=0.0
        longitude=0.0
        if request.POST['latitude']:
            latitude=request.POST['latitude']
        if request.POST['longitude']:
            longitude=request.POST['longitude']
   
        item_berria = item(fk_ob_user=erabiltzailea,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,edm_year=edm_year,dc_language=dc_language, edm_language=edm_language,edm_object=irudia_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
        item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        #update_index.Command().handle(age=1)
         
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
            id = bozkatuena.path.id
            path_ids.append(id)
       
        #hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
        path_bozkatuenak=path.objects.filter(id__in=path_ids) 
  
        #path_bozkatuenak=path.objects.filter(id__in=[path_ids]) 
    else:
        path_bozkatuenak=[]
    
    return render_to_response('ibilbide_bozkatuenak.xml', {'paths': path_bozkatuenak}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_lortu_eguneko_itema (request):
    
    #Irudirik ez duten itemak ez ditugu erakutsiko
    eguneko_itemak=item.objects.filter(egunekoa=1).exclude(edm_object="")
  
    return render_to_response('eguneko_itema.xml', {'items': eguneko_itemak}, context_instance=RequestContext(request), mimetype='application/xml')

def ajax_lortu_eguneko_ibilbidea (request):
    
    #Irudirik ez duten itemak ez ditugu erakutsiko
    eguneko_ibilbideak=path.objects.filter(egunekoa=1).exclude(paths_thumbnail="")
  
    return render_to_response('eguneko_ibilbidea.xml', {'paths': eguneko_ibilbideak}, context_instance=RequestContext(request), mimetype='application/xml')


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
        
        #KONPONDU? fk_item=itema,
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
        language=request.POST.get('hizkuntza')
        
        ######paths_thumbnail=str(azken_id)+paths_thumbnail
       
        #fileObject= request.FILES.get('fileObject')
        #fileObject= request.GET.get('fileObject')
        #print fileObject
        ##
        print "paths_thumbnail"
        print paths_thumbnail
        if paths_thumbnail =="":
            paths_thumbnail_url="/uploads/NoIrudiItem.png"
        else:
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
                                        paths_thumbnail = paths_thumbnail_url,
                                        language=language)
    
    
        path_berria.save() #AUTOMATIKOKI SOLR INDIZEA ERE EGUNERATZEN DA
        request_answer = path_berria.id  
        
        #Haystack update_index EGIN!!!
        #update_index.Command().handle()   ##ATASKATU EGITEN DA :-(  -> BAINA EGUNERATZEN DA INDIZEA
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_eguneratu(request):
    
    print request.POST
    path_id=request.POST.get('path_id')
    fk_usr_id=request.user.id
    dc_title=request.POST.get('dc_title')
    dc_subject=request.POST.get('dc_subject')
    dc_description=request.POST.get('dc_description')
    paths_thumbnail = request.POST.get('paths_thumbnail')
    language=request.POST.get('hizkuntza')
    
    
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
                           creation_date = timezone.now(),
                           language=language)
    
    
    path_eguneratua.save()
    request_answer = path_id 
        
    #Haystack update_index EGIN!!!
    #update_index.Command().handle()
    
    # Ezabatu path-eko nodo guztiak
    node.objects.filter(fk_path_id__id=path_id).delete()

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
        print "ajax_path_node_gorde"
        print node_berria.id
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
 
 
#################AJAX HORNITZAILE FITXA ##############
'''
def ajax_edit_proposal_area(request):
    response_proposal = None
    if request.GET:
        area = request.GET.get('area')
        form = ModalAreaForm({"area": area})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_area(area)
                response_proposal = proposal
        change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_area_response.html",{"response": response,"proposal":response_proposal},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("area")
            return render_to_response("ajax/ajax_area_response.html",{"response": response,},context_instance=RequestContext(request.request))  
'''

def ajax_edit_arloa(request):
   
   
    if request.GET:
        area = request.GET.get('area')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(erakundeMota=area)
            erakundeMota = area
            response= "id_area"
            return render_to_response("ajax/ajax_area_response.html",{"response": response,"erakundeMota":erakundeMota},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_area_response.html",{"response": response,},context_instance=RequestContext(request.request))  
        
            
def ajax_edit_izena(request):
   
   
    if request.GET:
        izena = request.GET.get('izena')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(izena=izena)
           
            response= izena
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  
        
def ajax_edit_deskribapena(request):
   
   
    if request.GET:
        deskribapena = request.GET.get('deskribapena')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(deskribapena=deskribapena)
           
            response= deskribapena
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  
        
def ajax_edit_kokalekua (request):
   
   
    if request.GET:
        kokalekua = request.GET.get('kokalekua')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(helbidea=kokalekua)
           
            response= kokalekua
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  




       
def ajax_edit_where(request):
    
    if request.GET:
        
        where = request.GET.get("where")
        
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(helbidea=where)
            response=where
            
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
       
        else:
            response=""
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
  
def fitxa_gorde(request):
    
    non="fitxaE"
    
    
    user_id=request.user.id
    
    if request.POST['latitude']:
        latitude=request.POST['latitude']
    else:
        horni_db=hornitzailea.objects.get(fk_user__id=user_id)
        latitude=horni_db.geoloc_latitude
    if request.POST['longitude']:
        longitude=request.POST['longitude']
    else:
        horni_db=hornitzailea.objects.get(fk_user__id=user_id)
        longitude=horni_db.geoloc_longitude
    
    if not request.user.is_anonymous():
            
        hornitzailea.objects.filter(fk_user__id=user_id).update(geoloc_longitude=longitude,geoloc_latitude=latitude)
        mezua="Ondo sortu da fitxa"
        
    hornitzaile =hornitzailea.objects.get(fk_user__id=user_id)
    return render_to_response('hornitzaile_fitxa_editatu.html',{'non':non,"hornitzailea":hornitzaile,'mezua_fitxa':mezua},context_instance=RequestContext(request))
    
                
      
def ajax_hornitzaile_irudia_gorde (request):

   
    print "ajax_hornitzaile_irudia_gorde"
    print request.FILES
    
    user_id=request.user.id
    if request.is_ajax() and request.method == 'POST':
       
        
        #Irudirik igotzen ez denean errorea ez emateko beharrezko da baldintza hau jartzea
        if(request.FILES):
        
            
            fileObject= request.FILES.get('hornitzaile_argazkia')
           
            print fileObject
           
            username =request.user.username
            fileName=str(username)+fileObject.name

            print fileName
            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            ikonoa="/uploads/"+fileName
            hornitzailea.objects.filter(fk_user__id=user_id).update(ikonoa=ikonoa)
            response=ikonoa
    
  
    return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
       




   
    
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



