#-*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.utils.translation import ugettext as _,get_language
from itertools import islice, chain
from django.utils import simplejson
from django.template import Context, Template
from django.utils import timezone
from django.core.mail import send_mail
from django.http import Http404

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
#from KULTURBIDEAK.kulturbideak_app.models import node_tmp
from KULTURBIDEAK.kulturbideak_app.models import hornitzailea
from KULTURBIDEAK.kulturbideak_app.models import workspace_item
from django.contrib.auth.models import User,Group
from KULTURBIDEAK.kulturbideak_app.forms import *
from KULTURBIDEAK.kulturbideak_app.models import *
from haystack.management.commands import update_index
from KULTURBIDEAK.settings import *

from django.utils.translation import ugettext as _

from datetime import datetime

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

def hasiera(request):
    """Hasiera orria"""
     
    login_form = LoginForm()
    erabiltzailea_form = CreateUserForm() 
    
    if 'login' in request.POST:
        logina(request)
        
    if 'Erabiltzailea_gehitu' in request.POST:
        erregistratu(request)
        
    # Kontadoreko kopuruak lortu datu-basetik
    # Itemak
    itemKop = item.objects.count()
    itemKop = itemKop / 1000
    #eguneko itema
    egunekoItem = item.objects.filter(egunekoa=1).order_by('?')[:1]
    if (not egunekoItem):
        egunekoItem = item.objects.order_by('?')[:1]
        
    egunekoItem = egunekoItem[0] 
    #Ibilbideak
    ibilbideKop = path.objects.filter(acces__in=("2","3","4")).count()   
    #Karruselerako Ibilbideak
    ibilbideak = path.objects.order_by('?').exclude(acces=1)[:5]
    #eguneko patha
    egunekoPath = path.objects.filter(egunekoa=1).order_by('?')[:1]
    ## eguneko path-ik ez badago hartu karruseleko lehena
    if (not egunekoPath):
        egunekoPath = ibilbideak[0]    
    else:
        egunekoPath = egunekoPath[0];
    ibilbideak=ibilbideak[1:]
    
    
    #Hornitzaileak
    hornitzaileKop = hornitzailea.objects.count()
    #hornitzaile bat erakutsi
    #egunekoHornitzaile = hornitzailea.objects.order_by('?')[:1]
    #egunekoHornitzaile = egunekoHornitzaile[0];
    egunekoHornitzaile = hornitzailea.objects.get(fk_user__id=58)
    #eguneko hornitzaileen artetik bat ausaz hartu
    egunekoHornitzaile = hornitzailea.objects.filter(egunekoa=1).order_by('?')[0]
    #Erabiltzaileak
    erabiltzaileKop = usr.objects.count()
    #Hasierako pantailan erakutsi behar den berria hartu datu-basetik
    erakBerria=berria.objects.get(erakutsi=1)
    currentDate= datetime.datetime.now()
    #return render_to_response('hasiera.html',{'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))
    return render_to_response('index.html',{'login_form':login_form,'erabiltzailea_form':erabiltzailea_form,'currentDate': currentDate ,'ibilbideak':ibilbideak,'egunekoItem':egunekoItem,'egunekoPath':egunekoPath,'egunekoHornitzaile':egunekoHornitzaile,'itemKop':itemKop,'ibilbideKop':ibilbideKop,'hornitzaileKop':hornitzaileKop,'erabiltzaileKop':erabiltzaileKop,'erakBerria':erakBerria},context_instance=RequestContext(request))

 
'''
def hasiera_old(request):
    
    
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
    return render_to_response('index_brandy.html',{'itemKop':itemKop,'ibilbideKop':ibilbideKop,'hornitzaileKop':hornitzaileKop,'erabiltzaileKop':erabiltzaileKop},context_instance=RequestContext(request))
'''
   
