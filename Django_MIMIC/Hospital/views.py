from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from .models import Admissions, Patients, Prescriptions, Labevents, Datetimeevents, Cptevents, DCpt, DLabitems, \
    Caregivers
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from django.db.models import Max


def dashboard(request):  #
    if not request.session.get('is_login', None):
        return redirect('/login/')
    n_pat = Patients.objects.count()
    n_adm = Admissions.objects.count()
    n_cg = Caregivers.objects.count()
    sex_m = Patients.objects.filter(gender='M').count()
    sex_f = Patients.objects.filter(gender='F').count()
    un_dead = Patients.objects.filter(expire_flag='0').count()
    dead = Patients.objects.filter(expire_flag='1').count()
    lab = Labevents.objects.count()
    cpt = Cptevents.objects.count()
    pre = Prescriptions.objects.count()
    time0 = Admissions.objects.filter(admittime__startswith='210').count()
    time1 = Admissions.objects.filter(admittime__startswith='211').count()
    time2 = Admissions.objects.filter(admittime__startswith='212').count()
    time3 = Admissions.objects.filter(admittime__startswith='213').count()
    time4 = Admissions.objects.filter(admittime__startswith='214').count()
    time5 = Admissions.objects.filter(admittime__startswith='215').count()
    time6 = Admissions.objects.filter(admittime__startswith='216').count()
    time7 = Admissions.objects.filter(admittime__startswith='217').count()
    time8 = Admissions.objects.filter(admittime__startswith='218').count()
    time9 = Admissions.objects.filter(admittime__startswith='219').count()
    time10 = Admissions.objects.filter(admittime__startswith='220').count()
    admlist = Admissions.objects.order_by("-admittime")[0:5]
    return render(request, 'Hospital/dashboard.html', locals())


def patient(request):  # 查看所有病人
    if not request.session.get('is_login', None):
        return redirect('/login/')
    patients = Patients.objects.all()
    return render(request, 'Hospital/Patient_List.html', {'patients': patients})


def detail(request, subject_id):  # 查看病人详细信息,问诊信息
    if not request.session.get('is_login', None):
        return redirect('/login/')
    details = Patients.objects.get(subject_id=subject_id)
    adm = Admissions.objects.filter(subject_id=subject_id)
    return render(request, 'Hospital/detail.html', {'detail': details, 'adm': adm})


def edit(request, subject_id):  # 编辑
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    edit_patient = Patients.objects.get(subject_id=subject_id)
    return render(request, 'Hospital/edit.html', {'patient': edit_patient})


def do_edit(request):  # 对上传的数据进行存储 返回病人
    if not request.session.get('is_login', None):
        return redirect('/login/')
    gender = request.POST['gender']
    dob = request.POST['dob']
    dod = request.POST['dod']
    expire_flag = request.POST['expire_flag']
    subject_id = request.POST['subject_id']
    language = request.POST['language']
    religion = request.POST['religion']
    marital_status = request.POST['marital_status']
    ethnicity = request.POST['ethnicity']
    edited_patient = Patients.objects.filter(subject_id=subject_id)
    edited_patient.update(gender=gender)
    edited_patient.update(dob=dob)
    edited_patient.update(dod=dod)
    edited_patient.update(expire_flag=expire_flag)
    edited_patient.update(language=language)
    edited_patient.update(religion=religion)
    edited_patient.update(marital_status=marital_status)
    edited_patient.update(ethnicity=ethnicity)
    return redirect("Hospital:detail", subject_id)


def edit_adm(request, hadm_id, subject_id):  # 编辑页面
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    edit_adm = Admissions.objects.get(hadm_id=hadm_id)
    return render(request, 'Hospital/edit_adm.html', {'adm': edit_adm})


