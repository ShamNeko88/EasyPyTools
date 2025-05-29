from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # パスワードハッシュの自動化等
from django.core.validators import MinLengthValidator


class UserRegistrationForm(UserCreationForm):
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

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # UserCreationFormのフィールドを使用


class EmailSettingForm(forms.ModelForm):
    email = forms.EmailField(
        label="メールアドレス",
        required=True,
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )

    class Meta:
        model = User
        fields = ['email']