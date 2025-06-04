""" テンプレートタグ
テンプレートで使用するユーティリティ関数を定義
テンプレート内での複雑なデータアクセスを可能にする
"""

from django import template

# テンプレートタグの登録
register = template.Library()


# テンプレートタグの定義
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# テンプレートタグの定義
@register.filter
def get_attr(obj, attr):
    if obj is None:
        return ""
    return getattr(obj, attr, "")
