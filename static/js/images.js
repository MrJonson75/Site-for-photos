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