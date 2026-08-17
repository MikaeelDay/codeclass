from django.conf import settings
from django.db import models
from django.utils.text import slugify



class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    title = models.CharField(max_length=150, blank=True)
    code = models.TextField()
    output = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    instructor_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title or 'بدون عنوان'} — {self.student.username}"


class Article(models.Model):
    title = models.CharField("عنوان", max_length=200)
    slug = models.SlugField("نامک", max_length=220, unique=True, blank=True)
    summary = models.CharField("خلاصه", max_length=300, blank=True)
    content = models.TextField("متن مقاله")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="نویسنده",
    )
    published = models.BooleanField("منتشرشده", default=True)
    created_at = models.DateTimeField("تاریخ انتشار", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین ویرایش", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)
