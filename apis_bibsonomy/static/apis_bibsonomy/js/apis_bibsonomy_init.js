function reinitialize_bibsonomy_tooltips() {
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
		functionInit: function (instance, helper) {
			try {
				$('#bibs-form select.listselect2').select2('destroy')
			} catch (err) { console.log(err) } //fixme: shouldnt be needed to destroy and build again
			$deepc = $('#bibs-form').clone(deepWithDataAndEvents = true)
			$form_id = 'bibs-form_' + ($('#bibs-form').length + 1)
			$deepc.attr('id', $form_id)
			$bib = helper.origin.dataset
			$deepc.children('input#id_object_id').val($bib.bibsObject_pk)
			$deepc.children('input#id_content_type').val($bib.bibsContenttype)
			$deepc.children('input#id_attribute').val($bib.bibsAttribute)
			$res = $('<div class="bibs-container"><table class="table"><thead><tr><td>delete</td><td>authors</td><td>title</td><td>year</td><td>Pages Start</td><td>Pages End</td><td>Folio</td><td>Notes</td><td>Detail</td></tr></thead><tbody></tbody></table></div>')
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
		},
		functionBefore: function (instance, helper) {
			$bib = helper.origin.dataset
			$.ajax({
				url: $('#bibs-form').attr('action'),
				type: 'get',
				data: { 'contenttype': $bib.bibsContenttype, 'object_pk': $bib.bibsObject_pk, 'attribute': $bib.bibsAttribute },
				complete: function (data) {
					$('div.bibs-container > table > tbody').html('');
					$('div.bibs-container > div#bibs-messages').html('');
					data.responseJSON.forEach(function (entry) {
						$('div.bibs-container > table > tbody').append($('<tr id="bib-entry-' + entry.pk + '"><td><a href="#" data-bib-id="' + entry.pk + '" class="delete-bib-entry"><i data-feather="trash"></i></a></td><td>' + entry.author + '</td><td>' + entry.title + '</td><td>' + entry.year + '</td><td>' + entry.pages_start + '</td><td>' + entry.pages_end + '</td><td>' + entry.folio + '</td><td>' + entry.notes + '</td><td><a href="/bibsonomy/references/'+entry.pk+'"><i data-feather="book-open"></a></td></tr>'))
					});
					feather.replace()
				}
			})
		}
	})
}
$(document).ready(function () {
	$(".bibsonomy-anker-hidden").each(function () {
		var form_data = $(this).data('bibs-form-elements')
		var entity_type = $(this).data('bibs-contenttype')
		if (form_data) {
			form_data = form_data.split("|")
			var obj_pk = $(this).data('bibs-object_pk')
			var f = $(this).parents('.card-body')
			form_data.forEach(function (item) {
				if (el !== null) {
					var node = document.createElement("a");
					node.setAttribute("class", "bibsonomy-anker")
					node.setAttribute("data-bibs-contenttype", entity_type)
					node.setAttribute('data-bibs-object_pk', obj_pk)
					node2 = document.createElement('i');
					node2.setAttribute('data-feather', "book-open")
					node2.setAttribute('style', 'margin-bottom: .5rem')
					node.append(node2)
					if (item != 'self') {
						var el = document.getElementById('div_id_' + item);
						if (el) {
							node.setAttribute('data-bibs-attribute', item)
							el.prepend(node)
						}
					} else {
						$('h1').prepend(node)
					}
				}
			});
			feather.replace()

		}
	});
	reinitialize_bibsonomy_tooltips();
});

$(document).on('submit', 'button.bibsonomy-anker', function (event) {
	event.preventDefault();
	event.stopPropagation();
})

$(document).on('submit', 'form.bibs-forms', function (event) {
	event.preventDefault();
	event.stopPropagation();
	var form_data = $(this).serialize();
	var post_url = $(this).attr("action");
	var form_object = $(this);
	$(this).parent().children('div#bibs-messages').html('')
	$.ajax({
		url: post_url,
		type: 'post',
		data: form_data,
		complete: function (response) {
			if (response.status != 201) {
				form_object.parent().children('div#bibs-messages').append($('<div class="alert alert-danger" role="alert">' + response.responseJSON.message + '</div>'))
			}
			else {
				form_object.parent().children('div#bibs-messages').append($('<div class="alert alert-primary" role="alert">' + response.responseJSON.message + '</div>'))
			}
		}
	})
})


$(document).on('click', 'a.delete-bib-entry', function (event) {
	event.preventDefault();
	event.stopPropagation();
	var post_url = $('#bibs-form').attr("action");
	var pk = $(this).data('bib-id')
	$.ajax({
		url: post_url,
		type: 'delete',
		data: { 'pk': pk },
		beforeSend: function (request) {
			var csrftoken = getCookie('csrftoken');
			request.setRequestHeader("X-CSRFToken", csrftoken);
		},
		complete: function (response) {
			if (response.status == 204) {
				$('#bib-entry-' + pk).remove()
			}
		}
	})
})
