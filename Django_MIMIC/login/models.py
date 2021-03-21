from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    cg_id = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    auth = models.CharField(max_length=128, default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "验证码"
        verbose_name_plural = "验证码"


class ResetConfirmString(models.Model):
    code = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "找回账户验证码"
        verbose_name_plural = "找回账户验证码"
