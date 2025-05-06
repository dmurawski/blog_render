from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import Field, Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="",
    )

    def __init__(self, *args, **kwargs):
        post_id = kwargs.pop("post_id", None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse(
            "blog:post_share", kwargs={"post_id": post_id}
        )
        self.helper.form_class = "form-horizontal mt-5"
        self.helper.label_class = "col-sm-3 col-form-label"
        self.helper.field_class = "p-2"

        self.helper.layout = Layout(
            Fieldset(
                "Imię",  # Tytuł sekcji
                FloatingField("name", placeholder="Your first name"),
            ),
            Fieldset(
                "Kontakt",  # Druga sekcja
                FloatingField("email"),
                FloatingField("to"),
            ),
            Fieldset(
                "Wiadomość",  # Trzecia sekcja
                Field("comments", label="", rows="5", cols="0"),
                cols="12",
            ),
            Submit("submit", "Send e-mail", css_class="btn btn-primary col-12 fw-bold"),
        )
