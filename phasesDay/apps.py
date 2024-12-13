from django.apps import AppConfig


class PhasesdayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phasesDay'

    def ready(self):
        call_command('loaddata', 'phasesDay.json', verbosity=0)
