// (C) Wolfgang Huber 2010-2011

// Script parameters - these are set up by R in the function 'writeReport' when copying the 
//   template for this script from arrayQualityMetrics/inst/scripts into the report.

var highlightInitial = [ false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false ];
var arrayMetadata    = [ [ "1", "GSM524151", "beta-cells_non-diabetic condition_donor1", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "67", "39.0", "non-diabetic control", "female" ], [ "2", "GSM524152", "beta-cells_non-diabetic condition_donor2", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "65", "34.0", "non-diabetic control", "female" ], [ "3", "GSM524153", "beta-cells_non-diabetic condition_donor3", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "62", "22.4", "non-diabetic control", "female" ], [ "4", "GSM524154", "beta-cells_non-diabetic condition_donor4", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "60", "31.0", "non-diabetic control", "male" ], [ "5", "GSM524155", "beta-cells_non-diabetic condition_donor5", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "59", "36.4", "non-diabetic control", "male" ], [ "6", "GSM524156", "beta-cells_non-diabetic condition_donor6", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "52", "26.0", "non-diabetic control", "male" ], [ "7", "GSM524157", "beta-cells_non-diabetic condition_donor7", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "54", "34.2", "non-diabetic control", "male" ], [ "8", "GSM524158", "beta-cells_non-diabetic condition_donor8", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "64", "27.1", "non-diabetic control", "female" ], [ "9", "GSM524159", "beta-cells_non-diabetic condition_donor9", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "57", "27.7", "non-diabetic control", "male" ], [ "10", "GSM524160", "beta-cells_non-diabetic condition_donor10", "CTL", "human beta-cells_non-diabetic", "disease: non-diabetic control", "63", "28.5", "non-diabetic control", "male" ], [ "11", "GSM524161", "beta-cells_diabetic condition_donor1", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "74", "26.0", "type 2 diabetes", "male" ], [ "12", "GSM524162", "beta-cells_diabetic condition_donor2", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "68", "29.4", "type 2 diabetes", "female" ], [ "13", "GSM524163", "beta-cells_diabetic condition_donor3", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "63", "29.4", "type 2 diabetes", "male" ], [ "14", "GSM524164", "beta-cells_diabetic condition_donor4", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "64", "NA", "type 2 diabetes", "male" ], [ "15", "GSM524165", "beta-cells_diabetic condition_donor5", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "74", "28.6", "type 2 diabetes", "female" ], [ "16", "GSM524166", "beta-cells_diabetic condition_donor6", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "69", "33.6", "type 2 diabetes", "male" ], [ "17", "GSM524167", "beta-cells_diabetic condition_donor7", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "61", "27.8", "type 2 diabetes", "male" ], [ "18", "GSM524168", "beta-cells_diabetic condition_donor8", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "79", "25.9", "type 2 diabetes", "male" ], [ "19", "GSM524169", "beta-cells_diabetic condition_donor9", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "56", "31.0", "type 2 diabetes", "male" ], [ "20", "GSM524170", "beta-cells_diabetic condition_donor10", "T2DM", "human beta-cells_diabetic", "disease: type 2 diabetes", "65", "46.0", "type 2 diabetes", "female" ] ];
var svgObjectNames   = [ "pca", "dens" ];

var cssText = ["stroke-width:1; stroke-opacity:0.4",
               "stroke-width:3; stroke-opacity:1" ];

// Global variables - these are set up below by 'reportinit'
var tables;             // array of all the associated ('tooltips') tables on the page
var checkboxes;         // the checkboxes
var ssrules;


function reportinit() 
{
 
    var a, i, status;

    /*--------find checkboxes and set them to start values------*/
    checkboxes = document.getElementsByName("ReportObjectCheckBoxes");
    if(checkboxes.length != highlightInitial.length)
	throw new Error("checkboxes.length=" + checkboxes.length + "  !=  "
                        + " highlightInitial.length="+ highlightInitial.length);
    
    /*--------find associated tables and cache their locations------*/
    tables = new Array(svgObjectNames.length);
    for(i=0; i<tables.length; i++) 
    {
        tables[i] = safeGetElementById("Tab:"+svgObjectNames[i]);
    }

    /*------- style sheet rules ---------*/
    var ss = document.styleSheets[0];
    ssrules = ss.cssRules ? ss.cssRules : ss.rules; 

    /*------- checkboxes[a] is (expected to be) of class HTMLInputElement ---*/
    for(a=0; a<checkboxes.length; a++)
    {
	checkboxes[a].checked = highlightInitial[a];
        status = checkboxes[a].checked; 
        setReportObj(a+1, status, false);
    }

}


