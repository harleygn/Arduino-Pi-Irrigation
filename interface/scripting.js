function getDate(difference) {
    let date = new Date();
    date.setDate(date.getDate() - difference);
    let dd = date.getDate();
    let mm = date.getMonth() + 1; //January is 0!
    let yyyy = date.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }

    return dd + '-' + mm + '-' + yyyy;
}

function getChartName(difference) {
    return './charts/' + getDate(difference) + '_chart.html'
}


$(document).ready(function () {
    $.ajax({
        url: "../schedules/schedule_template.json",
        dataType: 'json',
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

window.onload = function () {
    document.getElementById("today").innerHTML = getDate(0);
    document.getElementById("today").href = getChartName(0);
    document.getElementById("1-day-prev").innerHTML = getDate(1);
    document.getElementById("1-day-prev").href = getChartName(1);
    document.getElementById("2-day-prev").innerHTML = getDate(2);
    document.getElementById("2-day-prev").href = getChartName(2);
    document.getElementById("3-day-prev").innerHTML = getDate(3);
    document.getElementById("3-day-prev").href = getChartName(3);
    document.getElementById("4-day-prev").innerHTML = getDate(4);
    document.getElementById("4-day-prev").href = getChartName(4);
    document.getElementById("5-day-prev").innerHTML = getDate(5);
    document.getElementById("5-day-prev").href = getChartName(5);
    document.getElementById("6-day-prev").innerHTML = getDate(6);
    document.getElementById("6-day-prev").href = getChartName(6);
    document.getElementById("chart-frame").src = getChartName(0);
};
