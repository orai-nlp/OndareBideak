from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from partaidetza.partaidetza_app.models import User,Status, Area, Phase, Genre, Profile, Proposal, ProposalArea, ProposalDocument, ProjectCard, ProjectArea, ProposalComment, Criterion, ProposalCriterion, Vote, PresentialVotes, CarouselContent, InfoContent, ProcessManagement, Themes, ThemeImages
from partaidetza.partaidetza_app.forms import ModalCostForm, ModalAreaForm, NewProposalTitleForm, \
NewProposalSummaryForm, NewProposalNecessityForm, NewProposalRecipientForm, NewProposalWhereForm
from solr_utils import get_more_like_this_in_titles, get_more_like_this_in_summaries, get_more_like_this_in_necessities, get_more_like_this_in_recipients, get_more_like_this_in_wheres
from utils import correct_language,change_related_info
from db_views import db_restore_password
import urllib2,re

def ajax_translate(request):
    """Translate via ajax"""
    url="http://api.opentrad.com/translate.php"
    url_text="?text="+request.GET.get("text").strip()
    url_lang="&lang="+request.GET.get("lang")
    url_client="&cod_client="+request.GET.get("cod_client")
    URL=url+url_text+url_lang+url_client
    print "URLA: ",URL

    try:
        response = urllib2.urlopen(URL.replace(' ','%20').encode("utf-8")).read()
    except:
        response = urllib2.urlopen(URL.replace(' ','%20')).read()

    print "RESPONSE: ",response
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))

@login_required
def ajax_delete_corporation_image(request):
    """Delete corporation image via ajax"""
    ThemeImages.objects.delete_corporation_image()
    return render_to_response("ajax/ajax_response.html",{"response": '',},context_instance=RequestContext(request))

@login_required
def ajax_vote(request):
    """Vote via ajax"""
    if request.GET:
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id = int(project_id))
      
        response = project.vote(request.user)
        return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))
        
@login_required
def ajax_fond(request):
    """Fond via ajax"""
    if request.GET:
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id = int(proposal_id))
      
        response = proposal.fond(request.user)
        return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))


def ajax_edit_proposal_cost(request):
    if request.GET:
        cost = request.GET.get('cost')
        form = ModalCostForm({"cost": cost})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_cost(cost)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("cost")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request)) 
            
 
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
        
            
def ajax_edit_proposal_title(request):
    if request.GET:
        language = request.GET.get("language")
        title = request.GET.get("title")
        form = NewProposalTitleForm({"title":title})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_title(title,language)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("title")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
            
def ajax_edit_proposal_summary(request):
    if request.GET:
        language = request.GET.get("language")
        summary = request.GET.get("summary")
        form = NewProposalSummaryForm({"summary":summary})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_summary(summary,language)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("summary")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_proposal_necessity(request):
    if request.GET:
        language = request.GET.get("language")
        necessity = request.GET.get("necessity")
        form = NewProposalNecessityForm({"necessity":necessity})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_necessity(necessity,language)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("necessity")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
         
            
def ajax_edit_proposal_recipient(request):
    if request.GET:
        language = request.GET.get("language")
        recipient = request.GET.get("recipient")
        form = NewProposalRecipientForm({"recipient":recipient})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_recipient(recipient,language)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_proposal_where(request):
    if request.GET:
        language = request.GET.get("language")
        where = request.GET.get("where")
        form = NewProposalWhereForm({"where":where})
        if form.is_valid():
            proposal = Proposal.objects.get(id=int(request.GET.get('proposal_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or proposal.is_author(request.user)):
                response = proposal.set_where(where,language)
		change_related_info('proposal','edit',proposal.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("where")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
def ajax_get_proposal_area(request):
    areas =[]
    if request.GET:
        area = map(lambda x: int(x),request.GET.get('area'))
        areas = Area.objects.filter(id__in=area)
    return render_to_response("ajax/ajax_get_area_response.html",{"areas": areas},context_instance=RequestContext(request))     

def ajax_get_proposal_state(request):
    if request.GET:
        state = request.GET.get('state')
        state = Status.objects.get(id=int(state))
    return render_to_response("ajax/ajax_get_state_response.html",{"state": state},context_instance=RequestContext(request)) 
 
def ajax_edit_project_cost(request):
    if request.GET:
        cost = request.GET.get('cost')
        form = ModalCostForm({"cost": cost})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_cost(cost)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("cost")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request)) 
            
  
def ajax_edit_project_area(request):
    response_project = None
    if request.GET:
        area = request.GET.get('area')
        form = ModalAreaForm({"area": area})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_area(area)
                response_project = project
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_area_response.html",{"response": response,"proposal":response_project},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("area")
            return render_to_response("ajax/ajax_area_response.html",{"response": response,},context_instance=RequestContext(request))    
 

            
def ajax_edit_project_title(request):
    if request.GET:
        language = request.GET.get("language")
        title = request.GET.get("title")
        form = NewProposalTitleForm({"title":title})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_title(title,language)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("title")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
            
            
def ajax_edit_project_summary(request):
    if request.GET:
        language = request.GET.get("language")
        summary = request.GET.get("summary")
        form = NewProposalSummaryForm({"summary":summary})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_summary(summary,language)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("summary")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_project_necessity(request):
    if request.GET:
        language = request.GET.get("language")
        necessity = request.GET.get("necessity")
        form = NewProposalNecessityForm({"necessity":necessity})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_necessity(necessity,language)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("necessity")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
         
            
def ajax_edit_project_recipient(request):
    if request.GET:
        language = request.GET.get("language")
        recipient = request.GET.get("recipient")
        form = NewProposalRecipientForm({"recipient":recipient})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_recipient(recipient,language)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("recipient")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))  
            
            
