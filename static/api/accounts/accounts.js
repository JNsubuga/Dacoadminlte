var protocol = window.location.protocol
/////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host +"/"

$(() => {
    accounts();
})

const accounts = () => {
    const csrftoken = document.querySelector('#global-auth-form [name=csrfmiddlewaretoken]').value;
    $("#spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();
    // var auth_user_id = $("#auth-user-id").val();
    // console.log(auth_user_id);
    // console.log(auth_user_token);

    var settings = {
        "url": hostUrl + "api/en/daco/accounts/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
        onerror: (error) => {
            $("#spinner-container").hide();
            console.log(error.responseText)
        }
    };
      
    $.ajax(settings).done((response) => {
        $("#spinner-container").hide();
        // console.log(response);
        var allAccounts = [];
        for (let i=0; i < response.length; i++){
            var account = response[i];
            // console.log(account)
            let anualPrinciple = account.anualPrinciple.toLocaleString({
                style: 'currency',
                currency: 'JPY',
                currencyDisplay: 'UGX',
                useGrouping: true        
            })
            allAccounts.push({
                Name: account.name,
                Year: account.accountYear,
                Code: account.code,
                anualPrinciple: anualPrinciple,
                // "created_by": account.created_by,
                // "created": account.created,
                Actions: '<button type="button" onclick="accountForm(' + account.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteAccount(' + account.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            })
        }
        // console.log(allAccounts)
        const dataSet = allAccounts.map(({Name, Year, Code, anualPrinciple, Actions}) => [Name, Year, Code, anualPrinciple, Actions])
        $("#account-data-table").DataTable({
            data: dataSet,
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                {title: "Account Name"},
                {title: "Account Code"},
                {title: "Account Year"},
                {title: "Annual Principle", className: 'dt-right'},
                {title: "Action(s)", className: 'dt-center'},
            ]
        })
        .buttons()
        .container()
        .appendTo("#account-data-table_wrapper .col-md-6:eq(0)")
    });
}

// Display Data Form
const accountForm = (accountid = null) => {
    $("#modal-xl").modal('show');
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector("#account-form [name=csrfmiddlewaretoken]").value;
    if(accountid != null){
        $("#spinner-container-init-edit").show();
        $("#selected-account-id").val(accountid);
        $(".modal-title").html("Edit Account");
        $("#save-btn").html("Save Changes");
        // $(".save-btn").html("Save Changes");
        $("#is-disabod").html('<input class="custom-control-input" type="checkbox" id="is-disabled"><label for="is-disabled" class="custom-control-label">Disabled</label>');
        ///////////////////
        $.ajax({"url": hostUrl+"api/en/daco/account/"+accountid,
            "method": "GET",
            "headers": {
              "Authorization": "Token "+auth_user_token
            },
            onerror:(error) =>{
                $("#spinner-container-init-edit").hide();
                console.log(error.responseText);
            }
        }).done(function (response) {
            console.log(response);
            $("#account-id").val(response.id);
            $("#account-name-id").val(response.name)
            $("#account-code-id").val(response.code)
            $("#account-year-id").val(response.accountYear)
            $("#annual-principle-id").val(response.anualPrinciple)
            // $("#").val()
        });
    }
    else{
        var accountid = "null";
        $("#selected-account-id").val(accountid);
        $("#modal-title").html("Register Account");
        $("#save-btn").html("Submit");
        $("#is-disabod").html('')
    }
}

// Save Form Data
const saveData = () => {
    var auth_user_id = $("#auth-user-id").val();
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector("#account-form [name=csrfmiddlewaretoken]").value;
    var accountid = $("#selected-account-id").val();
    $("#spinner-container-init-edit").show();

    var data = JSON.stringify({
        "name": $("#account-name-id").val(),
        "code": $("#account-code-id").val(),
        "accountYear": $("#account-year-id").val(),
        "anualPrinciple": $("#annual-principle-id").val(),
        // "created_by_id": auth_user_id
    });
    // console.log(data)

    if(accountid != 'null'){

    }
    else{
        $.ajax({
            "url": hostUrl +"api/en/daco/create/account/",
            "method": "POST",
            "headers": {
                "Authorization": "Token " +auth_user_token,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
           "data": data,
        }).done((response) => {
            // console.log(response);
            if (response.status) {
                $("#form-alert").html('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fas fa-check"></i> Success!</h5>' + response.message + '</div>');
                setTimeout(() => {
                  $("#modal-xl").modal('hide');
                }, 2000);
              } else {
                $("#form-alert").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
              }
              accounts();
        });
    }
      
}