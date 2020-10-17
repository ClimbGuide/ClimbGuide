// Event Handlers
function showDayTripForm () {
    let dayTripForm = document.querySelector("#daytrip-form")
    let editDayTripButton = document.querySelector("#edit-daytrip-button")
    dayTripForm.classList.remove("hidden")
    editDayTripButton.classList.add("hidden")
}

function showUserForm () {
    let userForm = document.querySelector("#user-form")
    let editUserButton = document.querySelector("#edit-user-button")
    userForm.classList.remove("hidden")
    editUserButton.classList.add("hidden")
}

function showAddDayTripForm () {
    let addDayTripForm = document.querySelector("#add-daytrip-form")
    let addDayTripButton = document.querySelector("#add-daytrip-button")
    addDayTripForm.classList.remove("hidden")
    addDayTripButton.classList.add("hidden")
}

function showAddRoutePhotoForm () {
    let addRoutePhotoForm = document.querySelector("#add-routephoto-form")
    let addRoutePhotoButton = document.querySelector("#add-routephoto-button")
    addRoutePhotoForm.classList.remove("hidden")
    addRoutePhotoButton.classList.add("hidden")
}

// Event Listeners
let editDayTrip = document.querySelector("#edit-daytrip-button")
if (editDayTrip) {
    editDayTrip.addEventListener("click", showDayTripForm)
}

let editUser = document.querySelector("#edit-user-button")
if (editUser) {
    editUser.addEventListener("click", showUserForm)
}

let addDayTrip = document.querySelector("#add-daytrip-button")
if (addDayTrip) {
    addDayTrip.addEventListener("click", showAddDayTripForm)
}

let addRoutePhoto = document.querySelector("#add-routephoto-button")
if (addRoutePhoto) {
    addRoutePhoto.addEventListener("click", showAddRoutePhotoForm)
}