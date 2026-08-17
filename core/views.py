from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .code_runner import run_python_code
from .models import Submission, Article
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ArticleForm
from django.core.paginator import Paginator



STARTER_CODE = '''# اینجا کد پایتون خودتان را بنویسید
print("سلام دنیا!")
'''


def home(request):
    articles_qs = Article.objects.filter(published=True)
    paginator = Paginator(articles_qs, 6)  # ۶ مقاله در هر صفحه
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)
    return render(request, "core/home.html", {"articles": articles})


@login_required
def dashboard(request):
    my_submissions = request.user.submissions.all()[:20]
    return render(
        request,
        "core/dashboard.html",
        {
            "starter_code": STARTER_CODE,
            "my_submissions": my_submissions,
        },
    )

@login_required
@require_POST
def run_code(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "داده‌ی ارسالی نامعتبر است."}, status=400)

    code = data.get("code", "")
    if not code.strip():
        return JsonResponse({"error": "کدی برای اجرا نوشته نشده است."}, status=400)

    result = run_python_code(code)
    return JsonResponse(result)

@login_required
@require_POST
def save_submission(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "داده‌ی ارسالی نامعتبر است."}, status=400)

    code = data.get("code", "")
    output = data.get("output", "")
    title = (data.get("title") or "").strip()

    if not code.strip():
        return JsonResponse({"error": "کدی برای ثبت وجود ندارد."}, status=400)

    submission = Submission.objects.create(
        student=request.user,
        title=title,
        code=code,
        output=output,
    )
    return JsonResponse({
        "ok": True,
        "id": submission.id,
        "created_at": submission.created_at.strftime("%Y-%m-%d %H:%M"),
    })

def is_instructor(user):
    return user.is_staff


@user_passes_test(is_instructor)
def instructor_overview(request):
    from django.contrib.auth import get_user_model
    from django.db.models import Count

    User = get_user_model()
    students = (
        User.objects.filter(is_staff=False)
        .annotate(submission_count=Count("submissions"))
        .order_by("username")
    )
    return render(request, "core/instructor_overview.html", {"students": students})


@user_passes_test(is_instructor)
def instructor_student_detail(request, user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    student = get_object_or_404(User, pk=user_id)
    submissions = student.submissions.all()
    return render(
        request,
        "core/instructor_student_detail.html",
        {"student": student, "submissions": submissions},
    )

@user_passes_test(is_instructor)
@require_POST
def mark_reviewed(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    submission.reviewed = True
    note = request.POST.get("note", "").strip()
    if note:
        submission.instructor_note = note
    submission.save()
    return redirect("instructor_student_detail", user_id=submission.student_id)



def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    return render(request, "core/article_detail.html", {"article": article})


@user_passes_test(is_instructor)
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("article_detail", slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, "core/article_form.html", {"form": form, "mode": "create"})


@user_passes_test(is_instructor)
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("article_detail", slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, "core/article_form.html", {"form": form, "mode": "edit", "article": article})


@user_passes_test(is_instructor)
def my_articles(request):
    articles_qs = Article.objects.filter(author=request.user)
    paginator = Paginator(articles_qs, 10)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)
    return render(request, "core/my_articles.html", {"articles": articles})

@user_passes_test(is_instructor)
@require_POST
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    article.delete()
    return redirect("my_articles")