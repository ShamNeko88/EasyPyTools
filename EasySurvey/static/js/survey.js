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
 * 回答者を追加ボタンのクリックイベントを処理する
 * 回答者を回答者一覧に追加する為の関数
 */
document.addEventListener("DOMContentLoaded", function () {
    // 回答者追加ボタンの取得
    const addResponderBtn = document.getElementById("add-responder-btn");
    // 回答者を追加するためのコンテナの取得
    const respondersContainer = document.getElementById("responders-container");

    // 回答者追加ボタンがクリックされたときの処理
    let responderCount = 1; // 現在の回答者数をカウントする変数
    addResponderBtn.addEventListener("click", function () {
        responderCount++;
        // 新しい回答者のHTMLを作成
        const newResponderDiv = document.createElement("div");
        // あたらしい回答者のdivにクラスを追加（bootstrap）
        newResponderDiv.classList.add(
            "form-group",
            "d-flex",
            "align-items-center",
            "mb-2"
        );
        // 新しい回答者のHTMLを設定
        newResponderDiv.innerHTML = `
            <input type="text" class="form-control mr-2" id="responder${responderCount}" name="responders[]" placeholder="回答者名を入力" style="flex: 1;">
            <button type="button" class="btn btn-danger remove-responder-btn">削除</button>
        `;
        // 回答者を追加するコンテナに新しい回答者を追加
        respondersContainer.appendChild(newResponderDiv);

        // 削除ボタンのクリックイベントを追加
        const removeBtn = newResponderDiv.querySelector(
            ".remove-responder-btn"
        );
        removeBtn.addEventListener("click", function () {
            respondersContainer.removeChild(newResponderDiv);
        });
    });
});
