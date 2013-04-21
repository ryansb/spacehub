import json


def validate_generic(request):
    """
    Generic validator that doesn't really do anything
    For testing/rapid dev stuff
    """
    data = json.loads(request.body)
    request.validated.update(data)


