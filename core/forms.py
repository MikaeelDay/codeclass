from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "summary", "content", "published"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "عنوان مقاله"}),
            "summary": forms.TextInput(attrs={"placeholder": "خلاصه‌ی کوتاه (اختیاری)"}),
            "content": forms.Textarea(attrs={"rows": 14, "placeholder": "متن کامل مقاله..."}),
        }