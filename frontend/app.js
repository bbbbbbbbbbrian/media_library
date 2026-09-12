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
        chapter.textContent =
            "Current: Chapter " + comic.current_chapter +
            " | Latest: Chapter " + comic.latest_chapter;

        const chapterInput = document.createElement("input");
        chapterInput.type = "text";
        chapterInput.placeholder = "Chapter";
        chapterInput.value = comic.current_chapter;
        chapterInput.className = "chapter-input";

        const updateButton = document.createElement("button");
        updateButton.textContent = "Update Chapter";
        updateButton.className = "update-button";

        updateButton.addEventListener("click", async function() {
            const newChapter = chapterInput.value.trim();

            if (!newChapter) {
                return;
            }

            try {
                const response = await fetch(
                    "http://127.0.0.1:8000/reading/" +
                    comic.id +
                    "?current_chapter=" +
                    encodeURIComponent(newChapter),
                    {
                        method: "PUT"
                    }
                );

                const data = await response.json();

                console.log("PUT response:", response.status, data);

                if (!response.ok) {
                    alert("Update failed: " + (data.error || "Unknown error"));
                    return;
                }

                loadReadingList();

            } catch (error) {
                console.error("Update error:", error);
                alert("Could not connect to the backend.");
            }
        });
        const readButton = document.createElement("a");
        readButton.href = comic.current_url;
        readButton.textContent = "Read";
        readButton.target = "_blank";
        readButton.className = "read-button";

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", async function() {
            await fetch(
                "http://127.0.0.1:8000/reading/" + comic.id,
                {
                    method: "DELETE"
                }
            );

            item.remove();
        });

        item.appendChild(title);
        item.appendChild(chapter);
        item.appendChild(chapterInput);
        item.appendChild(updateButton);
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

    await fetch(
        "http://127.0.0.1:8000/reading?url=" +
        encodeURIComponent(url),
        {
            method: "POST"
        }
    );

    document.getElementById("url-input").value = "";

    loadReadingList();
});