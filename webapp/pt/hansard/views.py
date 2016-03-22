from django.shortcuts import render

# PARLIAMENT TREE
from pt.core.utils import is_cron, gae_admin_cron_or_task_only


@gae_admin_cron_or_task_only
def import_speeches(request):
    """ This view is called on a cron (currently daily).  It should scrape the latest MPs' speeches
        from Hansard and save them into the pt.core.models.Speech model.
    """
    # If this view is being called from the App Engine cron, then defer it onto a task queue.
    # This allows us to pause the cron by pausing the task queue and also gives it automatic retries.
    if is_cron(request):
        deferred.defer(hansard_import, request, _queue=settings.QUEUES.HANSARD_IMPORT)
        return

    # Notes:
    # * This code needs to check the `timestamp` of the most recent Speech that we currently have
    #   stored and collect new data from that point forward.  Just relying on the fact that this
    #   cron runs daily is probably not a good idea.
    # * The cron is currently scheduled to run at midnight every day.  But we should find out what
    #   time Hansard updates the site each day, and run just after that.  See cron.yaml.
    # * Before we can import speeches, we need a way of getting all the names and constituencies of
    #   the MPs.  Maybe we can just do MP.get_or_create(**things), or maybe we should have a
    #   separate cron/task/something which keeps the list updated.

    # TODO: WRITE ME!!

