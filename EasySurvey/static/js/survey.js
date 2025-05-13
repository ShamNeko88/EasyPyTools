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
    // アンケート作成ページの質問追加オブジェクト
    const addQuestionBtn = document.getElementById("add-question-btn");
    const questionsContainer = document.getElementById("questions-container");

    // アンケート編集ページの質問追加オブジェクト
    const addNewQuestionBtn = document.getElementById("add-new-question-btn");
    const newQuestionsContainer = document.getElementById("new-questions-container");

    if (addQuestionBtn && questionsContainer) {
        // アンケート作成ページの処理
        addQuestionBtn.addEventListener("click", function () {
            // 新しい質問のHTMLを作成
            const newQuestionDiv = document.createElement("div");
            newQuestionDiv.classList.add("form-group");

            // 新しい質問の番号を取得
            const questionCount = questionsContainer.getElementsByClassName('form-group').length + 1;

            // 新しい質問のHTMLを設定
            newQuestionDiv.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" 
                               id="show_choices${questionCount}" 
                               name="show_choices[]" 
                               value="${questionCount}" checked>
                        <label class="form-check-label text-nowrap" 
                               for="show_choices${questionCount}"></label>
                    </div>
                    <input type="text" class="form-control mr-2" 
                           name="questions[]" 
                           placeholder="質問を入力" required/>
                    <button type="button" class="btn btn-danger remove-question-btn text-nowrap">削除</button>
                </div>
            `;

            // 質問を追加するコンテナに新しい質問を追加
            questionsContainer.appendChild(newQuestionDiv);

            // 削除ボタンのクリックイベントを追加
            const removeBtn = newQuestionDiv.querySelector(".remove-question-btn");
            removeBtn.addEventListener("click", function () {
                questionsContainer.removeChild(newQuestionDiv);
            });
        });
    } else if (addNewQuestionBtn && newQuestionsContainer) {
        // アンケート編集ページの処理
        addNewQuestionBtn.addEventListener("click", function () {
            // 新しい質問のHTMLを作成
            const newQuestionDiv = document.createElement("div");
            newQuestionDiv.classList.add("form-group", "d-flex", "align-items-center", "mb-2");

            // 新しい質問のHTMLを設定
            newQuestionDiv.innerHTML = `
                <input type="text" class="form-control mr-2" name="new_questions[]" placeholder="質問を入力" style="flex: 1;">
                <button type="button" class="btn btn-danger remove-question-btn">削除</button>
            `;

            // 質問を追加するコンテナに新しい質問を追加
            newQuestionsContainer.appendChild(newQuestionDiv);

            // 削除ボタンのクリックイベントを追加
            const removeBtn = newQuestionDiv.querySelector(".remove-question-btn");
            removeBtn.addEventListener("click", function () {
                newQuestionsContainer.removeChild(newQuestionDiv);
            });
        });
    }
});

/**
 * URLコピー機能
 */
document.addEventListener('DOMContentLoaded', function () {
    const copyButton = document.getElementById('copy-url-btn');
    if (copyButton) {
        copyButton.addEventListener('click', function () {
            copyToClipboard('survey-url'); // 汎用関数を利用
        });
    }
});

/**
 * 指定されたIDの要素の値をクリップボードにコピーする関数
 */
function copyToClipboard(elementId) {
    const copyText = document.getElementById(elementId);
    if (copyText) {
        navigator.clipboard.writeText(copyText.value)
            .then(() => {
                alert('URLがコピーされました: ' + copyText.value);
            })
            .catch(err => {
                console.error('クリップボードへのコピーに失敗しました:', err);
                alert('URLのコピーに失敗しました。');
            });
    } else {
        alert('コピーする要素が見つかりません。');
    }
}
