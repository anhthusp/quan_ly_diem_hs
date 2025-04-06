from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import GiaoVien, HocSinh, LopHoc, MonHoc, MonHocLop, HocSinhLop, KetQua, PhuHuynh, YKien, YKienGV
from .forms import AddHocSinhForm, EditHocSinhForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils.http import urlencode

# Trang chủ admin
@login_required(login_url='login')
def admin_home(request):
    hoc_sinh_count = HocSinh.objects.count()
    giao_vien_count = GiaoVien.objects.count()
    lop_hoc_count = LopHoc.objects.count()
    mon_hoc_count = MonHoc.objects.count()

    context = {
        "hoc_sinh_count": hoc_sinh_count,
        "giao_vien_count": giao_vien_count,
        "lop_hoc_count": lop_hoc_count,
        "mon_hoc_count": mon_hoc_count,
    }
    return render(request, "hod_template/home_content.html", context)

@login_required(login_url='login')
def assign_student_to_class(request):
    old_namhoc = request.GET.get("old_namhoc")
    old_khoi = request.GET.get("old_khoi")
    old_lop = request.GET.get("old_lop")

    khoi_list = [10, 11, 12]
    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct()
    ds_lop = LopHoc.objects.all()

    danh_sach = []
    if old_namhoc and old_lop:
        danh_sach = HocSinhLop.objects.filter(
            MaLOP__MaLOP=old_lop,
            NamHOC=old_namhoc
        ).select_related("MaHS")

        # ✅ Thêm danh sách các lớp đã học cho mỗi học sinh
        for hs_lop in danh_sach:
            ds_lop_da_gan = HocSinhLop.objects.filter(MaHS=hs_lop.MaHS).select_related("MaLOP")
            hs_lop.da_gan_list = [(i.MaLOP.TenLOP, i.NamHOC) for i in ds_lop_da_gan]

    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_students[]") or request.POST.getlist("selected_students")
        new_lop = request.POST.get("new_lop")
        new_namhoc = request.POST.get("new_namhoc")

        if not selected_ids or not new_lop or not new_namhoc:
            messages.error(request, "Vui lòng chọn học sinh và lớp mới.")
            return redirect("assign_student")

        lop_moi = get_object_or_404(LopHoc, MaLOP=new_lop, NamHOC=new_namhoc)
        count = 0
        for mahs in selected_ids:
            hs = get_object_or_404(HocSinh, MaHS=mahs)
            if not HocSinhLop.objects.filter(MaHS=hs, MaLOP=lop_moi, NamHOC=new_namhoc).exists():
                HocSinhLop.objects.create(MaHS=hs, MaLOP=lop_moi, NamHOC=new_namhoc)
                count += 1

        messages.success(request, f"Đã gán {count} học sinh vào lớp {lop_moi.TenLOP} ({new_namhoc})")

        # Giữ lại trạng thái lọc
        base_url = reverse('assign_student')
        query_string = urlencode({
            'old_namhoc': old_namhoc,
            'old_khoi': old_khoi,
            'old_lop': old_lop,
        })
        return redirect(f"{base_url}?{query_string}")

    return render(request, "hod_template/assign_student_template.html", {
        "ds_namhoc": ds_namhoc,
        "khoi_list": khoi_list,
        "ds_lop": ds_lop,
        "old_namhoc": old_namhoc,
        "old_khoi": old_khoi,
        "old_lop": old_lop,
        "danh_sach": danh_sach
    })

@login_required(login_url='login')
def add_student(request):
    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct()
    ds_khoi = [10, 11, 12]
    ds_lop = LopHoc.objects.all().order_by("Khoi", "TenLOP")

    # Xoá message cũ ngay khi load trang (dù GET hay POST)
    list(get_messages(request))  # Điều này giúp reset session message trước mỗi render

    if request.method == "POST":
        mahs = request.POST.get("MaHS")
        hoten = request.POST.get("HoTen")
        ngaysinh = request.POST.get("NgaySinh")
        gioitinh = request.POST.get("GTinh")
        email = request.POST.get("Email")
        sdt = request.POST.get("SoDT")
        password = request.POST.get("password")

        namhoc = request.POST.get("namhoc")
        khoi = request.POST.get("khoi")
        lop = request.POST.get("lop")

        if HocSinh.objects.filter(MaHS=mahs).exists():
            messages.error(request, "Mã học sinh đã tồn tại!")
            return redirect("add_student")

        try:
            user = User.objects.create_user(username=mahs, email=email, password=password)
            hs = HocSinh.objects.create(
                user=user,
                MaHS=mahs,
                HoTen=hoten,
                NgaySinh=ngaysinh,
                GTinh=gioitinh,
                Email=email,
                SoDT=sdt,
            )
            lop_hoc = LopHoc.objects.get(MaLOP=lop, NamHOC=namhoc)
            HocSinhLop.objects.create(MaHS=hs, MaLOP=lop_hoc, NamHOC=namhoc)

            messages.success(request, "Thêm học sinh thành công!")
            return redirect("add_student")

        except Exception as e:
            messages.error(request, f"Lỗi khi thêm: {e}")
            return redirect("add_student")

    return render(request, "hod_template/add_student_template.html", {
        "ds_namhoc": ds_namhoc,
        "ds_khoi": ds_khoi,
        "ds_lop": ds_lop,
    })

