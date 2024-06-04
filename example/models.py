import uuid
from typing_extensions import Self

from slugify import slugify

from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.blocks.stream_block import StreamValue

from wagtailstreamforms.blocks import WagtailFormBlock
from wagtailstreamforms.models.abstract import AbstractFormSetting
from wagtailstreamforms.models import Form


FORM_INDEX_PAGE_TITLE = "Forms"


class AdvancedFormSetting(AbstractFormSetting):
    to_address = models.EmailField()


class FormPage(Page):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel('form'),
    ]

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
        return {
            **super().get_context(request, *args, **kwargs),
            "form_block": self.form.get_form(),
        }


class FormIndexPage(Page):
    show_in_menus_default = True

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
            title=FORM_INDEX_PAGE_TITLE,
            slug=slugify(FORM_INDEX_PAGE_TITLE),
            depth=home_page.depth + 1
        )
        home_page.add_child(instance=form_index_page)
        return form_index_page
