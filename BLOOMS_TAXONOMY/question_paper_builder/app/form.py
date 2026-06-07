import datetime
from django import forms
from .models import College, Branch, Subject, SEMESTER_CHOICES, YEAR_CHOICES, EXAM_TYPE_CHOICES


class question_paper_form(forms.Form):
    college_name = forms.ModelChoiceField(
        queryset=College.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_college'}),
        empty_label="-- Select College --",
    )
    branch_name = forms.ModelChoiceField(
        queryset=Branch.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_branch'}),
        empty_label="-- Select Branch --",
    )
    year = forms.ChoiceField(
        choices=[('', '-- Select Year --')] + YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    semester = forms.ChoiceField(
        choices=[('', '-- Select Semester --')] + SEMESTER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_semester'}),
    )
    subject_name = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_subject'}),
        empty_label="-- Select Subject --",
        required=False,
    )
    custom_subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Or type subject name manually',
        }),
        required=False,
    )
    exam_type = forms.ChoiceField(
        choices=EXAM_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    faculty = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Faculty Name',
        }),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': datetime.date.today().isoformat(),
        }),
    )
    qb = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = datetime.date.today().isoformat()
        if 'college_name' in self.data:
            try:
                college_id = int(self.data.get('college_name'))
                self.fields['branch_name'].queryset = Branch.objects.filter(college_id=college_id)
            except (ValueError, TypeError):
                pass
        if 'branch_name' in self.data and 'semester' in self.data:
            try:
                branch_id = int(self.data.get('branch_name'))
                semester = self.data.get('semester')
                self.fields['subject_name'].queryset = Subject.objects.filter(
                    branch_id=branch_id, semester=semester
                )
            except (ValueError, TypeError):
                pass
