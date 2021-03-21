from django.db import models
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admissions(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject = models.ForeignKey('Patients', models.CASCADE, db_column='SUBJECT_ID', blank=True, null=True, to_field='subject_id')
    hadm_id = models.IntegerField(db_column='HADM_ID', unique=True, blank=True, null=True)
    admittime = models.CharField(db_column='ADMITTIME', max_length=50, blank=True, null=True)
    dischtime = models.CharField(db_column='DISCHTIME', max_length=50, blank=True, null=True)
    deathtime = models.CharField(db_column='DEATHTIME', max_length=50, blank=True, null=True)
    admission_type = models.CharField(db_column='ADMISSION_TYPE', max_length=50, blank=True, null=True)
    admission_location = models.CharField(db_column='ADMISSION_LOCATION', max_length=50, blank=True, null=True)
    discharge_location = models.CharField(db_column='DISCHARGE_LOCATION', max_length=50, blank=True, null=True)
    insurance = models.CharField(db_column='INSURANCE', max_length=255, blank=True, null=True)
    edregtime = models.CharField(db_column='EDREGTIME', max_length=50, blank=True, null=True)
    edouttime = models.CharField(db_column='EDOUTTIME', max_length=50, blank=True, null=True)
    diagnosis = models.CharField(db_column='DIAGNOSIS', max_length=300, blank=True, null=True)
    hospital_expire_flag = models.IntegerField(db_column='HOSPITAL_EXPIRE_FLAG', blank=True, null=True)
    has_chartevents_data = models.IntegerField(db_column='HAS_CHARTEVENTS_DATA', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admissions'
        verbose_name = "问诊"
        verbose_name_plural = "问诊"

    def __str__(self):
        return "问诊ID:{}".format(self.hadm_id)


class Caregivers(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    cgid = models.IntegerField(db_column='CGID', unique=True, blank=True, null=True)
    label = models.CharField(db_column='LABEL', max_length=15, blank=True, null=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caregivers'
        verbose_name = "医护人员"
        verbose_name_plural = "医护人员"

    def __str__(self):
        return "ID:{}".format(self.cgid)


class Cptevents(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject = models.ForeignKey('Patients', models.CASCADE, db_column='SUBJECT_ID', blank=True, null=True, to_field='subject_id')
    hadm = models.ForeignKey(Admissions, models.CASCADE, db_column='HADM_ID', blank=True, null=True, to_field='hadm_id')
    costcenter = models.CharField(db_column='COSTCENTER', max_length=10, blank=True, null=True)
    chartdate = models.CharField(db_column='CHARTDATE', max_length=50, blank=True, null=True)
    cpt_cd = models.CharField(db_column='CPT_CD', max_length=10, blank=True, null=True)
    cpt_number = models.IntegerField(db_column='CPT_NUMBER', blank=True, null=True)
    cpt_suffix = models.CharField(db_column='CPT_SUFFIX', max_length=5, blank=True, null=True)
    ticket_id_seq = models.IntegerField(db_column='TICKET_ID_SEQ', blank=True, null=True)
    sectionheader = models.CharField(db_column='SECTIONHEADER', max_length=50, blank=True, null=True)
    subsectionheader = models.CharField(db_column='SUBSECTIONHEADER', max_length=300, blank=True, null=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cptevents'


class DCpt(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    category = models.SmallIntegerField(db_column='CATEGORY', blank=True, null=True)
    sectionrange = models.CharField(db_column='SECTIONRANGE', max_length=100, blank=True, null=True)
    sectionheader = models.CharField(db_column='SECTIONHEADER', max_length=50, blank=True, null=True)
    subsectionrange = models.CharField(db_column='SUBSECTIONRANGE', unique=True, max_length=100, blank=True, null=True)
    subsectionheader = models.CharField(db_column='SUBSECTIONHEADER', max_length=300, blank=True, null=True)
    codesuffix = models.CharField(db_column='CODESUFFIX', max_length=5, blank=True, null=True)
    mincodeinsubsection = models.IntegerField(db_column='MINCODEINSUBSECTION', blank=True, null=True)
    maxcodeinsubsection = models.IntegerField(db_column='MAXCODEINSUBSECTION', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_cpt'


class DLabitems(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    itemid = models.IntegerField(db_column='ITEMID', unique=True, blank=True, null=True)
    label = models.CharField(db_column='LABEL', max_length=100, blank=True, null=True)
    fluid = models.CharField(db_column='FLUID', max_length=100, blank=True, null=True)
    category = models.CharField(db_column='CATEGORY', max_length=100, blank=True, null=True)
    loinc_code = models.CharField(db_column='LOINC_CODE', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_labitems'


class Datetimeevents(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject = models.ForeignKey('Patients', models.CASCADE, db_column='SUBJECT_ID', blank=True, null=True, to_field='subject_id')
    hadm = models.ForeignKey(Admissions, models.CASCADE, db_column='HADM_ID', blank=True, null=True, to_field='hadm_id')
    icustay_id = models.IntegerField(db_column='ICUSTAY_ID', blank=True, null=True)
    itemid = models.IntegerField(db_column='ITEMID', blank=True, null=True)
    charttime = models.CharField(db_column='CHARTTIME', max_length=50, blank=True, null=True)
    storetime = models.CharField(db_column='STORETIME', max_length=50, blank=True, null=True)
    cgid = models.ForeignKey('Caregivers', models.CASCADE, db_column='CGID', blank=True, null=True, to_field='cgid')
    value = models.CharField(db_column='VALUE', max_length=50, blank=True, null=True)
    valueuom = models.CharField(db_column='VALUEUOM', max_length=50, blank=True, null=True)
    warning = models.SmallIntegerField(db_column='WARNING', blank=True, null=True)
    error = models.SmallIntegerField(db_column='ERROR', blank=True, null=True)
    resultstatus = models.CharField(db_column='RESULTSTATUS', max_length=50, blank=True, null=True)
    stopped = models.CharField(db_column='STOPPED', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datetimeevents'


class Labevents(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject = models.ForeignKey('Patients', models.CASCADE, db_column='SUBJECT_ID', blank=True, null=True, to_field='subject_id')
    hadm = models.ForeignKey(Admissions, models.CASCADE, db_column='HADM_ID', blank=True, null=True, to_field='hadm_id')
    itemid = models.IntegerField(db_column='ITEMID', blank=True, null=True)
    charttime = models.CharField(db_column='CHARTTIME', max_length=50, blank=True, null=True)
    value = models.CharField(db_column='VALUE', max_length=200, blank=True, null=True)
    valuenum = models.FloatField(db_column='VALUENUM', blank=True, null=True)
    valueuom = models.CharField(db_column='VALUEUOM', max_length=20, blank=True, null=True)
    flag = models.CharField(db_column='FLAG', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'labevents'
        verbose_name = "检查"
        verbose_name_plural = "检查"


class Patients(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject_id = models.IntegerField(db_column='SUBJECT_ID', unique=True, blank=True, null=True)
    gender = models.CharField(db_column='GENDER', max_length=5, blank=True, null=True)
    dob = models.CharField(db_column='DOB', max_length=50, blank=True, null=True)
    dod = models.CharField(db_column='DOD', max_length=50, blank=True, null=True)
    dod_hosp = models.CharField(db_column='DOD_HOSP', max_length=50, blank=True, null=True)
    dod_ssn = models.CharField(db_column='DOD_SSN', max_length=50, blank=True, null=True)
    expire_flag = models.CharField(db_column='EXPIRE_FLAG', max_length=5, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients'
        verbose_name = "病人"
        verbose_name_plural = "病人"

    def __str__(self):
        return "病人ID:{}".format(self.subject_id)


class Prescriptions(models.Model):
    row_id = models.IntegerField(db_column='ROW_ID', primary_key=True)
    subject = models.ForeignKey(Patients, models.CASCADE, db_column='SUBJECT_ID', blank=True, null=True, to_field='subject_id')
    hadm = models.ForeignKey(Admissions, models.CASCADE, db_column='HADM_ID', blank=True, null=True, to_field='hadm_id')
    icustay_id = models.IntegerField(db_column='ICUSTAY_ID', blank=True, null=True)
    startdate = models.CharField(db_column='STARTDATE', max_length=50, blank=True, null=True)
    enddate = models.CharField(db_column='ENDDATE', max_length=50, blank=True, null=True)
    drug_type = models.CharField(db_column='DRUG_TYPE', max_length=100, blank=True, null=True)
    drug = models.CharField(db_column='DRUG', max_length=100, blank=True, null=True)
    drug_name_poe = models.CharField(db_column='DRUG_NAME_POE', max_length=100, blank=True, null=True)
    drug_name_generic = models.CharField(db_column='DRUG_NAME_GENERIC', max_length=100, blank=True, null=True)
    formulary_drug_cd = models.CharField(db_column='FORMULARY_DRUG_CD', max_length=120, blank=True, null=True)
    gsn = models.CharField(db_column='GSN', max_length=200, blank=True, null=True)
    ndc = models.CharField(db_column='NDC', max_length=120, blank=True, null=True)
    prod_strength = models.CharField(db_column='PROD_STRENGTH', max_length=120, blank=True, null=True)
    dose_val_rx = models.CharField(db_column='DOSE_VAL_RX', max_length=120, blank=True, null=True)
    dose_unit_rx = models.CharField(db_column='DOSE_UNIT_RX', max_length=120, blank=True, null=True)
    form_val_disp = models.CharField(db_column='FORM_VAL_DISP', max_length=120, blank=True, null=True)
    form_unit_disp = models.CharField(db_column='FORM_UNIT_DISP', max_length=120, blank=True, null=True)
    route = models.CharField(db_column='ROUTE', max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prescriptions'
        verbose_name = "处方"
        verbose_name_plural = "处方"
