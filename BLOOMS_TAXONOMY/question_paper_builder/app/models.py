from django.db import models


class College(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Branch(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('college', 'name')


SEMESTER_CHOICES = [
    ('SEM I',   'Semester I'),
    ('SEM II',  'Semester II'),
    ('SEM III', 'Semester III'),
    ('SEM IV',  'Semester IV'),
    ('SEM V',   'Semester V'),
    ('SEM VI',  'Semester VI'),
    ('SEM VII', 'Semester VII'),
    ('SEM VIII','Semester VIII'),
]

YEAR_CHOICES = [
    ('First Year',  'First Year'),
    ('Second Year', 'Second Year'),
    ('Third Year',  'Third Year'),
    ('Fourth Year', 'Fourth Year'),
]

EXAM_TYPE_CHOICES = [
    ('Unit Test I',   'Unit Test I'),
    ('Unit Test II',  'Unit Test II'),
    ('Unit Test III', 'Unit Test III'),
    ('Mid Semester',  'Mid Semester'),
    ('End Semester',  'End Semester'),
]


class Subject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    subject_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.semester})"

    class Meta:
        ordering = ['name']
        unique_together = ('branch', 'name', 'semester')


class Subject_data(models.Model):
    college_name = models.CharField(max_length=200)
    branch_name  = models.CharField(max_length=100)
    semester     = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=150)
    course_code  = models.CharField(max_length=30, blank=True, default='')
    year         = models.CharField(max_length=50)
    faculty      = models.CharField(max_length=100)
    exam_type    = models.CharField(max_length=50, default='Unit Test I')
    qb           = models.FileField()
    q1  = models.CharField(max_length=1000)
    q2  = models.CharField(max_length=1000)
    q3  = models.CharField(max_length=1000)
    q4  = models.CharField(max_length=1000)
    q5  = models.CharField(max_length=1000)
    q6  = models.CharField(max_length=1000)
    q7  = models.CharField(max_length=1000)
    q8  = models.CharField(max_length=1000)
    q9  = models.CharField(max_length=1000)
    q10 = models.CharField(max_length=1000)
    bl1  = models.CharField(max_length=50)
    bl2  = models.CharField(max_length=50)
    bl3  = models.CharField(max_length=50)
    bl4  = models.CharField(max_length=50)
    bl5  = models.CharField(max_length=50)
    bl6  = models.CharField(max_length=50)
    bl7  = models.CharField(max_length=50)
    bl8  = models.CharField(max_length=50)
    bl9  = models.CharField(max_length=50)
    bl10 = models.CharField(max_length=50)
    co1  = models.CharField(max_length=10, default='CO1')
    co2  = models.CharField(max_length=10, default='CO1')
    co3  = models.CharField(max_length=10, default='CO1')
    co4  = models.CharField(max_length=10, default='CO1')
    co5  = models.CharField(max_length=10, default='CO1')
    co6  = models.CharField(max_length=10, default='CO1')
    co7  = models.CharField(max_length=10, default='CO1')
    co8  = models.CharField(max_length=10, default='CO1')
    co9  = models.CharField(max_length=10, default='CO1')
    co10 = models.CharField(max_length=10, default='CO1')
    m1  = models.IntegerField()
    m2  = models.IntegerField()
    m3  = models.IntegerField()
    m4  = models.IntegerField()
    m5  = models.IntegerField()
    m6  = models.IntegerField()
    m7  = models.IntegerField()
    m8  = models.IntegerField()
    m9  = models.IntegerField()
    m10 = models.IntegerField()
    date       = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.branch_name} – {self.semester} – {self.subject_name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Question Paper'
        verbose_name_plural = 'Question Papers'
