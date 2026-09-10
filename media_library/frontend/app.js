async function loadReadingList() {
    const response = await fetch("http://127.0.0.1:8000/reading");
    const comics = await response.json();

    const readingList = document.getElementById("reading-list");
    readingList.innerHTML = "";

    for (const comic of comics) {
        const item = document.createElement("div");
        item.className = "reading-item";

        const title = document.createElement("h3");
        title.textContent = comic.title;

        const chapter = document.createElement("p");
        chapter.textContent = comic.chapter;

        const readButton = document.createElement("a");
        readButton.href = comic.url;
        readButton.textContent = "Read";
        readButton.target = "_blank";
        readButton.className = "read-button";

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", async function() {
            await fetch("http://127.0.0.1:8000/reading/" + comic.id, {
                method: "DELETE"
            });

            item.remove();
        });

        item.appendChild(title);
        item.appendChild(chapter);
        item.appendChild(readButton);
        item.appendChild(deleteButton);

        readingList.appendChild(item);
    }
}

loadReadingList();

const addForm = document.getElementById("add-form");

addForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const url = document.getElementById("url-input").value;

    await fetch("http://127.0.0.1:8000/reading?url=" + encodeURIComponent(url), {
        method: "POST"
    });

    document.getElementById("url-input").value = "";

    loadReadingList();
});