/////////////////// IMAGE SWITCHER ///////////////////////
function change_images()
{
	if(timerid)
	{
		timerid = 0;
	}
	var tDate = new Date();
	
	if(countimages == images.length)
	{
		countimages = 0;
	}
	if(tDate.getSeconds() % 5 == 0)
	{
		document.getElementById("id_image").src = images[countimages];
	}
	countimages++;
	timerid = setTimeout("change_images()", 1000);
}


//////////////////// IMAGE PREVIEW /////////////////////////

function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var format = input.files[0].name.split('.')[input.files[0].name.split('.').length-1];
            if ($.inArray(format.toLowerCase(),accepted_image_formats) >= 0 || $.inArray(format,accepted_image_formats) >= 0){
                reader.onload = function (e) {
                    $('#imgPreview').attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
}

/////////////////////////////////////////////////////////////

function load_errorlist_changes(){
    $(document).ready(function(){
        $('.errorlist').each( function( index, element ){
          $(this).prev().addClass("errorInput")
        });
    });
}


function get_coordinates(){
    var coordinates = $("#id_coordinates");
    $(layer_array).each(function( index, element ){
        coordinates.val(coordinates.val()+"["+$(this)[0]+","+$(this)[1]+"]|");
    });

}

function load_add_info_content_scripts(){
    $(function() {
        $('.upload_p').formset({
        });
    });
    
    $('#content_div textarea').focusout(function() {
        correct_language($(this),"content");
    });    


}

function load_diagnostics_scripts(){}

function load_add_diagnostics_scripts(){
    
    /*$("#id_area").chosen();*/
    
    $('#good_div textarea').focusout(function() {
        correct_language($(this),"good");
    });
    $('#bad_div textarea').focusout(function() {
        correct_language($(this),"bad");
    });
    $('#challenge_div textarea').focusout(function() {
        correct_language($(this),"challenge");
    });

}


function manage_new_email_scripts(){

    $("#id_all").click(function (){
	if ($(this).prop("checked")){
	    $("#id_recipient").parent().parent().hide();
	}
	else{
	    $("#id_recipient").parent().parent().show();
	}

    });

}


function manage_comments_scripts(){
    $(document).ready(function() {
        $('#comments_table').DataTable({
                                        paging: false,

                                    });
    } );

    $('#comments_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#comments_table thead th input').prop("checked")){
                $('#comments_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_delete_comments").attr("href", $("#id_delete_comments").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                  
                });
        }
        else{
                $('#comments_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_delete_comments").attr("href", $("#id_delete_comments").attr("href").replace($("#id_delete_comments").attr("href").split('/')[$("#id_delete_comments").attr("href").split('/').length-1],""));
                  
                });
        
        }
    } );
    
    
    $('#comments_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_delete_comments").attr("href", $("#id_delete_comments").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            
        }
        else{
            $("#id_delete_comments").attr("href", $("#id_delete_comments").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            
            $(this).prop("checked", false );
        }
    } );



}


function manage_diagnostics_scripts(){
    $(document).ready(function() {
        $('#diagnostics_table').DataTable({
                                        paging: false,
                                        
                                    });
    } );
    
    if($("#p_info").length){
        $('#info-text').modal('toggle');
	setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);

    }    

    
    $('#diagnostics_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#diagnostics_table thead th input').prop("checked")){
                $('#diagnostics_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
         	  $("#id_delete_diagnostics").attr("href", $("#id_delete_diagnostics").attr("href")+"["+$(this).closest('tr').attr("id")+"]");         
                });
        }
        else{
                $('#diagnostics_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace($("#id_multiple_xlsx").attr("href").split('/')[$("#id_multiple_xlsx").attr("href").split('/').length-1],""));
                  $("#id_delete_diagnostics").attr("href", $("#id_delete_diagnostics").attr("href").replace($("#id_delete_diagnostics").attr("href").split('/')[$("#id_delete_diagnostics").attr("href").split('/').length-1],""));
                });
        
        }
    } );
    
    
    $('#diagnostics_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            $("#id_delete_diagnostics").attr("href", $("#id_delete_diagnostics").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
        }
        else{
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            $("#id_delete_diagnostics").attr("href", $("#id_delete_diagnostics").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));

            $(this).prop("checked", false );
        }
    } );

}

function load_register_scripts(){
    /* Loads register template's javascripts */
       
    $(document).ready(function(){
        $('#id_institution_name_div').fadeOut();
        $('#id_institution').change(function(){
            if(this.checked)
                $('#id_institution_name_div').fadeIn('slow');
            else
                $('#id_institution_name_div').fadeOut('slow');

        });
    });
    
}

function load_profile_scripts(){
    /* Loads register template's javascripts */
       
    $(document).ready(function(){
        $('#id_institution').change(function(){
            if(this.checked)
                $('#id_institution_name_div').fadeIn('slow');
            else
                $('#id_institution_name_div').fadeOut('slow');

        });
    });
    
}

function load_password_scripts(){}


