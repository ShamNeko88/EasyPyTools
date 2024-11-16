from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label="ユーザー名",
        max_length=50,
        validators=[MinLengthValidator(3)],  # 3文字以上のバリデーション
        error_messages={
            'required': 'ユーザー名は必須です。',
            'max_length': 'ユーザー名は50文字以内である必要があります。',
            'min_length': 'ユーザー名は3文字以上である必要があります。',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8)],  # 8文字以上のバリデーション
        label="パスワード"
    )

    class Meta:
        model = User
        fields = ['username', 'password']
