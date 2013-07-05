function textCounter(field, meter) {
    document.getElementById(meter).value = document.getElementById(field).value.length
    document.getElementById(field).value = document.getElementById(field).value.substring(0, 160)
}

function Compare(x, y) {
    var min = parseInt(document.getElementById(x).value)
    var max = parseInt(document.getElementById(y).value)
    if (min > max) {
        alert("le prix MINIMAL est SUPÉRIEUR au prix MAXIMAL!")
        document.formacha.min.focus()
    }
}

function Rabais(x, y, z) {
    var a = parseInt(document.getElementById(x).value)
    var b = parseInt(document.getElementById(y).value)
    //c = a - (a*b/100)
    return c = b - (b*a/100)
}

function Solde(x, y){
    document.getElementById(x).innerHTML = Separe(y)
}

function Tel(x, y) {
    var handler = function(e) {
        var a = document.getElementById(x).value
        document.getElementById(y).innerHTML = "Son Numéro : " + a.substr(0, 2) + " " + a.substr(2, 2) + " " + a.substr(4, 2) + " " + a.substr(6, 2) + " " + a.substr(8, 2)
        if (a.length > 10) {
            alert("Le numéro doit contenir 10 chiffres")
        }
    };
    document.getElementById(x).onchange = handler;
    document.getElementById(x).onkeyup = handler;
}

function Separe(prix) {
    nStr = Number(document.getElementById(prix).value) * 100
    nStr += '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(nStr)) {
        nStr = nStr.replace(rgx, '$1' + ' ' + '$2');
    }
    return nStr + " Centimes";
}

function Forma(prix, dest) {
    var handler = function(e) {
        document.getElementById(dest).innerHTML = Separe(prix)
    };
    document.getElementById(prix).onchange = handler;
    document.getElementById(prix).onkeyup = handler;
}