def itemak_hasiera(request):
    
    #print "itemak_hasiera"
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK ITEMAK LORTZEKO 
    #Itemen hasierako pantailan erakutsi behar diren Itemen informazioa datu-basetik lortu eta pasa
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
    '''
   
    login_form = LoginForm()
    erabiltzailea_form = CreateUserForm() 
    
    if 'login' in request.POST:
        logina(request)
        
    if 'Erabiltzailea_gehitu' in request.POST:
        erregistratu(request)
   
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
        
    #IBILBIDEAK
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
    
        
    #ALDAKETA-CROSS-SEARCH
    
    #Datu-baseko hornitzaileak lortu                                                                                             
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)

    #Datu-baseko motak lortu                                                                                                     
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)

    #Datu-baseko lizentziak lortu                                                                                                
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))

    non="" #??fitxaE
    
    z='i'
    if request.GET.get('z'):
        z = request.GET.get('z')   
    #paths=[]
    bilaketa_filtroak=1
    galdera=''
    hizkuntza='eu'
    hizkF=''
    horniF=''
    motaF=''
    ordenaF=''
    lizentziaF=''
    besteaF=''
    search_models_items=[item]
    
    items = SearchQuerySet().all().models(*search_models_items)
    search_models_paths=[path]
    paths = SearchQuerySet().all().models(*search_models_paths)
    
     
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
    
    
    return render_to_response('cross_search.html',{'login_form':login_form,'erabiltzailea_form':erabiltzailea_form,'non':non,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))
      
    #return render_to_response('itemak_hasiera.html',{'non':non,'itemak':itemak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak},context_instance=RequestContext(request))
    
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


def admin_hornitzaile_fitxa_editatu(request):
    
    non="fitxaE"
    erabId=request.GET.get('erabId')
    user_id=int(erabId)
    hornitzaile =hornitzailea.objects.get(fk_user__id=user_id)
    return render_to_response('hornitzaile_fitxa_editatu.html',{'non':non,"hornitzailea":hornitzaile},context_instance=RequestContext(request))


def hornitzaile_fitxa_editatu(request):
    
    #INPLEMENTATU
    non="fitxaE"
    user_id=request.user.id
    hornitzaile =hornitzailea.objects.get(fk_user__id=user_id)
    return render_to_response('hornitzaile_fitxa_editatu.html',{'non':non,"hornitzailea":hornitzaile},context_instance=RequestContext(request))
    #return render_to_response('proposal.html',{'non':non,"hornitzailea":hornitzaile},context_instance=RequestContext(request))



def get_user(request):
    """Get user from DB to edit in user form"""
    userid = request.GET.get('id')
    user = User.objects.get(id=int(userid))
    user_form = UserForm(initial={"userid":userid,"izena":user.first_name,"abizena":user.last_name,"username":user.username,"posta":user.email})
    return render_to_response('user_form.html', {'user_form':user_form}, context_instance = RequestContext(request))



def admin_reset_user_password(request):
    
    userid = request.GET.get('id')
    user = User.objects.get(id=int(userid))
    posta=user.email
    
 	#Ausazko pasahitza sortu 
 	#datu-basean aldatu
    pasahitzBerria=randomword(8)  
    user.set_password(pasahitzBerria)                   
    user.save()
 	
 	#erabiltzaileari eta guri mezua bidali
    mezua=_("Erabiltzaile honen pasahitza berrasieratu da:")+str(user.username)+"\n"+_("Erabiltzaileak aldatu bitartean pasahitza berria hau da:")+str(pasahitzBerria)
    send_mail('OndareBideak - Erabiltzaile baten pasahitza berrasieratu da', mezua, 'ondarebideak@elhuyar.eus',['ondarebideak@elhuyar.eus'], fail_silently=False)   
    mezua_erab=_("Zure pasahitza aldatu da.")+"\n"+_("Hau da zure pasahitz berria:")+"\n"+str(pasahitzBerria)+"\n"+_("Ahalik eta azkarren aldatzea gomendatzen dizugu.")
    send_mail('OndareBideak - zure pasahitza aldatu da', mezua_erab, posta,[posta], fail_silently=False)
       
    hornitzaileak = []
    hornitzaileak = hornitzailea.objects.filter(fk_user__groups__id=3)
    hornitzaileak_id = []
    hornitzaileak_id = [x.fk_user.id for x in hornitzaileak]
    erabiltzaileak = User.objects.all()
    user_form = UserForm()
    non='fitxaE'
    return render_to_response('admin_erabiltzaileak_kudeatu.html',{'non':non,'erabiltzaileak':erabiltzaileak,'hornitzaileak':hornitzaileak,'hornitzaileak_id':hornitzaileak_id,'user_form':user_form},context_instance=RequestContext(request))
	
   


def admin_erabiltzaileak_kudeatu(request):

    if 'save_user' in request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data   
            user = User.objects.get(id=int(cd.get('userid')))
            user.first_name = cd.get("izena")
            user.last_name = cd.get("abizena")
            user.username = cd.get("username")
            user.email= cd.get("posta") 
            user.save()
            
        else:
    		print "admin_erabiltzaileak_kudeatu: form is not valid"
    		#raise Http404 
    
    hornitzaileak = []
    hornitzaileak = hornitzailea.objects.filter(fk_user__groups__id=3)
    hornitzaileak_id = []
    hornitzaileak_id = [x.fk_user.id for x in hornitzaileak]
    
    erabiltzaileak = User.objects.all()
    user_form = UserForm()
	
    non='fitxaE'
    return render_to_response('admin_erabiltzaileak_kudeatu.html',{'non':non,'erabiltzaileak':erabiltzaileak,'hornitzaileak':hornitzaileak,'hornitzaileak_id':hornitzaileak_id,'user_form':user_form},context_instance=RequestContext(request))


def get_berria(request):
	"""Get berria from DB to edit in user form"""
	berriaid = request.GET.get('id')
	berri = berria.objects.get(id=int(berriaid))
	erakutsi=berri.erakutsi
	irudia=berri.argazkia
	berria_form = BerriaForm(initial={"berriaid":berriaid,"titulua_eu":berri.title_eu,"desk_eu":berri.desk_eu,"titulua_es":berri.title_es,"desk_es":berri.desk_es,"titulua_en":berri.title_en,"desk_en":berri.desk_en,"titulua_fr":berri.title_fr,"desk_fr":berri.desk_fr,"url":berri.url,"irudia":irudia,"publikatu":erakutsi})
	return render_to_response('berria_form.html', {'berria_form':berria_form}, context_instance = RequestContext(request))
    


def admin_berriak_kudeatu(request):

	if 'save_berria' in request.POST:
		berria_form = BerriaForm(request.POST,request.FILES)

		if berria_form.is_valid():
			##EDITATU
			cd = berria_form.cleaned_data    
			berri = berria.objects.get(id=int(cd.get('berriaid')))
			if cd.get("titulua_eu"):
				berri.title_eu = cd.get("titulua_eu")
			if cd.get("desk_eu"):
				berri.desk_eu = cd.get("desk_eu")
			if cd.get("titulua_es"):
				berri.title_es = cd.get("titulua_es")
			if cd.get("desk_es"):
				berri.desk_es = cd.get("desk_es")
			if cd.get("titulua_en"):
				berri.title_en = cd.get("titulua_en")
			if cd.get("desk_en"):
				berri.desk_en = cd.get("desk_en")
			if cd.get("titulua_fr"):
				berri.title_fr = cd.get("titulua_fr")
			if cd.get("desk_fr"):
				berri.desk_fr = cd.get("desk_fr")
			
			berri.url = cd.get("url")
			
			irudia_url=''

			if(request.FILES.get('irudia')):    
				fileObject= request.FILES.get('irudia')
				fname, fext = os.path.splitext(fileObject.name)
				fileName='karrusel_img_'+randomword(5)+fname+fext
				irudia_url=MEDIA_URL+str(fileName)#izen berekoak gainidatzi egingo dira bestela
				berri.argazkia=irudia_url
				
			
			if request.POST.get('publikatu'):
				#GUZTIEI erakutsi=0 JARRI!!!!BAKARRA ERAKUTSIKO DA (?)
				berri_guztiak = berria.objects.all()
				berri_guztiak.update(erakutsi=False)
			
				berri.erakutsi=1
				
			else:
				berri.erakutsi=0
            	
			
			#Gaurko data hartu
			data=datetime.datetime.now()  
			berri.data=data  
       
			#Irudia igo
			if(irudia_url!=""):
				handle_uploaded_file(request.FILES['irudia'],fileName)
			
			#GORDE	BERRIA EDITATUTA	
			berri.save()
            
		else:
			#BERRIA SORTU
			print "Berria sortu!"
			if request.POST.get('berriaid')=='':
				print "Berria id hutsa da"
				title_eu=request.POST.get('titulua_eu')
				desk_eu=request.POST.get('desk_eu')
				print "title_eu"
				print title_eu
				print "desk_eu"
				print desk_eu
				title_es=request.POST.get('titulua_es')
				desk_es=request.POST.get('desk_es')
				
				title_en=request.POST.get('titulua_en')
				desk_en=request.POST.get('desk_en')
				
				title_fr=request.POST.get('titulua_fr')
				desk_fr=request.POST.get('desk_fr')
				
				url=request.POST.get('url')
				
				irudia_url=''

				if(request.FILES.get('irudia')):    
					fileObject= request.FILES.get('irudia')
					fname, fext = os.path.splitext(fileObject.name)
					fileName='karrusel_img_'+randomword(5)+fname+fext
					irudia_url=MEDIA_URL+str(fileName)#izen berekoak gainidatzi egingo dira bestela
				
			
				if request.POST.get('publikatu'):
					#GUZTIEI erakutsi=0 JARRI!!!!BAKARRA ERAKUTSIKO DA (?)
					berri_guztiak = berria.objects.all()
					berri_guztiak.update(erakutsi=False)
					
					erakutsi=1
				else:
					erakutsi=0
								
				#Gaurko data hartu
				data=datetime.datetime.now()  
       
				#Irudia igo
				if(irudia_url!=""):
					handle_uploaded_file(request.FILES['irudia'],fileName)
					
				#Sortu berria datu-basean
				berri_berria = berria(title_eu=title_eu,desk_eu=desk_eu,title_es=title_es,desk_es=desk_es,title_en=title_en,desk_en=desk_en,title_fr=title_fr,desk_fr=desk_fr,url=url,argazkia=irudia_url,data=data,erakutsi=erakutsi)
				berri_berria.save()

	berriak = []
	berriak = berria.objects.all()
	berria_form = BerriaForm()
	
	non='fitxaE'
	return render_to_response('admin_berriak_kudeatu.html',{'non':non,'berriak':berriak,'berria_form':berria_form},context_instance=RequestContext(request))
	
def admin_eguneko_hornitzaileak_kudeatu(request):

	if request.GET.get('id'):
		#Aldatu eguneko egoera
		horni_id=request.GET.get('id')
		horni_id_int=int(horni_id)
		momentukoHornitzailea=hornitzailea.objects.get(id=horni_id_int)
		egunekoaDa=momentukoHornitzailea.egunekoa
		if(egunekoaDa ==1):
			momentukoHornitzailea.egunekoa=0
			momentukoHornitzailea.save()     
		else:
			momentukoHornitzailea.egunekoa=1
			momentukoHornitzailea.save() 
	
	hornitzaileak =hornitzailea.objects.all()
	
	non='fitxaE'
	return render_to_response('admin_eguneko_hornitzaileak_kudeatu.html',{'hornitzaileak':hornitzaileak},context_instance=RequestContext(request))
	
def admin_hornitzaile_bihurtu (request):

	if request.GET.get('erabId'):
	
		userid=request.GET.get('erabId')
		erabiltzailea = User.objects.get(id=int(userid))
		erabiltzaile_emaila=erabiltzailea.email
		
		
		#3 taldea eman
		group = Group.objects.get(name='hornitzailea') 
		group.user_set.add(erabiltzailea)
        
		#2 taldea kendu
		group = Group.objects.get(name='herritarra') 
		group.user_set.remove(erabiltzailea)
		
		#Hornitzaile-fitxa 'hutsa' sortu EZ BALDIN BADAUKA 
		#Erabiltzaile "herritar" moduan erregistratu bada ez du edukiko, baina "hornitzaile" izateko eskaera egin badu, edukiko du fitxa hutsa
		num_results = hornitzailea.objects.filter(fk_user=erabiltzailea).count()
		hornitzaile_izena=erabiltzailea.username
		if num_results == 0:	
			hornitzaile_fitxa=hornitzailea(fk_user=erabiltzailea,izena=hornitzaile_izena)
			hornitzaile_fitxa.save()
		
		#Emaila bidali		
		mezua=_("Hornitzailearen izena:")+str(hornitzaile_izena)+".\n"+_("Hornitzailea da hemendik aurrera. Datu-basean burutu dira egin beharreko aldaketak.")
		send_mail('OndareBideak - Hornitzaile berria sortu da', mezua, 'ondarebideak@elhuyar.eus',['ondarebideak@elhuyar.eus'], fail_silently=False)
        
		#Emaila bidali erabiltzaileari
		mezua=str(hornitzaile_izena)+":\n"+_("OndareBideak sisteman hornitzailea zara hemendik aurrera. Edozein zalantza idatzi hona: ondarebideak@elhuyar.eus")
		send_mail('OndareBideak - Hornitzaile izateko baimenak jaso dituzu', mezua, 'ondarebideak@elhuyar.eus',[erabiltzaile_emaila], fail_silently=False)
            
	
	hornitzaileak = []
	hornitzaileak = hornitzailea.objects.filter(fk_user__groups__id=3)
	hornitzaileak_id = []
	hornitzaileak_id = [x.fk_user.id for x in hornitzaileak]
    
	erabiltzaileak = User.objects.all()
	user_form = UserForm()
	
	non='fitxaE'
	return render_to_response('admin_erabiltzaileak_kudeatu.html',{'non':non,'erabiltzaileak':erabiltzaileak,'hornitzaileak':hornitzaileak,'hornitzaileak_id':hornitzaileak_id,'user_form':user_form},context_instance=RequestContext(request))
	


def eguneko_itema_kendu(request):
    
    item_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    
    
    item.objects.filter(id=item_id).update(egunekoa = 0,proposatutakoa=1)   

    #GURI ALDAKETAREN BERRI EMAN?   
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko item hau kendu du (id): "+str(item_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko itemetan aldaketak', mezua, 'ondarebideak@elhuyar.com',['ondarebideak@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        
        #!!! HEMENDIK NIRE ITEMAK SAKATZEAN SARTUKO DA
        userName=request.user.username
        userID=request.user.id
        itemak=[]
        itemak = item.objects.filter(fk_ob_user__id=userID).order_by('-dc_date')
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
        '''
    elif(nondik=="bilaketa"):
       
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
    
        nireak=request.GET['nireak']
        
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
        
        hornitzaile_izena=request.GET['hornitzaile_search']
        if hornitzaile_izena !="":
            #dagokion hornitzailearenak hartuko ditugu behean hasteko
            #hornitzaileakF=""
            horni_id=request.GET['horni_id']
         
            hornitzaile_id=int(horni_id)     
           
            hornitzailea_obj=hornitzailea.objects.get(fk_user__id=hornitzaile_id)
            hornitzaile_izena=hornitzailea_obj.izena
        
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:        
                items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa                                                                                                   
            if(hornitzaileakF != ""):

                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=hornitzaileakF_list)

            #Mota filtroa,                                                           
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)


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

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                  
                    items=items.filter(item_id__in=bozkatuenak_ids)


            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else:   
            
                paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa                                                                                                   
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
       
            #Ordena Filtroa
            bozkatuenak_path_zerrenda=[]
            if(ordenakF != ""):            
                if(oData == "data"):
                    paths = paths.order_by('-path_creation_date')
                if(oData2 == "dataAsc"):
                    paths = paths.order_by('path_creation_date')              
                if(oBoto == "botoak"):
                    ##PROBATU order_by erabiltzen! agian azka
                    bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
                    paths_ids=[]
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
       
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
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
       
                items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa                                                                                                
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa,                                                                                                       
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

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
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                     
                    items=items.filter(item_id__in=bozkatuenak_ids)


            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))

            if(hornitzaileakF != ""):

                #hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]                                                  
                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)#if(hornitzaileakF != ""):

       
      
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                          
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)
      
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
        
        elif hizkuntza == 'en':
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
       
                items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
          
            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa,                                                                                                          
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

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
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    items=items.filter(item_id__in=bozkatuenak_ids)

                    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
        
                paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)
       
     
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)
        
      
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
            
            
            
            
        #ITEMAK
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
    
        #IBILBIDEAK
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
            
    
    
        z="i"
        
        #Datu-baseko hornitzaileak lortu                                                                                           
        db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
        db_hornitzaileak_text ="_".join(db_hornitzaileak)

        #Datu-baseko motak lortu                                                                                                    
        db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
        db_motak_text ="_".join(db_motak)

        #Datu-baseko lizentziak lortu                                                                                               
        db_lizentziak=lizentzia.objects.all()
        db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
        if  hornitzaile_izena !="":
            
            geoloc_longitude=hornitzailea_obj.geoloc_longitude
            geoloc_latitude=hornitzailea_obj.geoloc_latitude
            
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzailea_obj,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))

        else:
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'db_hornitzaileak_text':db_hornitzaileak_text,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    elif nondik =="ikusi":
     
        item_tupla = item.objects.get(pk=item_id)
            
   
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        hornitzailea=item_tupla.edm_provider
        #hornitzailea=item_tupla.dc_creator
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
       
        
        botatuDu=0
        botoKopurua=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
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
        qrUrl="http://ondarebideak.org/erakutsi_item?id="+item_id
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
        #LORTU ITEMAREN KOMENTARIOAK
        comments = item_tupla.get_comments()
      
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()

    
        non="erakutsi_item"

        
        return render_to_response('item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    

    elif nondik.startswith("path"):
        print "nondik ba? ikusi path"
        item_tupla = item.objects.get(pk=item_id)
        path_id=nondik[4:]
            
   
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        hornitzailea=item_tupla.edm_provider
        #hornitzailea=item_tupla.dc_creator
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
       
        
        botatuDu=0
        botoKopurua=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
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
        qrUrl="http://ondarebideak.org/nabigatu?path_id="+path_id+"&item_id="+item_id
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
        #LORTU ITEMAREN KOMENTARIOAK
        comments = item_tupla.get_comments()
      
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        print "item.html deitu baino lehen"
    
        non="nabigazio_item"
        
        
        return render_to_response('nabigazio_item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    

    else:
        
        #editatu
        item_tupla = item.objects.get(pk=item_id)
        titulua=item_tupla.dc_title
        deskribapena=item_tupla.dc_description
        gaia=item_tupla.dc_subject
        herrialdea=item_tupla.edm_country
      
        data=item_tupla.dc_date
        
       
        mota=item_tupla.edm_type
        if("TEXT" in mota):
            mota=1
            mot="TEXT"
        elif("VIDEO" in mota):
            mota=2
            mot="VIDEO"
        elif("IMAGE" in mota):
            mota=3
            mot="IMAGE"
        else:
            #SOUND
            mota=4
            mot="SOUND"
 
        lizentzia=item_tupla.edm_rights
        if("http://creativecommons.org/publicdomain/mark/1.0/" in lizentzia):
        
            lizentzia=1
            liz="Public Domain Mark"
        elif("http://www.europeana.eu/rights/out-of-copyright-non-commercial/" in lizentzia):
            lizentzia=2
            liz="Out of copyright - non commercial re-use"
        elif("http://creativecommons.org/publicdomain/zero/1.0/" in lizentzia):
            lizentzia=3
            liz="CC0"
        elif("http://creativecommons.org/licenses/by/4.0" in lizentzia):
            lizentzia=4
            liz="CC-BY"
        elif("http://creativecommons.org/licenses/by-sa/4.0/" in lizentzia):
            lizentzia=5
            liz="CC-BY-SA"
        elif("http://creativecommons.org/licenses/by-nd/4.0/" in lizentzia):
            lizentzia=6
            liz="CC-BY-ND"
        elif("http://creativecommons.org/licenses/by-nc/4.0/" in lizentzia):
            lizentzia=7
            liz="CC-BY-NC" 
        elif("http://creativecommons.org/licenses/by-nc-sa/4.0/" in lizentzia):
            lizentzia=8
            liz="CC-BY-NC-SA"
        elif("http://creativecommons.org/licenses/by-nc-nd/4.0/" in lizentzia):
            lizentzia=9
            liz="CC-BY-NC-ND"
        elif("http://www.europeana.eu/rights/rr-f/" in lizentzia):
            lizentzia=10
            liz="Rights Reserved - Free Access"
        elif("http://www.europeana.eu/rights/rr-p/" in lizentzia):
            lizentzia=11
            liz="Rights Reserved - Paid Access"
        elif("http://www.europeana.eu/rights/orphan-work-eu/" in lizentzia):
            lizentzia=12
            liz="Orphan Work"           
        else:
            #http://www.europeana.eu/rights/unknown/
            lizentzia=13
            liz="Unknown"
            
        ob_language=item_tupla.ob_language
        if('eu' in ob_language):
            eu=True
        else:
            eu=False
        if('es' in ob_language):
            es=True
        else:
            es=False
        if('en' in ob_language):
            en=True
        else:
            en=False
        
        #kategoria=item_tupla.dc_type
        eskubideak=item_tupla.dc_rights
            
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.dc_date 
        viewAtSource=item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        objektua=item_tupla.edm_object
        hornitzailea=item_tupla.edm_provider
        sortzailea=item_tupla.dc_creator
        gaia = item_tupla.dc_subject
        herrialdea =item_tupla.edm_country
        jatorrizkoa =item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
        
        non="itema_editatu" #Mapako baimenak kontrolatzeko erabiliko da hau
       
       
        #itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'eu':eu, 'es':es, 'en':en, 'data':data,'mota':mota,'lizentzia':lizentzia,'herrialdea':herrialdea})
        #return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'hizkuntza':ob_language,'viewAtSource':viewAtSource},context_instance=RequestContext(request))
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'mota':mota,'objektua':objektua, 'herrialdea':herrialdea , 'jatorrizkoa': jatorrizkoa, 'sortzailea':sortzailea,'gaia':gaia, 'lizentzia':lizentzia, 'data':data,'eu':eu,'es':es,'en':en})
        return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'viewAtSource':viewAtSource,'mota':mot,'liz':liz,'objektua':objektua},context_instance=RequestContext(request))

        
       

