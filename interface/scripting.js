// Gets the current date in the format DD-MM-YY applies the offset specified by 'difference'
function getDate(difference) {
    // Creates a new data object
    let date = new Date();
    // Applies the offset to the data object
    date.setDate(date.getDate() - difference);
    // Gets the day value
    let dd = date.getDate();
    // Gets the month value (January is 0)
    let mm = date.getMonth() + 1;
    // Gets the year value
    let yyyy = date.getFullYear();
    // Adds a leading zero to the day if necessary
    if (dd < 10) {
        dd = '0' + dd;
    }
    // Adds a leading zero to the month if necessary
    if (mm < 10) {
        mm = '0' + mm;
    }

    // Returns the date as a string in the format 'DD-MM-YYYY'
    return dd + '-' + mm + '-' + yyyy;
}

// Builds the path of a chart using the date stamp
function getChartName(difference) {
    return './charts/' + getDate(difference) + '_chart.html'
}

function getScheduleName(){
    return './schedules/' + getDate(0) + '_schedule.json'
}

// Loads the schedule data using a local AJAX HTTP request
$(document).ready(function () {
    $.ajax({
        // Location of the schedule (local)
        url: getScheduleName(),
        // Data returned in JSON format
        dataType: 'json',
        // Upon making a successful call the table cells are filled with the relevant data
        success: function (data) {
            document.getElementById("morn-start").innerHTML = (data['schedule'][0]['start']);
            document.getElementById("morn-end").innerHTML = (data['schedule'][0]['end']);
            document.getElementById("aft-start").innerHTML = (data['schedule'][1]['start']);
            document.getElementById("aft-end").innerHTML = (data['schedule'][1]['end']);
            document.getElementById("morn-dur").innerHTML = (data['schedule'][0]['duration']);
            document.getElementById("aft-dur").innerHTML = (data['schedule'][1]['duration']);
        },
    });
});

// When the pages loads:
window.onload = function () {
    // Loads the date for the historical data links
    document.getElementById("today").innerHTML = getDate(0);
    document.getElementById("1-day-prev").innerHTML = getDate(1);
    document.getElementById("2-day-prev").innerHTML = getDate(2);
    document.getElementById("3-day-prev").innerHTML = getDate(3);
    document.getElementById("4-day-prev").innerHTML = getDate(4);
    document.getElementById("5-day-prev").innerHTML = getDate(5);
    document.getElementById("6-day-prev").innerHTML = getDate(6);
    // Sets the href value of each link to the relevant address
    document.getElementById("today").href = getChartName(0);
    document.getElementById("1-day-prev").href = getChartName(1);
    document.getElementById("2-day-prev").href = getChartName(2);
    document.getElementById("3-day-prev").href = getChartName(3);
    document.getElementById("4-day-prev").href = getChartName(4);
    document.getElementById("5-day-prev").href = getChartName(5);
    document.getElementById("6-day-prev").href = getChartName(6);
    // Set the src value for the iframe to the address of the current chart
    document.getElementById("chart-frame").src = getChartName(0);
};
