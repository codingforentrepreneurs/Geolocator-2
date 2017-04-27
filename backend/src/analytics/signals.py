from django.dispatch import Signal


user_logged_in = Signal(providing_agrs=['request'])