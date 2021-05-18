function validate() {
    var zip = document.getElementById('id_zip').value;
    var email = document.getElementById('id_restaurant_email').value;
	var mobile2 = document.getElementById('id_restaurant_contact').value;
	var mobile1 = parseInt(mobile2);
	var pword = document.getElementById('id_password').value;
	var cost_for_two = document.getElementById('id_cost_for_two').value;
	var outlets = document.getElementById('id_outlets').value;
    var from_time = document.getElementById('from_time').value;
    var to_time = document.getElementById('to_time').value;
    const cuisine = document.querySelectorAll(`input[name="cuisine"]:checked`);
    const working_days = document.querySelectorAll(`input[name="working_days"]:checked`);

    if (zip.length != 6 || zip.startsWith("0")) {
        alert("Zip Code should contain exactly 6 digits.");
        document.getElementById('id_zip').focus();
        return false;
	}

    var at = email.indexOf("@");
    var dot = email.lastIndexOf(".");
    if ((at < 1) || (dot < at+2) || (dot+2 >= email.length)) {
        alert("Please enter a valid e-mail address.\nEmail should be of type someone@example.com");
        document.getElementById('id_restaurant_email').focus();
        return false;
    }

    if (mobile1 < 6000000000 || mobile1 > 9999999999 || mobile2.length != 10) {
        alert("Mobile Number should contain:\n1. Exactly 10 digits.\n2. Value must be between 6000000000 and 9999999999");
        document.getElementById('id_restaurant_contact').focus();
        return false;
	}

	if (!(pword.match(/[a-z]/g) && pword.match(/[A-Z]/g) && pword.match(/[0-9]/g) && pword.match(/[^a-zA-Z\d]/g) && pword.length >= 8)) {
        alert("Password should contain:\n1. Atleast 1 uppercase character.\n2. Atleast 1 lowercase character.\n3. Atleast 1 digit.\n4. Atleast 1 special character.\n5. Minimum 8 characters.");
        document.getElementById('id_password').focus();
        return false;
    }

    if (cost_for_two < 100 || cost_for_two > 10000) {
        alert("Cost For Two must be between Rs 100 and Rs 5000");
        document.getElementById('id_cost_for_two').focus();
        return false;
	}

	if (outlets < 1 || outlets > 10000) {
        alert("Number of Outlets must be between 1 and 100");
        document.getElementById('id_outlets').focus();
        return false;
	}

    if (parseInt(from_time) >= parseInt(to_time)) {
        alert("Opening Time can't be same as or after the Closing Time.");
        document.getElementById('from_time').focus();
        return false;
    }

    if (cuisine.length == 0) {
        alert("Please select atleast one cuisine.");
        return false;
    }

    if (working_days.length == 0) {
        alert("Please select all your working days.");
        return false;
    }

	return true;
}

