
console.log("HI");
const playerNumberInput = document.getElementById("input-players");

const inputValue =5;
const beginButton = document.getElementById("begin-button")
if (beginButton){
document.getElementById("begin-button").addEventListener("click", async function() {
    const response = await fetch("/create-game");
    const data = await response.json();

    window.location.href = "/game/" + data.room_id;
});
};
const button1 = document.getElementById("button1");


if(button1){

button1.addEventListener("click", async function() {
    console.log("Button was clicked!");
    console.log(inputValue)
    socket.send("Hello from this player!");
    socket.send("button1_clicked");

    
    for (let i =0;i <inputValue;i++ ){
        console.log(i)
        const response = await fetch("/random-character");
        const data = await response.json();


        const img = document.createElement('img');

        img.src = data.image;
        img.className = 'character-img'
        img.alt = 'A descriptive text for accessibility';
        const img_container = document.querySelector(".img-container")
        img_container.append(img);
    };


});

};

const roomId = window.location.pathname.split("/").pop();

async function joinRoom() {
    const response = await fetch("/join/" + roomId);
    const data = await response.json();

    console.log("Room ID:", roomId);
    console.log(data);
}



// joinRoom();

const socket = new WebSocket(
    `ws://${window.location.host}/ws/${roomId}`
);

socket.onopen = function() {
    console.log("Connected to room!");
};

socket.onmessage = function(event) {
    console.log("My player ID:", event.data);
    if (event.data === "button1_clicked") {
        button1.style.backgroundColor = "red";
    }
};
