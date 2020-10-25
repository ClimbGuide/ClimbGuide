// Event Handlers
function showFormOne () {
    let formOne = document.querySelector("#form-one")
    if (formOne.classList.contains("hidden")) {
        formOne.classList.remove("hidden")
    } else {
        formOne.classList.add("hidden")
    }
}

function showFormTwo () {
    let formTwo = document.querySelector("#form-two")
    if (formTwo.classList.contains("hidden")) {
        formTwo.classList.remove("hidden")
    } else {
        formTwo.classList.add("hidden")
    }
}

function showFormThree () {
    let formThree = document.querySelector("#form-three")
    if (formThree.classList.contains("hidden")) {
        formThree.classList.remove("hidden")
    } else {
        formThree.classList.add("hidden")
    }
}

// Event Listeners
let buttonOne = document.querySelector("#button-one")
if (buttonOne) {
    buttonOne.addEventListener("click", showFormOne)
}

let buttonTwo = document.querySelector("#button-two")
if (buttonTwo) {
    buttonTwo.addEventListener("click", showFormTwo)
}

let buttonThree = document.querySelector("#button-three")
if (buttonThree) {
    buttonThree.addEventListener("click", showFormThree)
}