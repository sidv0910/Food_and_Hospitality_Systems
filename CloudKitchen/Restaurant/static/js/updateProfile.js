function validate() {
    var zip = document.getElementById('id_zip').value;
	var mobile2 = document.getElementById('id_restaurant_contact').value;
	var mobile1 = parseInt(mobile2);
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

    if (mobile1 < 6000000000 || mobile1 > 9999999999 || mobile2.length != 10) {
        alert("Mobile Number should contain:\n1. Exactly 10 digits.\n2. Value must be between 6000000000 and 9999999999");
        document.getElementById('id_restaurant_contact').focus();
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

    var array1 = [];
    var checkboxes1 = document.querySelectorAll(`input[name="cuisine"]:checked`);
    for (var i = 0; i < checkboxes1.length; i++) {
        array1.push(checkboxes1[i].value);
    }
    document.getElementById('cuisines').value = array1;

    var array2 = [];
    var checkboxes2 = document.querySelectorAll(`input[name="working_days"]:checked`);
    for (var i = 0; i < checkboxes2.length; i++) {
        array2.push(checkboxes2[i].value);
    }
    document.getElementById('working_day').value = array2;

	return true;
}