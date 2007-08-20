
///////////////////////////////////////////////////////////////////////////////
//
//  Cookie class for manipulating cookies, and information within a cookie.
//  Information within a cookie is modelled as property/value pairs, where
//  property can be any string, and value can be one or more strings. All 
//  strings are escaped within the class, so the user need not worry about 
//  that.  
//
//  I have attempted to do a crude check for violations of the specified
//  maxumum cookie size.  Any properties beyond the maximum size are lopped
//  off without warning or error messages being produced.  
//
//  Example of setting a cookie:
//      var cookie = new Cookie("MyDog");
//      cookie.reset();
//      cookie.set("name", "Fido");
//      cookie.set("colour", "brown");
//      cookie.append("pups", "Bubble");
//      cookie.append("pups", "Squeak");
//      cookie.save();
//
//  Example of using the cookie:
//      var cookie = new Cookie("MyDog");
//      alert("Name: " + cookie.get("name"));
//      alert("Colour: " + cookie.get("colour"));
//      var pups = cookie.getAsArray("pups");
//      if (pups != null) {
//          var i;
//          for (i = 0; i < pups.length; i++) {
//              alert("Pup " + i + ": " + pups[i]);
//          }
//      }
//
///////////////////////////////////////////////////////////////////////////////


// Construct a Cookie object.  If the current document has one with
// the specified name, the cookie's data is read into the object.
function Cookie(name) {
    this.escapedName = escape(name);
    this.escapedProps = new Array();
    this.escapedVals = new Array();
    var documentCookie = document.cookie;
    var prefix = this.escapedName + "=";
    var begin = documentCookie.indexOf("; " + prefix);
    if (begin == -1) {
        // Required cookie found; it is the only one associated with document
        begin = documentCookie.indexOf(prefix);
        if (begin != 0) {
            // Required cookie not found
            return;
        }
    } else {
        // Found required cookie amongst several associated with the document
        begin += 2;
    }
    var end = documentCookie.indexOf(";", begin);
    if (end == -1) {
        end = documentCookie.length;
    }
    var cookieStr = documentCookie.substring(begin + prefix.length, end);
    var escapedPropValPairs = cookieStr.split("&");
    var escapedPropValPair;
    var i;
    var n = escapedPropValPairs.length;
	for (i = 0; i < n; i++) {
	    escapedPropValPair = escapedPropValPairs[i].split(":");
	    this.escapedProps[i] = escapedPropValPair[0];
	    this.escapedVals[i] = escapedPropValPair[1];
	}
}

// Set a property/value pair in the Cookie object.  If the property 
// is already there, its value is changed; if not, the property 
// is created.
Cookie.prototype.set = function(prop, val) {
    var escapedProp = escape(prop);
    var escapedVal = escape(val);
    var i;
    var n = this.escapedProps.length;
    for (i = 0; i < n; i++) {
        if (this.escapedProps[i] == escapedProp) {
            this.escapedVals[i] = escapedVal;
            return;
        }
    }
    this.escapedProps[i] = escapedProp;
    this.escapedVals[i] = escapedVal;
};

// Property values can have multiple values.  Appends a value to a property.  
// If the property does not already exist, it is created.
Cookie.prototype.append = function(prop, val) {
    var escapedProp = escape(prop);
    var escapedVal = escape(val);
    var i;
    var n = this.escapedProps.length;
    for (i = 0; i < n; i++) {
        if (this.escapedProps[i] == escapedProp) {
            if (this.escapedVals[i] == "") {
                this.escapedVals[i] = escapedVal;
            } else {
                this.escapedVals[i] += "," + escapedVal;
            }
            return;
        }
    }
    this.escapedProps[i] = escapedProp;
    this.escapedVals[i] = escapedVal;
};

// Returns the property value.  If the property does not exist, null
// is returned.  If the property has multiple values, all values 
// are returned as a comma separated string.  Note that if the values
// themselves contain a comma, this is not ideal - see also getAsArray().
Cookie.prototype.get = function(prop) {
    var escapedProp = escape(prop);
    var i;
    var n = this.escapedProps.length;
    for (i = 0; i < n; i++) {
        if (this.escapedProps[i] == escapedProp) {
            return unescape(this.escapedVals[i]);
        }
    }
    return null;
};

// Returns the property value as an array.  If the property value 
// has a simple value or an empty string, an array of size 1 is returned.
// If the property does not exist, null is returned.
Cookie.prototype.getAsArray = function(prop) {
    var escapedProp = escape(prop);
    var i;
    var n = this.escapedProps.length;
    for (i = 0; i < n; i++) {
        if (this.escapedProps[i] == escapedProp) {
            var escapedElements = this.escapedVals[i].split (",");
            var j;
            var elementCount = escapedElements.length;
            var elements = new Array(elementCount - 1);
	        for (j = 0; j < elementCount; j++) {
	            elements[j] = unescape(escapedElements[j]);
	        }
            return elements;
        }
    }
    return null;
};

// Deletes all properties and values from the Cookie object.
Cookie.prototype.reset = function() {
    this.escapedProps = new Array();
    this.escapedVals = new Array();
    document.cookie = this.escapedName + "=";
};

// Writes the Cookie object as an actual cookie.
// expires - expiration date of the cookie 
//           (defaults to end of current session)
// path    - path for which the cookie is valid 
//           (defaults to path of calling document)
// domain  - domain for which the cookie is valid 
//           (defaults to domain of calling document)
// secure  - Boolean value indicating if the cookie 
//           transmission requires a secure transmission
// NB: An argument defaults when it is assigned null as a placeholder, and a null 
//     placeholder is not required for trailing omitted arguments.  So in the 
//     simplest case all arguments can be ommitted.
Cookie.prototype.save = function(name, value, expires, path, domain, secure) {
    var cookieStr = "";
    var metaInfo = 
    ((expires) ? "; expires=" + expires.toGMTString() : "") +
    ((path) ? "; path=" + path : "") +
    ((domain) ? "; domain=" + domain : "") +
    ((secure) ? "; secure" : "");
    // RFC 2109 specifies the max cookie size
    var maxCookieSize = 4096;
    // The information bit is less than this maximum, to allow for the cookie name, 
    // the equals sign after the name, and the meta information.
    var maxCookieInfoSize = maxCookieSize - this.escapedName - 1 - metaInfo.length;
    var i;
    var n = this.escapedProps.length;
    for (i = 0; i < n; i++) {
        cookieStr += this.escapedProps[i] + ":" + this.escapedVals[i];
        if (i != n - 1) {
            cookieStr += "&";
        }
    }
    if (cookieStr.length > maxCookieInfoSize) {
        posLastOkAmpersand = cookieStr.lastIndexOf("&", maxCookieInfoSize - 1);
        if (posLastOkAmpersand == -1) {
            cookieStr = "";
        } else {
            cookieStr = cookieStr.substring(0, posLastOkAmpersand - 1);
        }
    }
    document.cookie = this.escapedName + "=" + cookieStr + metaInfo;
};

