from django.core.cache import cache
from django.http import HttpResponseForbidden

# here for traking invalid cridential attempes we need middleware

# it blockes ips with more than 3 invalid cridetial attemps


class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        failed_attempts = cache.get(ip, 0)
        if failed_attempts >= 3:
            return HttpResponseForbidden("Too many failed login attempts. you have been blocked for 1 hour.")
        response = self.get_response(request)
        return response
# getting ip inorder to be able to block more than 3 invalid attemps

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
