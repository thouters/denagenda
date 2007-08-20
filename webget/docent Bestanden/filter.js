// Generated Automatically on 7 feb 2007 09:18:00
_
// S+ Prog ID: SplusList
// Institution Start Date: 18 sep 2006
// Copyright Scientia Ltd 2007
// Scientia does not accept any warranty with regard to the content or usage of this file
function PopulateFilter(strZoneOrDept, cbxFilter) {
    var deptarray = new Array(1);
    for (var i=0; i<deptarray.length; i++) {
        deptarray[i] = new Array(1);
    }
    deptarray[0] [0] = "Departement Technologie";
    deptarray[0] [1] = "Technologie";
    deptarray.sort();
    var zonearray = new Array(7);
    for (var i=0; i<zonearray.length; i++) {
        zonearray[i] = new Array(1);
    }
    zonearray[0] [0] = "De Nayer Instituut";
    zonearray[0] [1] = "De Nayer Instituut";
    zonearray[1] [0] = "Beeldende Kunst Gent";
    zonearray[1] [1] = "Beeldende Kunst Gent";
    zonearray[2] [0] = "Sint-Lucas Gent";
    zonearray[2] [1] = "Sint-Lucas Gent";
    zonearray[3] [0] = "Sint-Lucas Brussel";
    zonearray[3] [1] = "Sint-Lucas Brussel";
    zonearray[4] [0] = "BMF - Architectuur Brussel";
    zonearray[4] [1] = "BMF - Architectuur Brussel";
    zonearray[5] [0] = "BMF - Architectuur Gent";
    zonearray[5] [1] = "BMF - Architectuur Gent";
    zonearray[6] [0] = "BMF - Beeldende Kunst";
    zonearray[6] [1] = "BMF - Beeldende Kunst";
    zonearray.sort();
    if (strZoneOrDept != "DeptIdentifier") {
        cbxFilter.options[0] = new Option("Kies","(None)");
        var j = 1;
    }
    else {
        var j = 0;
    }
    if (strZoneOrDept == "Zone") {
        for (var i = 0; i<zonearray.length; i++) {
            cbxFilter.options[j] = new Option(zonearray[i] [0], zonearray[i] [1]);
            j++;
        }
    }
    else {
        if ((strZoneOrDept == "Dept") || (strZoneOrDept == "DeptIdentifier")) {
            for (var i = 0; i<deptarray.length; i++) {
                if (strZoneOrDept == "Dept") {
                    cbxFilter.options[j] = new Option(deptarray[i] [0], deptarray[i] [1]);
                    j++;
                }
                else {
                    cbxFilter.options[j] = new Option(deptarray[i] [0], deptarray[i] [1]);
                    j++;
                }
            }
        }
    }
}
function PopulateFilterWithProgrammes(cbxFilter) {
var progarray = new Array(17);
    for (var i=0; i<progarray.length; i++ ) {
        progarray[i] = new Array(2);
    }
    progarray[0] [0] = "1PBEIE";
    progarray[0] [1] = "Technologie";
    progarray[0] [2] = "%23SPLUS97B8B7";
    progarray[1] [0] = "1PBEII";
    progarray[1] [1] = "Technologie";
    progarray[1] [2] = "%23SPLUS97B8B6";
    progarray[2] [0] = "1PBAT";
    progarray[2] [1] = "Technologie";
    progarray[2] [2] = "%23SPLUSE639E5";
    progarray[3] [0] = "2PBAT";
    progarray[3] [1] = "Technologie";
    progarray[3] [2] = "%23SPLUSE639E6";
    progarray[4] [0] = "3PBAT";
    progarray[4] [1] = "Technologie";
    progarray[4] [2] = "%23SPLUSE639E7";
    progarray[5] [0] = "3PBEIE";
    progarray[5] [1] = "Technologie";
    progarray[5] [2] = "%23SPLUSE639E9";
    progarray[6] [0] = "2PBEII";
    progarray[6] [1] = "Technologie";
    progarray[6] [2] = "%23SPLUSE639EB";
    progarray[7] [0] = "3PBEII";
    progarray[7] [1] = "Technologie";
    progarray[7] [2] = "%23SPLUSE639EC";
    progarray[8] [0] = "1PBEM/MP";
    progarray[8] [1] = "Technologie";
    progarray[8] [2] = "%23SPLUSE639ED";
    progarray[9] [0] = "3PBEMA";
    progarray[9] [1] = "Technologie";
    progarray[9] [2] = "%23SPLUSE639EE";
    progarray[10] [0] = "3PBEMK";
    progarray[10] [1] = "Technologie";
    progarray[10] [2] = "%23SPLUSE639EF";
    progarray[11] [0] = "3PBEMO";
    progarray[11] [1] = "Technologie";
    progarray[11] [2] = "%23SPLUSE639F0";
    progarray[12] [0] = "2PBMP";
    progarray[12] [1] = "Technologie";
    progarray[12] [2] = "%23SPLUSE639F1";
    progarray[13] [0] = "3PBMP";
    progarray[13] [1] = "Technologie";
    progarray[13] [2] = "%23SPLUSE639F2";
    progarray[14] [0] = "2PBEM";
    progarray[14] [1] = "Technologie";
    progarray[14] [2] = "%23SPLUSE63A0B";
    progarray[15] [0] = "2PBEIE";
    progarray[15] [1] = "Technologie";
    progarray[15] [2] = "%23SPLUSE63A10";
    progarray[16] [0] = "1PBEI";
    progarray[16] [1] = "Technologie";
    progarray[16] [2] = "%23SPLUSE639E8";
    progarray.sort();
    cbxFilter.options[0] = new Option("Kies","(None)");
    var j = 1;
    for (var i = 0; i<progarray.length; i++) {
        cbxFilter.options[j] = new Option(progarray[i] [0], progarray[i] [0]);
        j++;
    }
}
function FilterRooms(Form) {
var roomarray = new Array(79);
    for (var i=0; i<roomarray.length; i++ ) {
        roomarray[i] = new Array(2);
    }
    roomarray[0] [0] = "F015";
    roomarray[0] [1] = "De Nayer Instituut";
    roomarray[0] [2] = "%23SPLUSAC419F";
    roomarray[1] [0] = "";
    roomarray[1] [1] = "Unknown";
    roomarray[1] [2] = "%23SPLUSAFC646";
    roomarray[2] [0] = "";
    roomarray[2] [1] = "Unknown";
    roomarray[2] [2] = "%23SPLUSAFC63D";
    roomarray[3] [0] = "H1.06";
    roomarray[3] [1] = "De Nayer Instituut";
    roomarray[3] [2] = "%23SPLUS13FC79";
    roomarray[4] [0] = "A116";
    roomarray[4] [1] = "De Nayer Instituut";
    roomarray[4] [2] = "%23SPLUS33C0DF";
    roomarray[5] [0] = "F002";
    roomarray[5] [1] = "De Nayer Instituut";
    roomarray[5] [2] = "%23SPLUS1A8571";
    roomarray[6] [0] = "F010";
    roomarray[6] [1] = "De Nayer Instituut";
    roomarray[6] [2] = "%23SPLUS1A8572";
    roomarray[7] [0] = "D006";
    roomarray[7] [1] = "De Nayer Instituut";
    roomarray[7] [2] = "%23SPLUS7E4FBA";
    roomarray[8] [0] = "G117";
    roomarray[8] [1] = "De Nayer Instituut";
    roomarray[8] [2] = "%23SPLUS13FC7A";
    roomarray[9] [0] = "G120";
    roomarray[9] [1] = "De Nayer Instituut";
    roomarray[9] [2] = "%23SPLUS13FC7B";
    roomarray[10] [0] = "K204";
    roomarray[10] [1] = "De Nayer Instituut";
    roomarray[10] [2] = "%23SPLUS13FC7C";
    roomarray[11] [0] = "K206";
    roomarray[11] [1] = "De Nayer Instituut";
    roomarray[11] [2] = "%23SPLUS13FC7D";
    roomarray[12] [0] = "C208";
    roomarray[12] [1] = "De Nayer Instituut";
    roomarray[12] [2] = "%23SPLUS13FC7E";
    roomarray[13] [0] = "A202";
    roomarray[13] [1] = "De Nayer Instituut";
    roomarray[13] [2] = "%23SPLUS13FC73";
    roomarray[14] [0] = "A203";
    roomarray[14] [1] = "De Nayer Instituut";
    roomarray[14] [2] = "%23SPLUS13FC74";
    roomarray[15] [0] = "A213";
    roomarray[15] [1] = "De Nayer Instituut";
    roomarray[15] [2] = "%23SPLUS13FC75";
    roomarray[16] [0] = "A217";
    roomarray[16] [1] = "De Nayer Instituut";
    roomarray[16] [2] = "%23SPLUS13FC76";
    roomarray[17] [0] = "D016";
    roomarray[17] [1] = "De Nayer Instituut";
    roomarray[17] [2] = "%23SPLUS13FC77";
    roomarray[18] [0] = "D018";
    roomarray[18] [1] = "De Nayer Instituut";
    roomarray[18] [2] = "%23SPLUS13FC78";
    roomarray[19] [0] = "D008";
    roomarray[19] [1] = "De Nayer Instituut";
    roomarray[19] [2] = "%23SPLUS33C0E2";
    roomarray[20] [0] = "D011";
    roomarray[20] [1] = "De Nayer Instituut";
    roomarray[20] [2] = "%23SPLUS33C0E3";
    roomarray[21] [0] = "D012";
    roomarray[21] [1] = "De Nayer Instituut";
    roomarray[21] [2] = "%23SPLUS33C0E4";
    roomarray[22] [0] = "D013";
    roomarray[22] [1] = "De Nayer Instituut";
    roomarray[22] [2] = "%23SPLUS33C0E5";
    roomarray[23] [0] = "A110";
    roomarray[23] [1] = "De Nayer Instituut";
    roomarray[23] [2] = "%23SPLUS33C0DD";
    roomarray[24] [0] = "A111";
    roomarray[24] [1] = "De Nayer Instituut";
    roomarray[24] [2] = "%23SPLUS33C0DE";
    roomarray[25] [0] = "D004";
    roomarray[25] [1] = "De Nayer Instituut";
    roomarray[25] [2] = "%23SPLUS33C0E0";
    roomarray[26] [0] = "D007";
    roomarray[26] [1] = "De Nayer Instituut";
    roomarray[26] [2] = "%23SPLUS33C0E1";
    roomarray[27] [0] = "D019";
    roomarray[27] [1] = "De Nayer Instituut";
    roomarray[27] [2] = "%23SPLUS13FC63";
    roomarray[28] [0] = "A009";
    roomarray[28] [1] = "De Nayer Instituut";
    roomarray[28] [2] = "%23SPLUS13FC64";
    roomarray[29] [0] = "A010";
    roomarray[29] [1] = "De Nayer Instituut";
    roomarray[29] [2] = "%23SPLUS13FC65";
    roomarray[30] [0] = "A011";
    roomarray[30] [1] = "De Nayer Instituut";
    roomarray[30] [2] = "%23SPLUS13FC66";
    roomarray[31] [0] = "A022";
    roomarray[31] [1] = "De Nayer Instituut";
    roomarray[31] [2] = "%23SPLUS13FC67";
    roomarray[32] [0] = "A023";
    roomarray[32] [1] = "De Nayer Instituut";
    roomarray[32] [2] = "%23SPLUS13FC68";
    roomarray[33] [0] = "A021";
    roomarray[33] [1] = "De Nayer Instituut";
    roomarray[33] [2] = "%23SPLUS13FC69";
    roomarray[34] [0] = "A208";
    roomarray[34] [1] = "De Nayer Instituut";
    roomarray[34] [2] = "%23SPLUS13FC6A";
    roomarray[35] [0] = "A209";
    roomarray[35] [1] = "De Nayer Instituut";
    roomarray[35] [2] = "%23SPLUS13FC6B";
    roomarray[36] [0] = "C006";
    roomarray[36] [1] = "De Nayer Instituut";
    roomarray[36] [2] = "%23SPLUS13FC6C";
    roomarray[37] [0] = "C014";
    roomarray[37] [1] = "De Nayer Instituut";
    roomarray[37] [2] = "%23SPLUS13FC6D";
    roomarray[38] [0] = "C015";
    roomarray[38] [1] = "De Nayer Instituut";
    roomarray[38] [2] = "%23SPLUS13FC6E";
    roomarray[39] [0] = "C017";
    roomarray[39] [1] = "De Nayer Instituut";
    roomarray[39] [2] = "%23SPLUS13FC6F";
    roomarray[40] [0] = "C018";
    roomarray[40] [1] = "De Nayer Instituut";
    roomarray[40] [2] = "%23SPLUS13FC70";
    roomarray[41] [0] = "C019";
    roomarray[41] [1] = "De Nayer Instituut";
    roomarray[41] [2] = "%23SPLUS13FC71";
    roomarray[42] [0] = "C106";
    roomarray[42] [1] = "De Nayer Instituut";
    roomarray[42] [2] = "%23SPLUS13FC72";
    roomarray[43] [0] = "N003";
    roomarray[43] [1] = "De Nayer Instituut";
    roomarray[43] [2] = "%23SPLUS13FC5C";
    roomarray[44] [0] = "N004";
    roomarray[44] [1] = "De Nayer Instituut";
    roomarray[44] [2] = "%23SPLUS13FC5D";
    roomarray[45] [0] = "N008";
    roomarray[45] [1] = "De Nayer Instituut";
    roomarray[45] [2] = "%23SPLUS13FC5E";
    roomarray[46] [0] = "N009";
    roomarray[46] [1] = "De Nayer Instituut";
    roomarray[46] [2] = "%23SPLUS13FC5F";
    roomarray[47] [0] = "N010";
    roomarray[47] [1] = "De Nayer Instituut";
    roomarray[47] [2] = "%23SPLUS13FC60";
    roomarray[48] [0] = "N011";
    roomarray[48] [1] = "De Nayer Instituut";
    roomarray[48] [2] = "%23SPLUS13FC61";
    roomarray[49] [0] = "N103";
    roomarray[49] [1] = "De Nayer Instituut";
    roomarray[49] [2] = "%23SPLUS13FC62";
    roomarray[50] [0] = "K104";
    roomarray[50] [1] = "De Nayer Instituut";
    roomarray[50] [2] = "%23SPLUS33C0CC";
    roomarray[51] [0] = "K103";
    roomarray[51] [1] = "De Nayer Instituut";
    roomarray[51] [2] = "%23SPLUS33C0CD";
    roomarray[52] [0] = "N001";
    roomarray[52] [1] = "De Nayer Instituut";
    roomarray[52] [2] = "%23SPLUS33C0CE";
    roomarray[53] [0] = "N002";
    roomarray[53] [1] = "De Nayer Instituut";
    roomarray[53] [2] = "%23SPLUS33C0CF";
    roomarray[54] [0] = "F109";
    roomarray[54] [1] = "De Nayer Instituut";
    roomarray[54] [2] = "%23SPLUS33C0C2";
    roomarray[55] [0] = "F110";
    roomarray[55] [1] = "De Nayer Instituut";
    roomarray[55] [2] = "%23SPLUS33C0C3";
    roomarray[56] [0] = "F113";
    roomarray[56] [1] = "De Nayer Instituut";
    roomarray[56] [2] = "%23SPLUS33C0C4";
    roomarray[57] [0] = "F114";
    roomarray[57] [1] = "De Nayer Instituut";
    roomarray[57] [2] = "%23SPLUS33C0C5";
    roomarray[58] [0] = "K107";
    roomarray[58] [1] = "De Nayer Instituut";
    roomarray[58] [2] = "%23SPLUS33C0C6";
    roomarray[59] [0] = "K108";
    roomarray[59] [1] = "De Nayer Instituut";
    roomarray[59] [2] = "%23SPLUS33C0C7";
    roomarray[60] [0] = "K111";
    roomarray[60] [1] = "De Nayer Instituut";
    roomarray[60] [2] = "%23SPLUS33C0C8";
    roomarray[61] [0] = "K112";
    roomarray[61] [1] = "De Nayer Instituut";
    roomarray[61] [2] = "%23SPLUS33C0C9";
    roomarray[62] [0] = "K113";
    roomarray[62] [1] = "De Nayer Instituut";
    roomarray[62] [2] = "%23SPLUS33C0CA";
    roomarray[63] [0] = "K114";
    roomarray[63] [1] = "De Nayer Instituut";
    roomarray[63] [2] = "%23SPLUS33C0CB";
    roomarray[64] [0] = "A113";
    roomarray[64] [1] = "De Nayer Instituut";
    roomarray[64] [2] = "%23SPLUS13FC59";
    roomarray[65] [0] = "A117";
    roomarray[65] [1] = "De Nayer Instituut";
    roomarray[65] [2] = "%23SPLUS13FC5A";
    roomarray[66] [0] = "A118";
    roomarray[66] [1] = "De Nayer Instituut";
    roomarray[66] [2] = "%23SPLUS13FC5B";
    roomarray[67] [0] = "A014";
    roomarray[67] [1] = "De Nayer Instituut";
    roomarray[67] [2] = "%23SPLUS33C0BD";
    roomarray[68] [0] = "A015";
    roomarray[68] [1] = "De Nayer Instituut";
    roomarray[68] [2] = "%23SPLUS33C0BE";
    roomarray[69] [0] = "A017";
    roomarray[69] [1] = "De Nayer Instituut";
    roomarray[69] [2] = "%23SPLUS33C0BF";
    roomarray[70] [0] = "A018";
    roomarray[70] [1] = "De Nayer Instituut";
    roomarray[70] [2] = "%23SPLUS33C0C0";
    roomarray[71] [0] = "A019";
    roomarray[71] [1] = "De Nayer Instituut";
    roomarray[71] [2] = "%23SPLUS33C0C1";
    roomarray[72] [0] = "A103";
    roomarray[72] [1] = "De Nayer Instituut";
    roomarray[72] [2] = "%23SPLUS13FC57";
    roomarray[73] [0] = "A104";
    roomarray[73] [1] = "De Nayer Instituut";
    roomarray[73] [2] = "%23SPLUS13FC58";
    roomarray[74] [0] = "A002";
    roomarray[74] [1] = "De Nayer Instituut";
    roomarray[74] [2] = "%23SPLUS33C0B9";
    roomarray[75] [0] = "A003";
    roomarray[75] [1] = "De Nayer Instituut";
    roomarray[75] [2] = "%23SPLUS33C0BA";
    roomarray[76] [0] = "A004";
    roomarray[76] [1] = "De Nayer Instituut";
    roomarray[76] [2] = "%23SPLUS33C0BB";
    roomarray[77] [0] = "A005";
    roomarray[77] [1] = "De Nayer Instituut";
    roomarray[77] [2] = "%23SPLUS33C0BC";
    roomarray[78] [0] = "A102";
    roomarray[78] [1] = "De Nayer Instituut";
    roomarray[78] [2] = "%23SPLUS13FC56";
    roomarray.sort();
    var lbxObjects = Form.elements["identifier[]"];
    var cbxFilter = Form.elements["filter"];
    if (cbxFilter != null) {
        var strFilter = cbxFilter.options[cbxFilter.selectedIndex].value;
    }
    else {
        var strFilter = "(None)";
    }
    var j=0;
    lbxObjects.options.length = 0;
    if (strFilter == "(None)")
    {
        for (var i=0; i<roomarray.length; i++) {
            lbxObjects.options[j] = new Option(roomarray[i] [0], roomarray[i] [2]);
            j++;
        }
    }
    else
    {
        for (var i=0; i<roomarray.length; i++) {
            if (roomarray[i] [1] == strFilter) {
                lbxObjects.options[j] = new Option(roomarray[i] [0], roomarray[i] [2]);
                j++;
            }
        }
    }
}
function FilterStaff(Form) {
var staffarray = new Array(40);
    for (var i=0; i<staffarray.length; i++ ) {
        staffarray[i] = new Array(2);
    }
    staffarray[0] [0] = "MAES Johan";
    staffarray[0] [1] = "Technologie";
    staffarray[0] [2] = "%23SPLUS9411D6";
    staffarray[1] [0] = "JONKERS Bart";
    staffarray[1] [1] = "Technologie";
    staffarray[1] [2] = "%23SPLUS356543";
    staffarray[2] [0] = "PIRARD Hilde";
    staffarray[2] [1] = "Technologie";
    staffarray[2] [2] = "%23SPLUSCEF804";
    staffarray[3] [0] = "SCHEERS Ella";
    staffarray[3] [1] = "Technologie";
    staffarray[3] [2] = "%23SPLUSCEF805";
    staffarray[4] [0] = "VAN PELT Pihilip";
    staffarray[4] [1] = "Technologie";
    staffarray[4] [2] = "%23SPLUS7E3B6B";
    staffarray[5] [0] = "TIERENS Tom";
    staffarray[5] [1] = "Technologie";
    staffarray[5] [2] = "%23SPLUS761EDF";
    staffarray[6] [0] = "CLAESSENS Luc";
    staffarray[6] [1] = "Technologie";
    staffarray[6] [2] = "16007250295";
    staffarray[7] [0] = "BAUWENS Jimmy";
    staffarray[7] [1] = "Technologie";
    staffarray[7] [2] = "15809300476";
    staffarray[8] [0] = "BEHAEGELS Hubert";
    staffarray[8] [1] = "Technologie";
    staffarray[8] [2] = "15211060353";
    staffarray[9] [0] = "BERT Hugo";
    staffarray[9] [1] = "Technologie";
    staffarray[9] [2] = "15205090813";
    staffarray[10] [0] = "CEUPPENS Marc";
    staffarray[10] [1] = "Technologie";
    staffarray[10] [2] = "16601210294";
    staffarray[11] [0] = "Gastprof.. T.";
    staffarray[11] [1] = "Technologie";
    staffarray[11] [2] = "%23SPLUS1A8573";
    staffarray[12] [0] = "CUYKENS Benjamin";
    staffarray[12] [1] = "Technologie";
    staffarray[12] [2] = "15708010955";
    staffarray[13] [0] = "DAEMEN Christian";
    staffarray[13] [1] = "Technologie";
    staffarray[13] [2] = "16211100950";
    staffarray[14] [0] = "DAMS Wim";
    staffarray[14] [1] = "Technologie";
    staffarray[14] [2] = "18110270923";
    staffarray[15] [0] = "DE COSTER Johan";
    staffarray[15] [1] = "Technologie";
    staffarray[15] [2] = "16211040427";
    staffarray[16] [0] = "DE JONGE Joseph";
    staffarray[16] [1] = "Technologie";
    staffarray[16] [2] = "15710210431";
    staffarray[17] [0] = "DE NIES Geert";
    staffarray[17] [1] = "Technologie";
    staffarray[17] [2] = "16708170376";
    staffarray[18] [0] = "DE VOS Dirk";
    staffarray[18] [1] = "Technologie";
    staffarray[18] [2] = "15803130771";
    staffarray[19] [0] = "DEKETELAERE Wouter";
    staffarray[19] [1] = "Technologie";
    staffarray[19] [2] = "17710190379";
    staffarray[20] [0] = "DENEVE Kjell";
    staffarray[20] [1] = "Technologie";
    staffarray[20] [2] = "17709260593";
    staffarray[21] [0] = "DERUA Jan";
    staffarray[21] [1] = "Technologie";
    staffarray[21] [2] = "16704050102";
    staffarray[22] [0] = "DICTUS Denise";
    staffarray[22] [1] = "Technologie";
    staffarray[22] [2] = "24812043561";
    staffarray[23] [0] = "JACOBS Marc";
    staffarray[23] [1] = "Technologie";
    staffarray[23] [2] = "16512280492";
    staffarray[24] [0] = "JANSEN Hilde";
    staffarray[24] [1] = "Technologie";
    staffarray[24] [2] = "26507311147";
    staffarray[25] [0] = "MOYSON Koen";
    staffarray[25] [1] = "Technologie";
    staffarray[25] [2] = "16308030222";
    staffarray[26] [0] = "PELGRIMS Patrick";
    staffarray[26] [1] = "Technologie";
    staffarray[26] [2] = "16401040589";
    staffarray[27] [0] = "ROGGEMANS Marc";
    staffarray[27] [1] = "Technologie";
    staffarray[27] [2] = "16201270608";
    staffarray[28] [0] = "STROOBANTS Willy";
    staffarray[28] [1] = "Technologie";
    staffarray[28] [2] = "15601200922";
    staffarray[29] [0] = "SYMONS Paul";
    staffarray[29] [1] = "Technologie";
    staffarray[29] [2] = "15207310695";
    staffarray[30] [0] = "TWEEPENNINCKX Georges";
    staffarray[30] [1] = "Technologie";
    staffarray[30] [2] = "15304211271";
    staffarray[31] [0] = "VAN ELEWYCK Jan";
    staffarray[31] [1] = "Technologie";
    staffarray[31] [2] = "15212251029";
    staffarray[32] [0] = "VAN LOON Leonardus";
    staffarray[32] [1] = "Technologie";
    staffarray[32] [2] = "15508080922";
    staffarray[33] [0] = "VAN MALDEREN Marc";
    staffarray[33] [1] = "Technologie";
    staffarray[33] [2] = "15305250686";
    staffarray[34] [0] = "VAN POECK Jan";
    staffarray[34] [1] = "Technologie";
    staffarray[34] [2] = "15603290765";
    staffarray[35] [0] = "VAN ROSSUM Luc";
    staffarray[35] [1] = "Technologie";
    staffarray[35] [2] = "15011220650";
    staffarray[36] [0] = "VAN WESEMAEL Eric";
    staffarray[36] [1] = "Technologie";
    staffarray[36] [2] = "15512240505";
    staffarray[37] [0] = "VERELST Jan";
    staffarray[37] [1] = "Technologie";
    staffarray[37] [2] = "15909230886";
    staffarray[38] [0] = "VERSTRAETEN Julien";
    staffarray[38] [1] = "Technologie";
    staffarray[38] [2] = "15302070201";
    staffarray[39] [0] = "WINDERICKX Marc";
    staffarray[39] [1] = "Technologie";
    staffarray[39] [2] = "15505140408";
    staffarray.sort();
    var lbxObjects = Form.elements["identifier[]"];
    var cbxFilter = Form.elements["filter"];
    if (cbxFilter != null) {
        var strFilter = cbxFilter.options[cbxFilter.selectedIndex].value;
    }
    else {
        var strFilter = "(None)";
    }
    var j=0;
    lbxObjects.options.length = 0;
    if (strFilter == "(None)")
    {
        for (var i=0; i<staffarray.length; i++) {
            lbxObjects.options[j] = new Option(staffarray[i] [0], staffarray[i] [2]);
            j++;
        }
    }
    else
    {
        for (var i=0; i<staffarray.length; i++) {
            if (staffarray[i] [1] == strFilter) {
                lbxObjects.options[j] = new Option(staffarray[i] [0], staffarray[i] [2]);
                j++;
            }
        }
    }
}
function FilterStudentSets(Form) {
var studentsetarray = new Array(46);
    for (var i=0; i<studentsetarray.length; i++ ) {
        studentsetarray[i] = new Array(2);
    }
    studentsetarray[0] [0] = "1PBEII1";
    studentsetarray[0] [1] = "1PBEII";
    studentsetarray[0] [2] = "%23SPLUS97B8AF";
    studentsetarray[1] [0] = "1PBEII2";
    studentsetarray[1] [1] = "1PBEII";
    studentsetarray[1] [2] = "%23SPLUS97B8B2";
    studentsetarray[2] [0] = "1PBEIE1";
    studentsetarray[2] [1] = "1PBEIE";
    studentsetarray[2] [2] = "%23SPLUS97B8B3";
    studentsetarray[3] [0] = "1PBEI1";
    studentsetarray[3] [1] = "1PBEI";
    studentsetarray[3] [2] = "%23SPLUS0FC145";
    studentsetarray[4] [0] = "1PBEI3";
    studentsetarray[4] [1] = "1PBEI";
    studentsetarray[4] [2] = "%23SPLUS0FC146";
    studentsetarray[5] [0] = "1PBEI2";
    studentsetarray[5] [1] = "1PBEI";
    studentsetarray[5] [2] = "%23SPLUS0FC147";
    studentsetarray[6] [0] = "1PBEI4";
    studentsetarray[6] [1] = "1PBEI";
    studentsetarray[6] [2] = "%23SPLUS0FC14B";
    studentsetarray[7] [0] = "1PBEIE2";
    studentsetarray[7] [1] = "1PBEIE";
    studentsetarray[7] [2] = "%23SPLUS97B8B4";
    studentsetarray[8] [0] = "1PBAT1";
    studentsetarray[8] [1] = "1PBAT";
    studentsetarray[8] [2] = "%23SPLUSE639F3";
    studentsetarray[9] [0] = "1PBAT2";
    studentsetarray[9] [1] = "1PBAT";
    studentsetarray[9] [2] = "%23SPLUSE639F4";
    studentsetarray[10] [0] = "1PBAT3";
    studentsetarray[10] [1] = "1PBAT";
    studentsetarray[10] [2] = "%23SPLUSE639F5";
    studentsetarray[11] [0] = "1PBAT4";
    studentsetarray[11] [1] = "1PBAT";
    studentsetarray[11] [2] = "%23SPLUSE639F6";
    studentsetarray[12] [0] = "1PBAT5";
    studentsetarray[12] [1] = "1PBAT";
    studentsetarray[12] [2] = "%23SPLUSE639F7";
    studentsetarray[13] [0] = "1PBAT6";
    studentsetarray[13] [1] = "1PBAT";
    studentsetarray[13] [2] = "%23SPLUSE639F8";
    studentsetarray[14] [0] = "2PBAT1";
    studentsetarray[14] [1] = "2PBAT";
    studentsetarray[14] [2] = "%23SPLUSE639F9";
    studentsetarray[15] [0] = "2PBAT2";
    studentsetarray[15] [1] = "2PBAT";
    studentsetarray[15] [2] = "%23SPLUSE639FA";
    studentsetarray[16] [0] = "2PBAT3";
    studentsetarray[16] [1] = "2PBAT";
    studentsetarray[16] [2] = "%23SPLUSE639FB";
    studentsetarray[17] [0] = "2PBAT4";
    studentsetarray[17] [1] = "2PBAT";
    studentsetarray[17] [2] = "%23SPLUSE639FC";
    studentsetarray[18] [0] = "3PBAT1";
    studentsetarray[18] [1] = "3PBAT";
    studentsetarray[18] [2] = "%23SPLUSE639FD";
    studentsetarray[19] [0] = "3PBAT2";
    studentsetarray[19] [1] = "3PBAT";
    studentsetarray[19] [2] = "%23SPLUSE639FE";
    studentsetarray[20] [0] = "3PBAT3";
    studentsetarray[20] [1] = "3PBAT";
    studentsetarray[20] [2] = "%23SPLUSE639FF";
    studentsetarray[21] [0] = "3PBEMA";
    studentsetarray[21] [1] = "3PBEMA";
    studentsetarray[21] [2] = "%23SPLUSE63A00";
    studentsetarray[22] [0] = "3PBEMK";
    studentsetarray[22] [1] = "3PBEMK";
    studentsetarray[22] [2] = "%23SPLUSE63A01";
    studentsetarray[23] [0] = "3PBEMO";
    studentsetarray[23] [1] = "3PBEMO";
    studentsetarray[23] [2] = "%23SPLUSE63A02";
    studentsetarray[24] [0] = "2PBEII";
    studentsetarray[24] [1] = "2PBEII";
    studentsetarray[24] [2] = "%23SPLUSE63A03";
    studentsetarray[25] [0] = "3PBEIE1";
    studentsetarray[25] [1] = "3PBEIE";
    studentsetarray[25] [2] = "%23SPLUSE63A04";
    studentsetarray[26] [0] = "3PBEIE2";
    studentsetarray[26] [1] = "3PBEIE";
    studentsetarray[26] [2] = "%23SPLUSE63A05";
    studentsetarray[27] [0] = "3PBEII1";
    studentsetarray[27] [1] = "3PBEII";
    studentsetarray[27] [2] = "%23SPLUSE63A06";
    studentsetarray[28] [0] = "3PBEII2";
    studentsetarray[28] [1] = "3PBEII";
    studentsetarray[28] [2] = "%23SPLUSE63A07";
    studentsetarray[29] [0] = "2PBMP";
    studentsetarray[29] [1] = "2PBMP";
    studentsetarray[29] [2] = "%23SPLUSE63A08";
    studentsetarray[30] [0] = "3PBMP";
    studentsetarray[30] [1] = "3PBMP";
    studentsetarray[30] [2] = "%23SPLUSE63A09";
    studentsetarray[31] [0] = "2PBEM1";
    studentsetarray[31] [1] = "2PBEM";
    studentsetarray[31] [2] = "%23SPLUSE63A0A";
    studentsetarray[32] [0] = "2PBEM2";
    studentsetarray[32] [1] = "2PBEM";
    studentsetarray[32] [2] = "%23SPLUSE63A0C";
    studentsetarray[33] [0] = "2PBEM3";
    studentsetarray[33] [1] = "2PBEM";
    studentsetarray[33] [2] = "%23SPLUSE63A0D";
    studentsetarray[34] [0] = "2PBEM4";
    studentsetarray[34] [1] = "2PBEM";
    studentsetarray[34] [2] = "%23SPLUSE63A0E";
    studentsetarray[35] [0] = "2PBEIE1";
    studentsetarray[35] [1] = "2PBEIE";
    studentsetarray[35] [2] = "%23SPLUSE63A0F";
    studentsetarray[36] [0] = "2PBEIE2";
    studentsetarray[36] [1] = "2PBEIE";
    studentsetarray[36] [2] = "%23SPLUSE63A11";
    studentsetarray[37] [0] = "2PBEIE3";
    studentsetarray[37] [1] = "2PBEIE";
    studentsetarray[37] [2] = "%23SPLUSE63A12";
    studentsetarray[38] [0] = "2PBEIE4";
    studentsetarray[38] [1] = "2PBEIE";
    studentsetarray[38] [2] = "%23SPLUSE63A13";
    studentsetarray[39] [0] = "1PBEM/MP1";
    studentsetarray[39] [1] = "1PBEM/MP";
    studentsetarray[39] [2] = "%23SPLUSE63A14";
    studentsetarray[40] [0] = "1PBEM/MP3";
    studentsetarray[40] [1] = "1PBEM/MP";
    studentsetarray[40] [2] = "%23SPLUSE63A16";
    studentsetarray[41] [0] = "1PBEM/MP4";
    studentsetarray[41] [1] = "1PBEM/MP";
    studentsetarray[41] [2] = "%23SPLUSE63A17";
    studentsetarray[42] [0] = "1PBEM/MP5";
    studentsetarray[42] [1] = "1PBEM/MP";
    studentsetarray[42] [2] = "%23SPLUSE63A18";
    studentsetarray[43] [0] = "1PBEM/MP2";
    studentsetarray[43] [1] = "1PBEM/MP";
    studentsetarray[43] [2] = "%23SPLUSE63A15";
    studentsetarray[44] [0] = "1PBEM/MP6";
    studentsetarray[44] [1] = "1PBEM/MP";
    studentsetarray[44] [2] = "%23SPLUSE63A19";
    studentsetarray[45] [0] = "1PBEM/MP7";
    studentsetarray[45] [1] = "1PBEM/MP";
    studentsetarray[45] [2] = "%23SPLUSE63A1A";
    studentsetarray.sort();
    var lbxObjects = Form.elements["identifier[]"];
    var cbxFilter = Form.elements["filter"];
    if (cbxFilter != null) {
        var strFilter = cbxFilter.options[cbxFilter.selectedIndex].value;
    }
    else {
        var strFilter = "(None)";
    }
    var j=0;
    lbxObjects.options.length = 0;
    if (strFilter == "(None)")
    {
        for (var i=0; i<studentsetarray.length; i++) {
            lbxObjects.options[j] = new Option(studentsetarray[i] [0], studentsetarray[i] [2]);
            j++;
        }
    }
    else
    {
        for (var i=0; i<studentsetarray.length; i++) {
            if (studentsetarray[i] [1] == strFilter) {
                lbxObjects.options[j] = new Option(studentsetarray[i] [0], studentsetarray[i] [2]);
                j++;
            }
        }
    }
}
function AddWeeksToHTML(form) {
    form.elements["weeks"].options.length=0;
    AddWeeks("","deze week",form.elements["weeks"]);
    AddWeeks("1-14","1° semester",form.elements["weeks"]);
    AddWeeks("22-36","2° semester",form.elements["weeks"]);
    AddWeeks("1", "week 1 - 18/09/06",form.elements["weeks"]);
    AddWeeks("2", "week 2 - 25/09/06",form.elements["weeks"]);
    AddWeeks("3", "week 3 - 02/10/06",form.elements["weeks"]);
    AddWeeks("4", "week 4 - 09/10/06",form.elements["weeks"]);
    AddWeeks("5", "week 5 - 16/10/06",form.elements["weeks"]);
    AddWeeks("6", "week 6 - 23/10/06",form.elements["weeks"]);
    AddWeeks("7", "week 7 - 30/10/06",form.elements["weeks"]);
    AddWeeks("8", "week 8 - 06/11/06",form.elements["weeks"]);
    AddWeeks("9", "week 9 - 13/11/06",form.elements["weeks"]);
    AddWeeks("10", "week 10 - 20/11/06",form.elements["weeks"]);
    AddWeeks("11", "week 11 - 27/11/06",form.elements["weeks"]);
    AddWeeks("12", "week 12 - 04/12/06",form.elements["weeks"]);
    AddWeeks("13", "week 13 - 11/12/06",form.elements["weeks"]);
    AddWeeks("14", "week 14 - 18/12/06",form.elements["weeks"]);
    AddWeeks("15", "week 15 - 25/12/06",form.elements["weeks"]);
    AddWeeks("16", "week 16 - 01/01/07",form.elements["weeks"]);
    AddWeeks("17", "week 17 - 08/01/07",form.elements["weeks"]);
    AddWeeks("18", "week 18 - 15/01/07",form.elements["weeks"]);
    AddWeeks("19", "week 19 - 22/01/07",form.elements["weeks"]);
    AddWeeks("20", "week 20 - 29/01/07",form.elements["weeks"]);
    AddWeeks("21", "week 21 - 05/02/07",form.elements["weeks"]);
    AddWeeks("22", "week 22 - 12/02/07",form.elements["weeks"]);
    AddWeeks("23", "week 23 - 19/02/07",form.elements["weeks"]);
    AddWeeks("24", "week 24 - 26/02/07",form.elements["weeks"]);
    AddWeeks("25", "week 25 - 05/03/07",form.elements["weeks"]);
    AddWeeks("26", "week 26 - 12/03/07",form.elements["weeks"]);
    AddWeeks("27", "week 27 - 19/03/07",form.elements["weeks"]);
    AddWeeks("28", "week 28 - 26/03/07",form.elements["weeks"]);
    AddWeeks("29", "week 29 - 02/04/07",form.elements["weeks"]);
    AddWeeks("30", "week 30 - 09/04/07",form.elements["weeks"]);
    AddWeeks("31", "week 31 - 16/04/07",form.elements["weeks"]);
    AddWeeks("32", "week 32 - 23/04/07",form.elements["weeks"]);
    AddWeeks("33", "week 33 - 30/04/07",form.elements["weeks"]);
    AddWeeks("34", "week 34 - 07/05/07",form.elements["weeks"]);
    AddWeeks("35", "week 35 - 14/05/07",form.elements["weeks"]);
    AddWeeks("36", "week 36 - 21/05/07",form.elements["weeks"]);
    AddWeeks("37", "week 37 - 28/05/07",form.elements["weeks"]);
    AddWeeks("38", "week 38 - 04/06/07",form.elements["weeks"]);
    AddWeeks("39", "week 39 - 11/06/07",form.elements["weeks"]);
    AddWeeks("40", "week 40 - 18/06/07",form.elements["weeks"]);
    AddWeeks("41", "week 41 - 25/06/07",form.elements["weeks"]);
    AddWeeks("42", "week 42 - 02/07/07",form.elements["weeks"]);
    AddWeeks("43", "week 43 - 09/07/07",form.elements["weeks"]);
    AddWeeks("44", "week 44 - 16/07/07",form.elements["weeks"]);
    AddWeeks("45", "week 45 - 23/07/07",form.elements["weeks"]);
    AddWeeks("46", "week 46 - 30/07/07",form.elements["weeks"]);
    AddWeeks("47", "week 47 - 06/08/07",form.elements["weeks"]);
    AddWeeks("48", "week 48 - 13/08/07",form.elements["weeks"]);
    AddWeeks("49", "week 49 - 20/08/07",form.elements["weeks"]);
    AddWeeks("50", "week 50 - 27/08/07",form.elements["weeks"]);
    AddWeeks("51", "week 51 - 03/09/07",form.elements["weeks"]);
    AddWeeks("52", "week 52 - 10/09/07",form.elements["weeks"]);
}
