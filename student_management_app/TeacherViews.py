from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import MonHocLop, KetQua, HocSinhLop, HocSinh, GiaoVien, LopHoc

# Trang chủ giáo viên
def teacher_home(request):
    giao_vien = request.user.giaovien
    monhoclop = MonHocLop.objects.filter(MaGV=giao_vien)
    lop_ids = monhoclop.values_list("MaLOP__MaLOP", flat=True).distinct()
    lop_count = LopHoc.objects.filter(MaLOP__in=lop_ids).count()
    monhoc_count = monhoclop.values("MaMH").distinct().count()
    hoc_sinh_count = HocSinhLop.objects.filter(MaLOP__in=lop_ids).count()

    context = {
        "lop_count": lop_count,
        "monhoc_count": monhoc_count,
        "hoc_sinh_count": hoc_sinh_count,
    }
    return render(request, "teacher_template/teacher_home.html", context)

# Giao diện chọn lớp và môn để nhập điểm
def teacher_input_score_view(request):
    giao_vien = request.user.giaovien
    monhoclop = MonHocLop.objects.filter(MaGV=giao_vien)
    return render(request, "teacher_template/input_score_select.html", {"monhoclop": monhoclop})

# Nhập điểm cho học sinh trong lớp và môn học được chọn
def teacher_input_score_detail(request, mamhl):
    monhoclop = get_object_or_404(MonHocLop, MaMHL=mamhl)
    hocsinhlop = HocSinhLop.objects.filter(MaLOP=monhoclop.MaLOP, NamHOC=monhoclop.NamHOC)
    ketquas = KetQua.objects.filter(ma_mhl=monhoclop)
    ketqua_dict = {kq.hsid_id: kq for kq in ketquas}
    return render(request, "teacher_template/input_score_detail.html", {
        "monhoclop": monhoclop,
        "hocsinhlop": hocsinhlop,
        "ketqua_dict": ketqua_dict
    })

# Lưu điểm học sinh
def teacher_input_score_save(request, mamhl):
    if request.method == "POST":
        monhoclop = get_object_or_404(MonHocLop, MaMHL=mamhl)
        for key in request.POST:
            if key.startswith("hs_"):
                hsid = key.split("_")[1]
                kq, created = KetQua.objects.get_or_create(
                    hsid_id=hsid,
                    ma_mhl=monhoclop,
                    nam_hoc=monhoclop.NamHOC
                )
                # Điểm
                kq.hk1_tx1 = request.POST.get(f"hk1_tx1_{hsid}")
                kq.hk1_tx2 = request.POST.get(f"hk1_tx2_{hsid}")
                kq.hk1_tx3 = request.POST.get(f"hk1_tx3_{hsid}")
                kq.hk1_tx4 = request.POST.get(f"hk1_tx4_{hsid}")
                kq.hk1_gk = request.POST.get(f"hk1_gk_{hsid}")
                kq.hk1_ck = request.POST.get(f"hk1_ck_{hsid}")
                kq.hk2_tx1 = request.POST.get(f"hk2_tx1_{hsid}")
                kq.hk2_tx2 = request.POST.get(f"hk2_tx2_{hsid}")
                kq.hk2_tx3 = request.POST.get(f"hk2_tx3_{hsid}")
                kq.hk2_tx4 = request.POST.get(f"hk2_tx4_{hsid}")
                kq.hk2_gk = request.POST.get(f"hk2_gk_{hsid}")
                kq.hk2_ck = request.POST.get(f"hk2_ck_{hsid}")
                kq.save()
        messages.success(request, "Đã lưu điểm thành công.")
        return redirect("teacher_input_score")
    return HttpResponse("Phương thức không hợp lệ")

# Hồ sơ giáo viên
def teacher_profile(request):
    gv = request.user.giaovien
    return render(request, "teacher_template/teacher_profile.html", {"giaovien": gv})

# Cập nhật hồ sơ giáo viên
def teacher_profile_update(request):
    if request.method == "POST":
        gv = request.user.giaovien
        gv.HoTen = request.POST.get("HoTen")
        password = request.POST.get("password")
        if password:
            gv.set_password(password)
        gv.save()
        messages.success(request, "Cập nhật thông tin thành công.")
        return redirect("teacher_profile")
    return redirect("teacher_profile")