function manage_contents_scripts(text){
    $(document).ready(function() {
        $('#contents_table').DataTable({
                                        paging: false,
                                        
                                    });
    } );

    if($("#p_info").length){
        $('#info-text').modal('toggle');
	setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);

    }
    
    $('#contents_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#contents_table thead th input').prop("checked")){
                $('#contents_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_delete_contents").attr("href", $("#id_delete_contents").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                  
                });
        }
        else{
                $('#contents_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_delete_contents").attr("href", $("#id_delete_contents").attr("href").replace($("#id_delete_contents").attr("href").split('/')[$("#id_delete_contents").attr("href").split('/').length-1],""));
                  
                });
        
        }
    } );
    
    
    $('#contents_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_delete_contents").attr("href", $("#id_delete_contents").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            
        }
        else{
            $("#id_delete_contents").attr("href", $("#id_delete_contents").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            
            $(this).prop("checked", false );
        }
    } );
    
    
    $(".carousel_check").change(function() {
        var checked = $(this).is(':checked');
        var content_id = $(this).parents('tr').attr("id");
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_carousel',
          async: false,
          data: {content_id: content_id, checked:checked},
          dataType:'html',
          success : function(data, status, xhr){
            $('#info-text p').text(text);
            $('#info-text').modal('toggle');
	    setTimeout(function(){
                $("#info-text").modal('hide');
            }, 3000);

         }   
          
        });
    });
}

function load_manage_proposal_scripts(){
    $(document).ready(function() {
        $('#proposals_table').DataTable({
                                        paging: false,   
                                    });
    } );
    
    if($("#p_info").length){
        $('#info-text').modal('toggle');
	setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);

    }
    
    $('#proposals_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#proposals_table thead th input').prop("checked")){
                $('#proposals_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                  $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                });
        }
        else{
                $('#proposals_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace($("#id_multiple_xlsx").attr("href").split('/')[$("#id_multiple_xlsx").attr("href").split('/').length-1],""));
                  $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href").replace($("#id_delete_proposals").attr("href").split('/')[$("#id_delete_proposals").attr("href").split('/').length-1],""));
                });
        
        }
    } );
    
    
    $('#proposals_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            $(this).prop("checked", true );
        }
        else{
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            $("#id_delete_proposals").attr("href", $("#id_delete_proposals").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            $(this).prop("checked", false );
        }
    } );
    
    
}

function load_manage_accepted_proposal_scripts(){
    $(document).ready(function() {
        $('#projects_table').DataTable({
                                        paging: false,
                                        
                                    });
    } );
    
    
    if($("#p_info").length){
        $('#info-text').modal('toggle');
	setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);

    }
    
    $('#projects_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#projects_table thead th input').prop("checked")){
                $('#projects_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                  
                });
        }
        else{
                $('#projects_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace($("#id_multiple_xlsx").attr("href").split('/')[$("#id_multiple_xlsx").attr("href").split('/').length-1],""));
                  
                });
        
        }
    } );
    
    
    $('#projects_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            
        }
        else{
            $("#id_multiple_xlsx").attr("href", $("#id_multiple_xlsx").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            
            $(this).prop("checked", false );
        }
    } );
    
}


function manage_events_scripts(){
    $(document).ready(function() {
        $('#events_table').DataTable({ bPaginate : false});
    } );
    
    if($("#p_info").length){
        $('#info-text').modal('toggle');
	setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);

    }
    
    $('#events_table thead th').first().html('<input id="selecta_all" type="checkbox">').on( 'click', function ()     {
        if ($('#events_table thead th input').prop("checked")){
                $('#events_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", true );
                  $("#id_delete_events").attr("href", $("#id_delete_events").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
                  
                });
        }
        else{
                $('#events_table tbody .selection_check').each(function( index, element ){
                  $(this).prop("checked", false );
                  $("#id_delete_events").attr("href", $("#id_delete_events").attr("href").replace($("#id_delete_events").attr("href").split('/')[$("#id_delete_events").attr("href").split('/').length-1],""));
                  
                });
        
        }
    } );
    
    
    $('#events_table tbody').on( 'click', '.selection_check', function () {
        if ($(this).prop("checked")){
            $("#id_delete_events").attr("href", $("#id_delete_events").attr("href")+"["+$(this).closest('tr').attr("id")+"]");
            
        }
        else{
            $("#id_delete_events").attr("href", $("#id_delete_events").attr("href").replace("["+$(this).closest('tr').attr("id")+"]",""));
            
            $(this).prop("checked", false );
        }
    } );
}


function manage_accepted_proposal_scripts(){
    $(document).ready(function() {
        $('#projects_table').DataTable();
    } );
    
    $('#projects_table tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        if ($(this).hasClass("selected")){            
            $("#id_delete_projects").attr("href", $("#id_delete_projects").attr("href")+","+$(this).attr("id"));
        }
        else{            
            $("#id_delete_projects").attr("href", $("#id_delete_projects").attr("href").replace(","+$(this).attr("id"),""));
        }
    } );
}

function manage_my_contents_scripts(){
    $(document).ready(function() {
        $('#proposals_table').DataTable({ bPaginate : false});
        $('#diagnostics_table').DataTable({ bPaginate : false});
        if ($("#info-text").length){
            $('#info-text').modal('toggle');
	    setTimeout(function(){
               $("#info-text").modal('hide');
            }, 3000);

        }
        
    });
    
}

