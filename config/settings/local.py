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



# productionでエラー発生、ローカルでテストのため一時的にコメントアウト
# """メール設定: コンソールに出力"""
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


"""メール設定: Amazon SESを使用（現在の設定）"""
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

