from django.contrib.auth.backends import ModelBackend

class CustomModelBackend(ModelBackend):
    # We don't need the default implementation because we perform the necessary checks
    # in the form validation to return the appropriate error.
    def user_can_authenticate(self, user):
        return True