@login_required(login_url='login')
def manage_student(request):
    selected_khoi = request.GET.get("khoi")
    selected_lop = request.GET.get("lop")
    selected_namhoc = request.GET.get("namhoc")

    khoi_list = [10, 11, 12]
    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct()

    if selected_khoi and selected_namhoc:
        ds_lop = LopHoc.objects.filter(Khoi=selected_khoi, NamHOC=selected_namhoc)
    elif selected_khoi:
        ds_lop = LopHoc.objects.filter(Khoi=selected_khoi)
    elif selected_namhoc:
        ds_lop = LopHoc.objects.filter(NamHOC=selected_namhoc)
    else:
        ds_lop = LopHoc.objects.all()

    hs_lop_qs = HocSinhLop.objects.select_related("MaHS", "MaLOP")

    if selected_khoi:
        hs_lop_qs = hs_lop_qs.filter(MaLOP__Khoi=selected_khoi)
    if selected_lop:
        hs_lop_qs = hs_lop_qs.filter(MaLOP__MaLOP=selected_lop)
    if selected_namhoc:
        hs_lop_qs = hs_lop_qs.filter(NamHOC=selected_namhoc)

    context = {
        "ds_lop": LopHoc.objects.all(),
        "ds_namhoc": ds_namhoc,
        "khoi_list": khoi_list,
        "selected_khoi": selected_khoi,
        "selected_lop": selected_lop,
        "selected_namhoc": selected_namhoc,
        "danh_sach": hs_lop_qs
    }
    return render(request, "hod_template/manage_student_template.html", context)

@login_required(login_url='login')
def edit_student(request, mahs):
    hoc_sinh = get_object_or_404(HocSinh, MaHS=mahs)
    user = hoc_sinh.user

    if request.method == "POST":
        hoten = request.POST.get("HoTen")
        email = request.POST.get("Email")
        sdt = request.POST.get("SoDT")
        ngaysinh = request.POST.get("NgaySinh")
        gtinh = request.POST.get("GTinh")
        password = request.POST.get("password")

        hoc_sinh.HoTen = hoten
        hoc_sinh.Email = email
        hoc_sinh.SoDT = sdt
        hoc_sinh.NgaySinh = ngaysinh
        hoc_sinh.GTinh = gtinh
        user.email = email
        if password:
            user.set_password(password)

        user.save()
        hoc_sinh.save()

        messages.success(request, "Cập nhật học sinh thành công.")

        # Redirect kèm tham số lọc
        khoi = request.GET.get("khoi", "")
        lop = request.GET.get("lop", "")
        namhoc = request.GET.get("namhoc", "")
        return HttpResponseRedirect(f"{reverse('manage_student')}?khoi={khoi}&lop={lop}&namhoc={namhoc}")

    return render(request, "hod_template/edit_student_template.html", {"hoc_sinh": hoc_sinh})

@login_required(login_url='login')
def delete_student(request, student_id):
    hoc_sinh = get_object_or_404(HocSinh, MaHS=student_id)
    try:
        user = hoc_sinh.user  # lấy tài khoản liên kết
        hoc_sinh.delete()
        user.delete()  # xóa luôn tài khoản đăng nhập
        messages.success(request, "Xóa học sinh thành công.")
    except Exception as e:
        messages.error(request, f"Xóa học sinh thất bại: {e}")
    return redirect('manage_student')

# ==== QL Lớp Học ====#
@login_required(login_url='login')
def manage_class(request):
    selected_namhoc = request.GET.get("namhoc", "")
    selected_khoi = request.GET.get("khoi", "")

    # Danh sách năm học duy nhất
    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct().order_by("NamHOC")
    khoi_list = [10, 11, 12]

    # Lọc danh sách lớp học
    ds_lop = LopHoc.objects.all()
    if selected_namhoc:
        ds_lop = ds_lop.filter(NamHOC=selected_namhoc)
    if selected_khoi:
        ds_lop = ds_lop.filter(Khoi=int(selected_khoi))

    context = {
        "danh_sach": ds_lop,
        "ds_namhoc": ds_namhoc,
        "khoi_list": khoi_list,
        "selected_namhoc": selected_namhoc,
        "selected_khoi": selected_khoi,
    }
    return render(request, "hod_template/manage_class_template.html", context)

