from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

CLOUDINARY_STORAGE  = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        "BACKEND": 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
}
MEDIA_URL = '/media/'  # 本番用 URL (Cloudinary が自動提供)
MEDIA_ROOT = None  # Cloudinary 使用時は不要


"""メール設定: Mailgunを使用"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('MAILGUN_SMTP_SERVER', default='smtp.mailgun.org')
EMAIL_PORT = env('MAILGUN_SMTP_PORT', default=587)
EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# 500エラー出るのでデバッグ機能有効にする
DEBUG = True

if DEBUG:
    def show_toolbar(request):
        return True

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

    