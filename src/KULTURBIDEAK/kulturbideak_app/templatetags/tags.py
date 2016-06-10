from django.template.defaultfilters import stringfilter
from django import template
from settings import *
import re

from django.contrib.auth.models import Group
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False




@register.filter
def correct_float_format(value):
   return str(value).replace(',','.')



@register.filter
def correct_language_tags(value):
    
    value=value.replace('<div class=\"titulu_es\">', ' ')
    value=value.replace('</div>', ' ')
    value=value.replace('<div class=\"titulu_en\">', ' ')
    value=value.replace('</div>', ' ')
    value=value.replace('<div class=\"titulu_eu\">', ' ')
    value=value.replace('</div>',' ')
    value=value.replace('<div class=\"titulu_lg\">', ' ')
    value=value.replace('</div>',' ')
    return value



@register.filter
def choose_title_language(interfaceLang, item):
     
    titulua=item.dc_title
    titulu_es=""
    titulu_en=""
    titulu_eu=""
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 
    match_es = re.search('<div class=\"titulu_es\">(.*?)</div>', titulua)

    if match_es:
        titulu_es=match_es.group(0)
        titulu_es=titulu_es.replace("<div class=\"titulu_es\">", " ")
        titulu_es=titulu_es.replace("</div>", " ")
    else:
        titulu_es=""
        
    match_en = re.search('<div class=\"titulu_en\">(.*?)</div>', titulua)
    if match_en:
        titulu_en=match_es.group(0)
        titulu_en=titulu_en.replace("<div class=\"titulu_en\">", " ")
        titulu_en=titulu_en.replace("</div>", " ")
    else:
        titulu_en=""
    
    match_eu = re.search('<div class=\"titulu_eu\">(.*?)</div>', titulua)
    if match_eu:
        titulu_eu=match_eu.group(0)
        titulu_eu=titulu_eu.replace("<div class=\"titulu_eu\">", " ")
        titulu_eu=titulu_eu.replace("</div>", " ")
    else:
        titulu_eu=""
    
    #titulua= !!!erabaki defektuzkoa zein den eu,en,es
    if titulu_eu:
        titulua=titulu_eu
    elif titulu_es:
        titulua=titulu_es
    else:
        titulua=titulu_en
    #DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if titulua =="":
        titulua=item.dc_title
        titulua=titulua.replace("<div class=\"titulu_lg\">", " ")
        titulua=titulua.replace("</div>", " ")
        
    if interfaceLang == "eu":
         
        if titulu_eu != "":
            return titulu_eu          
        else:        
            return titulua
    if interfaceLang == "es":
        if titulu_es != "":
            return titulu_es          
        else:        
            return titulua
                
    if interfaceLang == "en":
         
        if titulu_en != "":
            return titulu_en          
        else:        
            return titulua
        
@register.filter
def choose_description_language(interfaceLang, item):
    
    deskribapena=item.dc_description
    deskribapena_es=""
    deskribapena_en=""
    deskribapena_eu=""
    #espresio erregularrak erabilita hizkuntza desberdinetako deskribapenak atera
    match_es = re.search('<div class=\"desc_es\">(.*?)</div>', deskribapena)

    if match_es:
        deskribapena_es=match_es.group(0)
        deskribapena_es=deskribapena_es.replace("<div class=\"desc_es\">", " ")
        deskribapena_es=deskribapena_es.replace("</div>", " ")
    else:
        deskribapena_es=""
        
    match_en = re.search('<div class=\"desc_en\">(.*?)</div>', deskribapena)
    if match_en:
        deskribapena_en=match_es.group(0)
        deskribapena_en=deskribapena_en.replace("<div class=\"desc_en\">", " ")
        deskribapena_en=deskribapena_en.replace("</div>", " ")
    else:
        deskribapena_en=""
    
    match_eu = re.search('<div class=\"desc_eu\">(.*?)</div>', deskribapena)
    if match_eu:
        deskribapena_eu=match_eu.group(0)
        deskribapena_eu=deskribapena_eu.replace("<div class=\"desc_eu\">", " ")
        deskribapena_eu=deskribapena_eu.replace("</div>", " ")
    else:
        deskribapena_eu=""
    
    #deskribapena= !!!erabaki defektuzkoa zein den eu,en,es
    if deskribapena_eu:
        deskribapena=deskribapena_eu
    elif deskribapena_es:
        deskribapena=deskribapena_es
    else:
        deskribapena=deskribapena_en
    #DBko deskribapenak hizkuntza kontrolik ez badu
    if deskribapena =="":
        deskribapena=item.dc_description
    
    
    if interfaceLang == "eu":
         
        if deskribapena_eu != "":
            return deskribapena_eu          
        else:        
            return deskribapena
        
    if interfaceLang == "es":
        if deskribapena_es != "":
            return deskribapena_es          
        else:        
            return deskribapena
                
    if interfaceLang == "en":
         
        if deskribapena_en != "":
            return deskribapena_en          
        else:        
            return deskribapena
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    