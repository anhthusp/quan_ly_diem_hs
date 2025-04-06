from django.urls import path
from . import views
from . import HodViews, TeacherViews, StudentViews

urlpatterns = [
    path('', views.home, name="home"), 
    # ==== Đăng nhập / đăng xuất ====
    path('login/', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout/', views.logout_user, name="logout_user"),

    # ==== Ban Giám Hiệu / Admin ====
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),

    # Quản lý giáo viên
    path('manage_teacher/', HodViews.manage_teacher, name="manage_teacher"),
    path('add_teacher/', HodViews.add_teacher, name="add_teacher"),
    path('edit_teacher/<str:magv>/', HodViews.edit_teacher, name="edit_teacher"),
    path('delete_teacher/<str:magv>/', HodViews.delete_teacher, name="delete_teacher"),

    # Quản lý học sinh
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('edit_student/<str:mahs>/', HodViews.edit_student, name="edit_student"),
    path('delete_student/<str:mahs>/', HodViews.delete_student, name="delete_student"),
    path('assign_student/', HodViews.assign_student_to_class, name="assign_student"),

    # ==== QL Lớp Học ====# 
  path('manage_class/', HodViews.manage_class, name="manage_class"),
  path('add_class/', HodViews.add_class, name='add_class'),
  path('edit_class/<str:malop>/', HodViews.edit_class, name="edit_class"),

    # ==== Giáo viên ====
    path('teacher_home/', TeacherViews.teacher_home, name="teacher_home"),
    path('teacher_profile/', TeacherViews.teacher_profile, name="teacher_profile"),
    path('teacher_profile_update/', TeacherViews.teacher_profile_update, name="teacher_profile_update"),

    # Nhập điểm
    path('teacher_input_score/', TeacherViews.teacher_input_score_view, name="teacher_input_score"),
    path('teacher_input_score/<str:mamhl>/', TeacherViews.teacher_input_score_detail, name="teacher_input_score_detail"),
    path('teacher_input_score_save/<str:mamhl>/', TeacherViews.teacher_input_score_save, name="teacher_input_score_save"),

    # ==== Học sinh ====
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_scores/', StudentViews.student_view_scores, name="student_view_scores"),
    path('student_report/', StudentViews.student_view_report, name="student_view_report"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),



    # #Thêm sau
    #   path('manage_class/', HodViews.manage_class, name="manage_class"),
      # path('manage_subject/', HodViews.manage_subject, name="manage_subject"),

    #QL Chuyên môn
    path('assign_teacher/', HodViews.assign_teacher_to_class, name="assign_teacher_to_class"),
    path('add_subject/', HodViews.add_subject, name='add_subject'),
    path('manage_subjects/', HodViews.manage_subjects, name="manage_subjects"),
    path('edit_subject/<str:mamh>/', HodViews.edit_subject, name="edit_subject"),
    path('delete_subject/<str:mamh>/', HodViews.delete_subject, name="delete_subject"),



]


