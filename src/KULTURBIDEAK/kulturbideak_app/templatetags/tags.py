from django.template.defaultfilters import stringfilter
from django import template
from settings import *
import re
import HTMLParser
import requests

from django.contrib.auth.models import User, Group
register = template.Library()

@register.filter
def proxyPassHttp(url):	
	return re.sub('^\s*http://','/kanpora/', url)

@register.filter
def lerroJauziakKendu(sarrera):

	return sarrera.replace("\n","");

@register.filter
def htmlEtiketakGarbitu(sarrera):

	return sarrera.replace("/<\/?[^>]+(>|$)/g", "");


@register.filter
def urlpath_exists(path):
	
	try:
		r = requests.head(path)
   		if str(r.status_code) == '404':
   			return "False"
   		else:
   			#200
   			return "True" 
   		#return r.status_code
        # returns the int of the status code. Find more at httpstatusrappers.com :)                                                       
	except requests.ConnectionError:
    	#print("failed to connect")
		return "False"




@register.filter
def is_in(id,list): 

    for item in list:       
        if int(id) == item.id:
            return 1
    
    return 0

@register.filter
def get_item_image(item): 
    img=item    
    return img


@register.filter
def cut_karrusel_text(input): 
    out=input[:150]
    if len(input) > len(out): 
        out=out+"..."
    return out


@register.filter
def add_ekm_prefix_to_desc(value): 
    value=value.replace('="/ImgsAuna/','="http://www.euskomedia.org/ImgsAuna/')
    value=value.replace('href="/aunamendi/', 'href="http://www.euskomedia.org/aunamendi/')
    
    return value

@register.filter
def get_substring(value): 
    short_value=value[:100]
    return short_value
    
@register.filter
def get_substring_150(value): 
    short_value=value[:150]
    return short_value

@register.filter
def convert_newline2br(value): 
    value=value.replace('\n','<br/>')    
    return value

@register.filter
def clean_http_prefix(value): 
    return value.replace('http://www.http://','http://')

@register.filter
def format_html(value): 
    html_parser = HTMLParser.HTMLParser()
    first = html_parser.unescape(value)
    return html_parser.unescape(first)

@register.filter
def replace_quotes(value): 
    return value.replace('"',"'")


@register.filter(name='hornitzailea_da')
def hornitzailea_da(path_user_id):
   
    path_user_id_int=int(path_user_id)
    erabiltzailea=User.objects.get(id=path_user_id_int)
    
    hornitzaileGroup = Group.objects.get(name='hornitzailea')
    return True if hornitzaileGroup in erabiltzailea.groups.all() else False



@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter
def ob_language_errep_kendu(value):

    value_array=value.split(' ')
    value_clean=set(value_array)
    value_str=' '.join(value_clean)

    return value_str
    

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
def correct_wikification_url_tags(value):
    
    value=value.replace('http://es.dbpedia.org/resource/', 'https://es.wikipedia.org/wiki/')
    value=value.replace('http://dbpedia.org/resource/', 'https://en.wikipedia.org/wiki/')


    return value

@register.filter
def choose_title_language(interfaceLang, item):
    
    if item is None:
        return ""
     
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
        titulu_en=match_en.group(0)
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
    elif interfaceLang == "es":
        if titulu_es != "":
            return titulu_es          
        else:        
            return titulua
                
    elif interfaceLang == "en":
         
        if titulu_en != "":
            return titulu_en          
        else:        
            return titulua
    else:
        return titulua
            
@register.filter       
def choose_karrusel_desk_language(interfaceLang, berria):

	desc_eu=berria.desk_eu
	desc_es=berria.desk_es
	desc_en=berria.desk_en
	desc_fr=berria.desk_fr
    
	if interfaceLang == "eu": 
		return desc_eu          
	elif interfaceLang == "es":
		if desc_es != "":
			return desc_es          
		else:        
			return desc_eu    
	elif interfaceLang == "en":     
		if desc_en != "":
			return desc_en          
		else:        
			return desc_eu
	elif interfaceLang == "fr":     
		if desc_fr != "":
			return desc_fr          
		else:        
			return desc_eu
	else:
		return desc_eu

