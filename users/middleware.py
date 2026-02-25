import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            cache_key = f"last-seen-{request.user.id}"

            cache.set(cache_key, now, 300)

        response = self.get_response(request)
        return response