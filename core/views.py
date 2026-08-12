from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .code_runner import run_python_code


STARTER_CODE = '''# اینجا کد پایتون خودتان را بنویسید
print("سلام دنیا!")
'''


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