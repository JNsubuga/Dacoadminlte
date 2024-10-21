var protocol = window.location.protocol;
//////////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host + "/";

$(() => {
    //
    $("#daco-login-form").submit(function (e) {
        e.preventDefault();
        loginUser();
    });
    $("#daco-login-form").on("keyup", function () {
        // console.log("Hello");
        $("#form-error").html("");
        $("#daco-input-email").removeClass("is-invalid");
        $("#daco-input-password").removeClass("is-invalid");
    })

    $("#form-error").show();
})

const loginUser = () => {
    const csrftoken = document.querySelector('#daco-login-form [name=csrfmiddlewaretoken]').value;
    var email = $("#daco-input-email").val();
    var password = $("#daco-input-password").val();
    $("#daco-btn-login").html("logging in...");
    $("#spinner-container").show();
    $("#form-error").hide();
    
    var settings = {
        "url": hostUrl + "api/en/auth/login/",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        'mode': 'same-origin',
        "data": JSON.stringify({
            "username": email,
            "password": password
        }),
    };

    $.ajax(settings).done((response) => {
        $("#spinner-container").hide();
        $("#form-error").show();
        // console.log(response);
        if (response.success) {
            $("#daco-btn-login").html("Sign In");

            $("#form-error").html("Login success, redirecting please wait...");
            $("#form-error").removeClass("text-danger");
            $("#form-error").addClass("text-success");

            $("#daco-input-email").removeClass("is-invalid");
            $("#daco-input-password").removeClass("is-invalid");
            ////
            $("#daco-login-form").unbind('submit');
            $("#daco-login-form").submit();
            $(':input[type="submit"]').prop('disabled', true);
        } else {
            $("#form-error").html(response.message);
            $("#form-error").addClass("text-danger");
            $("#form-error").removeClass("text-success");
            $("#form-error").html(response.message);
            $("#daco-input-email").addClass("is-invalid");
            $("#daco-input-password").addClass("is-invalid");
            $("#daco-btn-login").html("Sign In");
            $(':input[type="submit"]').prop('disabled', false);

        }
    });
}