// Список разрешенных расширений файлов
const ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif'];
// Максимальный размер файла: 5 МБ
const MAX_FILE_SIZE = 5 * 1024 * 1024;

// Функция для проверки файла
function validateFile(file) {
    // Проверка расширения файла
    const fileExtension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
        return 'Разрешены только файлы формата .jpg, .png или .gif';
    }
    // Проверка размера файла
    if (file.size > MAX_FILE_SIZE) {
        return 'Размер файла не должен превышать 5 МБ';
    }
    return null; // Файл прошел валидацию
}

// Функция обработки drag-and-drop
function handleDrop(event) {
    const fileInput = document.getElementById('image');
    const clientErrorMessage = document.getElementById('clientErrorMessage');
    const files = event.dataTransfer.files;

    // Скрыть сообщение об ошибке
    clientErrorMessage.style.display = 'none';

    // Проверка, что файл является изображением
    if (files.length > 0) {
        const error = validateFile(files[0]);
        if (error) {
            clientErrorMessage.textContent = error;
            clientErrorMessage.style.display = 'block';
        } else if (files[0].type.startsWith('image/')) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        } else {
            clientErrorMessage.textContent = 'Пожалуйста, выберите файл изображения.';
            clientErrorMessage.style.display = 'block';
        }
    }
}

// Обработчик изменения input файла
document.getElementById('image').addEventListener('change', function() {
    const clientErrorMessage = document.getElementById('clientErrorMessage');
    clientErrorMessage.style.display = 'none';

    if (this.files.length > 0) {
        const error = validateFile(this.files[0]);
        if (error) {
            clientErrorMessage.textContent = error;
            clientErrorMessage.style.display = 'block';
            this.value = ''; // Очистить input
        }
    }
});

// Обработчик отправки формы
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    const fileInput = document.getElementById('image');
    const clientErrorMessage = document.getElementById('clientErrorMessage');
    const submitBtn = document.getElementById('submitBtn');

    clientErrorMessage.style.display = 'none';

    if (fileInput.files.length > 0) {
        const error = validateFile(fileInput.files[0]);
        if (error) {
            event.preventDefault();
            clientErrorMessage.textContent = error;
            clientErrorMessage.style.display = 'block';
            return;
        }
    }
    // Отключить кнопку во время отправки
    submitBtn.disabled = true;
});

// Перенаправление на /images/ через 1 секунду после успешной загрузки
if (document.querySelector('.success-message')) {
    setTimeout(() => {
        window.location.href = '/images/';
    }, 1000);
}