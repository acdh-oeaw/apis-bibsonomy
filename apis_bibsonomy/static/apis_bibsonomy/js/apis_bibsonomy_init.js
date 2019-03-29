$( document ).ready(function() {
	if ($("[data-bib-entity-type]").length > 0) {
		$.ajax({
			type: 'GET',
                	url: '/bibsonomy/save_get/',
                	success: function(data) {
				  if (typeof $.apisbibform == 'undefined') {
				      $.apisbibform = {}; };
				$.apisbibform = data;
				$('body').append('<div id="tooltipster-templates" style="display: none"><form id="apis-bib-form-1"></form></div>')
				var form1 = $.parseHTML(data);
				$("#apis-bib-form-1").append(form1)
				$('#apis-bib-form-1 > p').wrap('<div class="form-group"></div>')

	$("[data-bib-entity-type]").tooltipster({
		contentCloning: true,
		interactive: true,
})
                    	},
                	error: function(error) {
                    		console.log(error)
                }
		})
	};
});
