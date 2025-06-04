/**
 * アンケートフォームの機能を管理するクラス
 */
class SurveyForm {
    constructor() {
        this.initializeEventListeners();
    }

    /**
     * イベントリスナーを初期化
     */
    initializeEventListeners() {
        document.addEventListener("DOMContentLoaded", () => {
            this.setupFormEnterKeyPrevention();
            this.setupQuestionManagement();
            this.setupUrlCopy();
            this.setupAnswerForm();
        });
    }

    /**
     * フォームのエンターキー入力を防止
     */
    setupFormEnterKeyPrevention() {
        const form = document.getElementById("survey-form");
        if (form) {
            form.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    event.preventDefault();
                }
            });
        }
    }

    /**
     * 質問管理機能のセットアップ
     */
    setupQuestionManagement() {
        const addQuestionBtn = document.getElementById("add-question-btn");
        const questionsContainer = document.getElementById("questions-container");
        const addNewQuestionBtn = document.getElementById("add-new-question-btn");
        const newQuestionsContainer = document.getElementById("new-questions-container");

        if (addQuestionBtn && questionsContainer) {
            this.setupQuestionAddition(addQuestionBtn, questionsContainer, false);
        } else if (addNewQuestionBtn && newQuestionsContainer) {
            this.setupQuestionAddition(addNewQuestionBtn, newQuestionsContainer, true);
        }
    }

    /**
     * 質問追加機能のセットアップ
     */
    setupQuestionAddition(button, container, isNewQuestion) {
        button.addEventListener("click", () => {
            const newQuestionDiv = this.createQuestionElement(container, isNewQuestion);
            container.appendChild(newQuestionDiv);
            this.setupRemoveButton(newQuestionDiv, container);
        });
    }

    /**
     * 質問要素の作成
     */
    createQuestionElement(container, isNewQuestion) {
        const newQuestionDiv = document.createElement("div");
        newQuestionDiv.classList.add("form-group", "d-flex", "align-items-center", "mb-2");

        if (isNewQuestion) {
            newQuestionDiv.innerHTML = this.getNewQuestionTemplate();
        } else {
            const questionCount = container.getElementsByClassName('form-group').length + 1;
            newQuestionDiv.innerHTML = this.getQuestionTemplate(questionCount);
        }

        return newQuestionDiv;
    }

    /**
     * 新規質問のテンプレート
     */
    getNewQuestionTemplate() {
        return `
            <div class="form-check d-flex align-items-center mr-2">
                <input type="checkbox" class="form-check-input" name="new_show_choices_flag[]" value="1" checked>
                <label class="form-check-label ml-1"></label>
            </div>
            <input type="text" class="form-control mr-2" name="new_questions[]" placeholder="質問を入力" style="flex: 1;">
            <button type="button" class="btn btn-danger remove-question-btn">削除</button>
        `;
    }

    /**
     * 通常質問のテンプレート
     */
    getQuestionTemplate(questionCount) {
        return `
            <div class="d-flex align-items-center w-100">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" 
                           id="show_choices${questionCount}" 
                           name="show_choices[]" 
                           value="${questionCount}" checked>
                    <label class="form-check-label text-nowrap" 
                           for="show_choices${questionCount}"></label>
                </div>
                <div class="flex-grow-1">
                    <input type="text" class="form-control" 
                           name="questions[]" 
                           placeholder="質問を入力" 
                           required/>
                </div>
                <button type="button" class="btn btn-danger remove-question-btn text-nowrap ml-2">削除</button>
            </div>
        `;
    }

    /**
     * 削除ボタンのセットアップ
     */
    setupRemoveButton(questionDiv, container) {
        const removeBtn = questionDiv.querySelector(".remove-question-btn");
        removeBtn.addEventListener("click", () => {
            container.removeChild(questionDiv);
        });
    }

    /**
     * URLコピー機能のセットアップ
     */
    setupUrlCopy() {
        const copyButton = document.getElementById('copy-url-btn');
        if (copyButton) {
            copyButton.addEventListener('click', () => this.copyToClipboard('survey-url'));
        }
    }

    /**
     * クリップボードへのコピー
     */
    async copyToClipboard(elementId) {
        const copyText = document.getElementById(elementId);
        if (!copyText) {
            this.showAlert('コピーする要素が見つかりません。', 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(copyText.value);
            this.showAlert(`URLがコピーされました: ${copyText.value}`, 'success');
        } catch (err) {
            console.error('クリップボードへのコピーに失敗しました:', err);
            this.showAlert('URLのコピーに失敗しました。', 'error');
        }
    }

    /**
     * アラート表示
     */
    showAlert(message, type = 'info') {
        alert(message);
    }

    /**
     * アンケート回答フォームのセットアップ
     */
    setupAnswerForm() {
        const answerForm = document.getElementById('answer-form');
        if (answerForm) {
            answerForm.addEventListener('submit', (e) => this.handleAnswerSubmit(e));
        }
    }

    /**
     * アンケート回答の送信処理
     */
    async handleAnswerSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showAnswerError(data.error);
            } else if (data.success && data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } catch (error) {
            console.error('Error:', error);
            this.showAnswerError('エラーが発生しました。もう一度お試しください。');
        }
    }

    /**
     * アンケート回答のエラー表示
     */
    showAnswerError(message) {
        const errorDiv = document.getElementById('error-message');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.className = 'alert alert-danger mb-4';
            errorDiv.style.display = 'block';
        }
    }
}

// アプリケーションの初期化
new SurveyForm();