def eguneko_itema_gehitu(request):
    
    item_id = request.GET.get('id')
    nondik = request.GET.get('nondik')

    item.objects.filter(id=item_id).update(egunekoa = 1)   
    #item_tartekoa.egunekoa=1
    #item_tartekoa.save()        

    #GURI ALDAKETAREN BERRI EMAN?
    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko item hau gehitu du (id): "+str(item_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko itemetan aldaketak', mezua, 'ondarebideak@elhuyar.com',['ondarebideak@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        
        #!!! HEMENDIK NIRE ITEMAK SAKATZEAN SARTUKO DA?
        userName=request.user.username
        userID=request.user.id
        itemak=[]
        itemak = item.objects.filter(fk_ob_user__id=userID).order_by('-dc_date')
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
        '''
    elif(nondik=="bilaketa"):
        #!! Hona 3 lekutatik etor daiteke:
        #ITEMEN HASIERA ORRITIK
        #HORNITZAILEAREN ORRITIK
        #GALDERA ARRUNT BATETIK
        
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
    
        nireak=request.GET['nireak']

        
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
                    
        hornitzaile_izena=request.GET['hornitzaile_search']
        hornitzaile_obj=[]
        if (hornitzaile_izena !=""):
            # dagokion hornitzailearenak hartuko ditugu behean hasteko          
            hornitz_id=request.GET['horni_id']
            hornitzaile_id=int(hornitz_id)     
           
            hornitzaile_obj=hornitzailea.objects.filter(fk_user__id=hornitzaile_id)
            hornitzaile_izena=hornitzaile_obj.izena
        
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
                
            else:
                #galdera arrunt baten filtroetatik
                items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
            
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
       
            #hornitzaile filtroa                                                                                                         
            if(hornitzaileakF != ""):

                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
              
                # username ->userid -> distinct(edm_provider)
                items = items.filter(edm_provider__in=hornitzaileakF_list)
              
            #Mota filtroa                                                                                                              
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                   
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)
    
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

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                  
                    items=items.filter(item_id__in=bozkatuenak_ids)
                
    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
            
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
            else:       
                paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            
            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
                #ID errepikatuak kendu 
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)
       
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
       
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
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
            
            else:
                items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            
            #hornitzaile filtroa                                                                                                        
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])
                
                #Mota filtroa,                                                                                                 
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)
                    
            #Lizentziak filtroa                                                                                                    
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

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
                    #print bozkatuenak_item_zerrenda[0].item_id                                                                          
                    items_ids=[]
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                       
                    items=items.filter(item_id__in=bozkatuenak_ids)


            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
        
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
            
            else:       
                paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa                                                                                                         
            if(hornitzaileakF != ""):

                #hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]                                                 
                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)
                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
                #ID errepikatuak kendu                                                                                                   
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
      
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                        
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)
                    
        
      
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
        elif hizkuntza == 'en':
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
            
            else:      
                items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
           
            #hornitzaile filtroa                                                                                                
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa,                                                                                                         
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                         
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

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
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)
                                        
                    items=items.filter(item_id__in=bozkatuenak_ids)


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
        
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
            
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa                                                                                                         
            if(hornitzaileakF != ""):

                
                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)
                
                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                             
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)
                
                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)
                #hornitzaile filtroa                                                                                                    
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                        
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
      
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

        #Datu-baseko hornitzaileak lortu                                                                                           
        db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
        db_hornitzaileak_text ="_".join(db_hornitzaileak)
        
        #Datu-baseko motak lortu                                                                                                   
        db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
        db_motak_text ="_".join(db_motak)
    
        #Datu-baseko lizentziak lortu                                                                                              
        db_lizentziak=lizentzia.objects.all()
        db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
        
        
        #ITEMAK
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
    
        #IBILBIDEAK
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
        
        
        #Maddalen:
        if hornitzaile_izena !="":
            geoloc_longitude=hornitzaile_obj.geoloc_longitude
            geoloc_latitude=hornitzaile_obj.geoloc_latitude
           
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzaile_obj,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))

        else:
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    elif nondik =="ikusi":
        print "nondik ba? ikusi"
        item_tupla = item.objects.get(pk=item_id)
            
   
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        hornitzailea=item_tupla.edm_provider
        #hornitzailea=item_tupla.dc_creator
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
       
        
        botatuDu=0
        botoKopurua=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
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
        qrUrl="http://ondarebideak.org/erakutsi_item?id="+item_id
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
        #LORTU ITEMAREN KOMENTARIOAK
        comments = item_tupla.get_comments()
      
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        #print "item.html deitu baino lehen"
    
        non="erakutsi_item"
        
        
        return render_to_response('item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    

    elif nondik.startswith("path"):
        print "nondik ba? ikusi path"
        item_tupla = item.objects.get(pk=item_id)
        path_id=nondik[4:]
            
   
        herrialdea=item_tupla.edm_country
        hizkuntza=item_tupla.dc_language
        kategoria=item_tupla.dc_type
        eskubideak=item_tupla.edm_rights
        urtea=item_tupla.edm_year 
        viewAtSource=item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        hornitzailea=item_tupla.edm_provider
        #hornitzailea=item_tupla.dc_creator
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
       
        
        botatuDu=0
        botoKopurua=0
        if(votes_item.objects.filter(item=item_id,user_id=request.user.id)):
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
        qrUrl="http://ondarebideak.org/nabigatu?path_id="+path_id+"&item_id="+item_id
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=item_tupla)
        
        #LORTU ITEMAREN KOMENTARIOAK
        comments = item_tupla.get_comments()
      
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        #print "item.html deitu baino lehen"
    
        non="nabigazio_item"
        
        
        return render_to_response('nabigazio_item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    
    else:
        
        #editatu
        item_tupla = item.objects.get(pk=item_id)
        titulua=item_tupla.dc_title
        deskribapena=item_tupla.dc_description
        gaia=item_tupla.dc_subject
        herrialdea=item_tupla.edm_country
        data=item_tupla.dc_date
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
        
        mota=item_tupla.edm_type
        if("TEXT" in mota):
            print "bai, TEXT da"
            mota=1
            mot="TEXT"
        elif("VIDEO" in mota):
            mota=2
            mot="VIDEO"
        elif("IMAGE" in mota):
            mota=3
            mot="IMAGE"
        else:
            #SOUND
            mota=4
            mot="SOUND"
 
        lizentzia=item_tupla.edm_rights
        if("http://creativecommons.org/publicdomain/mark/1.0/" in lizentzia):
        
            lizentzia=1
            liz="Public Domain Mark"
        elif("http://www.europeana.eu/rights/out-of-copyright-non-commercial/" in lizentzia):
            lizentzia=2
            liz="Out of copyright - non commercial re-use"
        elif("http://creativecommons.org/publicdomain/zero/1.0/" in lizentzia):
            lizentzia=3
            liz="CC0"
        elif("http://creativecommons.org/licenses/by/4.0" in lizentzia):
            lizentzia=4
            liz="CC-BY"
        elif("http://creativecommons.org/licenses/by-sa/4.0/" in lizentzia):
            lizentzia=5
            liz="CC-BY-SA"
        elif("http://creativecommons.org/licenses/by-nd/4.0/" in lizentzia):
            lizentzia=6
            liz="CC-BY-ND"
        elif("http://creativecommons.org/licenses/by-nc/4.0/" in lizentzia):
            lizentzia=7
            liz="CC-BY-NC" 
        elif("http://creativecommons.org/licenses/by-nc-sa/4.0/" in lizentzia):
            lizentzia=8
            liz="CC-BY-NC-SA"
        elif("http://creativecommons.org/licenses/by-nc-nd/4.0/" in lizentzia):
            lizentzia=9
            liz="CC-BY-NC-ND"
        elif("http://www.europeana.eu/rights/rr-f/" in lizentzia):
            lizentzia=10
            liz="Rights Reserved - Free Access"
        elif("http://www.europeana.eu/rights/rr-p/" in lizentzia):
            lizentzia=11
            liz="Rights Reserved - Paid Access"
        elif("http://www.europeana.eu/rights/orphan-work-eu/" in lizentzia):
            lizentzia=12
            liz="Orphan Work"           
        else:
            #http://www.europeana.eu/rights/unknown/
            lizentzia=13
            liz="Unknown"
            
        ob_language=item_tupla.ob_language
        if('eu' in ob_language):
            eu=True
        else:
            eu=False
        if('es' in ob_language):
            es=True
        else:
            es=False
        if('en' in ob_language):
            en=True
        else:
            en=False
        
        
          
        #kategoria=item_tupla.dc_type
        eskubideak=item_tupla.dc_rights
        urtea=item_tupla.dc_date 
        viewAtSource=item_tupla.edm_isshownat
        hornitzailea=item_tupla.edm_provider
        sortzailea=item_tupla.dc_creator
        gaia = item_tupla.dc_subject
        herrialdea =item_tupla.edm_country
        jatorrizkoa =item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
        
        non="itema_editatu" #Mapako baimenak kontrolatzeko erabiliko da hau
       
       
        #itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'hizkuntza':hizkuntza})
        #return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'hizkuntza':hizk,'viewAtSource':viewAtSource},context_instance=RequestContext(request))
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'mota':mota, 'herrialdea':herrialdea , 'jatorrizkoa': jatorrizkoa, 'sortzailea':sortzailea,'gaia':gaia, 'lizentzia':lizentzia, 'data':data,'eu':eu,'es':es,'en':en})
        return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'viewAtSource':viewAtSource,'mota':mot,'liz':liz},context_instance=RequestContext(request))

        
        
#EGUNEKO IBILBIDEA KUDEATZEKO BI FUNTZIO
def eguneko_ibilbidea_gehitu(request):
    
    path_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    
    path.objects.filter(id=path_id).update(egunekoa = 1)
  
  
    #GURI ALDAKETAREN BERRI EMAN?    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko ibilbide hau gehitu du (id): "+str(path_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko ibilbidetan aldaketak', mezua, 'ondarebideak@elhuyar.com',['ondarebideak@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        
        
        #HEMENDIK NIRE IBILBDEAK SAKATZEAN SARTUKO DA
        
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
   
        
        '''
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
        '''
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
    
        nireak=request.GET['nireak']
        
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
                    
        hornitzaile_izena=request.GET['hornitzaile_search']
        hornitzailea_obj=[]
        if hornitzaile_izena !="":
            # dagokion hornitzailearenak hartuko ditugu behean hasteko
            print "hornitzaile_search"
           
            #hornitzaileakF=""
            horni_id=request.GET['horni_id']
         
            hornitzaile_id=int(horni_id)     
           
            hornitzailea_obj=hornitzailea.objects.get(fk_user__id=hornitzaile_id)
            hornitzaile_izena=hornitzailea_obj.izena

    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
                #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
                items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            
            #hornitzaile filtroa                                                                                              
            if(hornitzaileakF != ""):

                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=hornitzaileakF_list)

            #Mota filtroa,                                                                                                         
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)
    
        
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

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                  
                    items=items.filter(item_id__in=bozkatuenak_ids)

            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            
            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
       
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

       
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
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
       
                items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
 
            #hornitzaile filtroa   
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa                                                                                                       
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

    
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
                    #print bozkatuenak_item_zerrenda[0].item_id                                                                     
                    
                    items_ids=[]

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                 
                    items=items.filter(item_id__in=bozkatuenak_ids)

                    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)
       
      
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)
        
      
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
        elif hizkuntza == 'en':
       
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
                items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            
            #hornitzaile filtroa                                                                                                  
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa,                                                                                                          
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)


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
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    items=items.filter(item_id__in=bozkatuenak_ids)

                    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):


                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
     
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
      
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
            
            
        #ITEMAK
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
    
        #IBILBIDEAK
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
    
    
        z="p"

        #Datu-baseko hornitzaileak lortu                                                                                             
        db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
        db_hornitzaileak_text ="_".join(db_hornitzaileak)

        #Datu-baseko motak lortu                                                                                                     
        db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
        db_motak_text ="_".join(db_motak)

        #Datu-baseko lizentziak lortu                                                                                                
        db_lizentziak=lizentzia.objects.all()
        db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak)) 
        
        if hornitzaile_izena !="":
            
            geoloc_longitude=hornitzailea_obj.geoloc_longitude
            geoloc_latitude=hornitzailea_obj.geoloc_latitude
            
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzailea_obj,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))

            
        else:
        
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    elif(nondik=="ikusi"):
        print "nondik ba?"
        print "nondik ba? ikusi"
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
        pathqrUrl="http://ondarebideak.dss2016.eu/nabigazioa_hasi?path_id="+str(path_id)
        itemqrUrl="http://ondarebideak.dss2016.eu/erakutsi_item?id="+str(item_id)
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=momentukoItema)
        
        #LORTU IBILBIDEAREN KOMENTARIOAK
        comments = momentukoPatha.get_comments()    
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        
        #Ezkerreko zutabea ez erakusteko
        non="fitxaE"
        return render_to_response('ibilbidea.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    else:
        #Editatu
            
        #lortu path-aren ezaugarriak
        ibilbidea = path.objects.get(id=path_id)
        titulua=ibilbidea.dc_title
        gaia=ibilbidea.dc_subject
        deskribapena=ibilbidea.dc_description
        irudia=ibilbidea.paths_thumbnail
      
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=ibilbidea,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
       
    
    
    return render_to_response('editatu_ibilbidea.html',{'momentukoPatha':ibilbidea,'path_id':path_id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))

def eguneko_ibilbidea_kendu(request):
    
    path_id = request.GET.get('id')
    nondik = request.GET.get('nondik')
    

    
    path.objects.filter(id=path_id).update(egunekoa = 0,proposatutakoa=1)   

    #GURI ALDAKETAREN BERRI EMAN?
    
    mezua="Hornitzailearen izena:"+str(request.user.username)+".\n"+"Eguneko ibilbide hau kendu du (id): "+str(path_id)+"\n"+"Beharra badago bidali mezua hornitzaileari: "+str(request.user.email)
    send_mail('OndareBideak - Eguneko ibilbideetan aldaketak', mezua, 'ondarebideak@elhuyar.com',['ondarebideak@elhuyar.com'], fail_silently=False)
    
    if(nondik=="hasiera"):
        
        #HEMENDIK NIRE IBILBDEAK SAKATZEAN SARTUKO DA
        
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
   
       
        '''
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
        '''
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
    
        nireak=request.GET['nireak']
        
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
                    
        
        hornitzaile_izena=request.GET['hornitzaile_search']
        if hornitzaile_izena !="":
            # dagokion hornitzailearenak hartuko ditugu behean hasteko
            print "hornitzaile_search"
           
            hornitzaileakF=""
            horni_id=request.GET['horni_id']
         
            hornitzaile_id=int(horni_id)     
           
            hornitzailea_obj=hornitzailea.objects.get(fk_user__id=hornitzaile_id)
            hornitzaile_izena=hornitzailea_obj.izena
        
        
    
        #GALDERA BOTA
        if hizkuntza == 'eu':
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
                #items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)| SQ(dc_language='eu') ).models(*search_models_items)       
                items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)       
       
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))


            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):

                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=hornitzaileakF_list)

            #Mota filtroa,                                                                                                          
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)
    

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

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                  
                    items=items.filter(item_id__in=bozkatuenak_ids)


            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                          
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":              
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                
        
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else: 
                paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            
            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
       
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
       
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
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
       
                items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
                
            #hornitzaile filtroa                                                                                                   
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa                                                                                                           
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)


                
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
                    #print bozkatuenak_item_zerrenda[0].item_id                                                                     

                    items_ids=[]

                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                                                  
                    items=items.filter(item_id__in=bozkatuenak_ids)

                    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":                        
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else:  
                paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
           
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            
            if(hornitzaileakF != ""):

                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)


      
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)

        
      
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
        elif hizkuntza == 'en':
            
            #ITEMS:hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "itemak" aukeratik dator       
                items = SearchQuerySet().all().models(*search_models_items)
            elif(hornitzaile_izena!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=hornitzaile_id).models(*search_models_items) 
                #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
            elif(nireak!=""):
                # hornitzaile baten orriko filtroak sakatuta
                items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
             
            else:
       
                items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
            #hornitzaile filtroa
            #hornitzaile filtroa                                                                                                    
            if(hornitzaileakF != ""):
                hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
                items = items.filter(edm_provider__in=[hornitzaileakF_list])

            #Mota filtroa,                                                                                                          
            if(motakF != ""):
                motakF_list = [str(x) for x in motakF.split(",")]
                items = items.filter(edm_type__in=motakF_list)

            #Lizentziak filtroa                                                                                                     
            if(lizentziakF != ""):
                lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
                items = items.filter(edm_rights__in=lizentziakF_list)

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
                    items_ids=map(lambda x: int(x.item_id),items)
                    bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)

                    items=items.filter(item_id__in=bozkatuenak_ids)


                    
            #Besteak filtroa
            if (besteakF != ""):  
                if bEgun=="egunekoa":
                    items=items.filter(egunekoa=1)
                if bProp == "proposatutakoa":
                    items=items.filter(proposatutakoa=1)
                if bWikify=="wikifikatua":
                    items=items.filter(aberastua=1)
                if bIrudiBai=="irudiaDu":             
              
                    items=items.filter(edm_object = Raw("[* TO *]"))  
                if bIrudiEz=="irudiaEzDu":
                    #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                    items=items.exclude(edm_object = Raw("[* TO *]"))
                    #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        #...
            #PATHS hasierako karga
            if (galdera =="" and hornitzaile_izena=="" and nireak==""):
                #menu nagusiko "ibilbideak" aukeratik dator 
                paths = SearchQuerySet().all().models(*search_models_paths) 
            elif(hornitzaile_izena!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzaile_id).models(*search_models_paths)      
            elif(nireak!=""):
                #hornitzaile baten orriko filtroak sakatuta
                paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)                
           
            else:  
                paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
            #hizkuntza filtroa
            if hizkuntzakF != "":       
                paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
            #hornitzaile filtroa TXUKUNDUUUU
            if(hornitzaileakF != ""):


                item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

                usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)

                #ID errepikatuak kendu                                                                                              
                usr_id_zerrenda_set = set(usr_id_zerrenda)
                usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

                paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)

       
     
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
                    paths_ids=map(lambda x: int(x.path_id),paths)
                    bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                    #Ordena mantentzen du??                                                                                         
                    paths=paths.filter(path_id__in=bozkatuenak_path_ids)


        
      
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
    
    
    
        #ITEMAK
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
    
        #IBILBIDEAK
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
            
    
        z="p"

        #Datu-baseko hornitzaileak lortu                                                                                         
                                                                                                                        
        db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
        db_hornitzaileak_text ="_".join(db_hornitzaileak)

        #Datu-baseko motak lortu                                                                                                   
        db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
        db_motak_text ="_".join(db_motak)

        #Datu-baseko lizentziak lortu                                                                                               
        db_lizentziak=lizentzia.objects.all()
        db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))

        if hornitzaile_izena !="":
            
            geoloc_longitude=hornitzailea_obj.geoloc_longitude
            geoloc_latitude=hornitzailea_obj.geoloc_latitude
            
            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzailea_obj,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))

            
        else:

            return render_to_response('cross_search.html',{'nireak':nireak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))

    elif (nondik=="ikusi"):
        print "nondik ba?"
        print "nondik ba? ikusi"
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
        pathqrUrl="http://ondarebideak.dss2016.eu/nabigazioa_hasi?path_id="+str(path_id)
        itemqrUrl="http://ondarebideak.dss2016.eu/erakutsi_item?id="+str(item_id)
        
        #Itema erabiltzen duten path-ak lortu
        itemPaths=node.objects.filter(fk_item_id=momentukoItema)
        
        #LORTU IBILBIDEAREN KOMENTARIOAK
        comments = momentukoPatha.get_comments()    
        comment_form = CommentForm() 
        comment_parent_form = CommentParentForm()
        
        #Ezkerreko zutabea ez erakusteko
        non="fitxaE"
        return render_to_response('ibilbidea.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    
    else:
    #Editatu
            
        #lortu path-aren ezaugarriak
        ibilbidea = path.objects.get(id=path_id)
        titulua=ibilbidea.dc_title
        gaia=ibilbidea.dc_subject
        deskribapena=ibilbidea.dc_description
        irudia=ibilbidea.paths_thumbnail
      
        #path hasierak hartu
        nodes = [] 
        erroak = node.objects.filter(fk_path_id=ibilbidea,paths_start=1)
        for erroa in erroak:
            nodes = nodes + get_tree(erroa)
       
    
    
    return render_to_response('editatu_ibilbidea.html',{'momentukoPatha':ibilbidea,'path_id':path_id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))

        

     
def ibilbideak_hasiera(request):
    
    
    #print "ibilbideak_hasiera"
    #Ibilbideen hasierako pantailan erakutsi behar diren Ibilbideen informazioa datu-basetik lortu eta pasa
     
    #DB-an GALDERA EGIN EGUNEKO/RANDOM/AZKENAK/IKUSIENA PATHA LORTZEKO   
    #DB-an GALDERA EGIN EGUNEKO IBILBIDEA LORTZEKO
   
    login_form = LoginForm()
    erabiltzailea_form = CreateUserForm() 
    
    if 'login' in request.POST:
        logina(request)
        
    if 'Erabiltzailea_gehitu' in request.POST:
        erregistratu(request)
   
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
    
    
    #Egunekoak
    eguneko_ibilbideak=[]
    eguneko_ibilbideak=path.objects.filter(egunekoa=1).exclude(acces='1')
    
    #Azkenak
    azken_ibilbideak=[]
    azken_ibilbideak=path.objects.order_by('-creation_date').exclude(acces='1')[:10]
    
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
    
    #Datu-baseko hornitzaileak lortu                                                                                             
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)

    #Datu-baseko motak lortu                                                                                                     
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)

    #Datu-baseko lizentziak lortu                                                                                                
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
    
    z='p'
    if request.GET.get('z'):
        z = request.GET.get('z')    
  
    
    items=[]
    bilaketa_filtroak=1
    galdera=''
    hizkuntza='eu'
    hizkF=''
    horniF=''
    motaF=''
    ordenaF=''
    lizentziaF=''
    besteaF=''
    search_models_paths=[path]
    search_models_items=[item]
    items = SearchQuerySet().all().models(*search_models_items)
    #ADMIN BADA, GUZTIAK HARTU, ACCESS =1 DUTENAK ERE BAI
    if request.user.is_superuser:
    	paths = SearchQuerySet().all().models(*search_models_paths).order_by('-path_creation_date')
    else:
    	paths = SearchQuerySet().all().models(*search_models_paths).exclude(acces='1').order_by('-path_creation_date')
        
     
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
    
    
    return render_to_response('cross_search.html',{'login_form':login_form,'erabiltzailea_form':erabiltzailea_form,'non':non,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))   
    #return render_to_response('ibilbideak_hasiera.html',{'non':non,'paths':paths,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'ibilbide_bozkatuenak':ibilbide_bozkatuenak},context_instance=RequestContext(request))

   
def hornitzaileak_hasiera(request):

    hornitzaileak = []
    hornitzaileak = hornitzailea.objects.filter(fk_user__groups__id=3)
    
    paginator = Paginator(hornitzaileak, 27)
    
    type(paginator.page_range)  # `<type 'rangeiterator'>` in Python 2.
 
    page = request.GET.get('page')
    try:
        hornitzaileak = paginator.page(page)                
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hornitzaileak = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hornitzaileak = paginator.page(paginator.num_pages)
        
    
    return render_to_response('hornitzaileak_hasiera.html', {'hornitzaileak':hornitzaileak}, context_instance=RequestContext(request))
    
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
    #suggestions_img = [result.edm_object for result in sqs]
    
    suggestions_img=[]
    for result in sqs:
    	if result.ob_thumbnail:
    	    suggestions_img.append(result.ob_thumbnail)
    	else:
    		suggestions_img.append(result.edm_object)
    
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
    
    login_form = LoginForm()
    erabiltzailea_form = CreateUserForm() 
    
    if 'login' in request.POST:
        logina(request)
        
    if 'Erabiltzailea_gehitu' in request.POST:
        erregistratu(request)
        
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
        #items=SearchQuerySet.all()filter(SQ(text_eu=Raw("{!dismax qf='dc_title^3 dc_description^2 text_eu'}" + galdera)|(text_es2eu=Raw("{!dismax qf='dc_title^3 dc_description^2 text_es2eu'}" + galdera)|(text_en2eu=Raw("{!dismax qf='dc_title^3 dc_description^2 text_en2eu'}" + galdera)).models(*search_models_items)
        items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)
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

    
    #'Zirriborroak' (acces=1) diren ibilbideak baztertu
    paths=paths.exclude(acces="1")   
    
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
    
    #ITEMAK
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
    
    #IBILBIDEAK
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
    
    
    
    #Datu-baseko hornitzaileak lortu
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)
    
    #Datu-baseko motak lortu
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)
    
    #Datu-baseko lizentziak lortu
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
    
    bilaketa_filtroak=1
    return render_to_response('cross_search.html',{'login_form':login_form,'erabiltzailea_form':erabiltzailea_form,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))


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
    #horniF.append(hornitzaile_izena)
   
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

    #'Zirriborroak' (acces=1) diren ibilbideak baztertu
    paths=paths.exclude(acces="1")   
     
    
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
    hornitzaile = hornitzailea.objects.get(fk_user__id=hornitzaile_id)
   
    geoloc_longitude=0.0
    geoloc_latitude=0.0
    geoloc_longitude=hornitzaile.geoloc_longitude
    geoloc_latitude=hornitzaile.geoloc_latitude
    
    bilaketa_filtroak=1
    
    #Datu-baseko hornitzaileak lortu
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)
    
    #Datu-baseko motak lortu
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)
    
    #Datu-baseko lizentziak lortu
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
    non='fitxaI'
 
    return render_to_response('cross_search.html',{'non':non,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'h':hornitzaile_izena,'geoloc_latitude':geoloc_latitude,'geoloc_longitude':geoloc_longitude,'hornitzailea':hornitzaile,'horniF':horniF,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza},context_instance=RequestContext(request))


def filtro_search(request):
    
    #Hona iristeko 4 aukera daude:
    #bilaketa arrunt baten filtroetatik
    #Menu nagusiko itemak edo ibilbideak sakatuta. Kasu honetan galdera="" eta z-ren balioak kontutan hartu
    #Hornitzaile bat kontsultatzetik. Kasu honetan  'hornitzailea' in request.GET  eta galdera hutsa da
    #Nire itemak ala Nire ibilbideak kontsultatzeko aukeratik ('nireak' aldagaiarekin kontrolatzen dugu aukera honetatik datorren)
    
    # Helburu hizkuntza guztietan burutuko du bilaketa
    hizkuntza=request.GET['hizkRadio']
   
    galdera=request.GET['search_input']
    z=request.GET['z']
 
    hizkuntzakF=request.GET['hizkuntzakF']
    hizkF=[] 
    hornitzaileakF=request.GET['hornitzaileakF']
   
    #horniF=[]
    motakF=request.GET['motakF']
    #motaF=[]
    ordenakF=request.GET['ordenakF']
    ordenaF=[]
    lizentziakF=request.GET['lizentziakF']
    #lizentziaF=[]  
    besteakF=request.GET['besteakF']
    besteaF=[]
    
  
    nireak=request.GET.get('nireak','')
    
    items=[]
    paths=[]
    search_models_items = [item]
    search_models_paths = [path]
    bilaketa_filtroak=1
    
    if 'hornitzailea' in request.GET:     
        hornitzaile_izena=request.GET['hornitzailea']
        hornitzailea_user_id=request.GET['hornitzailea_user_id']      
    else:
        hornitzaile_izena=""
        hornitzailea_user_id=""
    
    #FILTROAK PRESTATU
    hEu="ez"
    hEs="ez"
    hEn="ez"
    if hizkuntzakF != "": 
        hizkF=hizkuntzakF.split(',')

        for h in hizkF:
            print h
            if(h=="eu"):
                hEu="eu"
            if(h=="es"):
                hEs="es"
            if(h=="en"):
                hEn="en"
                
    
    
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
        #ITEMS:hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator       
            items = SearchQuerySet().all().models(*search_models_items)
        elif(hornitzaile_izena!=""):
            # hornitzaile baten orriko filtroak sakatuta
            items = SearchQuerySet().all().filter(item_user_id=hornitzailea_user_id).models(*search_models_items) 
            #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
        elif(nireak!=""):
            #Nire itemak kontsultatzetik 
            items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 
            
        else:
            #galdera arrunt baten filtroetatik
            items = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_items)
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            #!hornitzaile baten orri nagusitik baldin badator, hemen filtratuko ditugu hhornitzaile horri dagozkionak (goian gehitu diogu hornitzaileakF-ri)
            hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            items = items.filter(edm_provider__in=hornitzaileakF_list)

        #Mota filtroa,
        if(motakF != ""):            
            motakF_list = [str(x) for x in motakF.split(",")]      
            items = items.filter(edm_type__in=motakF_list)
        #Lizentziak filtroa 
        if(lizentziakF != ""):       
            lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
            items = items.filter(edm_rights__in=lizentziakF_list)  
        
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        print "ordenakF"
        print ordenakF
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
                
            if(oData2 == "dataAsc"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
                
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa            
                bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
                #print bozkatuenak_item_zerrenda[0].item_id
                items_ids=[]
     
                items_ids=map(lambda x: int(x.item_id),items)
                bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)
          
                #items=bozkatuenak_item_zerrenda.filter(item_id__in=items_ids)                
                items=items.filter(item_id__in=bozkatuenak_ids)
     
        #Besteak filtroa
        print "BESTE FILTRORIK?"
        print bEgun
        if (besteakF != ""):
        	
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=True)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(aberastua=1)
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
        
        #PATHS hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator 
            paths = SearchQuerySet().all().models(*search_models_paths) 
        elif(hornitzaile_izena!=""):
            #hornitzaile baten orriko filtroak sakatuta
            paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)      
        elif(nireak!=""):
            #Nire ibilbideak kontsultatzetik 
            paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)      
        
        else:
            #galdera arrunt batetik dator
            paths = SearchQuerySet().all().filter(SQ(text_eu=galdera)|SQ(text_es2eu=galdera)|SQ(text_en2eu=galdera)).models(*search_models_paths)
       
        #'Zirriborroak' (acces=1) diren ibilbideak baztertu
        if paths:
        	#print paths[0].acces
    		paths=paths.exclude(acces="1")
        
        
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa 
        if(hornitzaileakF != ""):
            
            #hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            item_hornitzaile_erab=item.objects.filter(edm_provider__in=hornitzaileakF_list)

            usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
            
            #ID errepikatuak kendu
            usr_id_zerrenda_set = set(usr_id_zerrenda)
            usr_id_zerrenda_uniq=list(usr_id_zerrenda_set)

            paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda_uniq)


        #Mota filtroa,IBILBIDEETAN EZ DAGO MOTA
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
                paths_ids=map(lambda x: int(x.path_id),paths)
                bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                #Ordena mantentzen du??                        
                paths=paths.filter(path_id__in=bozkatuenak_path_ids)  
        
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
        
        #ITEMS:hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator       
            items = SearchQuerySet().all().models(*search_models_items)
        elif(hornitzaile_izena!=""):
            # hornitzaile baten orriko filtroak sakatuta
            items = SearchQuerySet().all().filter(item_user_id=hornitzailea_user_id).models(*search_models_items) 
            #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
        elif(nireak!=""):
            #Nire itemak kontsultatzetik 
            items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 

        else:
            #galdera arrunt batetik dator       
            items = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_items)
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            items = items.filter(edm_provider__in=[hornitzaileakF_list])

        #Mota filtroa,
        if(motakF != ""):       
            motakF_list = [str(x) for x in motakF.split(",")]
            items = items.filter(edm_type__in=motakF_list) 
        
        #Lizentziak filtroa 
        if(lizentziakF != ""):       
            lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
            items = items.filter(edm_rights__in=lizentziakF_list)    
         
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
            if(oData2 == "dataAsc"):
              
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
                      
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=1)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(aberastua=1)
            if bIrudiBai=="irudiaDu":             
                #import pdb
                #pdb.set_trace()             
                #self.searchqueryset.exclude(edm_object = None ) hau egiten du behekoak
                items=items.filter(edm_object = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        
        #PATHS hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator 
            paths = SearchQuerySet().all().models(*search_models_paths) 
        elif(hornitzaile_izena!=""):
            #hornitzaile baten orriko filtroak sakatuta
            paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)      
        elif(nireak!=""):
            #Nire ibilbideak kontsultatzetik 
            paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)        
        else:
            #galdera arrunt batetik dator
            paths = SearchQuerySet().all().filter(SQ(text_es=galdera)|SQ(text_eu2es=galdera)|SQ(text_en2es=galdera)).models(*search_models_paths)
        
        #'Zirriborroak' (acces=1) diren ibilbideak baztertu
        if paths:
        	paths=paths.exclude(acces="1")   
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa TXUKUNDUUUU
        if(hornitzaileakF != ""):
            hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            item_hornitzaile_erab=item.objects.filter(edm_provider__in=[hornitzaileakF_list])
            usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
              
            paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda)
          
        #Ordena Filtroa
        bozkatuenak_path_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                paths = paths.order_by('-path_creation_date')
            if(oData2 == "dataAsc"):
                paths = paths.order_by('path_creation_date')              
            if(oBoto == "botoak"):
  
                bozkatuenak_path_zerrenda = votes_path.objects.annotate(votes_count=Count('path')).order_by('-votes_count')
                paths_ids=[]
                paths_ids=map(lambda x: int(x.path_id),paths)
                bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                #Ordena mantentzen du??                                                                                          
                paths=paths.filter(path_id__in=bozkatuenak_path_ids)

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

        #ITEMS:hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator       
            items = SearchQuerySet().all().models(*search_models_items)
        elif(hornitzaile_izena!=""):
            # hornitzaile baten orriko filtroak sakatuta
            items = SearchQuerySet().all().filter(item_user_id=hornitzailea_user_id).models(*search_models_items) 
            #paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)
        elif(nireak!=""):
            #Nire itemak kontsultatzetik 
            items = SearchQuerySet().all().filter(item_user_id=request.user.id).models(*search_models_items) 

        else:
            items = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_items)
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            items = items.filter(SQ(dc_language=hEu)|SQ(dc_language=hEs)|SQ(dc_language=hEn))
        
        #hornitzaile filtroa
        if(hornitzaileakF != ""):
            hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            items = items.filter(edm_provider__in=[hornitzaileakF_list])

        #Mota filtroa,
        if(motakF != ""):       
            motakF_list = [str(x) for x in motakF.split(",")]
            items = items.filter(edm_type__in=motakF_list) 
        
        #Lizentziak filtroa 
        if(lizentziakF != ""):       
            lizentziakF_list = [str(x) for x in lizentziakF.split(",")]
            items = items.filter(edm_rights__in=lizentziakF_list)   
             
        #Ordena Filtroa
        bozkatuenak_item_zerrenda=[]
        if(ordenakF != ""):            
            if(oData == "data"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('-edm_year')
            if(oData2 == "dataAsc"):
                #items = items.order_by('-dc_date')
                items = items.filter( edm_year= Raw("[* TO *]")).order_by('edm_year')
            if(oBoto == "botoak"):
                ##PROBATU order_by erabiltzen! agian azkarragoa                                                                 
                bozkatuenak_item_zerrenda = votes_item.objects.annotate(votes_count=Count('item')).order_by('-votes_count')
                items_ids=[]
                items_ids=map(lambda x: int(x.item_id),items)
                bozkatuenak_ids=map(lambda x: int(x.item_id),bozkatuenak_item_zerrenda)
                items=items.filter(item_id__in=bozkatuenak_ids)

                      
        #Besteak filtroa
        if (besteakF != ""):  
            if bEgun=="egunekoa":
                items=items.filter(egunekoa=1)
            if bProp == "proposatutakoa":
                items=items.filter(proposatutakoa=1)
            if bWikify=="wikifikatua":
                items=items.filter(aberastua=1)
            if bIrudiBai=="irudiaDu":             
                #import pdb
                #pdb.set_trace()             
                #self.searchqueryset.exclude(edm_object = None ) hau egiten du behekoak
                items=items.filter(edm_object = Raw("[* TO *]"))  
            if bIrudiEz=="irudiaEzDu":
                #self.searchqueryset.filter(edm_object = None ) hau egiten du behekoak
                items=items.exclude(edm_object = Raw("[* TO *]"))
                #items=items.filter(SQ(edm_object='null')|SQ(edm_object="uploads/NoIrudiItem.png"))
        
        #PATHS hasierako karga
        if (galdera =="" and hornitzaile_izena=="" and nireak==""):
            #menu nagusiko "itemak" aukeratik dator 
            paths = SearchQuerySet().all().models(*search_models_paths) 
        elif(hornitzaile_izena!=""):
            #hornitzaile baten orriko filtroak sakatuta
            paths = SearchQuerySet().all().filter(path_fk_user_id=hornitzailea_user_id).models(*search_models_paths)      
        elif(nireak!=""):
            #Nire ibilbideak kontsultatzetik 
            paths = SearchQuerySet().all().filter(path_fk_user_id=request.user.id).models(*search_models_paths)      
        else:
            #galdera arrunt batetik dator
            paths = SearchQuerySet().all().filter(SQ(text_en=galdera)|SQ(text_eu2en=galdera)|SQ(text_es2en=galdera)).models(*search_models_paths)
        
        #'Zirriborroak' (acces=1) diren ibilbideak baztertu
        if paths:
       		paths=paths.exclude(acces="1")   
        
        #hizkuntza filtroa
        if hizkuntzakF != "":       
            paths =paths.filter(SQ(language=hEu)|SQ(language=hEs)|SQ(language=hEn))
        #hornitzaile filtroa 
        if(hornitzaileakF != ""):
            hornitzaileakF_list = [str(x) for x in hornitzaileakF.split(",")]
            item_hornitzaile_erab=item.objects.filter(edm_provider__in=[hornitzaileakF_list])
            usr_id_zerrenda=map(lambda x: int(x.fk_ob_user.id),item_hornitzaile_erab)
              
            paths = paths.filter(path_fk_user_id__in=usr_id_zerrenda)
       
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
                paths_ids=map(lambda x: int(x.path_id),paths)
                bozkatuenak_path_ids=map(lambda x: int(x.path_id),bozkatuenak_path_zerrenda)
                #Ordena mantentzen du??                                                                                          
                paths=paths.filter(path_id__in=bozkatuenak_path_ids)##PROBATU order_by erabiltzen! agian azkarragoa                

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
    
    
    #Datu-basetik filtro aukerak lortu
    #Datu-baseko hornitzaileak lortu
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)
    
    #Datu-baseko motak lortu
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)
    
    #Datu-baseko lizentziak lortu
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
    if hornitzaile_izena:
        hornitzaile = hornitzailea.objects.get(fk_user__username=hornitzaile_izena)
        return render_to_response('cross_search.html',{'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'hornitzailea':hornitzaile,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkuntzakF,'horniF':hornitzaileakF,'motaF':motakF,'ordenaF':ordenakF,'lizentziaF':lizentziakF,'besteaF':besteakF},context_instance=RequestContext(request))
    else:
        
        return render_to_response('cross_search.html',{'nireak':nireak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkuntzakF,'horniF':hornitzaileakF,'motaF':motakF,'ordenaF':ordenakF,'lizentziaF':lizentziakF,'besteaF':besteakF},context_instance=RequestContext(request))

def nabigazioa_hasi(request):
    
    #print "nabigazioa_hasi"
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
        pathqrUrl="http://ondarebideak.dss2016.eu/nabigazioa_hasi?path_id="+str(path_id)
        itemqrUrl="http://ondarebideak.dss2016.eu/erakutsi_item?id="+str(item_id)
        
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
          
            autoplaypages.append(berria)
                      
        #Bestela TTSarekin 1.goa errepikatzen da
        autoplaypages.pop(0)

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
        offset=1 
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
      
        non="fitxaE"
        return render_to_response('nabigazio_item_berria.html',{'non':non,"mlt":mlt,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'offset':offset,'autoplay':autoplay,'autoplaypage':autoplaypage,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))
    
 
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
 
    non="fitxaE"
    return render_to_response('nabigazio_item_berria.html',{'non':non,"mlt":mlt,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'pathqrUrl':pathqrUrl,'itemqrUrl':itemqrUrl,'autoplay':autoplay,'hasieraBakarra':hasieraBakarra,'momentukoPatha':momentukoPatha,'botoKopuruaPath':botoKopuruaPath,'botoKopuruaItem':botoKopuruaItem,'botatuDuPath':botatuDuPath,'botatuDuItem':botatuDuItem,'path_id':path_id,'node_id':item_id,'path_nodeak': nodes,'momentukoNodea':momentukoNodea,'momentukoItema':momentukoItema,'hurrengoak':hurrengoak,'aurrekoak':aurrekoak},context_instance=RequestContext(request))

def nabigatu(request):
     
    
    path_id=request.GET['path_id']
    item_id=request.GET['item_id']
   
    if 'autoplay' in request.GET:
        autoplay=request.GET['autoplay']
    else:
        autoplay='0'
        
    if 'offset' in request.GET:
        offset=request.GET['offset']
    

    '''
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
    '''
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


    if(autoplay == '1'):
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
    '''
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
    elif(hasieraNodoak.count()==1):       
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
        hasieraBakarra=1
    else:
        hasieraBakarra=0       
        hurrengoak_list=map(lambda x: x.fk_item_id.id,list(hasieraNodoak))
    '''    
    ##NABIGAZIOAN ALDAKETAK
    if(hurrengoak != ""):
        hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
        
    else:
        momentukoId=momentukoNodea.fk_item_id.id
        bilatuUrl = 'nabigatu?path_id='+path_id_str+'&item_id='+str(momentukoId)
        indexa=autoplaypages.index(bilatuUrl)  
        indexa=int(indexa)+1
        if(indexa<len(autoplaypages)):
            hurrengoUrl=autoplaypages[indexa]
        else:
            hurrengoUrl=""


        if (hurrengoUrl != ""):
                    
            hurrengoID_str=hurrengoUrl.split("item_id=")    
            hurrengoak=hurrengoID_str[1]
            hurrengoak_list=map(lambda x: int(x),hurrengoak.split(","))
     
             
        else:
            #Lehen egiten zena egin
            if(hasieraNodoak.count()==1):
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
    """Login function. 
    BUG: the workspace is not shown until page is reloaded once logged in."""
    #!! Workspace bat sortu
    #Datu-basean: workspace eta usr_workspace taula eguneratu behar dira
    logina=LoginForm(request.POST)
    # return render_to_response('logina.html',{'logina':logina},context_instance=RequestContext(request))
    if logina.is_valid():
        login_egin_(request)
        return render_to_response('ajax/ajax_login.html',{'mezua':_("Ongi etorri OndareBideak sistemara")},context_instance=RequestContext(request))
    else:
        logina=LoginForm()
        #return render_to_response('logina.html',{'logina':logina},context_instance=RequestContext(request))

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
            mezua=_("Hornitzailearen izena:")+str(request.user.username)+".\n"+_("OAI Url-a")+str(baseurl)+"\n"+_("Bidali mezua hornitzaileari: ")+str(request.user.email)
            send_mail('OndareBideak - Itemak inportatzeko eskaera', mezua, 'ondarebideak@elhuyar.com',['ondarebideak@elhuyar.com'], fail_silently=False)
            return render_to_response('base.html',{'mezua':_("Zure eskaera jaso dugu. Itemen bilketa prest dagoenean jasoko duzu posta elektroniko bat.")},context_instance=RequestContext(request))
           
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
                    return render_to_response('base.html',{'mezua':_("OndareBideak sisteman Erregistratu zara. Momentu honetan erabiltzaile arrunt bezala zaude erregistratuta. Hornitzaile izateko eskaera bideratuta dago. Zure posta elektronikoan mezu bat jasoko duzu hornitzaile izateko baimena eskuratzen duzunean. Edozein zalantza jarri gurekin kontaktuan: ondarebideak@elhuyar.com")},context_instance=RequestContext(request)) 
                else:
                    return render_to_response('base.html',{'mezua':_("OndareBideak sisteman Erregistratu zara")},context_instance=RequestContext(request))
   
        else:
            #return render_to_response("izena_eman.html",{"bilaketa":bilaketa_form,"erabiltzailea":erabiltzailea_form},context_instance=RequestContext(request))
            return render_to_response("erregistratu.html",{"erabiltzailea_form":erabiltzailea_form},context_instance=RequestContext(request))
    return render_to_response("erregistratu.html",{"erabiltzailea_form":erabiltzailea_form},context_instance=RequestContext(request))

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
            mezua=_("Hornitzailearen izena:")+str(hornitzaile_izena)+".\n"+_("Ondorengoa egin datu-basean:")+" update auth_user_groups set group_id=3 where user_id="+str(erabiltzailea.id)+"\n"+_("Bidali mezua hornitzaileari: ")+str(erabiltzailea.email)
            send_mail('OndareBideak - Hornitzaile izateko eskaera', mezua, 'ondarebideak@elhuyar.eus',['ondarebideak@elhuyar.eus'], fail_silently=False)
            
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
                return render_to_response('base.html',{'mezua':_("Zure erabiltzaile Perfila eguneratu duzu")},context_instance=RequestContext(request))
   
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
                return render_to_response('base.html',{'mezua':_("Zure Pasahitza aldatu da")},context_instance=RequestContext(request))
   
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
        
        return render_to_response('base.html',{'mezua':_("Kultur Itema ezabatu da")},context_instance=RequestContext(request))
    
 
def ezabatu_ibilbidea(request):
    if 'id' in request.GET:
        id=request.GET['id']
        #Ibilbidea ezabatu
        path.objects.filter(id=id).delete()
        
        #votes_item
        votes_path.objects.filter(path__id=id).delete()
        #itemComment
        pathComment.objects.filter(patha__id=id).delete()
        
        
        return render_to_response('base.html',{'mezua':_("Ibilbidea ezabatu da")},context_instance=RequestContext(request))
    

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
            
    
    return render_to_response('editatu_ibilbidea.html',{'momentukoPatha':ibilbidea,'path_id':id,'path_nodeak': nodes, 'path_titulua': titulua,'path_gaia':gaia, 'path_deskribapena':deskribapena, 'path_irudia':irudia},context_instance=RequestContext(request))



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
            
    titulua=item_tupla.dc_title
    herrialdea=item_tupla.edm_country
    hizkuntza=item_tupla.dc_language
    kategoria=item_tupla.dc_type
    eskubideak=item_tupla.edm_rights
    urtea=item_tupla.edm_year 
    viewAtSource=item_tupla.edm_isshownat
    irudia=item_tupla.ob_thumbnail
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
    #print "item.html deitu baino lehen"
    
    non="erakutsi_item"

    return render_to_response('item_berria.html',{"non":non,"comment_form": comment_form, "comment_parent_form": comment_parent_form,"comments": comments,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'botoKopurua':botoKopurua,'item':item_tupla,'momentukoItema':item_tupla,'id':id,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDu},context_instance=RequestContext(request))    




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
    irudia=item_tupla.ob_thumbnail
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
        non="erakutsi_item"
        return render_to_response('item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopurua':botoKopuruaItem,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    

    
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
    irudia=item_tupla.ob_thumbnail
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
        non="erakutsi_item"
        return render_to_response('item_berria.html',{'mlt':mlt,"non":non,'itemPaths':itemPaths,'qrUrl':qrUrl,'mlt':mlt,'botoKopurua':botoKopuruaItem,'item':item_tupla,'momentukoItema':item_tupla,'id':item_id,'titulua':titulua,'herrialdea':herrialdea, 'hizkuntza':hizkuntza,'kategoria':kategoria,'eskubideak':eskubideak, 'urtea':urtea, 'viewAtSource':viewAtSource, 'irudia':irudia, 'hornitzailea':hornitzailea,'botatuDu':botatuDuItem},context_instance=RequestContext(request))    


def editatu_itema(request):
     
    #Hasieran, Formularioa kargatzerakoan hemen'botoKopurua':botoKopurua sartuko da
    if 'id' in request.GET: 
        
        item_id=request.GET['id']
    
        
    itema=ItemEditatuForm(request.POST, request.FILES)
    
    #Editatu botoia sakatzerakoan hemendik sartuko da eta POST bidez bidaliko dira datuak
    #if itema.is_valid():
    if request.POST:
        print "IS VALID"
        erabiltzailea=request.user
        irudi_izena_random =randomword(10);
        
        #azken_id = item.objects.latest('id').id
        #azken_id += 1
        item_id=request.POST['hidden_Item_id']
       
        
        dc_title=request.POST['titulua']
        dc_creator=request.POST['sortzailea']
        #uri="uri_"+ str(item_id)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['lizentzia']
        edm_country=request.POST['herrialdea']
        edm_type =request.POST['mota']
        edm_isshownat=request.POST['jatorrizkoa']
        dc_date=request.POST['data']
        
        irudia_url=""
        user_id=request.user.id
        #OB_THUMBNAIL
        if(request.FILES.get('irudia')):
        
            #edm_object=request.FILES['irudia'].name 
            fileObject= request.FILES.get('irudia')
            fname, fext = os.path.splitext(fileObject.name)
            fileName='item_img_'+str(user_id)+'_'+randomword(5)+fext
            irudia_url=MEDIA_URL+str(fileName)#izen berekoak gainidatzi egingo dira bestela
        
        #EDM_OBJECT
        if(request.FILES.get('objektua')): 
            fileObject2= request.FILES.get('objektua')
            fname2, fext2 = os.path.splitext(fileObject2.name)
            objektufileName='item_obj_'+str(user_id)+'_'+randomword(5)+fext2
            objektu_url=MEDIA_URL+str(objektufileName)#izen berekoak gainidatzi egingo dira bestela
        
        else:
            objektu_url=""
        
        '''
        #HIZKUNZA 
        dc_language=request.POST['hizkuntza']

        if(dc_language=="1"):
            dc_language="eu"
            edm_language="eu"
        elif(dc_language=="2"):
            dc_language="es"
            edm_language="es"            
        else:
            dc_language="en"
            edm_language="en"
        '''
        ob_language=''
        #Hizkuntza kontrola
        if 'eu' in request.POST:
            ob_language="eu"
        if 'es' in request.POST:
            ob_language=ob_language +" es"
        if 'en' in request.POST:
            ob_language=ob_language +" en"
        
        
        '''
        AMAIA:    
            edm:type eremuan bost balore besterik ezin dira eman eta letra larriz: "​TEXT, IMAGE, SOUND, VIDEO, 3D"
            dc:type eremuan berriz, librea da, printzipioz, nahiz eta komenigarria izan bertan agertzen diren datua "vocabulario controlado" batetik hartzea. 

            Nik edm:type erakutsiko nuke. Bertan agertzen den informazioa normalizatua egon beharko luke. Hutsik baldin badago eta dc:type ordea beteta, 
            dc:type-koa edm:type-n erakutsi, bai, letra txikiz. Ez dago ondo baina erabiltzaileei ez zaie inporta. Hala ere, guretzat argi izan behar dugu eta 
            ez nahasi edm eta dc, batez ere Europeanara jo nahiko bagenu edm izango bailitzake erabili beharreko eremua. Ez dakit irtenbide hau egokia den (nahastearena diot,...). 
        
        '''
        #MOTA
        if(edm_type=="1"):
            edm_type="TEXT"        
        elif(edm_type=="2"):
            edm_type="VIDEO"           
        elif(edm_type=="3"):
            edm_type="IMAGE"       
        elif(edm_type=="3"):
            edm_type="SOUND"           
        else:
            edm_type="3D"
            
            
        '''
        
        Public Domain Mark    <edm:rights rdf:resource="http://creativecommons.org/publicdomain/mark/1.0/"/
