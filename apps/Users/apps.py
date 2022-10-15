from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    #Be sure to insert app directory name after creating an app
    name = 'apps.Users'
