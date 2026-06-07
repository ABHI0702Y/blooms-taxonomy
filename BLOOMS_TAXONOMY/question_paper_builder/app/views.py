from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import JsonResponse

from app.verify import authentication, form_varification
from .form import question_paper_form
from app.models import Subject_data, College, Branch, Subject

import pandas as pd
import pickle
import numpy as np

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"

with open(DATASET_DIR / "blooms_level.pkl", "rb") as f:
    blooms_model = pickle.load(f)
with open(DATASET_DIR / "blooms_vector.pkl", "rb") as f:
    blooms_vector = pickle.load(f)


# ── Public views ─────────────────────────────────────────────────────────────

def index(request):
    stats = {
        'colleges': College.objects.count(),
        'papers': Subject_data.objects.count(),
        'subjects': Subject.objects.count(),
    }
    return render(request, "index.html", {'stats': stats})


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("log_in")
    return render(request, "log_in.html")


def register(request):
    if request.method == "POST":
        fname    = request.POST['fname']
        lname    = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password=password)
            user.first_name = fname
            user.last_name  = lname
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("log_in")
        else:
            messages.error(request, verify)
            return redirect("register")
    return render(request, "register.html")


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("/")


# ── AJAX helpers ─────────────────────────────────────────────────────────────

def get_branches(request):
    college_id = request.GET.get('college_id')
    branches = list(Branch.objects.filter(college_id=college_id).values('id', 'name'))
    return JsonResponse(branches, safe=False)


def get_subjects(request):
    branch_id = request.GET.get('branch_id')
    semester  = request.GET.get('semester')
    subjects  = list(Subject.objects.filter(branch_id=branch_id, semester=semester).values('id', 'name'))
    return JsonResponse(subjects, safe=False)


def preview_csv(request):
    """AJAX: read uploaded CSV, run ML predictions, return per-question preview."""
    if request.method != "POST":
        return JsonResponse({'error': 'POST required'}, status=405)
    csv_file = request.FILES.get('qb')
    if not csv_file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    try:
        reader = pd.read_csv(csv_file)
        if 'question' not in reader.columns:
            return JsonResponse({'error': "CSV must have a 'question' column"}, status=400)

        model      = pickle.load(open(DATASET_DIR / 'model.pkl', 'rb'))
        vectorizer = pickle.load(open(DATASET_DIR / 'vectorizer.pkl', 'rb'))

        X_new  = vectorizer.transform(reader['question'])
        y_pred = np.array(model.predict(X_new)).astype(int)
        reader['predicted_marks'] = y_pred

        rows = []
        for _, row in reader.iterrows():
            vec   = blooms_vector.transform([row['question']])
            level = blooms_model.predict(vec)[0]
            rows.append({
                'question':      row['question'],
                'marks':         int(row['predicted_marks']),
                'blooms_level':  level,
            })
        return JsonResponse({'rows': rows})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ── Dashboard ────────────────────────────────────────────────────────────────

@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    context = {
        'fname': request.user.first_name,
        'form':  question_paper_form(),
    }
    if request.method == "POST":
        form = question_paper_form(request.POST, request.FILES)
        try:
            if form.is_valid():
                college_obj  = form.cleaned_data['college_name']
                branch_obj   = form.cleaned_data['branch_name']
                semester     = form.cleaned_data['semester']
                year         = form.cleaned_data['year']
                faculty      = form.cleaned_data['faculty']
                exam_type    = form.cleaned_data['exam_type']
                date         = form.cleaned_data['date']
                qb           = form.cleaned_data['qb']

                # Subject: prefer dropdown, fall back to manual text
                subject_obj    = form.cleaned_data.get('subject_name')
                custom_subject = form.cleaned_data.get('custom_subject', '').strip()
                subject_name   = subject_obj.name if subject_obj else custom_subject
                if not subject_name:
                    messages.error(request, "Please select or enter a subject name.")
                    context['form'] = form
                    return render(request, "dashboard.html", context)

                verify_from = form_varification(faculty)
                if verify_from != "Success":
                    messages.error(request, verify_from)
                    return redirect("dashboard")

                model      = pickle.load(open(DATASET_DIR / 'model.pkl', 'rb'))
                vectorizer = pickle.load(open(DATASET_DIR / 'vectorizer.pkl', 'rb'))

                reader    = pd.read_csv(qb)
                X_new     = vectorizer.transform(reader['question'])
                y_pred    = np.array(model.predict(X_new)).astype(int)
                reader['predicted_marks'] = y_pred

                # Ensure we have at least 2 questions per mark bucket 4-8
                buckets = {}
                for m in [4, 5, 6, 7, 8]:
                    bucket = reader[reader['predicted_marks'] == m]
                    if len(bucket) < 2:
                        messages.error(request, f"Not enough questions for {m}-mark category (need at least 2).")
                        return redirect("dashboard")
                    buckets[m] = bucket

                selected_data = pd.concat([
                    buckets[8].sample(n=2, random_state=24),
                    buckets[7].sample(n=2, random_state=24),
                    buckets[6].sample(n=2, random_state=24),
                    buckets[5].sample(n=2, random_state=24),
                    buckets[4].sample(n=2, random_state=24),
                ], axis=0)

                blooms_level = []
                for _, row in selected_data[['question']].iterrows():
                    vec   = blooms_vector.transform(row)
                    level = blooms_model.predict(vec)[0]
                    blooms_level.append(level)

                selected_list = []
                for _, row in selected_data[['question', 'predicted_marks']].iterrows():
                    selected_list.append(row.to_list())

                qus = []
                [qus.extend([str(q), str(m)]) for q, m in selected_list]

                college_name = college_obj.name
                branch_name  = branch_obj.name

                paper = Subject_data(
                    college_name=college_name, branch_name=branch_name,
                    semester=semester, subject_name=subject_name,
                    year=year, faculty=faculty, exam_type=exam_type,
                    qb=qb, date=date,
                    q1=qus[0],  q2=qus[2],  q3=qus[4],  q4=qus[6],  q5=qus[8],
                    q6=qus[10], q7=qus[12], q8=qus[14], q9=qus[16], q10=qus[18],
                    m1=qus[1],  m2=qus[3],  m3=qus[5],  m4=qus[7],  m5=qus[9],
                    m6=qus[11], m7=qus[13], m8=qus[15], m9=qus[17], m10=qus[19],
                    bl1=blooms_level[0],  bl2=blooms_level[1],  bl3=blooms_level[2],
                    bl4=blooms_level[3],  bl5=blooms_level[4],  bl6=blooms_level[5],
                    bl7=blooms_level[6],  bl8=blooms_level[7],  bl9=blooms_level[8],
                    bl10=blooms_level[9],
                )
                paper.save()

                output_path = Path(__file__).resolve().parent.parent / f"{branch_name}_{semester}_{subject_name}_question_paper.csv"
                selected_data.to_csv(output_path, index=False)

                return redirect("result")

            else:
                messages.error(request, "Please fix the form errors.")
                context['form'] = form
                return render(request, "dashboard.html", context)

        except Exception as e:
            messages.error(request, f"Error generating paper: {str(e)}")
            return redirect("dashboard")

    return render(request, "dashboard.html", context)


