/**
 * フォーム全体でエンターキーを無効化
 */
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("survey-form");
    if (form) {
        form.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault(); // エンターキーのデフォルト動作を無効化
            }
        });
    }
});

/**
 * 質問追加ボタンのクリックイベントを処理する
 * 質問を追加するための関数
 */
document.addEventListener("DOMContentLoaded", function () {
    // 質問追加ボタンの取得
    const addQuestionBtn = document.getElementById("add-question-btn");
    // 質問を追加するためのコンテナの取得
    const questionsContainer = document.getElementById("questions-container");

    // 質問追加ボタンがクリックされたときの処理
    let questionCount = 1; // 現在の質問数をカウントする変数
    addQuestionBtn.addEventListener("click", function () {
        questionCount++;
        // 新しい質問のHTMLを作成
        const newQuestionDiv = document.createElement("div");
        // あたらしい質問のdivにクラスを追加（bootstrap）
        newQuestionDiv.classList.add(
            "form-group",
            "d-flex",
            "align-items-center",
            "mb-2"
        );
        // 新しい質問のHTMLを設定
        newQuestionDiv.innerHTML = `
            <input type="text" class="form-control mr-2" id="question${questionCount}" name="questions[]" placeholder="質問を入力" style="flex: 1;">
            <button type="button" class="btn btn-danger remove-question-btn">削除</button>
        `;
        // 質問を追加するコンテナに新しい質問を追加
        questionsContainer.appendChild(newQuestionDiv);

        // 削除ボタンのクリックイベントを追加
        const removeBtn = newQuestionDiv.querySelector(".remove-question-btn");
        removeBtn.addEventListener("click", function () {
            questionsContainer.removeChild(newQuestionDiv);
        });
    });
});

/**
 * URLコピー機能
 */
document.addEventListener('DOMContentLoaded', function () {
    const copyButton = document.getElementById('copy-url-btn');
    const urlField = document.getElementById('survey-url');

    if (copyButton && urlField) {
        copyButton.addEventListener('click', async function () {
            try {
                await navigator.clipboard.writeText(urlField.value);
                alert('URLがコピーされました: ' + urlField.value);
            } catch (err) {
                console.error('クリップボードへのコピーに失敗しました:', err);
                alert('URLのコピーに失敗しました。');
            }
        });
    }
});
