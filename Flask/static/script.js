const userForm = document.getElementById("userForm");
const usersList = document.getElementById("usersList");


// ---------------------------------------
// GET USERS
// ---------------------------------------

async function getUsers() {

    const response = await fetch("/api/users");

    const users = await response.json();

    displayUsers(users);
}


// ---------------------------------------
// DISPLAY USERS
// ---------------------------------------

function displayUsers(users) {

    usersList.innerHTML = "";

    users.forEach(user => {

        const userCard = document.createElement("div");

        userCard.className = "user-card";

        userCard.innerHTML = `
            <div class="user-info">
                <h3>${user.name}</h3>
                <p>${user.email}</p>
            </div>

            <button
                class="delete-btn"
                onclick="deleteUser(${user.id})">
                Delete
            </button>
        `;

        usersList.appendChild(userCard);
    });
}


// ---------------------------------------
// POST USER
// ---------------------------------------

userForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;


    const response = await fetch("/api/users", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name,
            email: email
        })

    });


    const data = await response.json();

    console.log(data);


    userForm.reset();

    getUsers();

});


// ---------------------------------------
// DELETE USER
// ---------------------------------------

async function deleteUser(id) {

    const response = await fetch(`/api/users/${id}`, {

        method: "DELETE"

    });


    const data = await response.json();

    console.log(data);


    getUsers();
}


// ---------------------------------------
// LOAD USERS WHEN PAGE OPENS
// ---------------------------------------

getUsers();