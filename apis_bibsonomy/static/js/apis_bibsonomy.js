function tohtml(item) {
  var $result = $('<span>');
  $result.html(item.text);
  return $result;
}
function activateBibsonomyDialog(element_id) {
  dialog = document.getElementById(element_id);
  dialog.showModal();
  dialog.querySelectorAll(".dalform").forEach(form => {
    form.querySelectorAll(".listselect2").forEach(element => {
      $(element).select2({
        ajax: {
          url: $(element).data("autocomplete-light-url"),
        },
        dropdownParent: $(form),
        templateResult: tohtml,
        templateSelection: tohtml,
      });
    });
  });
}
