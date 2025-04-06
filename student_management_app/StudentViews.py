from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from student_management_app.models import HocSinh, HocSinhLop, KetQua, HocBa
from django.contrib.auth.decorators import login_required

# Trang chủ học sinh
@login_required
def student_home(request):
    hocsinh = request.user.hocsinh
    hoc_sinh_lop = HocSinhLop.objects.filter(MaHS=hocsinh).order_by('-NamHOC').first()
    ketquas = KetQua.objects.filter(hsid=hoc_sinh_lop) if hoc_sinh_lop else []
    hocba = HocBa.objects.filter(HSID=hoc_sinh_lop).first() if hoc_sinh_lop else None

    context = {
        "hoc_sinh": hocsinh,
        "lop_hoc": hoc_sinh_lop.MaLOP if hoc_sinh_lop else None,
        "nam_hoc": hoc_sinh_lop.NamHOC if hoc_sinh_lop else None,
        "hocba": hocba,
        "ketquas": ketquas,
    }
    return render(request, "student_template/student_home.html", context)

# Xem học bạ
@login_required
def student_view_report(request):
    hocsinh = request.user.hocsinh
    hoc_sinh_lop = HocSinhLop.objects.filter(MaHS=hocsinh).order_by('-NamHOC').first()
    hocba = HocBa.objects.filter(HSID=hoc_sinh_lop).first() if hoc_sinh_lop else None
    context = {
        "hocba": hocba,
        "lop": hoc_sinh_lop.MaLOP if hoc_sinh_lop else None
    }
    return render(request, "student_template/student_view_report.html", context)

# Xem điểm theo môn học
@login_required
def student_view_scores(request):
    hocsinh = request.user.hocsinh
    hoc_sinh_lop = HocSinhLop.objects.filter(MaHS=hocsinh).order_by('-NamHOC').first()
    ketquas = KetQua.objects.filter(hsid=hoc_sinh_lop)
    context = {
        "ketquas": ketquas,
        "lop": hoc_sinh_lop.MaLOP if hoc_sinh_lop else None
    }
    return render(request, "student_template/student_scores.html", context)

# Hồ sơ học sinh
@login_required
def student_profile(request):
    hocsinh = request.user.hocsinh
    return render(request, "student_template/student_profile.html", {"hocsinh": hocsinh})

# Cập nhật hồ sơ học sinh
@login_required
def student_profile_update(request):
    if request.method == "POST":
        hs = request.user.hocsinh
        hs.HoTen = request.POST.get("HoTen")
        hs.Email = request.POST.get("Email")
        hs.SoDT = request.POST.get("SoDT")
        password = request.POST.get("password")
        if password:
            hs.set_password(password)
        hs.save()
        messages.success(request, "Cập nhật thông tin thành công.")
        return redirect("student_profile")
    return redirect("student_profile")
