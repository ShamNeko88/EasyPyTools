document.addEventListener('DOMContentLoaded', function() {
    const csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : ''; // CSRFトークンを取得

    if (!csrfToken) {
        console.error('CSRFトークンが見つかりません。フォームにトークンが含まれていることを確認してください。');
        return; // CSRFトークンがない場合は処理を中止
    }

    function updateCheckboxState(form) {
        const isIdeaChecked = form.querySelector('input[name="is_idea"]').checked;
        const completedCheckbox = form.querySelector('input[name="is_completed"]');
        const priorityCheckbox = form.querySelector('input[name="is_priority"]');

        // 思考中がチェックされている場合、完了と優先を無効化
        completedCheckbox.disabled = isIdeaChecked;
        priorityCheckbox.disabled = isIdeaChecked;
    }

    document.querySelectorAll('.task-update-form').forEach(form => {
        // ページ読み込み時に状態を更新
        updateCheckboxState(form);

        form.querySelectorAll('.update-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const taskId = form.getAttribute('data-task-id');
                const formData = new FormData(form);

                // 状態を更新
                updateCheckboxState(form);

                fetch(`/tasks/update/${taskId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken // CSRFトークンをヘッダーに追加
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('タスクが更新されました。');
                        // チェックボックスの状態を再評価
                        updateCheckboxState(form);
                    } else {
                        console.error('更新に失敗しました。');
                    }
                })
                .catch(error => {
                    console.error('エラーが発生しました:', error);
                });
            });
        });
    });
});