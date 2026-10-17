from django import forms

from .models import Category, Post, Topic


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
        labels = {"content": "Ваше повідомлення"}
        widgets = {"content": forms.Textarea(attrs={"rows": 4, "maxlength": 2000})}

    def clean_content(self):
        text = self.cleaned_data["content"].strip()
        if len(text) < 2:
            raise forms.ValidationError("Повідомлення занадто коротке.")
        if len(text) > 2000:
            raise forms.ValidationError("Максимум 2000 символів.")
        return text


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("category", "title")
        labels = {"category": "Розділ", "title": "Назва гілки"}

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Назва має містити щонайменше 3 символи.")
        return title


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {"name": "Назва розділу"}

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Назва занадто коротка.")
        return name
