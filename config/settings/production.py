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



"""メール設定: Amazon SESを使用"""
# メール送信バックエンド
EMAIL_BACKEND = 'django_ses.SESBackend'

# Amazon SESの設定
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME', default='us-east-1')  # バージニアリージョン（us-east-1）
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'

# 送信元メールアドレスの設定（SESで検証済みのメールアドレス）
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='hiroki71027923@icloud.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# メール送信者名（オプション）
EMAIL_SUBJECT_PREFIX = '[Django EC] '




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


# ログ設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'order': {  # orderアプリケーションのロガー
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {  # Djangoフレームワークのロガー
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}



    