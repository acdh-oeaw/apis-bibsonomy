document.querySelectorAll(".bibsonomydialog").forEach(element => {
  element.addEventListener("mousedown", function(evt) {
    evt.target == this && this.close();
  });
});
