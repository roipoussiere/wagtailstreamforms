from wagtail import hooks

from .models import FormIndexPage


@hooks.register("construct_explorer_page_queryset")
def on_construct_explorer_page_queryset(parent_page, pages, request):
    if isinstance(parent_page, FormIndexPage):
        return []

    return pages
