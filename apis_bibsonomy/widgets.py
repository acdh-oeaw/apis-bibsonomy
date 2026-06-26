from django.forms.widgets import Input


class Autocomplete(Input):
    template_name = "widgets/autocomplete.html"

    class Media:
        js = ["js/widgets/autocomplete.js"]
        css = {"all": ["css/widgets/autocomplete.css"]}
