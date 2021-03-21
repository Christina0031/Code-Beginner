from django.urls import path

from . import views

app_name = 'Hospital'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('Hospital/', views.hospital, name='hospital'),
    path('Patients/', views.patient, name='list'),
    path('Patients/insert/', views.insert, name='insert'),
    path('Patients/filer/', views.filter, name='filter'),
    path('Patients/filtered/', views.do_filter, name='do_filter'),
    path('Patients/filtered_admission/', views.do_filter_adm, name='do_filter_adm'),

    path('Patients/do_edit/', views.do_edit, name='do_edit'),
    path('Patients/do_insert/', views.do_insert, name='do_insert'),
    path('Patients/do_select/', views.do_select, name='do_select'),
    path('Patients/do_select_admission/', views.do_select_adm, name='do_select_adm'),
    path('Patients/do_insert_admission/', views.do_insert_adm, name='do_insert_adm'),
    path('Patients/do_edit_admission/', views.do_edit_adm, name='do_edit_adm'),
    path('Patients/insert_adm/', views.form_insert_adm, name='form_insert_adm'),

    path('Patients/<int:subject_id>/', views.detail, name='detail'),
    path('Patients/<int:subject_id>/edit/', views.edit, name='edit'),
    path('Patients/<int:subject_id>/delete/', views.delete, name='delete'),
    path('Patients/<int:subject_id>/admission/insert/', views.insert_adm, name='adm_insert'),
    path('Patients/<int:subject_id>/admission/<int:hadm_id>/edit/', views.edit_adm, name='edit_adm'),
    path('Patients/<int:subject_id>/admission/<int:hadm_id>/delete/', views.adm_delete, name='adm_delete'),
    path('Patients/<int:subject_id>/admission/<int:hadm_id>/more/', views.moreinfo, name='moreinfo'),

]
