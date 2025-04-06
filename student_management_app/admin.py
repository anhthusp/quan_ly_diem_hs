from django.contrib import admin
from .models import GiaoVien, HocSinh, PhuHuynh, LopHoc, MonHoc, MonHocLop, HocSinhLop, KetQua, HocBa, YKien, YKienGV

@admin.register(GiaoVien)
class GiaoVienAdmin(admin.ModelAdmin):
    list_display = ['MaGV', 'HoTen', 'VAI_TRO']
    search_fields = ['MaGV', 'HoTen', 'VAI_TRO']

@admin.register(HocSinh)
class HocSinhAdmin(admin.ModelAdmin):
    list_display = ['MaHS', 'HoTen', 'GTinh', 'NgaySinh', 'Email']
    search_fields = ['MaHS', 'HoTen', 'Email']

@admin.register(PhuHuynh)
class PhuHuynhAdmin(admin.ModelAdmin):
    list_display = ['MaPH', 'HoTen', 'Email', 'SoDT']

@admin.register(LopHoc)
class LopHocAdmin(admin.ModelAdmin):
    list_display = ['MaLOP', 'TenLOP', 'NamHOC', 'Khoi', 'GVCN']  # Thêm 'GVCN'
    
@admin.register(MonHoc)
class MonHocAdmin(admin.ModelAdmin):
    list_display = ['MaMH', 'TenMH', 'SoTiet', 'KieuDG']

@admin.register(MonHocLop)
class MonHocLopAdmin(admin.ModelAdmin):
    list_display = ['MaMHL', 'MaMH', 'MaLOP', 'MaGV', 'NamHOC']  # Đã có 'MaGV'

@admin.register(HocSinhLop)
class HocSinhLopAdmin(admin.ModelAdmin):
    list_display = ['HSID', 'MaHS', 'MaLOP', 'NamHOC']

@admin.register(KetQua)
class KetQuaAdmin(admin.ModelAdmin):
    list_display = ['kqid', 'hsid', 'ma_mhl', 'nam_hoc']

@admin.register(HocBa)
class HocBaAdmin(admin.ModelAdmin):
    list_display = ['HBID', 'HSID', 'NamHOC', 'XepLoaiHK1_HL', 'XepLoaiHK2_HL']

@admin.register(YKien)
class YKienAdmin(admin.ModelAdmin):
    list_display = ['YKID', 'MaHS', 'MaPH', 'ThoiGianGui', 'TrangThai']

@admin.register(YKienGV)
class YKienGVAdmin(admin.ModelAdmin):
    list_display = ['YKID', 'MaGV']
