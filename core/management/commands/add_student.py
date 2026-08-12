from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "یک حساب کارآموز جدید می‌سازد. مثال: python manage.py add_student ali 123456"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            raise CommandError(f"کاربری با نام «{username}» از قبل وجود دارد.")

        User.objects.create_user(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f"حساب کارآموز «{username}» با موفقیت ساخته شد."))