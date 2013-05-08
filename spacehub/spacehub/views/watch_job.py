""" Cornice services.
"""
from cornice import Service
from spacehub.models import ScrapeJob, DBSession
from spacehub.validators import validate_generic



watch_runner = Service(name="watch_runner", path="/watch_runner",
        description="Service to run the watcher for watched pages")

@watch_runner.get()
def get_watch_runner(request):
    """
        When GET'd to this, will get info on the running jorbs
    """
    jobs = DBSession.query(ScrapeJob).filter(ScrapeJob.status==1)
    if jobs:
        return dict(jobs=[j.to_dict() for j in jobs])

    return dict(jobs=[])

@watch_runner.post(validators=validate_generic)
def post_watch_runner(request):
    """
        When POSTED to this will start operating on watched pages
        Check to see if there is already a job with status 1 (running)
        If so return false else create new job and kick off a scrape
    """
    pass

@watch_runner.put(validators=validate_generic)
def put_watch_runner(request):
    """
        Update the runner's status.
    """
    job = DBSession.query(ScrapeJob).filter(
            ScrapeJob.id==request.validated['id']).one()

    job.status = request.validatated['new_status']

    return job.to_dict()
