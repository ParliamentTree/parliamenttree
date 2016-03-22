# STANDARD LIB
from functools import wraps

# THIRD PARTY
from django.http import HttpResponseForbidden
from google.appengine.api.users import is_current_user_admin


def is_cron(request):
    """ Is the given request generated by an App Engine cron job? """
    return request.META.get("HTTP_X_APPENGINE_CRON") or False


def is_task(request):
    """ Is the given request being ru by an App Engine cron job? """
    return request.META.get("HTTP_X_APPENGINE_QUEUENAME") or False


def gae_admin_cron_or_task_only(view_func):
    """ View decorator that requires the user to be an administrator of the App Engine app.
        Treats that anything being run in a cron or a task as being an admin user.
    """
    @wraps(view_func)
    def new_view(request, *args, **kwargs):
        if not (is_current_user_admin() or is_cron(request) or is_task(request)):
            return HttpResponseForbidden("Admin users only.")
        return view_func(request, *args, **kwargs)
    return new_view