function manage_process_scripts(text){
    $(document).ready(function() {
        $('#process_table').DataTable({ bPaginate : false});   
    });
    
    if($("#p_info").length){        
        $('#info-text').modal('toggle');
        setTimeout(function(){
           $("#info-text").modal('hide');
        }, 3000);
    }
    
    $(".process_check").change(function() {
        var checked = $(this).is(':checked');
        var process_id = $(this).parents('tr').attr("id");
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_process',
          async: false,
          data: {process_id:process_id,checked:checked},
          dataType:'html',
          success : function(data, status, xhr){
            $('#info-text p').text(text);
            $('#info-text').modal('toggle');
	    setTimeout(function(){
                $("#info-text").modal('hide');
            }, 3000);
         }   
          
        });
    });
    
}

function manage_criterion_scripts(){
    $(document).ready(function() {
        $('#criterions_table').DataTable({ bPaginate : false});
        $('#criterions_table').change(function() {
            $(".criterion_checkbox_criterion").click(function() {
                var change_element;
                change_element = $(this).next();
                change_element.val("changed");
            } );
        } );
        
        $(".criterion_checkbox_criterion").click(function() {
            var change_element;
            change_element = $(this).next();
            change_element.val("changed");
        } );
    } );
    
    
}



function load_proposal_scripts(){

    /*$('#area_modal').on('shown.bs.modal', function () {
      $("#id_modal_area").chosen();
    });*/
 
    $('#criterions_table').DataTable({ bPaginate : false});
        $('#criterions_table').change(function() {
            $(".criterion_checkbox_criterion").click(function() {
                var change_element;
                change_element = $(this).next();
                change_element.val("changed");
            } );
        } );
        
    $(".criterion_checkbox_criterion").click(function() {
        var change_element;
        change_element = $(this).next();
        change_element.val("changed");
    } );
    
    $(function() {
        $('.upload_p').formset({
        });
    });
}

function load_accepted_proposal_scripts(){
    
    
    
    /*$('#area_modal').on('shown.bs.modal', function () {
      $("#id_modal_area").chosen();
    });
    
    $('#technical_modal').on('shown.bs.modal', function () {
      $("#id_accepted").chosen();
      
    });*/
  
    
    
    
    
    $(function() {
        $('.upload_p').formset({
        });
        
    });
    $(function() {
        $('.upload_p2').formset({
        });
        
    });
}


function load_project_scripts(){
    $('#id_date').datepicker({dayNamesMin: day_names,monthNames:month_names, firstDay: 1});
    /*$('#status_modal').on('shown.bs.modal', function () {
      $("#id_state").chosen();
    });*/
}

/* MODAL FORM FUNCTIONS */

function remove_error_messages(modal_id){
    $(modal_id).find("#response").each( function( index, element ){
          $(this).remove();
        });
}


function save_proposal_area_IKER(proposal_id){

    var area = $("#id_modal_area").val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_area',
          async: false,
          data: {proposal_id: proposal_id, area:area},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response");
            if (response != ""){
                remove_error_messages("#area_modal");
                $("#area_modal").modal('hide');
                $("#id_area").html(response);
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_area").after(data);
            }
            
         }   
          
    });
}
function save_proposal_area(){
	
    var area = $("#id_arloa").val();
   
   
    $.ajax({
          url: '/ajax_edit_arloa',
          async: false,
          data: {area:area},
          dataType:'html',
          success : function(data, status, xhr){
            var response=data;
           
            if (response != ""){
            	$('#id_area').text(data);
            	$("#id_arloa").text(data);     
                //remove_error_messages("#area_modal");
                $("#area_modal").modal('hide');
                //$("#id_arloa").html(response); //BEGIRATU HAU, html kodea ordezkatzen du
                }
            else{
                
                $("#area_modal").modal('hide');
            }
            
         }   
          
    });
}

function save_proposal_cost(proposal_id){

    var cost = $("#id_modal_cost").val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_cost',
          async: false,
          data: {proposal_id: proposal_id, cost:cost},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#cost_modal");
                $("#cost_modal").modal('hide');
                $("#id_cost").html(cost+" &euro;");
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_cost").after(data);
            }
            
         }   
          
    });
}



function save_title(){
    var izena = $("#id_izena").val();
   
   
    $.ajax({
          url: '/ajax_edit_izena',
          async: false,
          data: {izena:izena},
          dataType:'html',
          success : function(data, status, xhr){
            var response=data;
           
            if (response != ""){
            	$('#id_title').text(data); 
            	$('#id_izena').text(data); 
            	         
                //remove_error_messages("#area_modal");
                $("#title_modal").modal('hide');
                //$("#id_arloa").html(response); //BEGIRATU HAU, html kodea ordezkatzen du
                }
            else{
                
                $("#title_modal").modal('hide');
            }
            
         }   
          
    });
}
function save_summary(){
	var deskribapena = $("#id_desk").val();
   
   
    $.ajax({
          url: '/ajax_edit_deskribapena',
          async: false,
          data: {deskribapena:deskribapena},
          dataType:'html',
          success : function(data, status, xhr){
            var response=data;
           
            if (response != ""){
            	$('#id_desk').text(data); 
            	$('#id_summary').text(data); 
            	         
                //remove_error_messages("#area_modal");
                $("#summary_modal").modal('hide');
                //$("#id_arloa").html(response); //BEGIRATU HAU, html kodea ordezkatzen du
                }
            else{
                
                $("#summary_modal").modal('hide');
            }
            
         }   
          
    });
	
	
}

