from Hospital.models import Caregivers
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings
import pytz


def hash_code(s, salt='jhw2333'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自MIMIC HOSPITAL的注册确认邮件'

    text_content = '''感谢注册MIMIC HOSPITAL！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>MIMIC HOSPITAL</a>，\
                    这里是基于MIMIC数据库实现的数据管理系统！</p>
                    <p>请点击链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('Hospital:dashboard')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_auth'] = user.auth
                request.session['user_name'] = user.name
                return redirect('Hospital:dashboard')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('Hospital:dashboard')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            cg_id = register_form.cleaned_data.get('cg_id')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if Caregivers.objects.filter(cgid=cg_id).count() == 0:
                message = '不存在此医护人员！'
                return render(request, 'login/register.html', locals())
            else:
                if password1 != password2:
                    message = '两次输入的密码不同！'
                    return render(request, 'login/register.html', locals())
                else:
                    same_name_user = models.User.objects.filter(name=username)
                    if same_name_user:
                        message = '用户名已经存在'
                        return render(request, 'login/register.html', locals())
                    same_email_user = models.User.objects.filter(email=email)
                    if same_email_user:
                        message = '该邮箱已经被注册了！'
                        return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.cg_id = cg_id
                label = Caregivers.objects.get(cgid=cg_id).label
                if 'RN' in label:
                    new_user.auth = '0'
                else:
                    new_user.auth = '1'
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    return redirect("/login/")


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def forgetpwd(request):
    if request.session.get('is_login', None):
        return redirect('Hospital:dashboard')

    if request.method == 'POST':
        forget_form = forms.ForgetPwdForm(request.POST)
        message = "请检查填写的内容！"
        if forget_form.is_valid():
            email = forget_form.cleaned_data.get('email')
            if models.User.objects.filter(email=email).count() == 0:
                message = '此邮箱尚未注册！'
                return render(request, 'login/forget.html', locals())
            else:
                code = make_forget_confirm_string(email)
                send_forget_email(email, code)
                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/forget.html', locals())
    forget_form = forms.ForgetPwdForm(request.POST)
    return render(request, 'login/forget.html', locals())


def send_forget_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自MIMIC HOSPITAL的密码找回邮件'

    text_content = '''感谢找回MIMIC HOSPITAL账号！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢登录<a href="http://{}/reset_confirm/?code={}" target=blank>MIMIC HOSPITAL</a>，\
                    这里是基于MIMIC数据库实现的数据管理系统！</p>
                    <p>请点击链接找回密码！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def make_forget_confirm_string(email):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(email, now)
    models.ResetConfirmString.objects.create(code=code, email=email, )
    return code


def reset_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ResetConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.delete()
        message = '您的邮件已经过期！请重新请求找回密码!'
        return render(request, 'login/confirm.html', locals())
    else:
        return redirect('reset', code)


def reset(request, code):
    if request.session.get('is_login', None):
        return redirect('Hospital:dashboard')
    reset_form = forms.ResetForm()
    return render(request, 'login/reset.html', {'code': code, 'reset_form': reset_form})


def do_reset(request, code):
    if request.session.get('is_login', None):
        return redirect('Hospital:dashboard')

    message = ''
    try:
        confirm = models.ResetConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    if request.method == 'POST':
        reset_form = forms.ResetForm(request.POST)
        message = "请检查填写的内容！"
        if reset_form.is_valid():
            password1 = reset_form.cleaned_data.get('password1')
            password2 = reset_form.cleaned_data.get('password2')
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/reset.html', locals())
            user = models.User.objects.get(email=confirm.email)
            user.password = hash_code(password1)
            user.save()
            confirm.delete()
            return redirect('/login/')
    reset_form = forms.ResetForm(request.POST)
    return render(request, 'login/reset.html', locals())
