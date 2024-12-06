document.querySelectorAll(".bibsonomydialog").forEach(element => {
  element.addEventListener("mousedown", function(evt) {
    evt.target == this && this.close();
  });
});
add_select2_reinit_listener();
reinit_select2();

function tohtml(item) {
    const span = document.createElement('span');
    span.innerHTML = item.text;
    return span;
}
function reinit_select2() {
  document.querySelectorAll(".listselect2, .modelselect2multiple, .modelselect2").forEach(element => {
    $(element).select2({
      ajax: {
        url: $(element).data("autocomplete-light-url"),
      },
      dropdownParent: $(element.form),
      templateResult: tohtml,
      templateSelection: tohtml,
    });
  });
  $('.select2-selection').addClass("form-control");
  autoFillBibsonomyForm();

}
function add_select2_reinit_listener() {
  document.body.addEventListener("reinit_select2", function(evt) {
    reinit_select2()
    autoFillBibsonomyForm();
  });
}

function autoFillBibsonomyForm() {
  last_bibsonomy_reference = document.getElementById("last_bibsonomy_reference");
  if (last_bibsonomy_reference) {
    $('select.listselect2').each(function() {
      var newOption = new Option(last_bibsonomy_reference.dataset.title, last_bibsonomy_reference.dataset.url, true, true);
      $(this).append(newOption).trigger("change");
    });
  }
}