$(document).ready(function(){
$('#attached_documents_form').submit(function(e) {

   var form = $(this);      
   var formdata = false;
   if(window.FormData){
     formdata = new FormData(form[0]);
                   
     }

   var formAction = form.attr('action');

                $.ajax({
                    type        : 'POST',
                    url         : '../ajax_hornitzaile_irudia_gorde',
                    cache       : false,
                    data        : formdata ? formdata : form.serialize(),
                    contentType : false,
                    processData : false,

                    success: function(response) {
                        if(response != 'error') {
                        	 //$('#id_image').text(response);
                        	 $('img#id_image').attr('src', response); //ikusten den irudia
                        	 $('#id_pic').text(response); //pantailaren ezkerrekoa
                        	 $('#hornitzaile_argazkia').text(response); //modal
                        	 
                        	 //$('#id_image').attr('img', response);
                             $("#attached_documents_modal").modal('hide');
                        } else {
                            $('#messages').addClass('alert alert-danger').text(response);
                        }
                    }
                });
                e.preventDefault();
            });
   
});




function save_proposal_summary(proposal_id, selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_summary',
          async: false,
          data: {proposal_id: proposal_id, language:language, summary:summary},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#summary_modal");
                $("#summary_modal").modal('hide');
                if (selected_language == language){
                    $("#id_summary").html(summary);
                }
            }
            else{
                remove_error_messages("#summary_modal");
                $("#id_modal_summary").after(data);
            }                       
         }
        });
   });
}

function save_proposal_recipient(proposal_id, selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_recipient',
          async: false,
          data: {proposal_id: proposal_id, language:language, recipient:recipient},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_modal");
                $("#recipient_modal").modal('hide');
                if (selected_language == language){
                    $("#id_recipient").html(recipient);
                }
            }
            else{
                remove_error_messages("#recipient_modal");
                $("#id_modal_recipient").after(data);
            }                       
         }
        });
   });
}


function save_proposal_necessity(proposal_id, selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_necessity',
          async: false,
          data: {proposal_id: proposal_id, language:language, necessity:necessity},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#necessity_modal");
                $("#necessity_modal").modal('hide');
                if (selected_language == language){
                    $("#id_necessity").html(necessity);
                }
            }
            else{
                remove_error_messages("#necessity_modal");
                $("#id_modal_necessity").after(data);
            }                       
         }
        });
   });
}


function save_proposal_where_IKER(proposal_id, selected_language){
    where_inputs = $("#where_div input");
    $(where_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_proposal_where',
          async: false,
          data: {proposal_id: proposal_id, language:language, where:where},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#where_modal");
                $("#where_modal").modal('hide');
                if (selected_language == language){
                    $("#id_where").html(where);
                }
            }
            else{
                remove_error_messages("#where_modal");
                $("#id_modal_where").after(data);
            }                       
         }
        });
        if (index == 0){
            search(where);
        }
   });
}

function save_where(){
    var kokalekua = $("#id_kokalekua").val();
   
   
    $.ajax({
          url: '/ajax_edit_kokalekua',
          async: false,
          data: {kokalekua:kokalekua},
          dataType:'html',
          success : function(data, status, xhr){
            var response=data;
           
            if (response != ""){
            	$('#id_kokalekua').text(data); 
            	$('#id_where').text(data); 
            	         
                $("#where_modal").modal('hide');
               }
            else{
                
                $("#where_modal").modal('hide');
            }
            
         }   
          
    });
}


function close_proposal_title_IKER(selected_language){
    title_inputs = $("#title_div input");
    $(title_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var title = $(this).val();
        remove_error_messages("#title_modal");
        $("#title_modal").modal('hide');
        if (selected_language == language){
            $("#id_title").html(title);
        }
   });
}


function close_proposal_summary(selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        remove_error_messages("#summary_modal");
        $("#summary_modal").modal('hide');
        if (selected_language == language){
            $("#id_summary").html(summary);
        }
   });
}


function close_proposal_recipient(selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        remove_error_messages("#recipient_modal");
        $("#recipient_modal").modal('hide');
        if (selected_language == language){
            $("#id_recipient").html(recipient);
        }
   });
}

function close_proposal_necessity(selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each(function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        remove_error_messages("#necessity_modal");
        $("#necessity_modal").modal('hide');
        if (selected_language == language){
            $("#id_necessity").html(necessity);
        }
   });
}

function close_proposal_where(selected_language){
    where_inputs = $("#where_div input");
    $(where_inputs).each(function( index, element ){
        
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        remove_error_messages("#where_modal");
        $("#where_modal").modal('hide');
        if (selected_language == language){
            $("#id_where").html(where);
        }
        if (index == 0){
            search(where);
        }
   });
   
   
   
}