@login_required(login_url='login')
def add_class(request):
    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct()
    ds_khoi = [10, 11, 12]
    gv_list = GiaoVien.objects.all()

    if request.method == "POST":
        malop = request.POST.get("MaLOP")
        tenlop = request.POST.get("TenLOP")
        namhoc = request.POST.get("NamHOC")
        khoi = request.POST.get("Khoi")
        gvcn = request.POST.get("GVCN")

        if LopHoc.objects.filter(MaLOP=malop).exists():
            messages.error(request, "Mã lớp đã tồn tại.")
            return redirect("add_class")

        LopHoc.objects.create(
            MaLOP=malop,
            TenLOP=tenlop,
            NamHOC=namhoc,
            Khoi=int(khoi),
            GVCN=GiaoVien.objects.get(id=gvcn) if gvcn else None
        )
        messages.success(request, "Thêm lớp học thành công.")
        return redirect("manage_class")

    return render(request, "hod_template/add_class_template.html", {
        "ds_namhoc": ds_namhoc,
        "ds_khoi": ds_khoi,
        "gv_list": gv_list,
    })

@login_required(login_url='login')
def edit_class(request, malop):
    lop = get_object_or_404(LopHoc, MaLOP=malop)

    if request.method == "POST":
        ten_lop = request.POST.get("TenLOP")
        nam_hoc = request.POST.get("NamHOC")
        khoi = request.POST.get("Khoi")
        gvcn_id = request.POST.get("GVCN")

        lop.TenLOP = ten_lop
        lop.NamHOC = nam_hoc
        lop.Khoi = int(khoi)
        lop.GVCN = GiaoVien.objects.get(id=gvcn_id) if gvcn_id else None
        lop.save()

        # ✅ Sử dụng redirect để quay về trang danh sách
        messages.success(request, "Cập nhật lớp học thành công.")
        return redirect("manage_class")

    gv_list = GiaoVien.objects.all()
    return render(request, "hod_template/edit_class_template.html", {"lop": lop, "gv_list": gv_list})

# Quản lý giáo viên
@login_required(login_url='login')
def manage_teacher(request):
    teachers = GiaoVien.objects.all()
    return render(request, "hod_template/manage_teacher_template.html", {"teachers": teachers})

@login_required(login_url='login')
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(GiaoVien, MaGV=teacher_id)
    return render(request, "hod_template/teacher_profile.html", {"teacher": teacher})

@login_required(login_url='login')
def add_teacher(request):
    if request.method == "POST":
        magv = request.POST.get("MaGV")
        hoten = request.POST.get("HoTen")
        email = request.POST.get("email")
        password = request.POST.get("password")
        vai_tro = request.POST.get("VAI_TRO", "giao_vien")
        sodt = request.POST.get("SoDT")

        try:
            # Kiểm tra mã giáo viên trùng
            if User.objects.filter(username=magv).exists():
                messages.error(request, "Mã giáo viên đã tồn tại.")
                return redirect("add_teacher")

            # 1. Tạo tài khoản User
            user = User.objects.create_user(
                username=magv,
                email=email,
                password=password,
                first_name=hoten.split(" ")[0],
                last_name=" ".join(hoten.split(" ")[1:]),
            )

            # 2. Tạo GiaoVien liên kết với User
            GiaoVien.objects.create(
                user=user,
                MaGV=magv,
                HoTen=hoten,
                VAI_TRO=vai_tro,
                SoDT=sodt
            )

            messages.success(request, "Thêm giáo viên thành công.")
            return redirect("manage_teacher")
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm giáo viên: {e}")
            return redirect("add_teacher")

    return render(request, "hod_template/add_teacher.html")