@register.filter       
def choose_karrusel_titulu_language(interfaceLang, berria):

	titulu_eu=berria.title_eu
	titulu_es=berria.title_es
	titulu_en=berria.title_en
	titulu_fr=berria.title_fr
    
	if interfaceLang == "eu": 
		return titulu_eu          
	elif interfaceLang == "es":
		if titulu_es != "":
			return titulu_es          
		else:        
			return titulu_eu    
	elif interfaceLang == "en":     
		if titulu_en != "":
			return titulu_en          
		else:        
			return titulu_eu
	elif interfaceLang == "fr":     
		if titulu_fr != "":
			return titulu_fr          
		else:        
			return titulu_eu
	else:
		return titulu_eu


@register.filter
def choose_language_text(Lang, item):
    
    text=""
    #TITULUA
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
        titulu_en=match_en.group(0)
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
    
    
    #DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if titulu_eu =="" and titulu_es =="" and titulu_en =="":
        titulua=item.dc_title
        titulua=titulua.replace("<div class=\"titulu_lg\">", " ")
        titulua=titulua.replace("</div>", " ")
        
    if Lang == "eu":
         
        if titulu_eu != "":
            text=titulu_eu          
        else:        
            text= titulua
    if Lang == "es":
        if titulu_es != "":
            text= titulu_es          
        else:        
            text= titulua
                
    if Lang == "en":
         
        if titulu_en != "":
            text= titulu_en          
        else:        
            text= titulua
    
    #DESKRIBAPENA
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
    
    #DBko deskribapenak hizkuntza kontrolik ez badu
    if deskribapena_eu=="" and deskribapena_es=="" and deskribapena_en=="":
        deskribapena=item.dc_description
        deskribapena=deskribapena.replace("<div class=\"desc_lg\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")
        
    
    if Lang == "eu":
         
        if deskribapena_eu != "":
            text=text +" "+ deskribapena_eu          
        else:        
            text=text +" "+ deskribapena
        
    if Lang == "es":
        if deskribapena_es != "":
            text=text +" "+ deskribapena_es          
        else:        
            text=text +" "+ deskribapena
                
    if Lang == "en":
         
        if deskribapena_en != "":
            text=text +" "+ deskribapena_en          
        else:        
            text=text +" "+ deskribapena

    
    return text




@register.filter
def choose_language_text_not_target(Lang, item):
    hizkuntzak=Lang.split("2")
    jat=hizkuntzak[0]
    helb=hizkuntzak[1]
    
    text=""
    #TITULUA
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
        titulu_en=match_en.group(0)
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
    
    
    #DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if titulu_eu =="" and titulu_es =="" and titulu_en =="":
        titulua=item.dc_title
        titulua=titulua.replace("<div class=\"titulu_lg\">", " ")
        titulua=titulua.replace("</div>", " ")
        
    if jat == "eu":
         
        if titulu_eu != "":
            text=titulu_eu
            if(helb=="es" and titulu_es != ""):
                text= ""
            if(helb=="en" and titulu_en != ""):
                text= ""          
        else:        
            text= titulua
    if jat == "es":
        if titulu_es != "":
            text= titulu_es 
            if(helb=="en" and titulu_en != ""):
                text= ""
            if(helb=="eu" and titulu_eu != ""):
                text= ""        
        else:        
            text= titulua
                
    if jat == "en":        
        if titulu_en != "":
            text= titulu_en
            if(helb=="es" and titulu_es != ""):
                text= ""
            if(helb=="eu" and titulu_eu != ""):
                text= ""       
        else:        
            text= titulua
    
    #DESKRIBAPENA
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
    
    #DBko deskribapenak hizkuntza kontrolik ez badu
    if deskribapena_eu=="" and deskribapena_es=="" and deskribapena_en=="":
        deskribapena=item.dc_description
        deskribapena=deskribapena.replace("<div class=\"desc_lg\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")
        
    
    if jat == "eu":
         
        if deskribapena_eu != "":
            desk= deskribapena_eu  
            if(helb=="es" and deskribapena_es != ""):
                desk=""
            if(helb=="en" and deskribapena_en != ""):
                desk=""
        else:        
            desk= deskribapena
        
    if jat == "es":
        if deskribapena_es != "":
            desk= deskribapena_es          
            if(helb=="eu" and deskribapena_eu != ""):
                desk=""
            if(helb=="en" and deskribapena_en != ""):
                desk=""
        else:        
            desk= deskribapena
                
    if jat == "en":
         
        if deskribapena_en != "":
            desk= deskribapena_en
            if(helb=="eu" and deskribapena_eu != ""):
                desk=""
            if(helb=="es" and deskribapena_es != ""):
                desk=""
        else:        
            desk= deskribapena

    text=text + " " + desk
    
    return text
    
