
console.log("HI");
const roomIdInput = document.getElementById("input-room");

const beginButton = document.getElementById("begin-button")
const roomButton = document.getElementById("room-button")

if (roomButton) {
    let roomIdVisible = false
    roomButton.addEventListener("click", async function () {


        console.log("CLICKED")
        if (roomIdInput.style.display === "none") {
            roomIdInput.style.display = "block"
            roomIdVisible = true

            roomButton.textContent = "NO ROOM ID"

        }
        else {
            roomIdInput.style.display = "none"

            roomButton.textContent = "I HAVE A ROOM ID"

        }
    });
}


if (beginButton) {
    document.getElementById("begin-button").addEventListener("click", async function () {
        const roomIdInputValue = roomIdInput.value;

        console.log("input value:", roomIdInputValue);
        const userNameInput = document.getElementById("input-username")
        const userNameInputValue = userNameInput.value


        if (roomIdInput.style.display === "block") {
            if (!userNameInputValue.trim() || !roomIdInputValue.trim()) {
                console.log("Empty field");
                return;
            }
            const response = await fetch(`/does-room-exist?room_id=${roomIdInputValue}`);
            const data = await response.json();
            console.log(data)
            if (data.exists == true) {
                console.log("YES, IT EXISTS", data.room_id);
                window.location.href =
                    `/game/${data.room_id}?username=${encodeURIComponent(userNameInputValue)}`;

            }
            else {
                console.log("DOESNT EXIST. INCORRECT ROOM ID.")
                return;

            }
        } else {
            if (!userNameInputValue.trim()) {
                console.log("Empty field");
                return


            }
            else {
                const response = await fetch(`/create-game`);
                const data = await response.json();
                window.location.href =
                    `/game/${data.room_id}?username=${encodeURIComponent(userNameInputValue)}`;

            }
        }



    });
};

const roomId = window.location.pathname.split("/").pop();

if (roomId && window.location.pathname.startsWith("/game/")) {
    const socket = new WebSocket(
        `ws://${window.location.host}/ws/${roomId}`
    );

    socket.onopen = function () {
        console.log("Connected to room!");
    };
    socket.onmessage = async function (event) {

        const data = JSON.parse(event.data);

        if (data.type !== "room_state") {
            return;
        }

        console.log("ROOM STATE:", data);

        const container = document.querySelector(".img-container");


        container.innerHTML = "";

        let imagesLoaded = 0;
        const totalImages = data.players.length;

        function imageFinishedLoading() {

            imagesLoaded++;

            console.log(
                `Images loaded: ${imagesLoaded}/${totalImages}`
            );

            if (imagesLoaded === totalImages) {
                document.getElementById("loading-screen").style.display = "none";
            }
        }

        for (const player of data.players) {

            const imgPlayerDiv = document.createElement("div");
            imgPlayerDiv.className = "character-img-container";

            const imgPlayer = document.createElement("img");
            imgPlayer.className = "character-img";
            imgPlayer.loading = "eager";

            imgPlayer.onload = imageFinishedLoading;
            imgPlayer.onerror = imageFinishedLoading;

            if (player.player_id === data.your_player_id) {

                imgPlayer.src =
                    `/blur-image/${player.image.split("/").pop()}`;

                imgPlayer.id = "players-img";

                const youText = document.createElement("p");
                youText.textContent = "YOU";
                youText.id = "you-text";
                youText.style.marginBottom = "50px";

                imgPlayerDiv.appendChild(imgPlayer);
                imgPlayerDiv.appendChild(youText);

            }

            else {

                imgPlayer.src = player.image;

                const playerText = document.createElement("p");
                playerText.textContent = player.username;
                playerText.className = "player-label";

                imgPlayerDiv.appendChild(imgPlayer);
                imgPlayerDiv.appendChild(playerText);
            }

            container.appendChild(imgPlayerDiv);
        }
    };
}