def ajax_edit_project_where(request):
    if request.GET:
        language = request.GET.get("language")
        where = request.GET.get("where")
        form = NewProposalWhereForm({"where":where})
        if form.is_valid():
            project = ProjectCard.objects.get(id=int(request.GET.get('project_id')))
            if not request.user.is_anonymous() and (request.user.profile.has_advanced_permissions() or project.is_author(request.user)):
                response = project.set_where(where,language)
		change_related_info('project','edit',project.id)
            else:
                response = None
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))       
        else:
            response = form.errors.get("where")
            return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))                                 
            
@login_required          
def ajax_more_like_this_in_titles(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_titles(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request)) 
        
@login_required           
def ajax_more_like_this_in_summaries(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_summaries(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))   
        
@login_required           
def ajax_more_like_this_in_recipients(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_recipients(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))  
        
@login_required           
def ajax_more_like_this_in_necessities(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_necessities(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))    
        
@login_required        
def ajax_more_like_this_in_wheres(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        type = request.GET.get("type")
        objects = get_more_like_this_in_wheres(query,language=language,type=type)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))           
                 

     
@login_required          
def ajax_more_like_this_in_events(request):
    if request.GET:
        query = request.GET.get("query")
        language = request.GET.get("language")
        objects = get_more_like_this_in_events(query,language=language)
        return render_to_response("ajax/related_documents.html",{"objects": objects,},context_instance=RequestContext(request))      
     
@login_required
def ajax_correct_language(request):
    language = request.GET.get("language")
    text = request.GET.get("text")
    response = correct_language(text,language)
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
    
    
@login_required
def ajax_validate_language(request):
    response = True
    for element in request.GET.keys():
        text = request.GET.get(element)
        language = element.split('_')[1]
        if text != "":            
            response = response and correct_language(text,language)
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))     
    
    
@login_required
def ajax_add_point_to_map_proposal(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id=int(proposal_id))
        proposal.set_map_point(float(lat),float(lng))
	change_related_info('proposal','edit',proposal.id)
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
    
    
@login_required
def ajax_add_point_to_map_project(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id=int(project_id))
        project.set_map_point(float(lat),float(lng))
	change_related_info('project','edit',project.id)
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
    
    
@login_required
def ajax_delete_point_from_map_proposal(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        proposal_id = request.GET.get("proposal_id")
        proposal = Proposal.objects.get(id=int(proposal_id))
        proposal.delete_map_point(float(lat),float(lng))
	change_related_info('proposal','edit',proposal.id)
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))   
    
    
@login_required
def ajax_delete_point_from_map_project(request):
    try:
        response = True
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        project_id = request.GET.get("project_id")
        project = ProjectCard.objects.get(id=int(project_id))
        project.delete_map_point(float(lat),float(lng))
	change_related_info('project','edit',project.id)
    except Exception as error:
        print error
        response = False
    return render_to_response("ajax/ajax_response.html",{"response": response,},context_instance=RequestContext(request))    
     
@login_required
def ajax_edit_carousel(request):
    content_id = request.GET.get("content_id")
    checked = request.GET.get("checked")
    if checked == "true": # insert into carousel
        CarouselContent.objects.insert(InfoContent.objects.get(id=int(content_id)))
    else: # delete from carousel
        CarouselContent.objects.delete(InfoContent.objects.get(id=int(content_id)))
     
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))      
        
@login_required        
def ajax_edit_process(request):
    process_id = request.GET.get("process_id")
    checked = request.GET.get("checked")
    process = ProcessManagement.objects.get(id=int(process_id))
    if checked == "true": # insert into carousel
        process.active = True
    else: # delete from carousel
        process.active = False
    process.save()     
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))      
    
    
@login_required
def ajax_edit_theme(request):
    theme_id = request.GET.get("theme_id")
    themes = Themes.objects.all()
    for theme in themes:
        if theme.id == int(theme_id):
            theme.selected = True
        else:
            theme.selected = False
        theme.save()
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))



@login_required
def ajax_edit_proposal_phase(request):
    proposal_id = request.GET.get("proposal_id")
    phase_id = request.GET.get("phase_id")
    proposal = Proposal.objects.get(id=int(proposal_id))
    phase = Phase.objects.get(id=int(phase_id))
    '''proposal.phase = phase
    proposal.save()'''
    proposal.set_phase(phase)
    change_related_info('proposal','status_change',proposal.id)
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))      
    

@login_required
def ajax_edit_proposal_phase_rejection(request):
    proposal_id = request.GET.get("proposal_id")
    rejection_id = request.GET.get("rejection_id")
    proposal = Proposal.objects.get(id=int(proposal_id))
    phase = Phase.objects.get(id=int(7))
    '''proposal.phase = phase
    proposal.save()'''
    proposal.set_phase(phase)
    proposal.set_rejection_reason(rejection_id)
    change_related_info('proposal','status_change',proposal.id)
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))      


@login_required
def ajax_edit_project_status(request):
    project_id = request.GET.get("project_id")
    status_id = request.GET.get("status_id")
    project = ProjectCard.objects.get(id=int(project_id))
    status = Status.objects.get(id=int(status_id))
    project.status=status
    project.save()
    change_related_info('project','status_change',project.id)
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))      
   
def restore_user_password(request):
    db_restore_password(User.objects.filter(email=request.GET["email"])[0])
    return render_to_response("ajax/ajax_response.html",{"response": True},context_instance=RequestContext(request))   
        
    
