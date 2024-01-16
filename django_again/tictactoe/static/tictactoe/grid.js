
const gridSize = 3;

let mainCont = document.querySelector('#main-container');
let subCont = document.querySelector('#sub-container');
let playerSym = null;
let cards = [];
let playerImage = null;
let board = null;
let turn = 'x';

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


// subCont.appendChild(x);
// subCont.appendChild(o);

// create the cards grid
for(let i = 0; i < gridSize; i++){
    let row = document.createElement('div');
    row.classList.add('row');
    row.classList.add('border');
    row.style.height = '100px';
    mainCont.appendChild(row);
    let line = [];
    for(let j = 0; j < gridSize; j++){
        let card = document.createElement('div');
        card.classList.add('col');
        card.classList.add('border');
        card.classList.add('justify-content-center');
        card.classList.add('align-items-center');
        card.classList.add('d-flex');
        card.style.height = '100px';
        line.push(card);
        row.appendChild(card);
    }
    cards.push(line);
}
console.log("cards", cards);

const gameName = JSON.parse(document.getElementById('game-name').textContent);
    let wsLoc = 'ws://'
                + window.location.host
                + '/ws/tictactoe/game/'
                + gameName
                + '/'
    console.log(wsLoc)
    const gameSocket = new WebSocket(wsLoc);

    gameSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data['type'] == 'initialize'){
            playerSym = data['player_symbol'];
            console.log(playerSym);
            if(playerSym === 'x'){
                playerImage = x;
            } else {
                playerImage = o;
            }
            subCont.appendChild(playerImage.cloneNode(true));
        } else {
            if(data['winner'] == 'o'){
                alert(`o wins`)
            }
            if(data['winner'] == 'x'){
                alert(`x wins`)
            }
            console.log(data['winner']);
        }
        // console.log("winner: ", data['winner']);
        turn = data['turn'];
        board = data['board'];
        console.log(board);
        updateBoard(board);
        document.querySelector('#symbol-turn').innerHTML = turn


        // document.querySelector('#chat-log').value += (data.message + '\n');
    };

    // chatSocket.onclose = function(e) {
    //     console.error('Chat socket closed unexpectedly');
    // };

    // document.querySelector('#chat-message-input').focus();
    // document.querySelector('#chat-message-input').onkeyup = function(e) {
    //     if (e.key === 'Enter') {  // enter, return
    //         document.querySelector('#chat-message-submit').click();
    //     }
    // };

    // document.querySelector('#chat-message-submit').onclick = function(e) {
    //     const messageInputDom = document.querySelector('#chat-message-input');
    //     const message = messageInputDom.value;
    //     chatSocket.send(JSON.stringify({
    //         'message': message
    //     }));
    //     console.log(message)
    //     messageInputDom.value = '';
    // };
    
    function updateBoard(board){
        console.log('turn: ', turn, 'player: ', playerSym);
        board.forEach((line, i) => {
            line.forEach((symbol, j) => {
            let card = cards[i][j];
            card.innerHTML = '';

            if(symbol == 'o'){
                card.appendChild(o.cloneNode(true));
            } else if(symbol == 'x'){
                card.appendChild(x.cloneNode(true));
            } else {
                card.innerHTML = '';
            }
        });
    });
        
}

cards.forEach((line, i) => {
    line.forEach((element, j) => {
        element.addEventListener('mouseover',() =>{
            element.classList.add('bg-light');
        })
        element.addEventListener('mouseout',() =>{
            element.classList.remove('bg-light');
        })
        element.addEventListener('click',() =>{
            if(turn === playerSym){
                gameSocket.send(JSON.stringify({
                    "move": [i, j],
                }))
            }
        })
    })
});


function getCardPos(i){
    let posx = i % gridSize;
    let posy = Math.floor(i/gridSize);
    return [posx, posy]
}