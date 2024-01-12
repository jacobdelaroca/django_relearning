
const gridSize = 3;

let mainCont = document.querySelector('#main-container');
let subCont = document.querySelector('#sub-container');

let cards = [];

let linesToCheck = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

let mark = null;
let markSym = null;

let x = document.createElement('div');
let o = document.createElement('div');
x.classList.add('row');
o.classList.add('row');
x.classList.add('x');
o.classList.add('o');
let imgx = document.createElement('img');
let imgo = document.createElement('img');
imgx.setAttribute('src', 'https://www.svgrepo.com/show/12848/x-symbol.svg');
imgo.setAttribute('src', 'https://www.svgrepo.com/show/135058/circle-outline.svg');
imgx.style.width = '70px';
imgx.style.height = '70px';
imgo.style.width = '70px';
imgo.style.height = '70px';

x.appendChild(imgx);
o.appendChild(imgo);


x.addEventListener('click', (e) => {
    mark = x;
    markSym = 'x';
    x.classList.add('bg-light');
    o.classList.remove('bg-light');
})
o.addEventListener('click', (e) => {
    mark = o;
    markSym = 'o';
    o.classList.add('bg-light');
    x.classList.remove('bg-light');
})


subCont.appendChild(x);
subCont.appendChild(o);

for(let i = 0; i < gridSize; i++){
    let row = document.createElement('div');
    row.classList.add('row');
    row.classList.add('border');
    row.style.height = '100px';
    mainCont.appendChild(row);
    for(let j = 0; j < gridSize; j++){
        let card = document.createElement('div');
        card.classList.add('col');
        card.classList.add('border');
        card.classList.add('justify-content-center');
        card.classList.add('align-items-center');
        card.classList.add('d-flex');
        card.style.height = '100px';
        cards.push(card);
        row.appendChild(card);

    }
}

cards.forEach((element, i) => {
    element.addEventListener('mouseover',() =>{
        element.classList.add('bg-light');
    })
    element.addEventListener('mouseout',() =>{
        element.classList.remove('bg-light');
    })
    element.addEventListener('click',() =>{
        let posx = 0;
        let posy = 0;
        [posx, posy] = getCardPos(i);
        console.log(posx, posy, i);
        if(mark == null){
            return;
        }

        let newMark= mark.cloneNode(true);
        newMark.classList.remove('bg-light');
        let hasMark = element.classList.contains('hasMark');
        if(hasMark){
            console.log('has x already');
            element.classList.add(markSym);
        } else {
            element.appendChild(newMark);
        }
        element.classList.add('hasMark');
        let winLine = checkMarkWin();
        console.log(winLine == null);
        if(!(winLine == null)){
            console.log('change bg');
            winLine.forEach(i => {
                cards[i].classList.add('bg-success');
            });
        }
    })
});

function checkMarkWin(mark){
    let winLine = null
    linesToCheck.forEach(line => {
        let win = true;
        line.forEach(i =>{
            if(cards[i].hasChildNodes() == false){
                win = false;
            } else {
                let child = cards[i].firstChild;
                if(!child.classList.contains(markSym)){
                    win = false;
                }
            }
        });
        if(win){
            winLine = line;
        }
    });
    return winLine;
}

function getCardPos(i){
    let posx = i % gridSize;
    let posy = Math.floor(i/gridSize);
    return [posx, posy]
}