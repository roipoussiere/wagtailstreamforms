import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from wagtail.admin import panels
from wagtail.models import Site
from wagtail.fields import RichTextField

from modelcluster.fields import ParentalManyToManyField
from slugify import slugify

from wagtailstreamforms import hooks
from wagtailstreamforms.fields import HookSelectField
from wagtailstreamforms.forms import FormBuilder
from wagtailstreamforms.streamfield import FormFieldsStreamField
from wagtailstreamforms.utils.general import get_slug_from_string
from wagtailstreamforms.utils.loading import get_advanced_settings_model
from wagtailstreamforms.models.submission import FormSubmission


class FormQuerySet(models.QuerySet):
    def for_site(self, site):
        """Return all forms for a specific site."""
        return self.filter(site=site)

def get_default_slug():
    return str(uuid.uuid4())

class AbstractForm(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
        default=get_default_slug,
    )
    fields = FormFieldsStreamField([], verbose_name=_("Fields"))
    submit_button_text = models.CharField(
        _("Submit button text"), max_length=100, default="Envoyer"
    )
    success_message = models.CharField(
        _("Success message"),
        blank=True,
        max_length=255,
        help_text=_("An optional success message to show when the form has been successfully submitted"),
    )
    post_redirect_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Post redirect page"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text=_("The page to redirect to after a successful submission"),
    )
    process_form_submission_hooks = HookSelectField(verbose_name=_("Submission hooks"), blank=True)

    # TODO: use a mixin for each tab?
    # TODO: allow to use tags in emails: [form_url], [form_name], [form_results], [form_result_1]

    email_orga_members = ParentalManyToManyField(
        User,
        blank=True,
        verbose_name=_("Destinataires"),
    )
    email_orga_subject = models.CharField(
        _("Sujet"),
        blank=True,
        max_length=255,
        help_text=_("Laissez vide pour ne pas envoyer de message."),
    )
    email_orga_body = RichTextField(
        _("Contenu"),
        blank=True,
    )
    email_author_subject = models.CharField(
        _("Sujet"),
        blank=True,
        max_length=255,
        help_text=_("Laissez vide pour ne pas envoyer de message."),
    )
    email_author_body = RichTextField(
        _("Contenu"),
        blank=True,
    )

    objects = FormQuerySet.as_manager()

    settings_panels = [
        panels.FieldPanel("title", classname="full"),
        panels.FieldPanel("submit_button_text"),
        panels.FieldPanel("success_message"),
        # FieldPanel("process_form_submission_hooks", classname="choice_field"),
        panels.PageChooserPanel("post_redirect_page"),
    ]

    field_panels = [
        panels.FieldPanel("fields"),
    ]

    action_panels = [
        panels.MultiFieldPanel([
            panels.FieldPanel("email_orga_members"),
            panels.FieldPanel("email_orga_subject"),
            panels.FieldPanel("email_orga_body"),
        ], "E-mail à destination des organisateur.ices"),
        panels.MultiFieldPanel([
            panels.FieldPanel("email_author_subject"),
            panels.FieldPanel("email_author_body"),
        ], "E-mail à destination de la personne ayant rempli le formulaire")
    ]

    edit_handler = panels.TabbedInterface(
        [
            panels.ObjectList(settings_panels, heading=_("General")),
            panels.ObjectList(field_panels, heading=_("Fields")),
            panels.ObjectList(action_panels, heading=_("Actions")),
        ]
    )

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        abstract = True
        ordering = ["title"]
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")

    def copy(self):
        """Copy this form and its fields."""

        form_copy = Form(
            site=self.site,
            title=self.title,
            slug=uuid.uuid4(),
            fields=self.fields,
            submit_button_text=self.submit_button_text,
            success_message=self.success_message,
            post_redirect_page=self.post_redirect_page,
            process_form_submission_hooks=self.process_form_submission_hooks,
        )
        form_copy.save(auto_slug=False)

        # additionally copy the advanced settings if they exist
        SettingsModel = get_advanced_settings_model()

        if SettingsModel:
            try:
                advanced = SettingsModel.objects.get(form=self)
                advanced.pk = None
                advanced.form = form_copy
                advanced.save()
            except SettingsModel.DoesNotExist:
                pass

        return form_copy

    copy.alters_data = True

    def get_data_fields(self):
        """Returns a list of tuples with (field_name, field_label)."""

        data_fields = [("submit_time", _("Submission date"))]
        data_fields += [
            (get_slug_from_string(field["value"]["label"]), field["value"]["label"])
            for field in self.get_form_fields()
        ]
        if getattr(settings, "WAGTAILSTREAMFORMS_SHOW_FORM_REFERENCE", False):
            data_fields += [("form_reference", _("Form reference"))]
        return data_fields

    def get_form(self, *args, **kwargs):
        """Returns the form."""

        form_class = self.get_form_class()
        return form_class(*args, **kwargs)

    def get_form_class(self):
        """Returns the form class."""

        return FormBuilder(self.get_form_fields()).get_form_class()

    def get_form_fields(self):
        """Returns the form field's stream data."""

        form_fields = self.fields._raw_data
        for fn in hooks.get_hooks("construct_submission_form_fields"):
            form_fields = fn(form_fields)
        return form_fields

    def get_submission_class(self):
        """Returns submission class."""

        return FormSubmission

    def process_form_submission(self, form):
        """Runs each hook if selected in the form."""

        for fn in hooks.get_hooks("process_form_submission"):
            if fn.__name__ in self.process_form_submission_hooks:
                fn(self, form)

    def save(self, *args, **kwargs):
        if kwargs.pop("auto_slug", True):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
        for post_save_form_hook in hooks.get_hooks("post_save_form"):
            post_save_form_hook(self)

    def delete(self, *args, **kwargs):
        for pre_delete_form_hook in hooks.get_hooks("pre_delete_form"):
            pre_delete_form_hook(self)
        super().delete(*args, **kwargs)


class Form(AbstractForm):
    pass
