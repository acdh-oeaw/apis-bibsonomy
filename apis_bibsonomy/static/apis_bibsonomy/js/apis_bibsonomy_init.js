$( document ).ready(function() {
console.log('got it');
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
			console.log(helper)
			$bib = helper.origin.dataset
			console.log($bib)
			$deepc.children('input#id_object_id').val($bib.bibsObject_pk)
			$deepc.children('input#id_content_type').val($bib.bibsContenttype)
			$deepc.children('input#id_attribute').val($bib.bibsAttribute)
			$res = $('<div class="bibs-container"><table class="table"><thead><tr><td>authors</td><td>title</td><td>year</td></tr></thead><tbody></tbody></table></div>')
			$res.append($deepc)
			instance.content($res)
			console.log('#'+$form_id+' input#id_content_type')
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
			console.log($bib)
			$.ajax({
				url: $('#bibs-form').attr('action'),
				type: 'get',
				data: {'contenttype': $bib.bibsContenttype, 'object_pk': $bib.bibsObject_pk, 'attribute': $bib.bibsAttribute},
				complete: function(data){
					console.log(data)
					$('div.bibs-container > table > tbody').html('');
					data.responseJSON.forEach(function(entry) {
    						console.log(entry);
						console.log(instance)
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
	console.log($(this))
	console.log('worked through')
	var form_data = $(this).serialize();
	var post_url = $(this).attr("action");
	$.ajax({
		url : post_url,
		type: 'post',
		data : form_data
	}).done(function(response){
		console.log(response);
	});

})