@register.filter
def choose_description_language(interfaceLang, item):
    
    if item is None:
        return ""
    
    deskribapena=item.dc_description
    deskribapena_es=""
    deskribapena_en=""
    deskribapena_eu=""
    #espresio erregularrak erabilita hizkuntza desberdinetako deskribapenak atera
    #Kontuz! .*? expresioak ez ditu lerro saltoak onartzen, Aunamendirekin adibidez arazoak
    #re.DOTALL
    #Make the '.' special character match any character at all, including a newline; without this flag, '.' will match anything except a newline.
    #match_es = re.search('<div class=\"desc_es\">(.*?)</div>', deskribapena,re.DOTALL) ??ERROREA EMATEN DU

    match_es = re.search('<div class=\"desc_es\">(.*?)</div>', deskribapena)

    if match_es:
        deskribapena_es=match_es.group(0)
        deskribapena_es=deskribapena_es.replace("<div class=\"desc_es\">", " ")
        deskribapena_es=deskribapena_es.replace("</div>", " ")

        deskribapena_es=format_html(deskribapena_es)
        deskribapena_es=re.sub('<p class=".*?">',"",deskribapena_es)
        deskribapena_es=re.sub("</?p>","",deskribapena_es)

    else:
        deskribapena_es=""
        
    match_en = re.search('<div class=\"desc_en\">(.*?)</div>', deskribapena)
    if match_en:
        deskribapena_en=match_en.group(0)
        deskribapena_en=deskribapena_en.replace("<div class=\"desc_en\">", " ")
        deskribapena_en=deskribapena_en.replace("</div>", " ")

        deskribapena_en=format_html(deskribapena_en)
        deskribapena_en=re.sub('<p class=".*?">',"",deskribapena_en)
        deskribapena_en=re.sub("</?p>","",deskribapena_en)

    else:
        deskribapena_en=""
    
    match_eu = re.search('<div class=\"desc_eu\">(.*?)</div>', deskribapena)
    if match_eu:
        deskribapena_eu=match_eu.group(0)
        deskribapena_eu=deskribapena_eu.replace("<div class=\"desc_eu\">", " ")
        deskribapena_eu=deskribapena_eu.replace("</div>", " ")

        
        #AUNAMEDIko etiketak kentzeko
        #deskribapena_eu=deskribapena_eu.replace('&lt;p class=&quot;','<p class="')
        #deskribapena_eu=deskribapena_eu.replace('&quot;&gt;','">')
        #deskribapena_eu=deskribapena_eu.replace('&lt;/p&gt;','</p>')
        #deskribapena_eu=deskribapena_eu.replace('&lt;p&gt;','<p>')
        deskribapena_eu=format_html(deskribapena_eu) 
        deskribapena_eu=re.sub('<p class=".*?">',"",deskribapena_eu) 
        deskribapena_eu=re.sub("</?p>","",deskribapena_eu)
        #print deskribapena_eu
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
        deskribapena=deskribapena.replace("<div class=\"desc_lg\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")
        #AUnamendi
        deskribapena=deskribapena.replace("<div class=\"desc_eu\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")
        deskribapena=deskribapena.replace("<div class=\"desc_es\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")
        deskribapena=deskribapena.replace("<div class=\"desc_en\">", " ")
        deskribapena=deskribapena.replace("</div>", " ")


        #AUNAMEDIko etiketak kentzeko
        #deskribapena=deskribapena.replace('&lt;p class=&quot;','<p class="')
        #deskribapena=deskribapena.replace('&quot;&gt;','">')
        #deskribapena=deskribapena.replace('&lt;/p&gt;','</p>')
        #deskribapena=deskribapena.replace('&lt;p&gt;','<p>')

        deskribapena=format_html(deskribapena) 
        deskribapena=re.sub('<p class=".*?">',"",deskribapena) 
        deskribapena=re.sub("</?p>","",deskribapena) 





    if interfaceLang == "eu":
         
        if deskribapena_eu != "":
            return deskribapena_eu          
        else:        
            return deskribapena
        
    elif interfaceLang == "es":
        if deskribapena_es != "":
            return deskribapena_es          
        else:        
            return deskribapena
                
    elif interfaceLang == "en":         
        if deskribapena_en != "":
            return deskribapena_en          
        else:        
            return deskribapena
    else:
        return deskribapena
    
    
@register.filter(name='to_int')
def to_int(value):
    return int(value)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
