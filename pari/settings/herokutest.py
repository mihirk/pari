import os
from .base import *  # noqa
import dj_database_url

DEBUG = bool(os.environ.get('DJANGO_DEBUG', 'true'))

COMPRESS_ENABLED = True



DATABASES['default'] = dj_database_url.config(default='postgres://postgres:postgres@localhost:5432/pari')
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": PROJECT_ROOT.child("dev.db"),
#        "USER": "",
#        "PASSWORD": "",
#        "HOST": "",
#        "PORT": "",
#    }
#}

INSTALLED_APPS += (
    "django_extensions",
)




DEFAULT_FILE_STORAGE = 'pari.article.storage.ParallelS3Storage'

# INSTALLED_APPS += (
#     "haystack",
# )

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': 'http://search-ruralindiaonline.rhcloud.com/',
#         'INDEX_NAME': 'haystack',
#     },
# }
