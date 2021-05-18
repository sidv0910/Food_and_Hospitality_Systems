function validate() {

    var pword = document.getElementById('id_password').value;
    var repword = document.getElementById('id_re_password').value;

    if (!(pword.match(/[a-z]/g) && pword.match(/[A-Z]/g) && pword.match(/[0-9]/g) && pword.match(/[^a-zA-Z\d]/g))) {
        alert("Password should contain:\n1. Atleast 1 uppercase character.\n2. Atleast 1 lowercase character.\n3. Atleast 1 digit.\n4. Atleast 1 special character.");
        document.getElementById('id_password').focus();
        return false;
    }

    if (pword != repword) {
        alert("Passwords did not match.");
        document.getElementById('id_re_password').focus();
        return false;
	}

    return true;
}