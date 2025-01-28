# Basic認証の設定
BASICAUTH_USERS = {
    'admin': 'pw'
}

# メール送信の設定
if DEBUG:
    # 開発環境: コンソールに出力
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # 本番環境: Mailgunを使用
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('MAILGUN_SMTP_SERVER', default='smtp.mailgun.org')
    EMAIL_PORT = env('MAILGUN_SMTP_PORT', default=587)
    EMAIL_HOST_USER = env('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = env('MAILGUN_SMTP_PASSWORD')
    EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL