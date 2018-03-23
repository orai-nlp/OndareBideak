# coding=utf-8
from lxml import etree
import subprocess
import os,time
import sys, getopt
import MySQLdb
from KULTURBIDEAK.kulturbideak_app.models import item
from haystack.management.commands import update_index
from django.utils.crypto import get_random_string




def oaiharveststore(collection, baseurl, wikify):

    print 'COLLECTION   :', collection
    print 'BASEURL      :', baseurl
    print 'WIKIFY       :', wikify
    


    print '++++++++++++++++START HARVESTER ++++++++++++++++'
   
    # BaseUrl: HEDATUZ http://hedatuz.euskomedia.org/cgi/oai2
    
    os.chdir(collection)
    #Subprocess ERABILI!!!
    #os.system("oai-harvest --no-delete -p edm '{0}'".format(baseurl))
    #erantzuna=subprocess.Popen(['perl','/home/maddalen/QARDF/QARDF_nagusia.pl',galdera], stdout=subprocess.PIPE)
    edm="edm"
    
    
    ##EZ DU BUKATU ARTE ITXOITEN   
    try:
        p=subprocess.Popen(['oai-harvest','-p', edm ,baseurl], stdout=subprocess.PIPE)
    except:
        return False
    
    
    
    ##ERRORE KONTROLA GEHITU!!!!
    '''
    while p.poll() == None:
        # We can do other things here while we wait
   
        (results, errors) = p.communicate()
        if errors != '':
            return False
    '''
    # BUKATU ARTE ITXOITEKO HAU GEHITU DUT,  TXUKUNDUU!!
    
    while p.poll() == None:
        time.sleep(0.5)
    
    
    ns = {'dcterms':'http://purl.org/dc/terms/','rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#','skos':'http://www.w3.org/2004/02/skos/core#','owl':'http://www.w3.org/2002/07/owl#','bibo':'http://purl.org/ontology/bibo/','ore':'http://www.openarchives.org/ore/terms/','xsi':'http://www.w3.org/2001/XMLSchema-instance','foaf':'http://xmlns.com/foaf/0.1/','edm':'http://www.europeana.eu/schemas/edm/','dc':'http://purl.org/dc/elements/1.1/'}
    

    print '+++++++++++++++START STORE      ++++++++++++++++'

    #for file in os.listdir(sys.argv[1]):
    for file in os.listdir(collection):
        
        if file.endswith(".xml"):
            print(file)
            tree=etree.parse(file)

            #Aldagaiak
            #EDM
            edmProvider=[]
            edmDataProvider=[]
            edmRights=[]
            edmIsShownAt=[]
            edmIsShownBy=[]
            edmObject=[]
            edmHasView=[]
            edmType=[]

            #DC
            dcTitle_eu=[]
            dcTitle_es=[]
            dcTitle_en=[]
            dcCreator=[]
            dcSubject=[]
            dcSubject2=[]
            dcDescription_eu=[]
            dcDescription_es=[]
            dcDescription_en=[]
            dcPublisher=[]
            dcLanguage=[]
            dcIdentifier=[]
            dcIsPartOf=[]
            dcIdentifier=[]
        
            #DCTERMS
            dctermsIssued=[]
            dctermsCreated=[]
            dctermsExtent=[]

            #EDM
            edmProviderValue="";
            edmDataProviderValue="";
            edmRightsValue="";
            edmIsShownAtValue="";
            edmIsShownByValue="";
            edmObjectValue="";
            edmHasViewValue="";
            edmTypeValue="";

            #DC
            dcTitle_lgValue=""
            dcTitle_euValue="";
            dcTitle_esValue="";
            dcTitle_enValue="";
            dcTitle_frValue="";
            dcCreatorValue="";
            dcSubjectValue="";
            dcDescription_lgValue="";
            dcDescription_euValue="";
            dcDescription_esValue="";
            dcDescription_enValue="";
            dcDescription_frValue="";
            dcPublisherValue="";
            dcLanguageValue="";
            dcIdentifierValue="";
            dcIsPartOfValue="";
            dcIdentifierValue="";

            #DCTERMS
            dctermsIssuedValue="";
            dctermsCreatedValue="";
            dctermsExtentValue="";


            #xpath-ak
            #EDM
            edmProvider=tree.xpath('/rdf:RDF/ore:Aggregation/edm:provider',namespaces=ns)
            edmDataProvider=tree.xpath('/rdf:RDF/ore:Aggregation/edm:dataProvider',namespaces=ns)
            edmRights=tree.xpath('/rdf:RDF/ore:Aggregation/edm:rights/@rdf:resource',namespaces=ns)
            edmIsShownAt=tree.xpath('/rdf:RDF/ore:Aggregation/edm:isShownAt/@rdf:resource',namespaces=ns)
            edmIsShownBy=tree.xpath('/rdf:RDF/ore:Aggregation/edm:isShownBy/@rdf:resource',namespaces=ns)
            edmObject=tree.xpath('/rdf:RDF/ore:Aggregation/edm:object/@rdf:resource',namespaces=ns)
            edmHasView=tree.xpath('/rdf:RDF/ore:Aggregation/edm:hasView/@rdf:resource',namespaces=ns)
            edmType=tree.xpath('/rdf:RDF/edm:ProvidedCHO/edm:type',namespaces=ns)

            #DC
            dcTitle_lg=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:title',namespaces=ns)
            dcTitle_eu=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:title[@xml:lang="eu"]',namespaces=ns)
            dcTitle_es=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:title[@xml:lang="es"]',namespaces=ns)
            dcTitle_en=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:title[@xml:lang="en"]',namespaces=ns)
            dcTitle_fr=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:title[@xml:lang="fr"]',namespaces=ns)
            dcCreator=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:creator/edm:Agent/skos:prefLabel',namespaces=ns)
            dcSubject=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:subject/skos:Concept/skos:prefLabel',namespaces=ns)
            dcSubject2=tree.xpath('/rdf:RDF/edm:ProvidedCHO/skos:prefLabel',namespaces=ns)
            dcDescription_lg=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:description',namespaces=ns)
            dcDescription_eu=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:description[@xml:lang="eu"]',namespaces=ns)
            dcDescription_es=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:description[@xml:lang="es"]',namespaces=ns)
            dcDescription_en=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:description[@xml:lang="en"]',namespaces=ns)
            dcDescription_fr=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:description[@xml:lang="fr"]',namespaces=ns)
            dcPublisher=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:publisher',namespaces=ns)
            dcLanguage=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:language',namespaces=ns)
            dcIdentifier=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:identifier',namespaces=ns)
            dcIsPartOf=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dc:isPartOf',namespaces=ns)
        
            #DCTERMS
            dctermsIssued=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dcterms:issued',namespaces=ns)
            dctermsCreated=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dcterms:created',namespaces=ns)
            dctermsExtent=tree.xpath('/rdf:RDF/edm:ProvidedCHO/dcterms:extent',namespaces=ns)

            #Balioak hartu
      
            #EDM
            for edukia in edmProvider:
                edmProviderValue = edmProviderValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in edmDataProvider:
                edmDataProviderValue = edmDataProviderValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in edmRights:
                edmRightsValue = edmRightsValue + " " + edukia 
            for edukia in edmIsShownAt:
                edmIsShownAtValue = edmIsShownAtValue + " " + edukia
            for edukia in edmIsShownBy:
                edmIsShownByValue = edmIsShownByValue + " " + edukia
            for edukia in edmObject:
                edmObjectValue = edmObjectValue + " " + edukia
            for edukia in edmHasView:
                edmHasViewValue = edmHasViewValue + " " + edukia
            for edukia in edmType:
                edmTypeValue = edmTypeValue +" " + edukia.text.encode('utf-8').strip()

        
            #DC     
            for edukia in dcTitle_eu:
                dcTitle_euValue = dcTitle_euValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcTitle_es:
                dcTitle_esValue = dcTitle_esValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcTitle_en:
                dcTitle_enValue = dcTitle_enValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcTitle_fr:
                dcTitle_frValue = dcTitle_frValue + " " + edukia.text.encode('utf-8').strip()
            if  dcTitle_euValue == "" and dcTitle_esValue=="" and dcTitle_enValue=="" and dcTitle_frValue=="":
                for edukia in dcTitle_lg:
                    dcTitle_lgValue = dcTitle_lgValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcCreator:
                dcCreatorValue = dcCreatorValue + " " +edukia.text.encode('utf-8').strip()
            for edukia in dcSubject:
                dcSubjectValue = dcSubjectValue + " " + edukia.text.encode('utf-8').strip()  #karaktere-kodeketa
            for edukia in dcSubject2:
                dcSubjectValue = dcSubjectValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcDescription_eu:
                dcDescription_euValue = dcDescription_euValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcDescription_es:
                dcDescription_esValue = dcDescription_esValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcDescription_en:
                dcDescription_enValue = dcDescription_enValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcDescription_fr:
                dcDescription_frValue = dcDescription_frValue + " " + edukia.text.encode('utf-8').strip()
            if  dcDescription_euValue == "" and dcDescription_esValue=="" and dcDescription_enValue=="" and dcDescription_frValue=="":
                for edukia in dcDescription_lg:
                    dcDescription_lgValue = dcDescription_lgValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcPublisher:
                dcPublisherValue = dcPublisherValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcLanguage:
                dcLanguageValue = dcLanguageValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcIdentifier:
                dcIdentifierValue = dcIdentifierValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dcIsPartOf:
                dcIsPartOfValue = dcIsPartOfValue + " " + edukia.text.encode('utf-8').strip()


            #DCTERMS
            for edukia in dctermsIssued:
                dctermsIssuedValue = dctermsIssuedValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dctermsCreated:
                dctermsCreatedValue = dctermsCreatedValue + " " + edukia.text.encode('utf-8').strip()
            for edukia in dctermsExtent:
                dctermsExtentValue = dctermsExtentValue + " " + edukia.text.encode('utf-8').strip()


            dcTitle=""
            if dcTitle_lgValue != "" :
                dcTitle = "<div class=\"titulu_lg\">"+dcTitle_lgValue+"</div>"
            else:    
                if dcTitle_euValue != "" :
                    dcTitle = "<div class=\"titulu_eu\">"+dcTitle_euValue+"</div>"
                if dcTitle_esValue != "" :
                    dcTitle =dcTitle +" "+"<div class=\"titulu_es\">"+dcTitle_esValue+"</div>"
                if dcTitle_enValue != "" :
                    dcTitle =dcTitle +" "+"<div class=\"titulu_en\">"+dcTitle_enValue+"</div>"
      

            dcDescription =""
            if dcDescription_lgValue != "" :
                dcDescription = "<div class=\"desc_lg\">"+dcDescription_lgValue+"</div>"
            else:    
                if dcDescription_euValue != "" :
                    dcDescription = "<div class=\"desc_eu\">"+dcDescription_euValue+"</div>"
                if dcDescription_esValue != "" :
                    dcDescription = dcDescription +" "+"<div class=\"desc_es\">"+dcDescription_esValue+"</div>"
                if dcDescription_enValue != "" :
                    dcDescription = dcDescription +" "+"<div class=\"desc_en\">"+dcDescription_enValue+"</div>"

            
            # Hizkuntzaren balioa egokitu. Hau garrantzitsua da, 
            #Solr-Haystack-ek balio honen arabera indexatuko du eta
            dcLanguageValue = dcLanguageValue.strip()
            if dcLanguageValue == "spa":
                dcLanguageValue="es"
            else:
                if dcLanguageValue == "eng":
                    dcLanguageValue="en"
                if dcLanguageValue == "baq":
                    dcLanguageValue="eu"
                if dcLanguageValue == "fre":
                    dcLanguageValue="fr"
             
            #item taulako uri eremuaren balioa ez errepikatzeko
            randomstr=get_random_string(length=12,allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            dcIdentifierValue=file+"_"+dcIdentifierValue+"_"+randomstr

                
            #Eremu hutsak prestatu
            usfd_id=''
            dc_contributor=''
            dc_format=''
            dc_source=''
            dc_relation=''
            dc_rights=''
            dc_coverage=''
            dcterms_provenance=''
            dcterms_temporal=''
            dcterms_spatial=''
            dcterms_medium=''
            dcterms_alternative=''
            dcterms_tableofcontents=''
            dcterms_isreplacedby=''
            edm_unstored=''
            edm_dataprovider=''
            #edm_isshownby=''
            edm_country=''
            edm_language=dcLanguageValue
            edm_uri=''
            edm_usertag=''
            edm_year=dctermsIssuedValue
            edm_previewnodistribute=''
            edm_hasobject=''
            paths_bow=''
            paths_facet_date=''
            paths_informativeness=0
            paths_trav_count=0
            proposatutakoa=0
            egunekoa=0
            geoloc_longitude=0.0
            geoloc_latitude=0.0
            aberastua=0


            #Datu-basean sartu    
            item_berria = item(uri=dcIdentifierValue, usfd_id=usfd_id, dc_title=dcTitle,dc_creator=dcCreatorValue,
                               dc_subject=dcSubjectValue,dc_description=dcDescription,dc_publisher=dcPublisherValue,
                               dc_contributor=dc_contributor,dc_date=dctermsCreatedValue,dc_type=edmTypeValue,dc_format=dc_format,dc_identifier=dcIdentifierValue,
                               dc_source=dc_source,dc_language=dcLanguageValue,dc_relation=dc_relation,
                               dc_rights=dc_rights,dc_coverage=dc_coverage,dcterms_provenance=dcterms_provenance,dcterms_ispartof=dcIsPartOfValue,dcterms_temporal=dcterms_temporal,
                               dcterms_spatial=dcterms_spatial,dcterms_medium=dcterms_medium,dcterms_extent=dctermsExtentValue,dcterms_alternative=dcterms_alternative,
                               dcterms_issued=dctermsIssuedValue,dcterms_tableofcontents=dcterms_tableofcontents,dcterms_isreplacedby=dcterms_isreplacedby,edm_unstored=edm_unstored,
                               edm_object=edmObjectValue,edm_provider=edmProviderValue,edm_type=edmTypeValue,edm_rights=edmRightsValue,edm_dataprovider=edm_dataprovider,
                               edm_isshownby=edmIsShownByValue,edm_isshownat=edmIsShownAtValue,edm_country=edm_country,edm_language=edm_language,
                               edm_uri=edm_uri,edm_usertag=edm_usertag,edm_year=edm_year,edm_previewnodistribute=edm_previewnodistribute,
                               edm_hasobject=edm_hasobject,paths_bow=paths_bow,paths_facet_date=paths_facet_date,
                               paths_informativeness=paths_informativeness,paths_trav_count=paths_trav_count,
                               proposatutakoa=proposatutakoa,egunekoa=egunekoa,geoloc_longitude=geoloc_longitude,geoloc_latitude=geoloc_latitude,aberastua=aberastua)
   
   
            item_berria.save()  
            
          
            
    #HAYSTAC reindex!
    #Haystack update_index EGIN berriak gehitzeko. age=1 pasata azkeneko ordukoak bakarrik hartzen dira berriak bezala
            
    #use 'remove' option to remove non-existing entries.
    #"interactive" would prevent haystack asking question if you really want to rebuild index. This is equivalent to --no-input command line option.
    #update_index.Command().handle(using='default',remove=True, interactive=False)
   
    update_index.Command().handle(age=1)
    
    
    return True