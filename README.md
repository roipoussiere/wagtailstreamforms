# Wagtail StreamForms

![](https://github.com/labd/wagtailstreamforms/workflows/Python%20Tests/badge.svg)
![](https://codecov.io/gh/labd/wagtailstreamforms/branch/master/graph/badge.svg)
![](https://img.shields.io/pypi/v/wagtailstreamforms.svg)
![](https://img.shields.io/github/stars/labd/wagtailstreamforms.svg?style=social&logo=github)

Allows you to build forms in the CMS admin area and add them to any StreamField in your site.
You can add your own fields along with the vast array of default fields which include the likes
of file fields. Form submissions are controlled by hooks that you can add that process the forms cleaned data.
Templates can be created which will then appear as choices when you build your form,
allowing you to display and submit a form however you want.

## Backwards Compatibility

Please note that due to this package being virtually re-written for version 3, you cannot upgrade any existing
older version of this package to version 3 and onwards.
If you have an existing version installed less than 3 then you will need to completely remove it including
tables and any migrations that were applied in the databases ``django_migrations`` table.

Older versions:

If you are using a version of wagtail 1.x, then the latest compatible version of this package is 1.6.3:

    pip install wagtailstreamforms<2

Other wise you must install a version of this package from 2 onwards:

    pip install wagtailstreamforms>=2

## What else is included?

*  Each form is built using a StreamField.
*  Customise things like success and error messages, post submit redirects and more.
*  Forms are processed via a `before_page_serve` hook. Meaning there is no fuss like remembering to include a page mixin.
*  The hook can easily be disabled to provide the ability to create your own.
*  Form submissions are controlled via hooks meaning you can easily create things like emailing the submission which you can turn on and off on each form.
*  Fields can easily be added to the form from your own code such as Recaptcha or a Regex Field.
*  The default set of fields can easily be replaced to add things like widget attributes.
*  You can define a model that will allow you to save additional settings for each form.
*  Form submissions are also listed by their form which you can filter by date and are ordered by newest first.
*  Files can also be submitted to the forms that are shown with the form submissions.
*  A form and its fields can easily be copied to a new form.
*  There is a template tag that can be used to render a form, in case you want it to appear outside a StreamField.

## Documentation

Can be found on `readthedocs <http://wagtailstreamforms.readthedocs.io/>`_.

## Screenshots

Example Front End:

![](./docs/_static/images/screen_1.png)

Form Fields Selection:

![](./docs/_static/images/screen_3.png)

## Example site

Installation

    git clone https://github.com/roipoussiere/wagtailstreamforms.git
    cd wagtailstreamforms
    python manage.py migrate
    python manage.py createsuperuser

Run

    python manage.py runserver

Go to http://127.0.0.1:8000