function close_proposal_area(){

    var area = $("#area_modal #id_area").val();
    remove_error_messages("#area_modal");
    $.ajax({
          url: '/partaidetzaDEMO/ajax_get_proposal_area',
          async: false,
          data: {area:area},
          dataType:'html',
          success : function(data, status, xhr){           
           remove_error_messages("#area_modal");
           $("#area_modal").modal('hide');
           $("#id_area_p").html(data);

         }   
          
    });   
    
}

function close_proposal_cost(){

    var cost = $("#id_cost").val()+" &euro;";
    remove_error_messages("#cost_modal");
    $("#cost_modal").modal('hide');
    $("#id_cost_p").html(cost);
}



function close_proposal_attached_documents(){
    
    $("#attached_documents_modal").modal('hide');
}

function close_proposal_proposal(){

    var proposal = $("#id_proposal").val();
    remove_error_messages("#proposal_modal");
    $("#proposal_modal").modal('hide');
    $("#id_proposal_p").html(proposal);
}

function close_proposal_state(){

    var state = $("#id_state").val();
    remove_error_messages("#state_modal");
    $.ajax({
          url: '/partaidetzaDEMO/ajax_get_proposal_state',
          async: false,
          data: {state:state},
          dataType:'html',
          success : function(data, status, xhr){           
           remove_error_messages("#state_modal");
           $("#state_modal").modal('hide');
           $("#id_state_p").html(data);

         }   
          
    }); 
}


////////////////////////////////////


function save_project_area(project_id){

    var area = $("#id_modal_area").val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_area',
          async: false,
          data: {project_id: project_id, area:area},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response");
            if (response != ""){
                remove_error_messages("#area_modal");
                $("#area_modal").modal('hide');
                $("#id_area").html(response);
                }
            else{
                remove_error_messages("#area_modal");
                $("#id_modal_area").after(data);
            }
            
         }   
          
    });
}

function save_project_cost(project_id){

    var cost = $("#id_modal_cost").val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_cost',
          async: false,
          data: {project_id: project_id, cost:cost},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#cost_modal");
                $("#cost_modal").modal('hide');
                $("#id_cost").html(cost);
                }
            else{
                remove_error_messages("#cost_modal");
                $("#id_modal_cost").after(data);
            }
            
         }   
          
    });
}



function save_project_title(project_id, selected_language){
    title_inputs = $("#title_div input");
    $(title_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var title = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_title',
          async: false,
          data: {project_id: project_id, language:language, title:title},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#title_modal");
                $("#title_modal").modal('hide');
                if (selected_language == language){
                    $("#id_title").html(title);
                }
            }
            else{
                remove_error_messages("#title_modal");
                $("#id_modal_title").after(data);
            }                       
         }
        });
   });
}

function save_project_summary(project_id, selected_language){
    summary_inputs = $("#summary_div textarea");
    $(summary_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var summary = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_summary',
          async: false,
          data: {project_id: project_id, language:language, summary:summary},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#summary_modal");
                $("#summary_modal").modal('hide');
                if (selected_language == language){
                    $("#id_summary").html(summary);
                }
            }
            else{
                remove_error_messages("#summary_modal");
                $("#id_modal_summary").after(data);
            }                       
         }
        });
   });
}

function save_project_recipient(project_id, selected_language){
    recipient_inputs = $("#recipient_div textarea");
    $(recipient_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var recipient = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_recipient',
          async: false,
          data: {project_id: project_id, language:language, recipient:recipient},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#recipient_modal");
                $("#recipient_modal").modal('hide');
                if (selected_language == language){
                    $("#id_recipient").html(recipient);
                }
            }
            else{
                remove_error_messages("#recipient_modal");
                $("#id_modal_recipient").after(data);
            }                       
         }
        });
   });
}


function save_project_necessity(project_id, selected_language){
    necessity_inputs = $("#necessity_div textarea");
    $(necessity_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var necessity = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_necessity',
          async: false,
          data: {project_id: project_id, language:language, necessity:necessity},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#necessity_modal");
                $("#necessity_modal").modal('hide');
                if (selected_language == language){
                    $("#id_necessity").html(necessity);
                }
            }
            else{
                remove_error_messages("#necessity_modal");
                $("#id_modal_necessity").after(data);
            }                       
         }
        });
   });
}

function save_project_where(project_id, selected_language){
    where_inputs = $("#where_div input");
    $(where_inputs).each( function( index, element ){
        var element_id = $(this).attr('id');
        var language = element_id.split('-')[0].split('_')[2];
        var where = $(this).val();
        $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_where',
          async: false,
          data: {project_id: project_id, language:language, where:where},
          dataType:'html',
          success : function(data, status, xhr){
            response = $(data+" #response").text();
            if (response == "True"){
                remove_error_messages("#where_modal");
                $("#where_modal").modal('hide');
                if (selected_language == language){
                    $("#id_where").html(where);
                }
            }
            else{
                remove_error_messages("#where_modal");
                $("#id_modal_where").after(data);
            }                       
         }
        });
        
        if (index == 0){
            search(where);
        }
   });
}






/* -------------------- */