@login_required(login_url='login')
@login_required(login_url='login')
def edit_teacher(request, magv):
    giaovien = get_object_or_404(GiaoVien, MaGV=magv)
    user = giaovien.user

    if request.method == "POST":
        hoten = request.POST.get("HoTen")
        email = request.POST.get("email")
        sdt = request.POST.get("SoDT")
        vai_tro = request.POST.get("VAI_TRO")
        password = request.POST.get("password")

        # Cập nhật thông tin
        giaovien.HoTen = hoten
        giaovien.VAI_TRO = vai_tro
        giaovien.SoDT = sdt
        user.email = email

        if password:
            user.password = make_password(password)

        try:
            user.save()
            giaovien.save()
            messages.success(request, "Cập nhật giáo viên thành công.")
        except Exception as e:
            messages.error(request, f"Lỗi khi cập nhật: {e}")
        return redirect("manage_teacher")

    return render(request, "hod_template/edit_teacher.html", {"giaovien": giaovien})

@login_required(login_url='login')
def delete_teacher(request, magv):
    giaovien = get_object_or_404(GiaoVien, MaGV=magv)
    try:
        giaovien.delete()
        messages.success(request, "Xóa giáo viên thành công.")
    except Exception as e:
        messages.error(request, f"Lỗi khi xóa giáo viên: {e}")
    return redirect("manage_teacher")

# @login_required(login_url='login')
# def manage_class(request):
#     classes = LopHoc.objects.all()
#     return render(request, "hod_template/manage_class_template.html", {"classes": classes})


@login_required(login_url='login')
def assign_subject_to_class(request):
    if request.method == "POST":
        mamh = request.POST.get("MaMH")
        malop = request.POST.get("MaLOP")
        magv = request.POST.get("MaGV")
        namhoc = request.POST.get("NamHOC")
        try:
            MonHocLop.objects.create(MaMHL=mamh+malop, MaMH_id=mamh, MaLOP_id=malop, MaGV_id=magv, NamHOC=namhoc)
            messages.success(request, "Gán môn học vào lớp thành công!")
        except:
            messages.error(request, "Thất bại khi gán môn học!")
    return redirect('manage_subjects')

@login_required(login_url='login')
def manage_scores(request):
    results = KetQua.objects.select_related('hsid', 'ma_mhl').all()
    return render(request, "hod_template/manage_scores_template.html", {"results": results})

@login_required(login_url='login')
def update_score(request, kqid):
    result = get_object_or_404(KetQua, pk=kqid)
    if request.method == "POST":
        fields = [
            'hk1_tx1','hk1_tx2','hk1_tx3','hk1_tx4','hk1_gk','hk1_ck',
            'hk2_tx1','hk2_tx2','hk2_tx3','hk2_tx4','hk2_gk','hk2_ck'
        ]
        for field in fields:
            setattr(result, field, request.POST.get(field))
        result.save()
        messages.success(request, "Cập nhật điểm thành công!")
        return redirect('manage_scores')
    return render(request, "hod_template/edit_score_template.html", {"result": result})

@login_required(login_url='login')
def ykien_phuhuynh(request):
    ykiens = YKien.objects.select_related('MaHS', 'MaPH').all()
    return render(request, "hod_template/ykien_phuhuynh.html", {"ykiens": ykiens})

@csrf_exempt
@login_required(login_url='login')
def reply_ykien_phuhuynh(request):
    if request.method == "POST":
        ykid = request.POST.get("YKID")
        magv = request.POST.get("MaGV")
        try:
            YKienGV.objects.create(YKID_id=ykid, MaGV_id=magv)
            return HttpResponse("OK")
        except:
            return HttpResponse("ERROR")

@login_required(login_url='login')
def admin_profile(request):
    return render(request, "hod_template/admin_profile.html", {"user": request.user})

@login_required(login_url='login')
def admin_profile_update(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "Cập nhật hồ sơ thành công")
        return redirect("admin_profile")
    return redirect("admin_profile")

