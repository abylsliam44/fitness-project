from .utils import send_welcome_email

class LoginNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            device_info = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
            if 'device_info' not in request.session:
                request.session['device_info'] = device_info
            elif request.session['device_info'] != device_info:
                # Удаляем этот вызов, чтобы не слал письма при каждом новом user-agent
                # send_welcome_email(request.user)
                request.session['device_info'] = device_info

        return self.get_response(request)