function load_main_scripts(){
    var date = new Date();
    $('#id_agenda').datepicker({
       beforeShowDay: function(date) {
            var m = date.getMonth(), d = date.getDate(), y = date.getFullYear();
            for (i = 0; i < dates.length; i++) {
                if($.inArray(y + '-' + (m+1) + '-' + d,dates) != -1) {
                    //return [false];
                    return [true, 'to-highlight', ''];
                }
            }
            return [true];

        }
    ,dayNamesMin: day_names,monthNames:month_names, firstDay: 1});
    
}

function load_search_scripts(){
    $("#id_main_search_box").val($("#id_search_query").val());
}

function load_header(corporation_image){
    $("#forget_password").hide();
    $("#forget_button").hide();
    $("#forget_text").hide();
    
   $('#navbar-wrapper').css("background-image","url('"+corporation_image+"')");


    $('.selectpicker').selectpicker({
        style: 'btn-default',
        size: false
    });
    
    $('.navbar-toggler').on('click', function(event) {
		event.preventDefault();
		$(this).closest('.navbar-minimal').toggleClass('open');
	});

    if ($("#id_file").length)
        $("#id_file").on('change', function(event) {
		$("#corporation_image_form").submit();
	});

    $("#delete_corporation").click(function(){
        delete_corporation_image();

    });

    $(document).ready(function(){
    /*$(".dropdown").click(            
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideDown("400");
            $(this).toggleClass('open');        
        },
        function() {
            $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideUp("400");
            $(this).toggleClass('open');       
        }
    );*/
    
    $(".menu_explanation").toggle()
    $('.menu_option').hover(
          function () {
            $("#"+$(this).attr('id')+"_explanation").toggle();
          }, 
          function () {
            $("#"+$(this).attr('id')+"_explanation").toggle();
          }
        );
});
}


function delete_corporation_image(){
    $.ajax({
          url: '/partaidetzaDEMO/ajax_delete_corporation_image',
          async: false,
          data: {},
          dataType:'html',
          success : function(data, status, xhr){
	      location = location; 
          }
    });

}

function submit_search(){
    $("#id_search_query").val($("#id_main_search_box").val());
    $('#search_form_id').submit();
}
    

function more_like_this_in(input_element, type, where){
    var input_element_id = $(input_element).attr('id');
    var language = input_element_id.split('-')[0].split('_')[2];
    var query = $(input_element).val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_more_like_this_in_'+where,
          async: false,
          data: {query:query, language:language, type:type},
          dataType:'html',
          success : function(data, status, xhr){
            if (data.indexOf("<li>") >= 0){
                $("#related_objects_"+where).hide();
                $("#related_objects_"+where+" ul").remove();
                var old_html = $("#related_objects_"+where).html();
                $("#related_objects_"+where).html(old_html+data);
                $("#related_objects_"+where).show(1000);
            }
            else{
                $("#related_objects_"+where).hide(1000);
            }
          } 
    });
}

function correct_language(input_element, where){
    var input_element_id = $(input_element).attr('id');
    var language = input_element_id.split('-')[0].split('_')[2]; 
    var text = $(input_element).val();
    if (text!=""){
        $.ajax({
              url: '/partaidetzaDEMO/ajax_correct_language',
              async: false,
              data: {language:language, text:text},
              dataType:'html',
              success : function(data, status, xhr){            
               var response;
               response = $(data+" #response").text(); 
               if (response=="True"){
                $("#language_error_"+where).hide(1000);
               }
               else{
                $("#language_error_"+where).show(1000);
               }
              } 
        });
    }

}


function validate_input_languages(){
    var no_errors = true;
    var json = create_proposal_json();
    
    

}

function create_language_json(element, type, json){
    $('#'+element+'_div '+type).each(function() {        
        var input_element_id = $(this).attr('id');
        var language = input_element_id.split('-')[0].split('_')[2]; 
        var text = $(this).val();
        json[element+'_'+language]=text;
    });
    
    return json;
}


function language_validation_dialog(message) {
    $("#dialog-confirm").html(message);

    // Define the Dialog and its properties.
    try{
    $("#dialog-confirm").dialog({
        resizable: false,
        modal: true,
        title: "Modal",
        height: 250,
        width: 400,
        buttons: {
            "Yes": function () {
                $(this).dialog('close');
                
                try{
                    $("#id_new_proposal_button").attr("onclick","");
                    $("#id_new_proposal_button").click();
                }
                catch(error){}
                try{
                    $("#id_new_accepted_proposal_button").attr("onclick","");
                    $("#id_new_accepted_proposal_button").click();
                }
                catch(error){}
            },
                "No": function () {
                $(this).dialog('close');
                return false;
            }
        }
    });
    }
    catch(ex){
        alert(ex);
    }
}

function validate_language(message){
    var json = {};
    json = create_language_json("title", "input", json);
    json = create_language_json("summary", "textarea", json);
    json = create_language_json("recipient", "textarea", json);
    json = create_language_json("necessity", "textarea", json);
    json = create_language_json("where", "textarea", json);

    var ajax_response;
    $.when($.ajax({
          url: '/partaidetzaDEMO/ajax_validate_language',
          async: false,
          data: json,
          dataType:'json',
          complete: function(jqXHR,status)
            {
                if (jqXHR.responseText.indexOf("False") >= 0){
                    ajax_response = false;
                }
                else{
                    ajax_response = true;
                }
            }
            
        })
        );
    

    if (!ajax_response){
        language_validation_dialog(message);
    }
    return ajax_response;
}


