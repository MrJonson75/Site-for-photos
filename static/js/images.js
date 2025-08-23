function copyLink(inputId) {
    // Выбор поля ввода по ID
    const input = document.getElementById(inputId);
    input.select();
    // Копирование ссылки в буфер обмена
    navigator.clipboard.writeText(input.value)
        .then(() => alert('Ссылка скопирована!'))
        .catch(() => alert('Ошибка при копировании ссылки.'));
}

function openModal(imageUrl, description) {
    // Получение элементов модального окна
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalDescription = document.getElementById('modalDescription');
    // Установка изображения и описания
    modalImage.src = imageUrl;
    modalImage.alt = description;
    modalDescription.textContent = description;
    // Показ модального окна
    modal.style.display = 'block';
}

function closeModal() {
    // Скрытие модального окна
    document.getElementById('imageModal').style.display = 'none';
}

// Закрытие модального окна при клике вне области контента
document.getElementById('imageModal').addEventListener('click', function(event) {
    if (event.target === this) {
        closeModal();
    }
});

// Функция для удаления изображения
function deleteImage(imageId) {
    if (!confirm('Вы уверены, что хотите удалить это изображение?')) {
        return;
    }

    fetch(`/delete/${imageId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            // После успешного удаления — обновляем страницу
            window.location.reload();
        } else {
            return response.json().then(error => {
                throw new Error(error.detail || 'Ошибка при удалении изображения');
            });
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось удалить изображение: ' + error.message);
    });
}

// Делегирование события — будет работать даже если кнопки подгрузятся позже
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-btn')) {
        const imageId = event.target.getAttribute('data-id');
        deleteImage(imageId);
    }
});
