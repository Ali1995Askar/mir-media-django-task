from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587


EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "99limitlesspark@gmail.com")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "99limitlesspark99limitlesspark")
EMAIL_TO = env.str("EMAIL_TO", "debug@mir.de")
