from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import GiaoVien, HocSinh, PhuHuynh


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("logout_user")  # ép logout nếu người dùng vào trang login khi đang đăng nhập
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return redirect("login")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        request.session.flush() 
        login(request, user)

        # Điều hướng theo vai trò
        if hasattr(user, 'giaovien'):
            role = user.giaovien.VAI_TRO
            if role in ["admin", "ban_giam_hieu"]:
                return redirect("admin_home")
            elif role == "giao_vien":
                return redirect("teacher_home")

        elif hasattr(user, 'hocsinh'):
            return redirect("student_home")

        elif hasattr(user, 'phuhuynh'):
            return redirect("parent_home")

        else:
            messages.error(request, "Không xác định được vai trò người dùng.")
            return redirect("login")
    else:
        messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        return redirect("login")


def logout_user(request):
    logout(request)               # Hủy đăng nhập
    request.session.flush()       # Xóa toàn bộ session
    response = redirect('login')
    response.delete_cookie('sessionid')  # Xóa cookie
    return response


@login_required(login_url='login')
def home(request):
    user = request.user
    if hasattr(user, 'giaovien'):
        role = user.giaovien.VAI_TRO
        if role in ["admin", "ban_giam_hieu"]:
            return redirect("admin_home")
        elif role == "giao_vien":
            return redirect("teacher_home")

    elif hasattr(user, 'hocsinh'):
        return redirect("student_home")

    elif hasattr(user, 'phuhuynh'):
        return redirect("parent_home")

    return redirect("login")
