function getDate() {
    let today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1; //January is 0!

    let yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }

    return dd + '-' + mm + '-' + yyyy;
}

function getGraphName() {
    return '../graphs/' + getDate() + '_graph.html'
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
    document.getElementById("today").innerHTML = getDate();
    document.getElementById("graph-frame").src = getGraphName();
};
