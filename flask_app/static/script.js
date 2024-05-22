

async function getSpaceData(spaceDate = randomDate()) {
    var response = await fetch("https://api.nasa.gov/planetary/apod?api_key=<<api_key>>" + spaceDate);
    var spaceData = await response.json();
    console.log(spaceData);
    displayPicture(spaceData);
}

async function getPOD() {
    var response = await fetch("https://api.nasa.gov/planetary/apod?api_key=<<api_key>>");
    var spaceData = await response.json();
    console.log(spaceData);
    displayPicture(spaceData);
}

function displayPicture(data) {
    var res = document.querySelector("#space");
    res.innerHTML = `${data.title} <span id="space_date">${data.date}</span> <img src="${data.url}" alt="space"> ${data.explanation}`;
}

async function addFavorite() {
    var space_date = document.querySelector("#space_date");
    var response = await fetch("http://127.0.0.1:5000/explore/favorite/" + space_date.innerText, {method: 'post'});
}

function randomDate() {
    let year = Math.floor(Math.random() * 10) + 2015;
    let month = Math.floor(Math.random() * 12) + 1;
    let day = Math.floor(Math.random() * 28) + 1;
    let random_date = (year + '-' + month + '-' + day);
    return random_date;
}
