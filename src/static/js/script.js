function getSongsFromDom() {
    const list = document.getElementById("song_list");
    if (!list) return null;
    const items = Array.from(list.querySelectorAll("li"))
        .map(li => li.textContent.trim())
        .filter(Boolean);
    return items.length ? items : null;
}

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


function loadSongs() {
    const fromDom = getSongsFromDom();
    if (fromDom) {
        localStorage.setItem("songs", JSON.stringify(fromDom));
        return fromDom;
    }
    return getSongsFromStorage() ?? [];
}

loadSongs();


const button = document.getElementById("us_button");
const user_input = document.getElementById("user_value");
const result = document.getElementById("result");


if (button && user_input && result) {
    button.addEventListener("click", () => {
        const query = user_input.value.trim();
        if (!query) {
            result.textContent = "Please enter a song name";
            return;
        }
        const songs = loadSongs();
        if (!songs.length) {
            result.textContent = "Song list is empty";
            return;
        }
        const song_index = songs.findIndex(song => song.toLowerCase().includes(query.toLowerCase()));
        if (song_index === -1) {
            result.textContent = "Song not found in the collection";
        } else {
            result.textContent = `The song ${songs[song_index]} was found in the collection at No.${song_index + 1}`;
        }
    });
}