Out of copyright - non commercial re-use    <edm:rights rdf:resource="http://www.europeana.eu/rights/out-of-copyright-non-commercial/"/>
CC0    <edm:rights rdf:resource="http://creativecommons.org/publicdomain/zero/1.0/"/>
CC-BY    <edm:rights rdf:resource="http://creativecommons.org/licenses/by/4.0/"/>
CC-BY-SA    <edm:rights rdf:resource="http://creativecommons.org/licenses/by-sa/4.0/"/>
CC-BY-ND    <edm:rights rdf:resource="http://creativecommons.org/licenses/by-nd/4.0/"/>
CC-BY-NC    <edm:rights rdf:resource="http://creativecommons.org/licenses/by-nc/4.0/"/>
CC-BY-NC-SA    <edm:rights rdf:resource="http://creativecommons.org/licenses/by-nc-sa/4.0/"/>
CC-BY-NC-ND    <edm:rights rdf:resource="http://creativecommons.org/licenses/by-nc-nd/4.0/"/>
Rights Reserved - Free Access    <edm:rights rdf:resource="http://www.europeana.eu/rights/rr-f/"/>
Rights Reserved - Paid Access    <edm:rights rdf:resource="http://www.europeana.eu/rights/rr-p/"/>
Orphan Work    <edm:rights rdf:resource="http://www.europeana.eu/rights/orphan-work-eu/"/>
Unknown    <edm:rights rdf:resource="http://www.europeana.eu/rights/unknown/"/>
        '''
        #LIZENTZIA
        if(edm_rights=="1"):
            #Public Domain Mark
            edm_rights="http://creativecommons.org/publicdomain/mark/1.0/"  
        elif(edm_rights=="2"):
            #Out of copyright - non commercial re-use
            edm_rights="http://www.europeana.eu/rights/out-of-copyright-non-commercial/"
        elif(edm_rights=="3"):
            #CC0
            edm_rights="http://creativecommons.org/publicdomain/zero/1.0/"
        elif(edm_rights=="4"):
            #CC-BY 
            edm_rights="http://creativecommons.org/licenses/by/4.0/"
        elif(edm_rights=="5"):
            #CC-BY-SA 
            edm_rights="http://creativecommons.org/licenses/by-sa/4.0/"
        elif(edm_rights=="6"):
            #CC-BY-ND
            edm_rights="http://creativecommons.org/licenses/by-nd/4.0/"
        elif(edm_rights=="7"):
            #CC-BY-NC
            edm_rights="http://creativecommons.org/licenses/by-nc/4.0/"
        elif(edm_rights=="8"):
            #CC-BY-NC-SA
            edm_rights="http://creativecommons.org/licenses/by-nc-sa/4.0/"
        elif(edm_rights=="9"):
            #CC-BY-NC-ND
            edm_rights="http://creativecommons.org/licenses/by-nc-nd/4.0/"
        elif(edm_rights=="10"):
            #Rights Reserved - Free Access 
            edm_rights="http://www.europeana.eu/rights/rr-f/"
        elif(edm_rights=="11"):
            #Rights Reserved - Paid Access
            edm_rights="http://www.europeana.eu/rights/rr-p/"
        elif(edm_rights=="12"):
            #Unknown
            edm_rights="http://www.europeana.eu/rights/orphan-work-eu/"
        else:
            #Unknown
            edm_rights="http://www.europeana.eu/rights/unknown/"
        #username-a ez da errepikatzen datu-basean, beraz, id bezala erabili dezakegu 
        #dc_creator= request.user.username # ondoren logeatutako erabiltzailea jarri
        if dc_creator =="":
            dc_creator="herritarra"
        
        item_db=item.objects.get(id=item_id)
        edm_provider= item_db.edm_provider
        uri =item_db.uri
        edm_year=item_db.edm_year
        #Gaurko data hartu (??)
        #dc_date=datetime.datetime.now()
        #edm_year=datetime.datetime.now()
        #dc_date=item_db.dc_date
        #edm_year=item_db.edm_year
        
       
        
        
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
       
        
        #OB_THUMBNAIL
        if(irudia_url!=""):
            #Irudia igo
            ob_thumbnail= fileName
            handle_uploaded_file(request.FILES['irudia'],ob_thumbnail)
            
            item.objects.filter(id=item_id).update(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,ob_language=ob_language, edm_language=ob_language,ob_thumbnail=irudia_url,edm_country=edm_country)
            
            #Item-a duten Ibilbideko nodoen argazkia ALDATU. node TAULAN, fk_item_id ALDAGAIA =item_id
            irudia_update=MEDIA_URL+ob_thumbnail            
            node.objects.filter(fk_item_id=item_id).update(paths_thumbnail=irudia_update)

        else:
            #Datu-basean irudi zaharra mantendu
            item_tupla = item.objects.get(pk=item_id)
            irudia_url=item_tupla.ob_thumbnail
            #item.objects.filter(id=item_id).update(fk_ob_user=erabiltzailea,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,edm_isshownat=edm_isshownat,dc_creator=dc_creator, edm_provider=edm_provider,edm_type=edm_type,dc_date=dc_date,edm_year=edm_year,ob_language=ob_language, edm_language=ob_language,ob_thumbnail=irudia_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
   			#erabiltzaile ez aldatu
            item.objects.filter(id=item_id).update(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,edm_isshownat=edm_isshownat,dc_creator=dc_creator, edm_provider=edm_provider,edm_type=edm_type,dc_date=dc_date,edm_year=edm_year,ob_language=ob_language, edm_language=ob_language,ob_thumbnail=irudia_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
   
        #EDM_OBJECT
        if(objektu_url!=""):
            #Objektua igo
            edm_object= objektufileName
            handle_uploaded_file(request.FILES['objektua'],edm_object)
            item.objects.filter(id=item_id).update(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,dc_creator=dc_creator, edm_provider=edm_provider,dc_date=dc_date,ob_language=ob_language, edm_language=ob_language,edm_object=objektu_url,edm_country=edm_country)
            
            #Item-a duten Ibilbideko nodoen objektua ALDAT? node TAULAN, fk_item_id ALDAGAIA =item_id
            #objektua_update=MEDIA_URL+edm_object              
            #node.objects.filter(fk_item_id=item_id).update(objektua=objektua_update)

        else:
            #Datu-basean objektu zaharra mantendu
            item_tupla = item.objects.get(pk=item_id)
            objektu_url=item_tupla.edm_object
            #item.objects.filter(id=item_id).update(fk_ob_user=erabiltzailea,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,edm_isshownat=edm_isshownat,dc_creator=dc_creator, edm_provider=edm_provider,edm_type=edm_type,dc_date=dc_date,edm_year=edm_year,ob_language=ob_language, edm_language=ob_language,edm_object=objektu_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
            #erabiltzaile ez aldatu
            item.objects.filter(id=item_id).update(uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_rights=dc_rights,edm_rights=edm_rights,edm_isshownat=edm_isshownat,dc_creator=dc_creator, edm_provider=edm_provider,edm_type=edm_type,dc_date=dc_date,edm_year=edm_year,ob_language=ob_language, edm_language=ob_language,edm_object=objektu_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude)
   
        
        
        
        
        
        #item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        #update_index.Command().handle(age=1)
        non="fitxaE"
        item_obj=item.objects.get(id=item_id)
        return render_to_response('base.html',{'non':non,'item':item_obj,'mezua':"itema editatu da",'nondik':"editatu_itema",'hizkuntza':ob_language,'irudia':irudia_url,'titulua':dc_title,'herrialdea':edm_country,'hornitzailea':edm_provider,'eskubideak':edm_rights,'urtea':dc_date,'geoloc_latitude':latitude,'geoloc_longitude':longitude},context_instance=RequestContext(request))
    
        #return render_to_response('base.html',{'non':non,'mezua':"itema editatu da",'nondik':"editatu_itema",'hizkuntza':dc_language,'irudia':irudia_url,'titulua':dc_title,'herrialdea':edm_country,'hornitzailea':edm_provider,'eskubideak':edm_rights,'urtea':dc_date,'geoloc_latitude':latitude,'geoloc_longitude':longitude},context_instance=RequestContext(request))
    
    else:
        #Hasieran hemendik sartuko da eta Datu-basetik kargatuko dira itemaren datuak
        item_tupla = item.objects.get(pk=item_id)
        titulua=item_tupla.dc_title
        deskribapena=item_tupla.dc_description
        gaia=item_tupla.dc_subject
        herrialdea=item_tupla.edm_country
        data=item_tupla.dc_date

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
            
        mota=item_tupla.edm_type
        if("TEXT" in mota):
            print "bai, TEXT da"
            mota=1
            mot="TEXT"
        elif("VIDEO" in mota):
            mota=2
            mot="VIDEO"
        elif("IMAGE" in mota):
            mota=3
            mot="IMAGE"
        else:
            #SOUND
            mota=4
            mot="SOUND"
 
        lizentzia=item_tupla.edm_rights
        if("http://creativecommons.org/publicdomain/mark/1.0/" in lizentzia):
        
            lizentzia=1
            liz="Public Domain Mark"
        elif("http://www.europeana.eu/rights/out-of-copyright-non-commercial/" in lizentzia):
            lizentzia=2
            liz="Out of copyright - non commercial re-use"
        elif("http://creativecommons.org/publicdomain/zero/1.0/" in lizentzia):
            lizentzia=3
            liz="CC0"
        elif("http://creativecommons.org/licenses/by/4.0" in lizentzia):
            lizentzia=4
            liz="CC-BY"
        elif("http://creativecommons.org/licenses/by-sa/4.0/" in lizentzia):
            lizentzia=5
            liz="CC-BY-SA"
        elif("http://creativecommons.org/licenses/by-nd/4.0/" in lizentzia):
            lizentzia=6
            liz="CC-BY-ND"
        elif("http://creativecommons.org/licenses/by-nc/4.0/" in lizentzia):
            lizentzia=7
            liz="CC-BY-NC" 
        elif("http://creativecommons.org/licenses/by-nc-sa/4.0/" in lizentzia):
            lizentzia=8
            liz="CC-BY-NC-SA"
        elif("http://creativecommons.org/licenses/by-nc-nd/4.0/" in lizentzia):
            lizentzia=9
            liz="CC-BY-NC-ND"
        elif("http://www.europeana.eu/rights/rr-f/" in lizentzia):
            lizentzia=10
            liz="Rights Reserved - Free Access"
        elif("http://www.europeana.eu/rights/rr-p/" in lizentzia):
            lizentzia=11
            liz="Rights Reserved - Paid Access"
        elif("http://www.europeana.eu/rights/orphan-work-eu/" in lizentzia):
            lizentzia=12
            liz="Orphan Work"           
        else:
            #http://www.europeana.eu/rights/unknown/
            lizentzia=13
            liz="Unknown"
            
        ob_language=item_tupla.ob_language
        if('eu' in ob_language):
            eu=True
        else:
            eu=False
        if('es' in ob_language):
            es=True
        else:
            es=False
        if('en' in ob_language):
            en=True
        else:
            en=False
        
        #kategoria=item_tupla.dc_type
        eskubideak=item_tupla.dc_rights
        
        urtea=item_tupla.dc_date 
        viewAtSource=item_tupla.edm_isshownat
        hornitzailea=item_tupla.edm_provider
        sortzailea=item_tupla.dc_creator
        gaia = item_tupla.dc_subject
        herrialdea =item_tupla.edm_country
        jatorrizkoa =item_tupla.edm_isshownat
        irudia=item_tupla.ob_thumbnail
        
        geoloc_longitude=item_tupla.geoloc_longitude
        geoloc_latitude=item_tupla.geoloc_latitude
        
        non="itema_editatu" #Mapako baimenak kontrolatzeko erabiliko da hau
       
        
        itema=ItemEditatuForm(initial={'hidden_Item_id':item_id,'titulua': titulua, 'deskribapena': deskribapena, 'gaia':gaia,'eskubideak':eskubideak, 'mota':mota, 'herrialdea':herrialdea , 'jatorrizkoa': jatorrizkoa, 'sortzailea':sortzailea,'gaia':gaia, 'lizentzia':lizentzia, 'data':data,'eu':eu,'es':es,'en':en})
        return render_to_response('editatu_itema.html',{"non":non,'geoloc_longitude':geoloc_longitude,'geoloc_latitude':geoloc_latitude,'item':item_tupla,'itema':itema,'id':item_id,'irudia':irudia,'titulua':titulua,'herrialdea':herrialdea,'hornitzailea':hornitzailea,'eskubideak':eskubideak,'urtea':urtea,'hizkuntza':hizk,'viewAtSource':viewAtSource,'mota':mot,'liz':liz},context_instance=RequestContext(request))


def handle_uploaded_file(f,izena):
    #Irudi fitxategia /uploads direktoriora igotzen du
    with open(MEDIA_ROOT+'/'+izena, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

'''
def nire_itemak_erakutsi(request):
    
    userName=request.user.username
    userID=request.user.id
    itemak=[]
    itemak = item.objects.filter(fk_ob_user__id=userID).order_by('-dc_date')
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
    bilaketa_filtroak=1
    
    return render_to_response('nire_itemak.html',{'non':non,'itemak':itemak,'bilaketa_filtroak':bilaketa_filtroak},context_instance=RequestContext(request))
  
