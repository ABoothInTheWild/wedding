$(document).ready(function() {
    window.name = JSON.stringify({
        loggedIn: false
    });

    //password toggle
    $('#showPassword').change(function() {
        var x = document.getElementById("password");
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    });

    $("#loginForm").submit(function(e) {
        e.preventDefault();
        checkLogin();
    });
});

function checkLogin() {
    var payload = {
        "password": $('#password').val()
    };

    $.ajax({
        type: 'POST',
        url: "/loginAttempt/",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(data) {
            // window.name = JSON.stringify({
            //     loggedIn: true
            // });
            // window.location.replace("/");
            if (data["success"] === true) {
                window.name = JSON.stringify({
                    loggedIn: true
                });
                window.location.replace("/");
            } else {
                $('#password').val("");
                $('#password').text("");
                alert("Incorrect Credentials");
            }
        }
    });
}