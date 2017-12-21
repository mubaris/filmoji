var emoji = new EmojiConvertor();
//emoji.img_sets.apple.path = 'https://unicodey.com/js-emoji/build/emoji-data/img-apple-64/';
//emoji.img_sets.apple.sheet = 'https://unicodey.com/js-emoji/build/emoji-data/sheet_apple_64.png';

var table = document.getElementById("main-table");
table.innerHTML = emoji.replace_unified(table.innerHTML);

function swapRows() {
    var row = document.getElementById('main-table').getElementsByTagName('tbody')[0].rows;;
    var rC = row.length;
    var tBody = row[0].parentNode;
    for (i = 0; i < rC; i++) {
        tBody.insertBefore(row[Math.ceil(Math.random() * (rC - 1))], row[i]);
    }
}

window.onload = swapRows;