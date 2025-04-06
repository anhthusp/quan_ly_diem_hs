from django.db import models
from django.contrib.auth.models import User

# === GIAO VIEN ===
class GiaoVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    MaGV = models.CharField(max_length=10, unique=True)
    HoTen = models.CharField(max_length=100)
    SoDT = models.CharField(max_length=15, null=True, blank=True)
    VAI_TRO = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Admin"),
            ("ban_giam_hieu", "Ban Giám Hiệu"),
            ("giao_vien", "Giáo Viên"),
        ],
        default="giao_vien",
    )

    def __str__(self):
        return f"{self.HoTen} ({self.MaGV}) - {self.VAI_TRO}"

    class Meta:
        db_table = "GIAOVIEN"


# === HOC SINH ===
class HocSinh(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    MaHS = models.CharField(max_length=15, unique=True)
    HoTen = models.CharField(max_length=100)
    NgaySinh = models.DateField()
    GTinh = models.CharField(max_length=5)
    Email = models.EmailField(null=True, blank=True)
    SoDT = models.CharField(max_length=15, null=True, blank=True)
    MaPH = models.ForeignKey('PhuHuynh', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.HoTen} ({self.MaHS})"

    class Meta:
        db_table = "HOCSINH"


# === PHU HUYNH ===
class PhuHuynh(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    MaPH = models.CharField(max_length=10, unique=True)
    HoTen = models.CharField(max_length=100)
    Email = models.EmailField(null=True, blank=True)
    SoDT = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.HoTen} ({self.MaPH})"

    class Meta:
        db_table = "PHUHUYNH"


# === MON HOC ===
class MonHoc(models.Model):
    MaMH = models.CharField(max_length=10, primary_key=True)
    TenMH = models.CharField(max_length=50)
    SoTiet = models.IntegerField()
    KieuDG = models.CharField(max_length=25)

    def __str__(self):
        return self.TenMH

    class Meta:
        db_table = "MONHOC"


# === LOP HOC ===
class LopHoc(models.Model):
    MaLOP = models.CharField(max_length=5, primary_key=True)
    TenLOP = models.CharField(max_length=15)
    NamHOC = models.CharField(max_length=15)
    Khoi = models.IntegerField()
    GVCN = models.ForeignKey(GiaoVien, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.TenLOP} - {self.NamHOC}"

    class Meta:
        db_table = "LOPHOC"


# === HOC SINH LOP ===
class HocSinhLop(models.Model):
    HSID = models.AutoField(primary_key=True)
    MaHS = models.ForeignKey(HocSinh, on_delete=models.CASCADE)
    MaLOP = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    NamHOC = models.CharField(max_length=15)

    class Meta:
        db_table = "HOCSINH_LOP"


# === MON HOC LOP ===
class MonHocLop(models.Model):
    MaMHL = models.CharField(max_length=10, primary_key=True)
    NamHOC = models.CharField(max_length=10)
    MaMH = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    MaLOP = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    MaGV = models.ForeignKey(GiaoVien, on_delete=models.CASCADE)

    class Meta:
        db_table = "MONHOC_LOP"


# === KET QUA ===
class KetQua(models.Model):
    kqid = models.AutoField(primary_key=True)
    hsid = models.ForeignKey(HocSinhLop, on_delete=models.CASCADE)
    ma_mhl = models.ForeignKey(MonHocLop, on_delete=models.CASCADE)
    nam_hoc = models.CharField(max_length=10)

    hk1_tx1 = models.FloatField(null=True, blank=True)
    hk1_tx2 = models.FloatField(null=True, blank=True)
    hk1_tx3 = models.FloatField(null=True, blank=True)
    hk1_tx4 = models.FloatField(null=True, blank=True)
    hk1_gk = models.FloatField(null=True, blank=True)
    hk1_ck = models.FloatField(null=True, blank=True)
    hk2_tx1 = models.FloatField(null=True, blank=True)
    hk2_tx2 = models.FloatField(null=True, blank=True)
    hk2_tx3 = models.FloatField(null=True, blank=True)
    hk2_tx4 = models.FloatField(null=True, blank=True)
    hk2_gk = models.FloatField(null=True, blank=True)
    hk2_ck = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "KETQUA"


# === HOC BA ===
class HocBa(models.Model):
    HBID = models.AutoField(primary_key=True)
    HSID = models.ForeignKey(HocSinhLop, on_delete=models.CASCADE)
    NamHOC = models.CharField(max_length=10)
    XepLoaiHK1_HL = models.CharField(max_length=10)
    XepLoaiHK2_HL = models.CharField(max_length=10)
    XepLoaiHK1_RL = models.CharField(max_length=10)
    XepLoaiHK2_RL = models.CharField(max_length=10)

    class Meta:
        db_table = "HOCBA"


# === Y KIEN ===
class YKien(models.Model):
    YKID = models.AutoField(primary_key=True)
    MaHS = models.ForeignKey(HocSinh, on_delete=models.CASCADE)
    MaPH = models.ForeignKey(PhuHuynh, on_delete=models.CASCADE)
    NoiDung = models.TextField()
    ThoiGianGui = models.DateTimeField(auto_now_add=True)
    TrangThai = models.CharField(max_length=20)

    class Meta:
        db_table = "YKIEN"


class YKienGV(models.Model):
    YKID = models.ForeignKey(YKien, on_delete=models.CASCADE)
    MaGV = models.ForeignKey(GiaoVien, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('YKID', 'MaGV'),)
        db_table = "YKIEN_GV"