# ── Result & History ─────────────────────────────────────────────────────────

_LEVEL_COLORS = {
    'Remember':   '#3f51b5',
    'Understand': '#17a2b8',
    'Apply':      '#28a745',
    'Analyse':    '#ffc107',
    'Evaluate':   '#dc3545',
    'Create':     '#6f42c1',
}
_LEVEL_SCORE = {
    'Remember': 10, 'Understand': 20,
    'Apply': 50,    'Analyse': 65,
    'Evaluate': 80, 'Create': 100,
}
_LEVEL_ORDER = ['Remember', 'Understand', 'Apply', 'Analyse', 'Evaluate', 'Create']
_NORMALIZE_MAP = {
    'remenber': 'Remember', 'remember': 'Remember', 'recall': 'Remember',
    'understand': 'Understand', 'understanding': 'Understand', 'comprehend': 'Understand',
    'apply': 'Apply', 'application': 'Apply', 'applying': 'Apply',
    'analyze': 'Analyse', 'analyse': 'Analyse', 'analysis': 'Analyse', 'analyzing': 'Analyse',
    'evaluate': 'Evaluate', 'evaluation': 'Evaluate', 'evaluating': 'Evaluate',
    'create': 'Create', 'creation': 'Create', 'synthesis': 'Create', 'creating': 'Create',
}

def _normalize_level(raw: str) -> str:
    """Pick the highest Bloom's level from a potentially compound/misspelled label."""
    parts = [p.strip().lower() for p in str(raw).split(',')]
    mapped = [_NORMALIZE_MAP.get(p, p.capitalize()) for p in parts if p]
    best = 'Remember'
    for m in mapped:
        if m in _LEVEL_ORDER and _LEVEL_ORDER.index(m) > _LEVEL_ORDER.index(best):
            best = m
    return best


def _paper_context(paper, user):
    levels = [
        _normalize_level(paper.bl1), _normalize_level(paper.bl2),
        _normalize_level(paper.bl3), _normalize_level(paper.bl4),
        _normalize_level(paper.bl5), _normalize_level(paper.bl6),
        _normalize_level(paper.bl7), _normalize_level(paper.bl8),
        _normalize_level(paper.bl9), _normalize_level(paper.bl10),
    ]
    counts = {}
    for lv in levels:
        counts[lv] = counts.get(lv, 0) + 1

    chart_labels  = list(counts.keys())
    chart_data    = list(counts.values())
    chart_colors  = [_LEVEL_COLORS.get(l, '#999') for l in chart_labels]

    raw_score = sum(_LEVEL_SCORE.get(l, 30) for l in levels) / 10
    if raw_score >= 75:
        grade, grade_color, grade_msg = 'A', 'success', 'Excellent — high-order thinking dominant'
    elif raw_score >= 55:
        grade, grade_color, grade_msg = 'B', 'primary', 'Good — balanced cognitive coverage'
    elif raw_score >= 35:
        grade, grade_color, grade_msg = 'C', 'warning', 'Average — mostly recall & comprehension'
    else:
        grade, grade_color, grade_msg = 'D', 'danger', 'Needs improvement — too many recall questions'

    return {
        'fname':        user.first_name,
        'subject_data': paper,
        'chart_labels': chart_labels,
        'chart_data':   chart_data,
        'chart_colors': chart_colors,
        'quality_grade':      grade,
        'quality_color':      grade_color,
        'quality_msg':        grade_msg,
        'quality_score':      round(raw_score),
    }


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def result(request):
    paper = Subject_data.objects.order_by('-id').first()
    return render(request, "result.html", _paper_context(paper, request.user))


@login_required(login_url="log_in")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def history(request):
    papers = Subject_data.objects.all()
    return render(request, "history.html", {
        'fname': request.user.first_name,
        'papers': papers,
    })


@login_required(login_url="log_in")
def view_paper(request, pk):
    paper = get_object_or_404(Subject_data, pk=pk)
    return render(request, "result.html", _paper_context(paper, request.user))
