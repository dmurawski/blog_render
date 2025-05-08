from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse

from .models import Comment


class SearchForm(forms.Form):
    query = forms.CharField()


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
            HTML("<hr>"),
            Fieldset(
                "Kontakt",  # Druga sekcja
                FloatingField("email"),
                FloatingField("to"),
            ),
            HTML("<hr>"),
            Fieldset(
                "Wiadomość",  # Trzecia sekcja
                Field("comments", rows="5", cols="0"),
                cols="12",
            ),
            Submit("submit", "Send e-mail", css_class="btn btn-primary col-12 fw-bold"),
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")

    def __init__(self, *args, **kwargs):
        post_id = kwargs.pop("post_id", None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"

        if post_id:
            self.helper.form_action = reverse(
                "blog:post_comment", kwargs={"post_id": post_id}
            )

        self.helper.form_class = "form-horizontal mt-5"
        self.helper.label_class = "col-sm-3 col-form-label"
        self.helper.field_class = "p-2"

        self.helper.layout = Layout(
            Fieldset(
                "Autor komentarza",
                FloatingField("name", placeholder="Your name"),
                FloatingField("email", placeholder="Your email"),
            ),
            HTML("<hr>"),
            Fieldset(
                "Treść komentarza",
                FloatingField("body", placeholder="Napisz coś..."),
            ),
            Submit(
                "submit", "Dodaj komentarz", css_class="btn btn-primary col-12 fw-bold"
            ),
        )
