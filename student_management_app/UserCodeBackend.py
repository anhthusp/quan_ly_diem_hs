from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from student_management_app.models import GiaoVien, HocSinh, PhuHuynh


class UserCodeBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
