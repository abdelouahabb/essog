//downloaded from http://techo.luefher.com/coding/javascript-js/how-to-determine-if-caps-lock-is-on-with-javascript/
function checkCapsLock(e) {
	var keyCode = e.keyCode ? e.keyCode : e.which; // get the key code
	var character = String.fromCharCode(keyCode); // convert to the corresponding character
	if (!/[A-Za-z]/.test(character)) { // if it's not a character, let's skip because caps lock has no effect in this case
		return;
	}
	var shiftKeyOn = e.shiftKey || keyCode == 16; // get the state of the shift key
	var capsOn = shiftKeyOn ? /[a-z]/.test(character) : /[A-Z]/.test(character); // if shift key is pressed but the character is lower case, caps lock is on, else, if shift key is not pressed but the character is upper case, caps lock is on
	document.getElementById('caps-on-warning').style.visibility = capsOn ? 'visible' : 'hidden'; // show/hide hint
}