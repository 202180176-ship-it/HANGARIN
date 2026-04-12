from .bootstrap import ensure_serverless_database_ready


class ServerlessDatabaseBootstrapMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ensure_serverless_database_ready()
        return self.get_response(request)
