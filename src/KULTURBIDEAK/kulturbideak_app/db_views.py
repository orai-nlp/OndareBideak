# This is where all the DB edit functions SHOULD BE gathered
from KULTURBIDEAK.kulturbideak_app.models import *
from django.contrib.auth import authenticate
#from utils import *

import re
import time, datetime



def db_add_itemcomment(comment_form, item, profile):
    """Update attached documents in the DB
    PARAMETERS:
    1. comment_form
    2. item
    3. profile
    """     
    
    cd = comment_form.cleaned_data
    parent = cd.get("parent_id", None) 
    
    if parent:
        parent = itemComment.objects.get(id=int(parent))
    
    itemComment.objects.create_comment(cd.get("comment"),item,profile, parent)




def db_add_pathcomment(comment_form, path, profile):
    """Update attached documents in the DB
    PARAMETERS:
    1. comment_form
    2. path
    3. profile
    """     
    #print "db_add_pathcomment"
    cd = comment_form.cleaned_data
    parent = cd.get("parent_id", None)  
    if parent:
        parent = pathComment.objects.get(id=int(parent))
    
    #print cd.get("comment")
    #print profile
    #print path.id
    #print "Parent"
    #print parent
    
    pathComment.objects.create_comment(cd.get("comment"),path,profile, parent)



def db_register(register_form):
    """Registers a user in the DB
    PARAMETERS:
    1. register_form
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: register_form, status_value==1: User object, status_value=2: error string
    """
    try:
        status_code = 1
        if register_form.is_valid():
            cd_register_form = register_form.cleaned_data
            profile = Profile.objects.create_profile(cd_register_form.get('username'),\
                                                cd_register_form.get('first_name'),\
                                                cd_register_form.get('last_name'),\
                                                cd_register_form.get('email'),\
                                                cd_register_form.get('hornitzailea'),\
                                                cd_register_form.get('hornitzaile_izena'),\
                                                cd_register_form.get('herrialdea'),\
                                                cd_register_form.get('password1'))      
            user = authenticate(username = cd_register_form.get('username'), password = cd_register_form.get('password1'))
            return (status_code,user) 
        else:
            status_code = 0
            return (status_code,register_form)
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)
    

def db_update_profile(profile_form):
    """Update a user in the DB
    PARAMETERS:
    1. profile_form
    RETURNS:
    (status_value,object)
    status_value -> 0: invalid form, 1: no errors, 2: other error
    object -> status_value==0: profile_form, status_value==1: Profile object, status_value=2: error string
    """
    try:
        status_code = 1
        if profile_form.is_valid():
            cd_profile_form = profile_form.cleaned_data
            profile = Profile.objects.update_profile(cd_profile_form.get('username'),\
                                                cd_profile_form.get('first_name'),\
                                                cd_profile_form.get('last_name'),\
                                                cd_profile_form.get('email'),\
                                                cd_profile_form.get('hornitzailea'),\
                                                cd_profile_form.get('hornitzaile_izena'),\
                                                cd_profile_form.get('herrialdea'))                  
            return (status_code,profile) 
        else:
            status_code = 0
            return (status_code,profile_form)
    except Exception as error:
        print error
        status_code = 2
        return (status_code,error)        
        


