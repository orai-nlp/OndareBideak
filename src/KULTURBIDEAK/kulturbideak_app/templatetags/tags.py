from django.template.defaultfilters import stringfilter
from django import template
from settings import *
import re
import HTMLParser
import requests
#import pdb

from django.conf import settings


from django.contrib.auth.models import User, Group
register = template.Library()

@register.filter
def proxyPassHttp(url):	
	result=re.sub('^\s*http://www.http://','http://', url)
	result=re.sub('liburuklik.euskadi.net','liburuklik.euskadi.eus', result)
        if not re.search('.(pdf|jpg|flv)$',result):
                result=re.sub('www.euskomedia.org','aunamendi.eusko-ikaskuntza.eus', result)

	result=re.sub('^\s*http://','/kanpora/', result)	
	if re.search(r'DBKVisorBibliotecaWEB', result, flags=re.IGNORECASE):
		result+='&contenido=meta'

	return result

@register.filter
def leading_wspace(url):	
	"""delete leading white spaces. """
	return re.sub('^\s*','', url)

@register.filter
def or_tartekatu(str):	
	"""add OR between words. """
	return str.replace(" ", " OR ")


@register.filter
def lerroJauziakKendu(sarrera):
	"""delete new line chars. """
	return sarrera.replace("\n","");

@register.filter
def htmlEtiketakGarbitu(sarrera):
	"""Clean html tags. """
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
def data_formatua(sarrera):
	"""format data. """
	if re.match(r'^\s*\"[^\"]+\"\s*$', sarrera):
		output= sarrera.replace('"','')
		if output == "0":
			output="-"
		return output	
				
	return sarrera.replace("-"," . ")

@register.filter
def is_in(id,list): 

    for item in list:       
        if int(id) == item.id:
            return 1
    
    return 0

@register.filter
def is_in_list(id,list): 

	 if int(id) in list:
	 	return True
	 
	 return False

@register.filter
def is_handle(value): 
	"""check if url contains image suffix. """
	if re.match(r'^.*\.(jpg|png|jpeg|tiff|gif)$', value, flags=re.IGNORECASE):
	 	return True
	 
	return False
	
@register.filter
def get_item_image(item): 
    img=item    
    return img


@register.filter
def cut_text(input,num): 
    out=input[:num]
    if len(input) > len(out): 
        out=out+"..."
    return out

@register.filter
def cut_words(input,num):
	kk=input.split("\s+")	 
	out=' '.join(kk[:num])
	if len(input) > len(out):
		out=out+"..."
		
	return out


@register.filter
def add_ekm_prefix_to_desc(value): 
    value=value.replace('="/ImgsAuna/','="/kanpora/aunamendi.eusko-ikaskuntza.eus/ImgsAuna/')
    value=value.replace('href="/aunamendi/', 'href="/kanpora/aunamendi.eusko-ikaskuntza.eus/aunamendi/')
    value=value.replace('http://maps.google.com', 'https://maps.google.com')
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
def format_html(value, max):
	
	html_parser = HTMLParser.HTMLParser()
	first = html_parser.unescape(value)
	if max >= 5:
		return first;
	else:
		if re.search("&.+?;",first):
			first=format_html(first,(max+1))
		
	return first

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
    
    #DESKRIBAPENA
    deskribapena=item.dc_description
    deskribapena_es=get_lang_field(deskribapena,"es","desc")
    deskribapena_en=get_lang_field(deskribapena,"en","desc")
    deskribapena_eu=get_lang_field(deskribapena,"eu","desc")
    #espresio erregularrak erabilita hizkuntza desberdinetako deskribapenak atera
    
    #DBko deskribapenak hizkuntza kontrolik ez badu
    if deskribapena_eu=="" and deskribapena_es=="" and deskribapena_en=="":
        deskribapena=item.dc_description
        deskribapena=get_lang_field(deskribapena,"lg","desc")
        
    
    if Lang == "eu":
         
        if deskribapena_eu != "":
            text=deskribapena_eu          
        else:        
            text=deskribapena
        
    if Lang == "es":
        if deskribapena_es != "":
            text=deskribapena_es          
        else:        
            text=deskribapena
                
    if Lang == "en":
         
        if deskribapena_en != "":
            text=deskribapena_en          
        else:        
            text=deskribapena
    
    return text


@register.filter
def choose_title_language(lang, item):
    
    if item is None:
        return ""
     
    titulua=item
    
    # no lang information -> return the title as it is
    if lang is None:
    	return titulua
    
    # title has no different langs coded -> return the title as it is
    if (not re.search('</div>', titulua)):
    	return titulua
    
	# extract different lang titles
    titulu_lang={}
    titulu_lang['es']=get_lang_field(titulua,"es","titulu")
    titulu_lang['en']=get_lang_field(titulua,"en","titulu")
    titulu_lang['eu']=get_lang_field(titulua,"eu","titulu")
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 
    
    # if all previous langs are null try one last abstract tag
    if titulu_lang['eu'] =="" and titulu_lang['es'] =="" and titulu_lang['en'] =="":        
        titulu_lang['lg']=get_lang_field(titulua,"lg","titulu")
    
    # absolute preference is for the lang given as parameter       
    if titulu_lang[lang] != "":
        return titulu_lang[lang]          
    else:
    	del titulu_lang[lang]
    	# second best option is "es" because most of our users are spanish speakers 
    	if lang!="es" and titulu_lang['es']!="":
    		return titulu_lang['es']
    	
    	# if we are here "es" info is not needed anymore
    	if lang!="es":
    		del  titulu_lang["es"]
    	# 3rd option: loop through extracted titles until we find one not being null.
    	for l in titulu_lang:
    		titulua=titulu_lang[l]
    		if titulua != "":
    			return titulua
    	#as last resort return the original title field.	
      	return item.dc_title