''' 

def nire_itemak_erakutsi(request):
    
    userName=request.user.username
    userID=request.user.id
    
    #ITEMAK
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
    
    #IBILBIDEAK
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
    
     
        
    
    #Datu-baseko hornitzaileak lortu                                                                                             
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)

    #Datu-baseko motak lortu                                                                                                     
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)

    #Datu-baseko lizentziak lortu                                                                                                
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))

    non="fitxaE"
    
    z='i' 
    paths=[]
    bilaketa_filtroak=1
    galdera=''
    hizkuntza='eu'
    hizkF=''
    horniF=''
    motaF=''
    ordenaF=''
    lizentziaF=''
    besteaF=''
    search_models_items=[item]
    
    items = SearchQuerySet().all().filter(item_user_id=userID).models(*search_models_items)
    
    '''
    search_models_paths=[path]
    paths = SearchQuerySet().all().filter(path_fk_user_id=userID).models(*search_models_paths)
    
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
    
    ''' 
    
    
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
        
    nireak='1'
    return render_to_response('cross_search.html',{'nireak':nireak,'non':non,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))
      



'''
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
   
'''

def nire_ibilbideak_erakutsi(request):

    userName=request.user.username
    userID=request.user.id
    
    #ITEMAK
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
    
    #IBILBIDEAK
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
    
    #Datu-baseko hornitzaileak lortu                                                                                             
    db_hornitzaileak=map(lambda x: x['edm_provider'],item.objects.values('edm_provider').distinct().order_by('edm_provider'))
    db_hornitzaileak_text ="_".join(db_hornitzaileak)

    #Datu-baseko motak lortu                                                                                                     
    db_motak=map(lambda x: x['edm_type'],item.objects.values('edm_type').distinct())
    db_motak_text ="_".join(db_motak)

    #Datu-baseko lizentziak lortu                                                                                                
    db_lizentziak=lizentzia.objects.all()
    db_lizentziak_text ="_".join(map(lambda x: x.url,db_lizentziak))
    
    
    z='p'
    if request.GET.get('z'):
        z = request.GET.get('z')    
  
    
    items=[]
    bilaketa_filtroak=1
    galdera=''
    hizkuntza='eu'
    hizkF=''
    horniF=''
    motaF=''
    ordenaF=''
    lizentziaF=''
    besteaF=''
    search_models_paths=[path]
    #search_models_items=[item]
    #items = SearchQuerySet().all().filter(item_user_id=userID).models(*search_models_items)

    paths = SearchQuerySet().all().filter(path_fk_user_id=userID).models(*search_models_paths)
    
  
    
     
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
    '''    
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
    '''
    nireak="1"
    return render_to_response('cross_search.html',{'nireak':nireak,'non':non,'ibilbide_bozkatuenak':ibilbide_bozkatuenak,'eguneko_ibilbideak':eguneko_ibilbideak,'azken_ibilbideak':azken_ibilbideak,'item_bozkatuenak':item_bozkatuenak,'eguneko_itemak':eguneko_itemak,'azken_itemak':azken_itemak,'db_hornitzaileak_text':db_hornitzaileak_text,'db_hornitzaileak':db_hornitzaileak,'db_motak_text':db_motak_text,'db_motak':db_motak,'db_lizentziak_text':db_lizentziak_text,'db_lizentziak':db_lizentziak,'z':z,'items':items,'paths':paths,'bilaketa_filtroak':bilaketa_filtroak,'bilaketaGaldera':galdera,'radioHizkuntza':hizkuntza,'hizkF':hizkF,'horniF':horniF,'motaF':motaF,'ordenaF':ordenaF,'lizentziaF':lizentziaF,'besteaF':besteaF},context_instance=RequestContext(request))   
    
    
 
    
def itema_gehitu(request):
    
    
    itema=ItemGehituForm(request.POST, request.FILES)
    print itema.errors 
    if itema.is_valid():
        #Datu-basean item-a gehitu
        irudi_izena_random =randomword(10); 
        erabiltzailea=request.user
        dc_title=request.POST['titulua']
        dc_creator=request.POST['sortzailea']
        uri="uri_interface_"+ str(irudi_izena_random)
        dc_description=request.POST['deskribapena']
        dc_subject=request.POST['gaia']
        edm_country=request.POST['herrialdea']
        edm_isshownat=request.POST['jatorrizkoa']
        dc_rights=request.POST['eskubideak']
        edm_rights=request.POST['lizentzia']
        dc_date=request.POST['data']
        irudia_url=""
        user_id=request.user.id
        
       
        if(request.FILES.get('irudia')):
        
        	#IRUDIA (ob_thumbnail)
             
            fileObject= request.FILES.get('irudia')
            fname, fext = os.path.splitext(fileObject.name)
            fileName='item_img_'+str(user_id)+'_'+randomword(5)+fext
            irudia_url=MEDIA_URL+str(fileName)#izen berekoak gainidatzi egingo dira bestela
      	
      	if(request.FILES.get('objektua')):
      		#OBJEKTUA (edm_object)
      		objektua=request.FILES.get('objektua')
      		fname2, fext2 = os.path.splitext(objektua.name)
      		objectfileName='item_obj_'+str(user_id)+'_'+randomword(5)+fext2
      		objektu_url=MEDIA_URL+str(objectfileName)#izen berekoak gainidatzi egingo dira bestela
      	
      		
      		
        #dc_language=request.POST['hizkuntza']
        #edm_language=request.POST['hizkuntza']
        '''
        if(dc_language=="1"):
            dc_language="eu"
            edm_language="eu"
        elif(dc_language=="2"):
            dc_language="es"
            edm_language="es"            
        else:
            dc_language="en"
            edm_language="en"
        '''
        ob_language=""
        #Hizkuntza kontrola
        if request.POST.get('eu'):
            ob_language="eu"
        if request.POST.get('es'):
            ob_language=ob_language +" es"
        if request.POST.get('en'):
            ob_language=ob_language +" en"
    
        
        edm_type=request.POST['mota']
        if(edm_type=="4"):
            edm_type="SOUND"        
        elif(edm_type=="2"):
            edm_type="VIDEO"         
        elif(edm_type=="3"):
            edm_type="IMAGE"
           
        elif(edm_type=="5"):
            edm_type="3D"        
        else:
            edm_type="TEXT"
         
        
        #LIZENTZIA
        if(edm_rights=="1"):
            #Public Domain Mark
            edm_rights="http://creativecommons.org/publicdomain/mark/1.0/"  
        elif(edm_rights=="2"):
            #Out of copyright - non commercial re-use
            edm_rights="http://www.europeana.eu/rights/out-of-copyright-non-commercial/"
        elif(edm_rights=="3"):
            #CC0
            edm_rights="http://creativecommons.org/publicdomain/zero/1.0/"
        elif(edm_rights=="4"):
            #CC-BY 
            edm_rights="http://creativecommons.org/licenses/by/4.0/"
        elif(edm_rights=="5"):
            #CC-BY-SA 
            edm_rights="http://creativecommons.org/licenses/by-sa/4.0/"
        elif(edm_rights=="6"):
            #CC-BY-ND
            edm_rights="http://creativecommons.org/licenses/by-nd/4.0/"
        elif(edm_rights=="7"):
            #CC-BY-NC
            edm_rights="http://creativecommons.org/licenses/by-nc/4.0/"
        elif(edm_rights=="8"):
            #CC-BY-NC-SA
            edm_rights="http://creativecommons.org/licenses/by-nc-sa/4.0/"
        elif(edm_rights=="9"):
            #CC-BY-NC-ND
            edm_rights="http://creativecommons.org/licenses/by-nc-nd/4.0/"
        elif(edm_rights=="10"):
            #Rights Reserved - Free Access 
            edm_rights="http://www.europeana.eu/rights/rr-f/"
        elif(edm_rights=="11"):
            #Rights Reserved - Paid Access
            edm_rights="http://www.europeana.eu/rights/rr-p/"
        elif(edm_rights=="12"):
            #Unknown
            edm_rights="http://www.europeana.eu/rights/orphan-work-eu/"
        else:
            #Unknown
            edm_rights="http://www.europeana.eu/rights/unknown/"   
           
             
        #DC_CREATOR Vs. EDM_PROVIDER       
        #dc_creator= request.user.username 
        #objektu digitalaren sortzailearen izena ipini, bestela balio lehenetsi bezala 'Herritarra' agertuko da
        if dc_creator == "":
            dc_creator="herritarra"
        
        
        #BEGIRATU EA HORNITZAILEA DEN EDO EZ. EZ BADA:herritarra balioa eman edm_providerri, bestela Hornitzailearen izena
        #erab_id=request.user.id         
        if( User.objects.filter(id=request.user.id, groups__name='hornitzailea').exists()):
            hornitzaile=hornitzailea.objects.get(fk_user=request.user)
            edm_provider=hornitzaile.izena
        else:
            edm_provider= "herritarra"
        
     	
        #Gaurko data hartu
        #dc_date=datetime.datetime.now()  
        #edm_year=datetime.datetime.now()  
       
        #ob_thumbnail
        if(irudia_url!=""):
            #Irudia igo : OB_thumbnail !!
            ob_thumbnail=fileName #izen berekoak gainidatzi egingo dira bestela
            handle_uploaded_file(request.FILES['irudia'],ob_thumbnail)
         
        #edm_object
        if(objektu_url!=""):
            #objektua igo : EDM_OBJECT !!
            edm_object=objectfileName #izen berekoak gainidatzi egingo dira bestela
            handle_uploaded_file(request.FILES['objektua'],edm_object)    
            
         
        
        latitude=0.0
        longitude=0.0
        if request.POST['latitude']:
            latitude=request.POST['latitude']
        if request.POST['longitude']:
            longitude=request.POST['longitude']
   
   
        print "ITEMA DATU_BASEAN SARTU AURRETIK"
   		
        item_berria = item(fk_ob_user=erabiltzailea,uri=uri, dc_title=dc_title, dc_description=dc_description,dc_subject=dc_subject,dc_date=dc_date,edm_year=dc_date,dc_rights=dc_rights,edm_rights=edm_rights,edm_isshownat=edm_isshownat,dc_creator=dc_creator, edm_provider=edm_provider,edm_type=edm_type,ob_language=ob_language, edm_language=ob_language,edm_object=objektu_url,edm_country=edm_country,geoloc_longitude=longitude,geoloc_latitude=latitude,ob_thumbnail=irudia_url)
        item_berria.save()   
         
        #Haystack update_index EGIN berria gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
        #update_index.Command().handle(age=1)
         
        return render_to_response('base.html',{'mezua':"item berria gehitu da"},context_instance=RequestContext(request))
    else:
    
    	print "ELSE"
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



    
    
	 
def ajax_path_edizio_aukerak_aldatu(request):
    
    #AJAX bidez bidali dira parametroak
    path_id=request.POST['pathId']
    acces_zbk=request.POST['acces']   

    path_old = path.objects.get(id=path_id)
    
    path_eguneratua = path(id=path_id,
    					   fk_user_id=path_old.fk_user_id,
    					   uri=path_old.uri,
    					   dc_title=path_old.dc_title,
    					   dc_subject=path_old.dc_subject,
    					   dc_description=path_old.dc_description,
    					   acces=acces_zbk,
    					   paths_thumbnail=path_old.paths_thumbnail,
    					   tstamp=path_old.tstamp,
    					   creation_date=path_old.creation_date,
    					   proposatutakoa=path_old.proposatutakoa,
    					   egunekoa=path_old.egunekoa,
    					   language=path_old.language
    					   )
        
    
    path_eguneratua.save()
    
    request_answer=1
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')
    


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

def ajax_lortu_eguneko_itema(request):
    
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
    
    #0: unknown error or itema errepikatua; else: workspace item created;
    #fk_usr_id=1
    
    print "ajax_workspace_item_gehitu"
        
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
        print "ajax_workspace_item_gehitu --",thumbnail
    
        #workspace eta item objektuak pasa!
        #workspace=workspace.objects.get(fk_usr_id__id=request.user.id)   
        workspacea=workspace.objects.get(fk_usr_id=request.user)       
        itema=item.objects.get(id=item_id)
        
        #Begiratu ea itema workspace-an jadanik badagoen
        wscount=workspace_item.objects.filter(fk_item_id=itema,fk_workspace_id = workspacea).count()
        print "COUNT"
        print wscount	
        if wscount==0:     
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
        	request_answer = ws_item_berria.fk_item_id.id
        
        #else:
		#request_answer= 0
    
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
        acces = request.POST.get('acces')
       
        
        
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
    fileName='1'

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
            fname, fext = os.path.splitext(fileObject.name)
            fileName='path_img_'+str(user_id)+'_'+randomword(5)+fext
            
            #fileName=str(azken_id)+fileObject.name   
            print fileName
            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            request_answer = fileName
    

    return render_to_response('request_answer.html', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_irudia_eguneratu (request):

    #KONPONTZEKO
    request_answer= 1
    
    #import pdb
    #pdb.set_trace()
    #print request.FILES
    #print request.POST
    #print request.POST.FILES
    #print request.GET

    fileName='1'

    if request.is_ajax() and request.method == 'POST':
    
        #Irudirik igotzen ez denean errorea ez emateko beharrezko da baldintza hau jartzea
        if(request.FILES):
        
 
            fileObject= request.FILES.get('file2')
            #irudiari id-a gehitzeko
            path_id=request.POST.get('path_id_h')
            user_id=request.user.id
            fname, fext = os.path.splitext(fileObject.name)
            fileName='path_img_'+str(user_id)+'_'+randomword(5)+fext

            print 'ajax_path_irudia_eguneratu   -- '+fileName
            #fileName=str(path_id)+str(user_id)+fileObject.name
            #fileName=str(user_id)+fileObject.name
            
           
    

            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            #request_answer = path_id
    
            request_answer = fileName
    return render_to_response('request_answer.html', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


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
    
    #print "ajax_path_berria_gorde"
    request_answer= 1
  
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
        acces=request.POST.get('acces')
        
        ######paths_thumbnail=str(azken_id)+paths_thumbnail
       
        #fileObject= request.FILES.get('fileObject')
        #fileObject= request.GET.get('fileObject')
        #print fileObject
        ##
        #print "paths_thumbnail"
        #print paths_thumbnail
        if paths_thumbnail =="" or paths_thumbnail =="0":
            paths_thumbnail_url="/uploads/NoIrudiItem.png"
        else:
            #paths_thumbnail_url=MEDIA_URL+str(azken_id)+str(fk_usr_id)+paths_thumbnail
            paths_thumbnail_url=MEDIA_URL+paths_thumbnail
       
     
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
                                        language=language,
                                        acces=acces)
    
    
        path_berria.save() #AUTOMATIKOKI SOLR INDIZEA ERE EGUNERATZEN DA
        request_answer = path_berria.id  
        
        #Haystack update_index EGIN!!!
        #update_index.Command().handle()   ##ATASKATU EGITEN DA :-(  -> BAINA EGUNERATZEN DA INDIZEA
       
    return render_to_response('request_answer.xml', {'request_answer': request_answer}, context_instance=RequestContext(request), mimetype='application/xml')


def ajax_path_eguneratu(request):
    

    path_id=request.POST.get('path_id')
    #fk_usr_id=request.user.id
    dc_title=request.POST.get('dc_title')
    dc_subject=request.POST.get('dc_subject')
    dc_description=request.POST.get('dc_description')
    paths_thumbnail = request.POST.get('paths_thumbnail')
    language=request.POST.get('hizkuntza')
    acces=request.POST.get('acces')
    

    
    #erabiltzaileak ibilbidearen irudia eguneratu ez baldin badu zaharra hartu
    if paths_thumbnail=='' or paths_thumbnail =="1":
                
        patha=path.objects.get(id=path_id)      
        paths_thumbnail_url=patha.paths_thumbnail 
    
    else:  
        
        #paths_thumbnail_url=MEDIA_URL+str(path_id)+str(fk_usr_id)+paths_thumbnail     
        paths_thumbnail_url=MEDIA_URL+paths_thumbnail

    path_old=path.objects.get(id=path_id)
    fk_usr_id_old= path_old.fk_user_id
    
    proposatutakoa_old=path_old.proposatutakoa
    egunekoa_old=path_old.egunekoa
    #request.user
    path_eguneratua = path(id=path_id,
                           fk_user_id = fk_usr_id_old,
                           dc_title = dc_title,
                           dc_subject = dc_subject,
                           dc_description = dc_description,
                           paths_thumbnail = paths_thumbnail_url,
                           tstamp = timezone.now(),
                           creation_date = timezone.now(),
                           proposatutakoa = proposatutakoa_old,
                           egunekoa = egunekoa_old,
                           language=language,
                           acces=acces)
    
    
    path_eguneratua.save()
    request_answer = path_id 
        
    #Haystack update_index EGIN!!!
    #update_index.Command().handle()
    
    
    # Ibilbide honen nodoen kopia egin => node_tmp taulan
    nodes_to_cp=node.objects.filter(fk_path_id__id=path_id)
    
    #Aurretik egon daitezkeen nodoak ezabatu
    if node_tmp.objects.filter(fk_path_id__id=path_id):
        node_tmp.objects.filter(fk_path_id__id=path_id).delete()
    
    print "nodoz nodo node_tmp-n sartu"
    for node_to_cp in nodes_to_cp:
    	print "nodo bat:"
    	print node_to_cp
        tmp_entry = node_tmp(fk_item_id=node_to_cp.fk_item_id, uri=node_to_cp.uri,fk_path_id=node_to_cp.fk_path_id,
        dc_source=node_to_cp.dc_source,dc_title=node_to_cp.dc_title,dc_description=node_to_cp.dc_description,
        type=node_to_cp.type,paths_thumbnail=node_to_cp.paths_thumbnail,paths_prev=node_to_cp.paths_prev,paths_next= node_to_cp.paths_next,
        paths_start=node_to_cp.paths_start,isdeleted=node_to_cp.isdeleted,tstamp=node_to_cp.tstamp,geoloc_longitude=node_to_cp.geoloc_longitude,geoloc_latitude=node_to_cp.geoloc_latitude )
    
        tmp_entry.save()
    
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
        #dc_source=request.user.username # ??
        dc_source=itema.dc_source # ??
        dc_title=request.POST.get('dc_title')    #titulua moztuta dator
        dc_title=itema.dc_title #titulu osoa hartzeko
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

def ajax_edit_telefonoa(request):
   
   
    if request.GET:
        telefonoa = request.GET.get('telefonoa')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(telefonoa=telefonoa)
          
            response= telefonoa
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  
              
def ajax_edit_emaila(request):
   
   
    if request.GET:
        emaila = request.GET.get('emaila')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(emaila=emaila)
          
            response= emaila
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  

def ajax_edit_website(request):
   
   
    if request.GET:
        web = request.GET.get('website')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(website=web)
          
            response= web
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  
              

              
def ajax_edit_ordutegia(request):
   
   
    if request.GET:
        ordutegia = request.GET.get('ordutegia')
        user_id=request.user.id
       
        if not request.user.is_anonymous():
            
            hornitzailea.objects.filter(fk_user__id=user_id).update(ordutegia=ordutegia)
          
            response= ordutegia
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
         
        else:
            response = None
            return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request.request))  
              
  

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
       
        print "HORNITZAILE FITXAKO DESKRIBAPENA EDITATU!!!"
        print deskribapena
        
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
            user_id=request.user.id
            fileName="hornitzaile_ikonoa_img_"+str(user_id)+fileObject.name
          
            print fileName
            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            ikonoa="/uploads/"+fileName
            hornitzailea.objects.filter(fk_user__id=user_id).update(ikonoa=ikonoa)
            response=ikonoa
    
  
    return render_to_response("ajax/ajax_response.html",{"response": response},context_instance=RequestContext(request))       
       


def ajax_hornitzaile_argazkia_gorde (request):

   

    print request.FILES
    
    user_id=request.user.id
    if request.is_ajax() and request.method == 'POST':
       
        
        #Irudirik igotzen ez denean errorea ez emateko beharrezko da baldintza hau jartzea
        if(request.FILES):
        
            
            fileObject= request.FILES.get('hornitzaile_argazkia2')
           
            print fileObject
           
            username =request.user.username
            user_id=request.user.id
            
            fileName="hornitzaile_argazkia_img_"+str(user_id)+fileObject.name

            print fileName
            #handle_uploaded_file(fileObject,fileObject.name)
            handle_uploaded_file(fileObject,fileName)
            ikonoa="/uploads/"+fileName
            hornitzailea.objects.filter(fk_user__id=user_id).update(argazkia=ikonoa)
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



