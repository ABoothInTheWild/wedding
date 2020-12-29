//global
var loggedIn = false;
if (window.name) {
    loggedIn = JSON.parse(window.name).loggedIn;
}

//login
if (!loggedIn) {
    window.location.replace("/login");
}

$(document).ready(function() {
    $('form').submit(function() {
        // show/hide
        $("#mainButton").hide();
        $("#hiddenButton").show();


        let formInfo = [];
        // Validate here
        $('.form-control').each(function(indx, x) {
            formInfo.push(x.value);
        });

        // payload for submission
        let payload = { "formInfo": formInfo };

        $.ajax({
            type: 'POST',
            url: "/saveFormData/",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ "data": payload }),
            success: function(data) {
                //do something
                $('.form-control').each(function(indx, x) {
                    x.value = "";
                });

                $("#mainForm").hide();
                $("#submitSuccess").show();
            }
        });

        return (false);
    });
});