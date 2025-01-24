""" Helper function for making requests """

import json


def is_json_request(req):
    """Check if the request content type is JSON."""
    return "form-data" not in req.content_type


def handle_json_request(req):
    """Parse and validate the JSON request body."""
    try:
        body = json.loads(req.data)
        return body.get("url", None)
    except (json.JSONDecodeError, KeyError) as exc:
        raise ValueError("Invalid request format or missing URL") from exc


def handle_audio_source(request):
    """Handle the audio source from the request."""
    if is_json_request(request):
        return handle_json_request(request)
    return request.files.get("audio")
