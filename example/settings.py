from os import environ
from os.path import dirname, abspath, join

from django.urls import reverse_lazy

SITE_DIR = dirname(abspath(__file__))


# Security

SECRET_KEY = environ.get('SECRET_KEY', 's3cr3t')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] + environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Wagtail
    'wagtail',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.sites',
    'wagtail_modeladmin', # TODO: migrate to wagtail's Snippets
                          # https://docs.wagtail.org/en/v5.2.3/reference/contrib/modeladmin/migrating_to_snippets.html
    # 'wagtail.contrib.settings',
    # 'wagtail.contrib.search_promotions',

    # Misc.
    'taggit',
    'generic_chooser', # TODO: migrate to wagtail's ChooserViewSet
                       # https://docs.wagtail.org/en/stable/extending/generic_views.html#chooserviewset

    # Example project
    'wagtailstreamforms',
    'example',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(SITE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'


# Database

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": SITE_DIR + "/default.db.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Django <no_reply@example.com>'


# Authentication

AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = reverse_lazy('admin:login')
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'


# Internationalization

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    join(SITE_DIR, "static"),
]
STATIC_URL = "/static/"

MEDIA_ROOT = join(SITE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail

WAGTAIL_SITE_NAME = 'example.com'
WAGTAILADMIN_BASE_URL = "/"

# Forms

WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = 'Formulaires'

WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = 'example.AdvancedFormSetting'

WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ('streamforms/form_block.html', 'Simple'),
    # ('app/custom_form_template.html', 'Custom Form Template'),
)