function load_add_event_scripts(){
    
    $('#id_date').datepicker({dayNamesMin: day_names,monthNames:month_names, firstDay: 1});

    $('#event_div textarea').focusout(function() {
        //more_like_this_in($(this),"Event", "event");
        correct_language($(this),"event");
    });
}

function load_agenda_scripts(){
    
    var date = new Date();
    $('#id_agenda').datepicker({
       beforeShowDay: function(date) {
            var m = date.getMonth(), d = date.getDate(), y = date.getFullYear();
            for (i = 0; i < dates.length; i++) {
                if($.inArray(y + '-' + (m+1) + '-' + d,dates) != -1) {
                    //return [false];
                    return [true, 'to-highlight', ''];
                }
            }
            return [true];

        }
    ,dayNamesMin: day_names,monthNames:month_names, firstDay: 1});
   
}

function load_add_proposal_scripts(){
    
    /*$('#area_modal').on('shown.bs.modal', function () {
      $("#area_modal #id_area").chosen();
    });*/
    
    $(".upload_p input").change(function(){
    readURL(this);
    });

    $(function() {
        $('.upload_p').formset({
    });
    $('#title_div input').focusout(function() {
        more_like_this_in($(this),"Proposal", "title");
        correct_language($(this),"title");
    });
    $('#summary_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "summary");
        correct_language($(this),"summary", "summary");
    });
    $('#recipient_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "recipient"); 
        correct_language($(this),"recipient", "recipient");       
    });
    $('#necessity_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "necessity");
        correct_language($(this),"necessity", "necessity");
    });
    /*$('#where_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "where");
        correct_language($(this),"where", "where");
    });*/
  })
    
}

function load_add_accepted_proposal_scripts(){
    
    /*$('#area_modal').on('shown.bs.modal', function () {
      $("#id_area").chosen();
    });*/
    
    $(".upload_p input").change(function(){
    readURL(this);
    });
    
    
    $('#title_div input').focusout(function() {
        more_like_this_in($(this),"Proposal", "title");
        correct_language($(this),"title");
    });
    $('#summary_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "summary");
        correct_language($(this),"summary", "summary");
    });
    $('#recipient_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "recipient"); 
        correct_language($(this),"recipient", "recipient");       
    });
    $('#necessity_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "necessity");
        correct_language($(this),"necessity", "necessity");
    });
    /*$('#where_div textarea').focusout(function() {
        more_like_this_in($(this),"Proposal", "where");
        correct_language($(this),"where", "where");
    });*/
    
  }
    




function paginated_search(url){
    $('#search_form_id').attr('action',$('#search_form_id').attr('action')+url);
    $('#search_form_id').submit();
}


/* VOTE SYSTEM */

function mark_as_voted(id){
    $( "#id_vote_show_"+id ).addClass("voted");
    $( "#id_vote_show_"+id ).attr('disabled', true);
}

function vote_via_ajax(project_id){
    $.ajax({
          url: '/partaidetzaDEMO/ajax_vote',
          async: false,
          data: {project_id:project_id},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                // mark as voted
                mark_as_voted(project_id);
                // Increment votes
                var votes = parseInt($( "#id_vote_show_"+project_id ).prev().find("span").text());
                votes ++;
                $( "#id_vote_show_"+project_id ).prev().find("span").text(votes);
            }
                       
               
          }
    });
}

/* FOND SYSTEM */

function mark_as_fonded(id){
    $( "#id_fond_show_"+id ).addClass("voted");
    $( "#id_fond_show_"+id ).attr('disabled', true);
}

function fond_via_ajax(proposal_id){
    $.ajax({
          url: '/partaidetzaDEMO/ajax_fond',
          async: false,
          data: {proposal_id:proposal_id},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();
            if (response == "True"){
                // mark as fonded
                mark_as_fonded(proposal_id);
                // Increment fonds
                var fonds = parseInt($( "#id_fond_show_"+proposal_id ).prev().find("span").text());
                fonds ++;
                $( "#id_fond_show_"+proposal_id ).prev().find("span").text(fonds);
            }
                       
               
          }
    });
}

function show_hide_related(link){
    var span = $(link).find("span");
    if (span.hasClass("glyphicon-plus")){
        span.attr("class","glyphicon glyphicon-minus");
        $("#related p").each( function( index, element ){
            if ($(this).hasClass("to_hide")){
                $(this).attr("class","to_hide");
            }
        });
    }
    else{
        span.attr("class","glyphicon glyphicon-plus");
        $("#related p").each( function( index, element ){
            if ($(this).hasClass("to_hide")){
                $(this).attr("class","to_hide hidden");
            }
        });
    }
}


/* ---------------- MAP -------------------- */