def do_edit_adm(request):  # 对上传的数据进行存储 结束返回病人列表
    if not request.session.get('is_login', None):
        return redirect('/login/')
    hadm_id = request.POST['hadm_id']  # 已定
    edregtime = request.POST['edregtime']
    subject_id = request.POST['subject_id']  # 已定
    admittime = request.POST['admittime']
    dischtime = request.POST['dischtime']
    admission_type = request.POST['admission_type']
    admission_location = request.POST['admission_location']
    discharge_location = request.POST['discharge_location']
    insurance = request.POST['insurance']
    edouttime = request.POST['edouttime']
    diagnosis = request.POST['diagnosis']
    hospital_expire_flag = request.POST["hospital_expire_flag"]
    has_chartevents_data = request.POST['has_chartevents_data']
    edited = Admissions.objects.filter(hadm_id=hadm_id)
    edited.update(admittime=admittime)
    edited.update(dischtime=dischtime)
    edited.update(admission_location=admission_location)
    edited.update(discharge_location=discharge_location)
    edited.update(insurance=insurance)
    edited.update(edregtime=edregtime)
    edited.update(admission_type=admission_type)
    edited.update(edouttime=edouttime)
    edited.update(diagnosis=diagnosis)
    edited.update(hospital_expire_flag=hospital_expire_flag)
    edited.update(has_chartevents_data=has_chartevents_data)
    return redirect("Hospital:detail", subject_id)


def insert(request):  # 新增病人页面
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    return render(request, 'Hospital/insert.html')


def do_insert(request):  # 对上传的数据进行保存，保存成功返回病人列表
    if not request.session.get('is_login', None):
        return redirect('/login/')
    gender = request.POST['gender']
    dob = request.POST['dob']
    dod = request.POST['dod']
    expire_flag = request.POST['expire_flag']
    language = request.POST['language']
    religion = request.POST['religion']
    marital_status = request.POST['marital_status']
    ethnicity = request.POST['ethnicity']
    row_id = Patients.objects.all().aggregate(Max('row_id'))['row_id__max'] + 1
    subject_id = Patients.objects.all().aggregate(Max('subject_id'))['subject_id__max'] + 1
    Patients.objects.create(row_id=row_id, subject_id=subject_id, gender=gender, dob=dob, dod=dod,
                            expire_flag=expire_flag, language=language, religion=religion,
                            marital_status=marital_status, ethnicity=ethnicity)
    return redirect("Hospital:detail", subject_id)


def delete(request, subject_id):  # 删除病人
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    do_delete = Patients.objects.filter(subject_id=subject_id)
    do_delete.delete()
    return redirect("Hospital:list")


def filter(request):  # 筛选
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'Hospital/filter.html')


def do_filter(request):  # 筛选
    if not request.session.get('is_login', None):
        return redirect('/login/')
    conditions = {}
    if request.POST['subject_id'] != "":
        conditions['subject_id__contains'] = request.POST['subject_id']
    if request.POST['gender'] != "":
        conditions['gender__contains'] = request.POST['gender']
    if request.POST['mode'] == "lte":
        if request.POST['dob'] != "":
            conditions['dob__lte'] = request.POST['dob']
    if request.POST['mode'] == "gte":
        if request.POST['dob'] != "":
            conditions['dob__gte'] = request.POST['dob']
    if request.POST['mode'] == "con":
        if request.POST['dob'] != "":
            conditions['dob__contains'] = request.POST['dob']
    if request.POST['mode_d'] == "lte":
        if request.POST['dod'] != "":
            conditions['dod__lte'] = request.POST['dod']
    if request.POST['mode_d'] == "gte":
        if request.POST['dod'] != "":
            conditions['dod__gte'] = request.POST['dod']
    if request.POST['mode_d'] == "con":
        if request.POST['dod'] != "":
            conditions['dod__contains'] = request.POST['dod']
    if request.POST['expire_flag'] != "":
        conditions['expire_flag__contains'] = request.POST['expire_flag']
    if request.POST['language'] != "":
        conditions['language__contains'] = request.POST['language']
    if request.POST['religion'] != "":
        conditions['religion__contains'] = request.POST['religion']
    if request.POST['marital_status'] != "":
        conditions['marital_status__contains'] = request.POST['marital_status']
    if request.POST['ethnicity'] != "":
        conditions['ethnicity__contains'] = request.POST['ethnicity']
    patients = Patients.objects.filter(**conditions)
    sex_m = patients.filter(gender='M').count()
    sex_f = patients.filter(gender='F').count()
    un_dead = patients.filter(expire_flag='0').count()
    dead = patients.filter(expire_flag='1').count()
    return render(request, 'Hospital/filtered.html', locals())


