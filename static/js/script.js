// Event Handlers
function showForm () {
    let formOne = document.querySelector("#form-one")
    let buttonOne = document.querySelector("#button-one")
    formOne.classList.remove("hidden")
    buttonOne.classList.add("hidden")
}

function showFormTwo () {
    let formTwo = document.querySelector("#form-two")
    let buttonTwo = document.querySelector("#button-two")
    formTwo.classList.remove("hidden")
    buttonTwo.classList.add("hidden")
}

function showFormThree () {
    let formThree = document.querySelector("#form-three")
    let buttonThree = document.querySelector("#button-three")
    formThree.classList.remove("hidden")
    buttonThree.classList.add("hidden")
}

// Event Listeners
let buttonOne = document.querySelector("#button-one")
if (buttonOne) {
    buttonOne.addEventListener("click", showForm)
}

let buttonTwo = document.querySelector("#button-two")
if (buttonTwo) {
    buttonTwo.addEventListener("click", showFormTwo)
}

let buttonThree = document.querySelector("#button-three")
if (buttonThree) {
    buttonThree.addEventListener("click", showFormThree)
}