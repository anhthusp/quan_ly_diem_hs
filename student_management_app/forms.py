from django import forms
from .models import HocSinh, LopHoc, HocSinhLop, PhuHuynh
from django.forms import ModelForm


# Tuỳ chỉnh date input
class DateInput(forms.DateInput):
    input_type = "date"


# Form thêm học sinh mới
class AddHocSinhForm(ModelForm):
    class Meta:
        model = HocSinh
        fields = ['MaHS', 'MaPH', 'HoTen', 'NgaySinh', 'GTinh', 'Email', 'SoDT']
        widgets = {
            'MaHS': forms.TextInput(attrs={'class': 'form-control'}),
            'MaPH': forms.Select(attrs={'class': 'form-control'}),
            'HoTen': forms.TextInput(attrs={'class': 'form-control'}),
            'NgaySinh': DateInput(attrs={'class': 'form-control'}),
            'GTinh': forms.Select(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'SoDT': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form chỉnh sửa học sinh
class EditHocSinhForm(ModelForm):
    class Meta:
        model = HocSinh
        exclude = ['MKhau']  # không chỉnh sửa mật khẩu tại đây
        widgets = {
            'MaPH': forms.Select(attrs={'class': 'form-control'}),
            'HoTen': forms.TextInput(attrs={'class': 'form-control'}),
            'NgaySinh': DateInput(attrs={'class': 'form-control'}),
            'GTinh': forms.Select(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'SoDT': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form gán học sinh vào lớp theo năm học
class HocSinhLopForm(ModelForm):
    class Meta:
        model = HocSinhLop
        fields = ['MaHS', 'MaLOP', 'NamHOC']
        widgets = {
            'MaHS': forms.Select(attrs={'class': 'form-control'}),
            'MaLOP': forms.Select(attrs={'class': 'form-control'}),
            'NamHOC': forms.TextInput(attrs={'class': 'form-control'}),
        }
