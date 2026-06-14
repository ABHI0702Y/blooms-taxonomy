from django.urls import path
from app import views

urlpatterns = [
    path("",               views.index,       name="home"),
    path("log_in",         views.log_in,      name="log_in"),
    path("register",       views.register,    name="register"),
    path("log_out",        views.log_out,     name="log_out"),
    path("dashboard",      views.dashboard,   name="dashboard"),
    path("result",         views.result,      name="result"),
    path("history",        views.history,     name="history"),
    path("paper/<int:pk>", views.view_paper,  name="view_paper"),

    path("paper/<int:pk>/delete", views.delete_paper, name="delete_paper"),

    # AJAX endpoints
    path("ajax/branches",       views.get_branches,   name="get_branches"),
    path("ajax/subjects",       views.get_subjects,   name="get_subjects"),
    path("ajax/preview_csv",    views.preview_csv,    name="preview_csv"),
    path("ajax/swap_question",  views.swap_question,  name="swap_question"),
]
