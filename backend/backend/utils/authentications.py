from rest_framework_simplejwt.authentication import JWTAuthentication


class SafeGetJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            try:
                return super().authenticate(request)
            except:
                return None
        else:
            return super().authenticate(request)