def do_filter_adm(request):  # 筛选
    if not request.session.get('is_login', None):
        return redirect('/login/')
    conditions = {}
    if request.POST['hadm_id'] != "":
        conditions['hadm_id__contains'] = request.POST['hadm_id']
    if request.POST['subject_id'] != "":
        conditions['subject_id__contains'] = request.POST['subject_id']
    if request.POST['mode_1t'] == "lte":
        if request.POST['admittime'] != "":
            conditions['admittime__lte'] = request.POST['admittime']
    if request.POST['mode_1t'] == "gte":
        if request.POST['admittime'] != "":
            conditions['admittime__gte'] = request.POST['admittime']
    if request.POST['mode_1t'] == "con":
        if request.POST['admittime'] != "":
            conditions['admittime__contains'] = request.POST['admittime']
    if request.POST['mode_2t'] == "lte":
        if request.POST['dischtime'] != "":
            conditions['dischtime__lte'] = request.POST['dischtime']
    if request.POST['mode_2t'] == "gte":
        if request.POST['dischtime'] != "":
            conditions['dischtime__gte'] = request.POST['dischtime']
    if request.POST['mode_2t'] == "con":
        if request.POST['dischtime'] != "":
            conditions['dischtime__contains'] = request.POST['dischtime']
    if request.POST['admission_type'] != "":
        conditions['admission_type__contains'] = request.POST['admission_type']
    if request.POST['admission_location'] != "":
        conditions['admission_location__contains'] = request.POST['admission_location']
    if request.POST['discharge_location'] != "":
        conditions['discharge_location__contains'] = request.POST['discharge_location']
    if request.POST['insurance'] != "":
        conditions['insurance__contains'] = request.POST['insurance']
    if request.POST['mode_3t'] == "lte":
        if request.POST['edregtime'] != "":
            conditions['edregtime__lte'] = request.POST['edregtime']
    if request.POST['mode_3t'] == "gte":
        if request.POST['edregtime'] != "":
            conditions['edregtime__gte'] = request.POST['edregtime']
    if request.POST['mode_3t'] == "con":
        if request.POST['edregtime'] != "":
            conditions['edregtime__contains'] = request.POST['edregtime']
    if request.POST['mode_4t'] == "lte":
        if request.POST['edouttime'] != "":
            conditions['edouttime__lte'] = request.POST['edouttime']
    if request.POST['mode_4t'] == "gte":
        if request.POST['edouttime'] != "":
            conditions['edouttime__gte'] = request.POST['edouttime']
    if request.POST['mode_4t'] == "con":
        if request.POST['edouttime'] != "":
            conditions['edouttime__contains'] = request.POST['edouttime']
    if request.POST['diagnosis'] != "":
        conditions['diagnosis__contains'] = request.POST['diagnosis']
    if request.POST['hospital_expire_flag'] != "":
        conditions['hospital_expire_flag__contains'] = request.POST['hospital_expire_flag']
    if request.POST['has_chartevents_data'] != "":
        conditions['has_chartevents_data__contains'] = request.POST['has_chartevents_data']
    adm = Admissions.objects.filter(**conditions).values('subject_id')
    patients = Patients.objects.filter(subject_id__in=adm)
    sex_m = patients.filter(gender='M').count()
    sex_f = patients.filter(gender='F').count()
    un_dead = patients.filter(expire_flag='0').count()
    dead = patients.filter(expire_flag='1').count()
    return render(request, 'Hospital/filtered.html', locals())


def do_select(request):  # 通过SubjcetID查找病人
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if not is_num_by_except(request.POST['subject_id']):
        return render(request, 'Hospital/404.html')
    subject_id = request.POST['subject_id']
    if Patients.objects.filter(subject_id=subject_id):
        return redirect("Hospital:detail", subject_id)
    return render(request, 'Hospital/404.html')


