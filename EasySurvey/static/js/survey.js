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
 * アンケートの送信ボタンのクリックイベントを処理する
 * 
 * 流れ↓
 * ページが読み込まれると、DOMContentLoadedイベントが発火。
 * 「送信ボタン」がクリックされると、フォームデータを収集。
 * fetchを使って非同期でサーバーにデータを送信。
 * サーバーからのレスポンスを処理し、成功またはエラーのメッセージを表示。
 * 必要に応じてページをリロード。
 */

// document.addEventListener("DOMContentLoaded", function () {
//     const submitSurveyBtn = document.getElementById("submit-survey-btn");
//     const surveyForm = document.getElementById("survey-form");

//     submitSurveyBtn.addEventListener("click", function () {
//         // フォームオブジェクト作成（データの取得）
//         const formData = new FormData(surveyForm);

//         // 非同期リクエストを送信
//         fetch("", {
//             method: "POST",
//             body: formData,
//             headers: {
//                 "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
//             },
//         })
//             .then((response) => {
//                 if (!response.ok) {
//                     // レスポンスがエラーの場合
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json(); // JSON をパース
//             })
//             .then((data) => {
//                 if (data.error) {
//                     alert(data.error);
//                 } else {
//                     // サーバーからのリダイレクト URL を使用してページ遷移
//                     window.location.href = data.redirect_url;
//                 }
//             })
//             .catch((error) => {
//                 console.error("Error:", error);
//                 alert("サーバーエラーが発生しました。詳細はコンソールを確認してください。");
//             });
// });


/**
 * URLコピー機能
 */
document.addEventListener('DOMContentLoaded', function () {
    const copyButton = document.getElementById('copy-url-btn');
    const urlField = document.getElementById('survey-url');

    copyButton.addEventListener('click', async function () {
        try {
            // Clipboard API を使用してクリップボードにコピー
            await navigator.clipboard.writeText(urlField.value);
            alert('URLがコピーされました: ' + urlField.value);
        } catch (err) {
            console.error('クリップボードへのコピーに失敗しました:', err);
            alert('URLのコピーに失敗しました。');
        }
    });
});
