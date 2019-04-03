$( document ).ready(function() {
	$(".bibsonomy-anker").tooltipster({
		contentCloning: true,
		interactive: true,
		content: 'loading...',
		contentAsHtml: true,
		trigger: 'click',
		minWidth: 600,
		maxWidth: 600,
		maxHeight: 400,
		zIndex: 900,
		functionInit: function(instance, helper){
			console.log(instance.content)
			$('#bibs-form select.listselect2').select2('destroy')
			$deepc = $('#bibs-form').clone(deepWithDataAndEvents=true)
			$form_id = 'bibs-form_'+($('#bibs-form').length+1)
			$deepc.attr('id', $form_id)
			$bib = helper.origin.dataset
			$deepc.children('input#id_object_id').val($bib.bibsObject_pk)
			$deepc.children('input#id_content_type').val($bib.bibsContenttype)
			$deepc.children('input#id_attribute').val($bib.bibsAttribute)
			$res = $('<div class="bibs-container"><table class="table"><thead><tr><td>authors</td><td>title</td><td>year</td></tr></thead><tbody></tbody></table></div>')
			$res.append($deepc)
			$res.append($('<div id="bibs-messages"></div>'))
			instance.content($res)
			$('#bibs-form select.listselect2').select2({
        allowClear: true,
          ajax: {
            url: $('#bibs-form select.listselect2').data('autocomplete-light-url'),
            dataType: 'json'
            // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
          }
        });
			console.log(instance.content)
		},
		functionBefore: function(instance, helper) {	
			$bib = helper.origin.dataset
			$.ajax({
				url: $('#bibs-form').attr('action'),
				type: 'get',
				data: {'contenttype': $bib.bibsContenttype, 'object_pk': $bib.bibsObject_pk, 'attribute': $bib.bibsAttribute},
				complete: function(data){
					console.log(data)
					$('div.bibs-container > table > tbody').html('');
					$('div.bibs-container > div#bibs-messages').html('');
					data.responseJSON.forEach(function(entry) {
						$('div.bibs-container > table > tbody').append($('<tr><td>'+entry.author+'</td><td>'+entry.title+'</td><td>'+entry.year+'</td></tr>'))
				});
				}
			})
		}
})
});

$(document).on('submit', 'form.bibs-forms', function(event){
	event.preventDefault();
	event.stopPropagation();
	var form_data = $(this).serialize();
	var post_url = $(this).attr("action");
	var form_object = $(this);
	$(this).parent().children('div#bibs-messages').html('')
	$.ajax({
		url : post_url,
		type: 'post',
		data : form_data,
		complete: function(response){
			if (response.status != 201){
				form_object.parent().children('div#bibs-messages').append($('<div class="alert alert-danger" role="alert">'+response.responseJSON.message+'</div>'))}
			else {
				form_object.parent().children('div#bibs-messages').append($('<div class="alert alert-primary" role="alert">'+response.responseJSON.message+'</div>'))
			}
	}
	})
})
