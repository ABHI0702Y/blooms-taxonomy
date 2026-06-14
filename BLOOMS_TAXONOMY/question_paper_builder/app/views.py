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
import io


def _read_csv(csv_file):
    """Read CSV file robustly — handles questions that contain commas."""
    content = csv_file.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8-sig', errors='replace')
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    if not lines:
        raise ValueError("CSV file is empty")
    header = lines[0].strip('"').strip().lower()
    if header == 'question':
        question_lines = lines[1:]
    else:
        question_lines = lines
    questions = [l.strip('"').strip() for l in question_lines if l.strip()]
    if not questions:
        raise ValueError("No questions found in CSV")
    return pd.DataFrame({'question': questions})

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"

with open(DATASET_DIR / "blooms_level.pkl", "rb") as f:
    blooms_model = pickle.load(f)
with open(DATASET_DIR / "blooms_vector.pkl", "rb") as f:
    blooms_vector = pickle.load(f)

# Bloom's level → SPPU Course Outcome auto-mapping
_BLOOMS_CO = {
    'Remember': 'CO1', 'Understand': 'CO2',
    'Apply': 'CO3',    'Analyse': 'CO4',
    'Evaluate': 'CO5', 'Create': 'CO6',
}

def _ml_rank_and_assign(questions_series):
    """Return (reader_df_sorted, mark_assignments_list) using proportional tier split."""
    model_pk   = pickle.load(open(DATASET_DIR / 'model.pkl', 'rb'))
    vector_pk  = pickle.load(open(DATASET_DIR / 'vectorizer.pkl', 'rb'))
    X          = vector_pk.transform(questions_series)
    y_raw      = np.array(model_pk.predict(X), dtype=float)
    df         = pd.DataFrame({'question': questions_series.values, 'raw_score': y_raw})
    df         = df.sort_values('raw_score').reset_index(drop=True)
    n, q       = len(df), len(df) // 5
    marks      = []
    for i, m in enumerate([4, 5, 6, 7, 8]):
        marks.extend([m] * (q if i < 4 else n - 4 * q))
    df['predicted_marks'] = marks
    return df


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
        reader = _read_csv(csv_file)
        if 'question' not in reader.columns:
            return JsonResponse({'error': "CSV must have a 'question' column"}, status=400)

        model      = pickle.load(open(DATASET_DIR / 'model.pkl', 'rb'))
        vectorizer = pickle.load(open(DATASET_DIR / 'vectorizer.pkl', 'rb'))

        X_new = vectorizer.transform(reader['question'])
        y_raw = np.array(model.predict(X_new), dtype=float)

        reader = reader.copy()
        reader['raw_score'] = y_raw
        reader = reader.sort_values('raw_score').reset_index(drop=True)
        n_q = len(reader)
        q   = n_q // 5
        mark_assignments = []
        for i, m in enumerate([4, 5, 6, 7, 8]):
            count = q if i < 4 else n_q - 4 * q
            mark_assignments.extend([m] * count)
        reader['predicted_marks'] = mark_assignments

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

                course_code = form.cleaned_data.get('course_code', '').strip()

                verify_from = form_varification(faculty)
                if verify_from != "Success":
                    messages.error(request, verify_from)
                    return redirect("dashboard")

                reader = _read_csv(qb)
                if len(reader) < 10:
                    messages.error(request, f"CSV needs at least 10 questions (found {len(reader)}).")
                    return redirect("dashboard")

                reader = _ml_rank_and_assign(reader['question'])

                buckets = {m: reader[reader['predicted_marks'] == m] for m in [4, 5, 6, 7, 8]}
                selected_data = pd.concat([
                    buckets[8].sample(n=2, random_state=24),
                    buckets[7].sample(n=2, random_state=24),
                    buckets[6].sample(n=2, random_state=24),
                    buckets[5].sample(n=2, random_state=24),
                    buckets[4].sample(n=2, random_state=24),
                ], axis=0)

                blooms_level = []
                co_list      = []
                for _, row in selected_data[['question']].iterrows():
                    vec   = blooms_vector.transform([row['question']])
                    level = blooms_model.predict(vec)[0]
                    norm  = _normalize_level(level)
                    blooms_level.append(level)
                    co_list.append(_BLOOMS_CO.get(norm, 'CO1'))

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
                    course_code=course_code,
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
                    co1=co_list[0],  co2=co_list[1],  co3=co_list[2],
                    co4=co_list[3],  co5=co_list[4],  co6=co_list[5],
                    co7=co_list[6],  co8=co_list[7],  co9=co_list[8],
                    co10=co_list[9],
                )
                paper.save()

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
    bl_fields = [paper.bl1, paper.bl2, paper.bl3, paper.bl4, paper.bl5,
                 paper.bl6, paper.bl7, paper.bl8, paper.bl9, paper.bl10]
    co_fields = [paper.co1, paper.co2, paper.co3, paper.co4, paper.co5,
                 paper.co6, paper.co7, paper.co8, paper.co9, paper.co10]
    levels = [_normalize_level(b) for b in bl_fields]

    bl_counts = {}
    for lv in levels:
        bl_counts[lv] = bl_counts.get(lv, 0) + 1

    co_counts = {}
    for co in co_fields:
        co_counts[co] = co_counts.get(co, 0) + 1

    chart_labels  = list(bl_counts.keys())
    chart_data    = list(bl_counts.values())
    chart_colors  = [_LEVEL_COLORS.get(l, '#999') for l in chart_labels]

    co_chart_labels = sorted(co_counts.keys())
    co_chart_data   = [co_counts[k] for k in co_chart_labels]

    _BL_COLORS_MAP = {
        'Remember': '#3f51b5', 'Understand': '#17a2b8',
        'Apply': '#28a745',    'Analyse': '#e6a817',
        'Evaluate': '#dc3545', 'Create': '#6f42c1',
    }
    questions = []
    for i in range(1, 11):
        bl_raw = getattr(paper, f'bl{i}')
        norm   = _normalize_level(bl_raw)
        questions.append({
            'num':   i,
            'text':  getattr(paper, f'q{i}'),
            'marks': getattr(paper, f'm{i}'),
            'bloom': norm,
            'bloom_color': _BL_COLORS_MAP.get(norm, '#999'),
            'co':    getattr(paper, f'co{i}'),
        })

    raw_score = sum(_LEVEL_SCORE.get(l, 30) for l in levels) / 10
    hot_pct   = round(sum(1 for l in levels if l in ('Analyse','Evaluate','Create')) * 10)

    if raw_score >= 75:
        grade, grade_color, grade_msg = 'A', 'success', 'Excellent — high-order thinking dominant'
    elif raw_score >= 55:
        grade, grade_color, grade_msg = 'B', 'primary', 'Good — balanced cognitive coverage'
    elif raw_score >= 35:
        grade, grade_color, grade_msg = 'C', 'warning', 'Average — mostly recall & comprehension'
    else:
        grade, grade_color, grade_msg = 'D', 'danger', 'Needs improvement — too many recall questions'

    # CO coverage suggestions
    covered_cos = set(co_fields)
    missing_cos = [f'CO{i}' for i in range(1,7) if f'CO{i}' not in covered_cos]
    suggestion  = ''
    if missing_cos:
        suggestion = f"COs not covered: {', '.join(missing_cos)}. Consider adding questions targeting higher-order thinking to improve PO attainment."
    elif hot_pct < 30:
        suggestion = "Only {}% HOT questions (Analyse/Evaluate/Create). Add more complex questions to strengthen CO5/CO6 coverage.".format(hot_pct)

    return {
        'fname':        user.first_name,
        'subject_data': paper,
        'chart_labels': chart_labels,
        'chart_data':   chart_data,
        'chart_colors': chart_colors,
        'co_chart_labels': co_chart_labels,
        'co_chart_data':   co_chart_data,
        'questions':       questions,
        'quality_grade':   grade,
        'quality_color':   grade_color,
        'quality_msg':     grade_msg,
        'quality_score':   round(raw_score),
        'hot_pct':         hot_pct,
        'suggestion':      suggestion,
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


@login_required(login_url="log_in")
def delete_paper(request, pk):
    if request.method == 'POST':
        paper = get_object_or_404(Subject_data, pk=pk)
        paper.delete()
        messages.success(request, "Paper deleted successfully.")
    return redirect('history')


@login_required(login_url="log_in")
def swap_question(request):
    """AJAX: replace one question in a saved paper from the same marks tier."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        paper_id = int(request.POST.get('paper_id', 0))
        q_num    = int(request.POST.get('q_num', 1))
        paper    = get_object_or_404(Subject_data, pk=paper_id)

        qb_file  = paper.qb
        qb_file.seek(0)
        reader   = _read_csv(qb_file)
        reader   = _ml_rank_and_assign(reader['question'])

        current_qs   = [getattr(paper, f'q{i}') for i in range(1, 11)]
        target_marks = int(getattr(paper, f'm{q_num}'))

        pool = reader[
            (reader['predicted_marks'] == target_marks) &
            (~reader['question'].isin(current_qs))
        ]
        if pool.empty:
            return JsonResponse({'error': 'No alternative questions available in this tier.'}, status=400)

        replacement = pool.sample(n=1).iloc[0]
        new_q   = replacement['question']
        vec     = blooms_vector.transform([new_q])
        new_bl  = blooms_model.predict(vec)[0]
        new_co  = _BLOOMS_CO.get(_normalize_level(new_bl), 'CO1')

        setattr(paper, f'q{q_num}',  new_q)
        setattr(paper, f'bl{q_num}', new_bl)
        setattr(paper, f'co{q_num}', new_co)
        paper.save(update_fields=[f'q{q_num}', f'bl{q_num}', f'co{q_num}'])

        return JsonResponse({'question': new_q, 'blooms': new_bl, 'co': new_co, 'marks': target_marks})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