function add_point_to_map_proposal(latlng,proposal_id){

    $.ajax({
          url: '/partaidetzaDEMO/ajax_add_point_to_map_proposal',
          async: false,
          data: {proposal_id:proposal_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}

function add_point_to_map_project(latlng,project_id){

    $.ajax({
          url: '/partaidetzaDEMO/ajax_add_point_to_map_project',
          async: false,
          data: {project_id:project_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}
            
            
function delete_point_from_map_proposal(latlng,proposal_id){

    $.ajax({
          url: '/partaidetzaDEMO/ajax_delete_point_from_map_proposal',
          async: false,
          data: {proposal_id:proposal_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}
            
function delete_point_from_map_project(latlng,project_id){

    $.ajax({
          url: '/partaidetzaDEMO/ajax_delete_point_from_map_project',
          async: false,
          data: {project_id:project_id,lat:latlng[0],lng:latlng[1]},
          dataType:'html',
          success : function(data, status, xhr){
            var response;
            response = $(data+" #response").text();            
          }
    });
}

function search(query){
    $.ajax({
          url: 'http://nominatim.openstreetmap.org/search',
          async: false,
          data: {q:query,format:'json'},
          dataType:'json',
          success : function(data, status, xhr){
            var show = false;
            $("#map_ul_id").html('');
            $("#map_where").hide(1000);
            $(data).each( function( index, element ){
                $("#map_ul_id").append('<li><a href="#" onclick="global_map.panTo(new L.LatLng('+$(this)[0].lat+','+$(this)[0].lon+'));return false;">'+$(this)[0].display_name+'</a></li>');
                show=true;
            });
            if (show){
                $("#map_where").show(1000);
            }
            //var lat= data[0].lat;
            //var lon = data[0].lon;
            //L.marker([lat,lon]).on("click",function(e) {global_map.removeLayer(this);}).on("click",function(e) {global_map.removeLayer(this);layer_array=jQuery.grep(layer_array, function(value) {return $(value).not([e.latlng.lat,e.latlng.lng]).length === 0 && $([e.latlng.lat,e.latlng.lng]).not(value).length === 0})}).addTo(global_map);
            //global_map.panTo(new L.LatLng(lat,lon));
          }
    });
}
//////////////////////////////////////////


function print_page(){
    window.print();
}

function restore_password(){
    $.ajax({
          url: '/partaidetzaDEMO/restore_password',
          async: false,
          data: {email:$("#id_email").val()},
          dataType:'html',
          success : function(data, status, xhr){
            $("#forget_text").toggle();
          }
    });

}

function hide_all_charts(id){
    $(".featured-article").hide();
    $("#"+id).show();
}


function save_proposal_phase(proposal_id,select,text){
    var phase_id;
    phase_id=$(select).val();
    if (phase_id!='7'){
            $.ajax({
                  url: '/partaidetzaDEMO/ajax_edit_proposal_phase',
                  async: false,
                  data: {proposal_id:proposal_id,phase_id:phase_id},
                  dataType:'html',
                  success : function(data, status, xhr){
                    $('#info-text p').html(text);
                    $('#info-text').modal('toggle');
		    setTimeout(function(){
	                $("#info-text").modal('hide');
        	    }, 3000);

                  },
                  error: function(data, status, xhr){
                    alert('zerbait gaizki joan da');//$('#myModal').modal('toggle');
                  }
                  
            }); 
    }
    else{ //Proposal has been rejected, ask why?

        $("#proposal_hidden_id").val(proposal_id)
        $("#phase_modal").modal('toggle');
        
    }    
}

function save_proposal_phase_rejection(proposal_id,select,rejection_text,text){
    var phase_id;
    rejection_id=$(select).val();
    if (rejection_id=='0'){
        rejection_id = rejection_text;
    }
            $.ajax({
                  url: '/partaidetzaDEMO/ajax_edit_proposal_phase_rejection',
                  async: false,
                  data: {proposal_id:proposal_id,rejection_id:rejection_id},
                  dataType:'html',
                  success : function(data, status, xhr){
                    $('#phase_update').modal('toggle');
                    $('#info-text p').html(text);
                    $('#info-text').modal('toggle');
                    setTimeout(function(){
	                $("#info-text").modal('hide');
        	    }, 3000);

                  },
                  error: function(data, status, xhr){
                    alert('zerbait gaizki joan da');//$('#myModal').modal('toggle');
                  }
                  
            }); 
}


function save_project_status(project_id,select,text){
    var status_id;
    status_id=$(select).val();
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_project_status',
          async: false,
          data: {project_id:project_id,status_id:status_id},
          dataType:'html',
          success : function(data, status, xhr){
            $('#info-text p').html(text);
            $('#info-text').modal('toggle');
	    setTimeout(function(){
                $("#info-text").modal('hide');
            }, 3000);

          },
          error: function(data, status, xhr){
            alert('Arazoren bat egon da');
          }
          
    }); 
}


function set_theme(theme_id){
    
    $.ajax({
          url: '/partaidetzaDEMO/ajax_edit_theme',
          async: false,
          data: {theme_id:theme_id},
          dataType:'html',
          success : function(data, status, xhr){
            location.reload(true);
          },
          error: function(data, status, xhr){
            alert('Arazoren bat egon da');
          }
          
    }); 
}


