import uuid
from typing_extensions import Self

from django.db import models
from django.utils.safestring import mark_safe

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from wagtailstreamforms.models.form import Form


class FormPage(Page):
    form = models.ForeignKey(Form, on_delete=models.PROTECT)

    parent_page_types = ['example.FormIndexPage']
    subpage_types = []

    @classmethod
    def create_or_update(cls, form: Form) -> Self:
        if FormPage.objects.filter(form__pk=form.pk).exists():
            form_page = FormPage.objects.get(form__pk=form.pk)
            form_page.title = form.title
            form_page.slug = form.slug
            form_page.save()
            return form_page

        form_index_page = FormIndexPage.get_or_create()
        form_page = FormPage(slug=form.slug, title=form.title, form=form)

        form_index_page.add_child(instance=form_page)
        return form_page

    def get_context(self, request, *args, **kwargs):
        form: Form = self.form.get_form()
        form.fields['form_id'].initial = self.form.pk
        form.fields['form_reference'].initial = uuid.uuid4()
        form.model = self.form
        rendered_form = form.renderer.render(
            template_name="streamforms/form_block.html",
            context=form.get_context(),
            request=request
        )
        return {
            **super().get_context(request, *args, **kwargs),
            "form": mark_safe(rendered_form),
        }


class FormIndexPage(Page):
    description = RichTextField(
        default="Liste des formulaires",
        help_text="Descrition de la page des formulaire, visible par le public",
    )

    content_panels = [FieldPanel("title"), FieldPanel("description")]
    parent_page_types = []
    subpage_types = ['example.FormPage']

    def get_context(self, request, *args, **kwargs):
        return {
            **super().get_context(request, *args, **kwargs),
            'form_pages': FormPage.objects.live(),
        }

    @classmethod
    def get_or_create(cls) -> Self:
        if FormIndexPage.objects.count() > 0:
            return FormIndexPage.objects.first()

        home_page = Page.objects.get(slug='home')
        form_index_page = FormIndexPage(
            title="Formulaires",
            slug="formulaires",
            depth=home_page.depth + 1
        )
        home_page.add_child(instance=form_index_page)
        return form_index_page