@register.filter
def choose_language_text_not_target(Lang, item):
    hizkuntzak=Lang.split("2")
    jat=hizkuntzak[0]
    helb=hizkuntzak[1]

    text=""
    #TITULUA                                                                                                                                
    deskribapena=item.dc_description
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera                                                                
    deskribapena_lang={}
    deskribapena_lang['es']=get_lang_field(deskribapena,"es","desc")
    deskribapena_lang['en']=get_lang_field(deskribapena,"en","desc")
    deskribapena_lang['eu']=get_lang_field(deskribapena,"eu","desc")
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera                                                                

    #DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada                                                                            
    if deskribapena_lang['eu'] =="" and deskribapena_lang['es'] =="" and deskribapena_lang['en'] =="":
        deskribapena=item.dc_description
        deskribapena=get_lang_field(deskribapena,"lg","desc")

    text=jat_helb_aukeratu(jat,helb,deskribapena_lang,deskribapena)

    return text


@register.filter
def choose_language_title_target(Langs, item):
    hizkuntzak=Langs.split("2")
    jat=hizkuntzak[0]
    helb=hizkuntzak[1]
    
    text=""
    #TITULUA
    titulua=item.dc_title
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 
    titulu_lang={}
    titulu_lang['es']=get_lang_field(titulua,"es","titulu")
    titulu_lang['en']=get_lang_field(titulua,"en","titulu")
    titulu_lang['eu']=get_lang_field(titulua,"eu","titulu")
    #espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 

    #DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if titulu_lang['eu'] =="" and titulu_lang['es'] =="" and titulu_lang['en'] =="":
        titulua=item.dc_title
        titulua=get_lang_field(titulua,"lg","titulu")

    text=jat_helb_aukeratu(jat,helb,titulu_lang,titulua)       
    return text

    
@register.filter
def choose_description_language(interfaceLang, item):
    
    if item is None:
        return ""
    
    deskribapena=item.dc_description
    deskribapena_es=get_lang_field(deskribapena,"es","desc")
    deskribapena_en=get_lang_field(deskribapena,"en","desc")
    deskribapena_eu=get_lang_field(deskribapena,"eu","desc")
    #espresio erregularrak erabilita hizkuntza desberdinetako deskribapenak atera

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

        deskribapena=format_html(deskribapena,1) 
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
    
    
# Custom tag for diagnostics
@register.filter(name='debug')    
def debug_object(var):
    return vars(var)    
    
    
@register.filter(name='split')
def split(value):
    return value.split(' ')
    
    
@register.filter
def setvar_license_icon_color(path):
	if "nabigazio_item" in path or "nabigatu" in path or "autoplay" in path:
		return "kolore-gris-0"
	
	return "kolore-beltza"
    
    
    
    
def get_lang_field(inputtext,lang,field):
	field_lang=field+'_'+lang 

	#espresio erregularrak erabilita hizkuntza desberdinetako deskribapenak atera
    #Kontuz! .*? expresioak ez ditu lerro saltoak onartzen, Aunamendirekin adibidez arazoak
    #re.DOTALL 
    #Make the '.' special character match any character at all, including a newline; without this flag, '.' will match anything except a newline.                                                                                                                 
    #match_es = re.search('<div class=\"desc_es\">(.*?)</div>', deskribapena,re.DOTALL) ??ERROREA EMATEN DU

	match_found = re.search(r'<div class=\"'+re.escape(field_lang)+r'\">(.*?)</div>', inputtext,re.S)	
	reslt=""
	if match_found:
		reslt=match_found.group(1)
		#reslt=re.sub(r'<div class=\"'+re.escape(field_lang)+r'\">',r' ',reslt)
		#reslt=reslt.replace("</div>", " ")

        reslt=format_html(reslt,1)
    	reslt=re.sub('<p class=".*?">',"",reslt)
        reslt=re.sub("</?p>","",reslt)

        
	return reslt
      
   
def jat_helb_aukeratu(src,tgt,fields,defaulttext):
	
	# if target language information is present we don't need any translation
	if fields[tgt] != "":
		return ""
	
	if src == "eu":
		if fields['eu'] != "":
			text=fields['eu']
			if(tgt=="es" and fields['es'] != ""):
				text= ""
			if(tgt=="en" and fields['en'] != ""):
				text= ""          
        else:        
            text= defaulttext
            
	if src == "es":
		if fields['es'] != "":
			text= fields['es'] 
			if(tgt=="en" and fields['en'] != ""):
				text= ""
			if(tgt=="eu" and fields['eu'] != ""):
				text= ""        
        else:        
            text= defaulttext
                
	if src == "en":        
		if fields['en'] != "":
			text= fields['en']
			if(tgt=="es" and fields['es'] != ""):
				text= ""
			if(tgt=="eu" and fields['eu'] != ""):
				text= ""       
        else:        
            text= defaulttext
        
	return text
    