function safeGetElementById(id)
{
    res = document.getElementById(id);
    if(res == null)
        throw new Error("Id '"+ id + "' not found.");
    return(res)
}

/*------------------------------------------------------------
   Highlighting of Report Objects 
 ---------------------------------------------------------------*/
function setReportObj(reportObjId, status, doTable)
{
    var i, j, plotObjIds, selector;

    if(doTable) {
	for(i=0; i<svgObjectNames.length; i++) {
	    showTipTable(i, reportObjId);
	} 
    }

    /* This works in Chrome 10, ssrules will be null; we use getElementsByClassName and loop over them */
    if(ssrules == null) {
	elements = document.getElementsByClassName("aqm" + reportObjId); 
	for(i=0; i<elements.length; i++) {
	    elements[i].style.cssText = cssText[0+status];
	}
    } else {
    /* This works in Firefox 4 */
    for(i=0; i<ssrules.length; i++) {
        if (ssrules[i].selectorText == (".aqm" + reportObjId)) {
		ssrules[i].style.cssText = cssText[0+status];
		break;
	    }
	}
    }

}

/*------------------------------------------------------------
   Display of the Metadata Table
  ------------------------------------------------------------*/
function showTipTable(tableIndex, reportObjId)
{
    var rows = tables[tableIndex].rows;
    var a = reportObjId - 1;

    if(rows.length != arrayMetadata[a].length)
	throw new Error("rows.length=" + rows.length+"  !=  arrayMetadata[array].length=" + arrayMetadata[a].length);

    for(i=0; i<rows.length; i++) 
 	rows[i].cells[1].innerHTML = arrayMetadata[a][i];
}

function hideTipTable(tableIndex)
{
    var rows = tables[tableIndex].rows;

    for(i=0; i<rows.length; i++) 
 	rows[i].cells[1].innerHTML = "";
}


/*------------------------------------------------------------
  From module 'name' (e.g. 'density'), find numeric index in the 
  'svgObjectNames' array.
  ------------------------------------------------------------*/
function getIndexFromName(name) 
{
    var i;
    for(i=0; i<svgObjectNames.length; i++)
        if(svgObjectNames[i] == name)
	    return i;

    throw new Error("Did not find '" + name + "'.");
}


/*------------------------------------------------------------
  SVG plot object callbacks
  ------------------------------------------------------------*/
function plotObjRespond(what, reportObjId, name)
{

    var a, i, status;

    switch(what) {
    case "show":
	i = getIndexFromName(name);
	showTipTable(i, reportObjId);
	break;
    case "hide":
	i = getIndexFromName(name);
	hideTipTable(i);
	break;
    case "click":
        a = reportObjId - 1;
	status = !checkboxes[a].checked;
	checkboxes[a].checked = status;
	setReportObj(reportObjId, status, true);
	break;
    default:
	throw new Error("Invalid 'what': "+what)
    }
}

/*------------------------------------------------------------
  checkboxes 'onchange' event
------------------------------------------------------------*/
function checkboxEvent(reportObjId)
{
    var a = reportObjId - 1;
    var status = checkboxes[a].checked;
    setReportObj(reportObjId, status, true);
}


/*------------------------------------------------------------
  toggle visibility
------------------------------------------------------------*/
function toggle(id){
  var head = safeGetElementById(id + "-h");
  var body = safeGetElementById(id + "-b");
  var hdtxt = head.innerHTML;
  var dsp;
  switch(body.style.display){
    case 'none':
      dsp = 'block';
      hdtxt = '-' + hdtxt.substr(1);
      break;
    case 'block':
      dsp = 'none';
      hdtxt = '+' + hdtxt.substr(1);
      break;
  }  
  body.style.display = dsp;
  head.innerHTML = hdtxt;
}