def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def do_select_adm(request):  # 通过hadm_id查找问诊
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if not is_num_by_except(request.POST['hadm_id']):
        return render(request, 'Hospital/404.html')
    hadm_id = request.POST['hadm_id']
    if Admissions.objects.filter(hadm_id=hadm_id):
        subject_id = Admissions.objects.get(hadm_id=hadm_id).subject_id
        return redirect("Hospital:detail", subject_id)
    return render(request, 'Hospital/404.html')


def insert_adm(request, subject_id):  # 新增问诊 页面
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    pat_adm = Patients.objects.get(subject_id=subject_id)
    return render(request, "Hospital/insert_adm.html", {'patient': pat_adm})


def form_insert_adm(request):  # 新增问诊 表单
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    subject_id = request.POST['subject_id']
    pat_adm = Patients.objects.filter(subject_id=subject_id)
    if pat_adm.count() == 0:
        return render(request, 'Hospital/404.html')
    pat = Patients.objects.get(subject_id=subject_id)
    return render(request, "Hospital/insert_adm.html", {'patient': pat})


def do_insert_adm(request):  # 对上传的数据进行保存，保存成功返回问诊列表
    if not request.session.get('is_login', None):
        return redirect('/login/')
    row_id = Admissions.objects.all().aggregate(Max('row_id'))['row_id__max'] + 1
    hadm_id = Admissions.objects.all().aggregate(Max('hadm_id'))['hadm_id__max'] + 1
    subject_id = request.POST['subject_id']  # 已定
    admittime = request.POST['admittime']
    dischtime = request.POST['dischtime']
    admission_type = request.POST['admission_type']
    admission_location = request.POST['admission_location']
    discharge_location = request.POST['discharge_location']
    insurance = request.POST['insurance']
    edregtime = request.POST['edregtime']
    edouttime = request.POST['edouttime']
    diagnosis = request.POST['diagnosis']
    hospital_expire_flag = request.POST['hospital_expire_flag']
    has_chartevents_data = request.POST['has_chartevents_data']
    Admissions.objects.create(row_id=row_id, subject_id=subject_id, hadm_id=hadm_id, admittime=admittime,
                              dischtime=dischtime, admission_type=admission_type, admission_location=admission_location,
                              discharge_location=discharge_location, insurance=insurance, edregtime=edregtime,
                              edouttime=edouttime, diagnosis=diagnosis, hospital_expire_flag=hospital_expire_flag,
                              has_chartevents_data=has_chartevents_data)
    return redirect("Hospital:detail", subject_id)


def adm_delete(request, hadm_id, subject_id):  # 删除问诊
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.session.get('user_auth') == '0':
        return render(request, 'Hospital/403.html')
    do_delete = Admissions.objects.filter(hadm_id=hadm_id)
    do_delete.delete()
    return redirect("Hospital:detail", subject_id)


def moreinfo(request, hadm_id, subject_id):  # 查看某次问诊的全部
    if not request.session.get('is_login', None):
        return redirect('/login/')
    pre = Prescriptions.objects.filter(hadm_id=hadm_id)
    lab = Labevents.objects.filter(hadm_id=hadm_id)
    time = Datetimeevents.objects.filter(hadm_id=hadm_id)
    cpt = Cptevents.objects.filter(hadm_id=hadm_id)
    flagabnormal = Labevents.objects.filter(hadm_id=hadm_id, flag__iexact='abnormal').count()
    flagnone = Labevents.objects.filter(hadm_id=hadm_id).count() - flagabnormal
    return render(request, 'Hospital/moreinfo.html',
                  {'lab': lab, 'pre': pre, 'time': time, 'cpt': cpt, 'fa': flagabnormal, 'fn': flagnone,
                   'subject_id': subject_id, 'hadm_id': hadm_id})


def hospital(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    cg = Caregivers.objects.all()
    dcpt = DCpt.objects.all()
    dlab = DLabitems.objects.all()
    return render(request, 'Hospital/Hospital.html', {'cg': cg, 'dcpt': dcpt, 'dlab': dlab})
