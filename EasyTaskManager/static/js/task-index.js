function addTask(title) {
    fetch('/', {  // タスク追加用のURL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({ title: title }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            renderTask(data.task);  // 新しいタスクを表示
        } else {
            console.error('タスクの追加に失敗しました:', data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}