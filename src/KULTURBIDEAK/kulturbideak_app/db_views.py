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




