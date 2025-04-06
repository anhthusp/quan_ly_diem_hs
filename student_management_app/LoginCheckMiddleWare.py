from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

class LoginCheckMiddleWare(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        allowed_paths = [
            reverse('login'),
            reverse('doLogin'),
            reverse('logout_user'),
        ]
        
        path = request.path

        # 1. Nếu chưa đăng nhập và truy cập không được phép
        if not request.user.is_authenticated:
            if not any(path.startswith(p) for p in allowed_paths) and not path.startswith('/static/'):
                return redirect('login')
            return None

        # 2. Nếu session không còn hợp lệ
        if '_auth_user_id' not in request.session:
            logout(request)
            return redirect('login')

        # 3. Phân quyền dựa trên modulename
        user = request.user
        modulename = view_func.__module__

        if hasattr(user, 'giaovien'):
            role = user.giaovien.VAI_TRO
            if role in ['admin', 'ban_giam_hieu']:
                if "HodViews" in modulename or "views" in modulename:
                    return None
                return redirect('admin_home')
            elif role == 'giao_vien':
                if "TeacherViews" in modulename:
                    return None
                return redirect('teacher_home')

        elif hasattr(user, 'hocsinh'):
            if "StudentViews" in modulename:
                return None
            return redirect('student_home')

        elif hasattr(user, 'phuhuynh'):
            if "ParentViews" in modulename:
                return None
            return redirect('parent_home')

        return None
