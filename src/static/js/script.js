// Отримуємо список пісень з HTML (DOM)
// Відбувається пошук <ul id="song_list"> з <li> елементами
// Функція повертає масив рядків (назви пісень)
// Функція повертає null, якщо списку немає або він порожній
function getSongsFromDom() {
    const list = document.getElementById("song_list");
    if (!list) return null;

    // Збираємо всі <li> всередині списку 'list'
    // Перетворюємо отримані дані в масив з композиціями
    // Масив зі спискок пісень буде зберігатися у сховищі браузера (localStorage)
    // localStorage дозволяє “пам'ятати” дані між переходами на інші сторінки
    const items = Array.from(list.querySelectorAll("li"))
        .map(li => li.textContent.trim())
        .filter(Boolean);
    return items.length ? items : null;
}

// Отримуємо список пісень зі сховища браузера (localStorage)
// Очікуємо, що в localStorage під ключем "songs" лежить JSON-масив рядків
// Отримуємо масив пісень або null, якщо в сховищі нічого немає/дані некоректні
function getSongsFromStorage() {
    const raw = localStorage.getItem("songs");
    if (!raw) return null;
    try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length) return parsed;
    } catch (e) {
    }
    return null;
}

// Функція, яка “вирішує”, звідки брати список пісень
// - Якщо на index.html є DOM-список, читаємо з HTML та зберігаємо в localStorage
// - Якщо DOM-списку немає (наприклад, search.html), пробуємо взяти з localStorage
// - Якщо нічого не знайшли - повертаємо порожній масив.
function loadSongs() {
    const fromDom = getSongsFromDom();
    if (fromDom) {
        // Запам'ятовуємо список пісень, щоб використовувати його на інших сторінках
        localStorage.setItem("songs", JSON.stringify(fromDom));
        return fromDom;
    }
    return getSongsFromStorage() ?? [];
}

// Одразу запускаємо завантаження списку
// На index.html функція збере пісні з DOM та збереже їх у localStorage
// На search.html DOM-список відсутній, тому функція спробує прочитати localStorage
loadSongs();

// Знаходимо html-об'єкти: кнопка, поле вводу та елемент для результату
const button = document.getElementById("us_button");
const user_input = document.getElementById("user_value");
const result = document.getElementById("result");

// Додаємо функції-обробник події 'click'
if (button && user_input && result) {
    button.addEventListener("click", () => {
        // Отримуємо назву пісні, яку ввів користувач
        // Прибираємо зайві пробіли по краях
        const query = user_input.value.trim();
        if (!query) {
            result.textContent = "Please enter a song name";
            return;
        }
        // В момент пошуку отримуємо актуальний список пісень з localStorage
        const songs = loadSongs();
        if (!songs.length) {
            result.textContent = "Song list is empty";
            return;
        }
        // Знаходимо індекс пісні в масиві пісень
        const song_index = songs.findIndex(song => song.toLowerCase().includes(query.toLowerCase()));
        // Перевірка дозволяє дізнатися чи присутня пісня в чарті
        if (song_index === -1) {
            result.textContent = "Song not found in the collection";
        } else {
            // Повертаємо результат
            result.textContent = `The song ${songs[song_index]} was found in the collection at No.${song_index + 1}`;
        }
    });
}