# QL chuyên môn
@login_required(login_url='login')
def assign_teacher_to_class(request):
    namhoc = request.GET.get("namhoc")
    khoi = request.GET.get("khoi")
    malop = request.GET.get("malop")
    mamh = request.GET.get("mamh")

    ds_namhoc = LopHoc.objects.values_list("NamHOC", flat=True).distinct()
    khoi_list = [10, 11, 12]
    ds_monhoc = MonHoc.objects.all()
    ds_lop = LopHoc.objects.none()
    ds_giaovien = GiaoVien.objects.none()  # ✅ Mặc định là rỗng
    phan_cong = None

    # Nếu có năm học và khối → lọc lớp
    if namhoc and khoi:
        try:
            khoi_int = int(khoi)
            ds_lop = LopHoc.objects.filter(NamHOC=namhoc, Khoi=khoi_int)
        except ValueError:
            pass

    # Nếu có cả lớp và môn học → lọc thêm giáo viên và phân công
    if namhoc and khoi and malop and mamh:
        try:
            phan_cong = MonHocLop.objects.get(
                NamHOC=namhoc, MaLOP__MaLOP=malop, MaMH__MaMH=mamh
            )
        except MonHocLop.DoesNotExist:
            phan_cong = None

        # 👉 Lọc giáo viên theo 2 ký tự cuối của mã môn học
        suffix = mamh[-2:].upper()
        ds_giaovien = GiaoVien.objects.filter(MaGV__iendswith=suffix)

    # Xử lý khi POST (lưu phân công)
    if request.method == "POST":
        mamh_post = request.POST.get("mamh")
        malop_post = request.POST.get("malop")
        namhoc_post = request.POST.get("namhoc")
        khoi_post = request.POST.get("khoi")
        gv_id = request.POST.get("gv")

        if mamh_post and malop_post and namhoc_post and gv_id:
            mamhl = mamh_post + malop_post
            mon = get_object_or_404(MonHoc, MaMH=mamh_post)
            lop = get_object_or_404(LopHoc, MaLOP=malop_post, NamHOC=namhoc_post)
            gv = get_object_or_404(GiaoVien, id=gv_id)

            MonHocLop.objects.update_or_create(
                MaMHL=mamhl,
                defaults={"NamHOC": namhoc_post, "MaMH": mon, "MaLOP": lop, "MaGV": gv}
            )

            messages.success(request, "Phân công giảng dạy thành công!")
            return redirect(f"{request.path}?namhoc={namhoc_post}&khoi={khoi_post}&malop={malop_post}&mamh={mamh_post}")

    context = {
        "ds_namhoc": ds_namhoc,
        "khoi_list": khoi_list,
        "ds_monhoc": ds_monhoc,
        "ds_lop": ds_lop,
        "ds_giaovien": ds_giaovien,
        "phan_cong": phan_cong,
        "selected_namhoc": namhoc,
        "selected_khoi": khoi,
        "selected_lop": malop,
        "selected_mon": mamh,
    }

    return render(request, "hod_template/assign_teacher_template.html", context)


@login_required(login_url='login')
def add_subject(request):
    if request.method == "POST":
        mamh = request.POST.get("MaMH")
        tenmh = request.POST.get("TenMH")
        sotiet = request.POST.get("SoTiet")
        kieudg = request.POST.get("KieuDG")

        if MonHoc.objects.filter(MaMH=mamh).exists():
            messages.error(request, "Mã môn học đã tồn tại!")
        else:
            MonHoc.objects.create(MaMH=mamh, TenMH=tenmh, SoTiet=sotiet, KieuDG=kieudg)
            messages.success(request, "Thêm môn học thành công!")
        return redirect("add_subject")

    return render(request, "hod_template/add_subject_template.html")

@login_required(login_url='login')
def add_subject(request):
    if request.method == "POST":
        mamh = request.POST.get("MaMH")
        tenmh = request.POST.get("TenMH")
        sotiet = request.POST.get("SoTiet")
        kieudg = request.POST.get("KieuDG")

        if MonHoc.objects.filter(MaMH=mamh).exists():
            messages.error(request, "Mã môn học đã tồn tại!")
        else:
            MonHoc.objects.create(MaMH=mamh, TenMH=tenmh, SoTiet=sotiet, KieuDG=kieudg)
            messages.success(request, "Thêm môn học thành công!")
        return redirect("add_subject")

    return render(request, "hod_template/add_subject_template.html")


@login_required(login_url='login')
def manage_subjects(request):
    ds_monhoc = MonHoc.objects.all()
    return render(request, "hod_template/manage_subjects.html", {
        "ds_monhoc": ds_monhoc
    })

@login_required(login_url='login')
def edit_subject(request, mamh):
    monhoc = get_object_or_404(MonHoc, MaMH=mamh)

    if request.method == "POST":
        tenmh = request.POST.get("TenMH")
        sotiet = request.POST.get("SoTiet")
        kieudg = request.POST.get("KieuDG")

        monhoc.TenMH = tenmh
        monhoc.SoTiet = sotiet
        monhoc.KieuDG = kieudg
        monhoc.save()

        messages.success(request, "Cập nhật môn học thành công!")
        return redirect("manage_subjects")

    return render(request, "hod_template/edit_subject_template.html", {"monhoc": monhoc})

@login_required(login_url='login')
def delete_subject(request, mamh):
    try:
        monhoc = get_object_or_404(MonHoc, MaMH=mamh)
        monhoc.delete()
        messages.success(request, f"Đã xóa môn học {mamh} thành công.")
    except Exception as e:
        messages.error(request, f"Lỗi khi xóa môn học: {e}")
    return redirect("manage_subjects")

