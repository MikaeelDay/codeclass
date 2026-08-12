from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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