// static/js/blog.js

function updatePreview(textareaId, previewId) {
    const textarea = document.getElementById(textareaId);
    const preview = document.getElementById(previewId);

    // textareaがnullでないことを確認
    if (textarea) {
        const markdownText = textarea.value;

        // marked.jsを使用してマークダウンをHTMLに変換
        const html = marked(formattedText);
        preview.innerHTML = html; // プレビューにHTMLを設定
    } else {
        console.error(`Textarea with ID ${textareaId} not found.`);
    }
}

// blog-detail.html用のマークダウン表示処理
document.addEventListener('DOMContentLoaded', function () {
    const contentPreview = document.getElementById('content-preview');
    const markdownText = contentPreview.getAttribute('data-content'); // データ属性からマークダウンテキストを取得
    // marked.jsを使用してマークダウンをHTMLに変換
    const html = marked(markdownText); // マークダウンをHTMLに変換
    contentPreview.innerHTML = html; // プレビューにHTMLを設定
});