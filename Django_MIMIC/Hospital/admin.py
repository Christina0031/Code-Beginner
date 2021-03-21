from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Admissions
from .models import Caregivers
from .models import Cptevents
from .models import DCpt
from .models import DLabitems
from .models import Datetimeevents
from .models import Labevents
from .models import Patients
from .models import Prescriptions

admin.site.register(Caregivers)
admin.site.register(Cptevents)
admin.site.register(DCpt)
admin.site.register(DLabitems)
admin.site.register(Labevents)
admin.site.register(Patients)
admin.site.register(Prescriptions)


@admin.register(Admissions)
class ArticleAdmin(admin.ModelAdmin):
    list_display=("row_id","subject","hadm_id","admittime")
    ordering=("row_id",)


@admin.register(Datetimeevents)
class ArticleAdmin(admin.ModelAdmin):
    list_display=("row_id","subject","hadm","cgid")
    ordering=("row_id",)