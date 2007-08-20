var selecteditemsarray;
var host = "localhost:8060";

function SaveMenuSelections(form, object) {

	var weeks = form.elements["weeks"].options[form.elements["weeks"].selectedIndex].value;

	var cookie_filter_val_key;
	var cookie_val_key;

	if (object == "student+set") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_student+set_vals";
    }
	else if (object == "staff") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_staff_vals";
    }
	else if (object == "location") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_location_vals";
    }

	var cookie = new Cookie("sws_cust");
	cookie.reset();
	cookie.set("weeks", weeks);
    if (cookie_filter_val_key != "") {
	    cookie.set(cookie_filter_val_key, form.elements["filter"].options[form.elements["filter"].selectedIndex].value);
    }

	var inputelement = form.elements["identifier[]"];

    for (var i = 0; i < inputelement.options.length; i++) {
		if (inputelement.options[i].selected) {
			cookie.append(cookie_val_key, inputelement.options[i].value);
		}
	}

	cookie.save();

}

function SetMenuSelections (form, object) {

	var cookie_filter_val_key;
	var cookie_val_key;

	if (object == "student+set") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_student+set_vals";
    }
	if (object == "staff") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_staff_vals";
    }
	if (object == "location") {
        cookie_filter_val_key = "saved_zone_filter_val";
	    cookie_val_key = "saved_location_vals";
    }

    var cookie = new Cookie("sws_cust");
    var saved_filter_val = "";
    if (cookie_filter_val_key != "") {
        saved_filter_val = cookie.get(cookie_filter_val_key);
    }
    if (saved_filter_val != "") {
        cbxfilter = form.elements["filter"];
        for (var i = 0; i < cbxfilter.options.length; i++) {
            if (cbxfilter.options[i].value == saved_filter_val) {
                cbxfilter.options[i].selected = true;
            }
        }
    }
	if (object == "student+set"){
        FilterStudentSets(form);
    }
    else if (object == "staff"){
        FilterStaff(form);
    }
	else if (object == "location"){
        FilterRooms(form);
    }

    var saved_vals = cookie.getAsArray(cookie_val_key);
    if (saved_vals != null) {
    	var inputelement = form.elements["identifier[]"];
  	    for (var i = 0; i < inputelement.options.length; i++) {
  	        for (var j = 0; j < saved_vals.length; j++) {
                if (inputelement.options[i].value == saved_vals[j]) {
                    inputelement.options[i].selected = true;
                    break;
                }
            }
   	    }
    }
	var saved_weeks = cookie.get("weeks");
    cbxweeks = form.elements["weeks"];
    for (var i = 0; i < cbxweeks.options.length; i++) {
        if (cbxweeks.options[i].value == saved_weeks) {
            cbxweeks.options[i].selected = true;
        }
    }
}

function AddWeeks(strWeekRange, strWeekLabel, cbxWeeks) {

	var intLength = cbxWeeks.options.length;

	cbxWeeks.options[intLength] = new Option(strWeekLabel, strWeekRange);

}