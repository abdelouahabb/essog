//source code http://javascript.about.com/library/blvalsub4.htm
var submitted = 0;
function formvalidation(form) {
	if (submitted) {
		alert("vous avez deja envoyer, veuillez patienter");
		return false;
	}

	if (!submitted) {
		form.submitit.disabled = true;
		submitted = 1;
		form.submit();
	}
}