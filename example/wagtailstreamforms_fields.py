from django import forms

from wagtail.blocks import RichTextBlock, StructBlock
from wagtailstreamforms.fields import BaseField, register


class RichTextWidget(forms.widgets.Input):
    input_type = "hidden"
    template_name = "example/rich_text_widget.html"
    rich_text = ""

    def get_context(self, *args):
        return {
            **super().get_context(*args),
            "rich_text": self.rich_text,
        }


@register('information_text')
class RichTextField(BaseField):
    field_class = forms.CharField
    widget = RichTextWidget
    icon = "title"
    label = "Information text"

    def get_options(self, block_value):
        self.widget.rich_text = block_value["label"]
        return super().get_options(block_value)

    def get_form_block(self):
        return StructBlock(
            [("label", RichTextBlock())],
            icon=self.icon,
            label=self.label,
        )
