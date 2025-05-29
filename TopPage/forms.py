from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # パスワードハッシュの自動化等
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
import re


def validate_email_format(value):
    if value:  # 空の場合はスキップ（任意入力のため）
        # 基本的なメールアドレス形式のチェック
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError('有効なメールアドレスを入力してください。')

        # ドメイン部分の長さチェック
        domain = value.split('@')[1]
        if len(domain) > 255:
            raise ValidationError('メールアドレスのドメイン部分が長すぎます。')

        # ローカル部分の長さチェック
        local = value.split('@')[0]
        if len(local) > 64:
            raise ValidationError('メールアドレスのローカル部分が長すぎます。')


# ユーザー登録フォーム
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
    email = forms.EmailField(
        label="メールアドレス",
        required=False,  # 任意入力
        validators=[validate_email_format],
        error_messages={
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# メールアドレス設定フォーム
class EmailSettingForm(forms.ModelForm):
    email = forms.EmailField(
        label="メールアドレス",
        required=False,
        validators=[validate_email_format],
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )

    class Meta:
        model = User
        fields = ['email']