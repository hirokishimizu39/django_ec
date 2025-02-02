from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']


STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        "BACKEND": 'django.core.files.storage.FileSystemStorage',
    },
}
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


"""メール設定: コンソールに出力"""
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if DEBUG:
    def show_toolbar(request):
        return True
    INTERNAL_IPS = ['127.0.0.1']
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

