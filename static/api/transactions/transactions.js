var protocol = window.location.protocol
///////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host +"/"

$(() => {
    transactions();
})

const transactions = () => {
    const csrftoken = document.querySelector('#global-auth-form [name=csrfmiddlewaretoken]').value;
    $("spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();
      
    $.ajax({
        "url": hostUrl + "api/en/daco/transactions/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
    }).done((response) => {
        $("#spinner-container").hide();
        // console.log(response);
        var allTransactions = [];
        for(let i=0; i < response.length; i++){
            var transaction = response[i];
            var dateFormat = new Date(transaction.txnDate)
            allTransactions.push({
                txnDate: dateFormat.toLocaleDateString("en-GB"),
                event: transaction.event.id,
                Folio: "F" + transaction.account.accountYear +"-"+ transaction.member.code + "-" + transaction.account.code,
                Amount: transaction.Amount.toLocaleString('en-GB', {
                    style: 'currency',
                    currency: 'UGX',
                    minimumFractionDigits: 2
                }),
                Actions: '<button type="button" onclick="transactionForm(' + transaction.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteTransaction(' + transaction.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            })
        }
        const dataSet = allTransactions.map(({txnDate, event, Folio, Amount, Actions}) => [txnDate, event, Folio, Amount, Actions]);
        $("#transaction-data-table").DataTable({
            data: dataSet,
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                {title: "Date"},
                {title: "Event"},
                {title: "Folio"},
                {title: "Amount", className: 'dt-right'},
                {title: "Action(s)", className: 'dt-center'}
            ]
        })
        .buttons()
        .container()
        .appendTo("#transaction-data-table_wrapper .col-md-6:eq(0)")
    });
}

const transactionForm = (transactionid = null) => {
    $("#modal-xl").modal('show');
    var auth_user_token = $("#auth-user-token").val()
    const csrftoken = document.querySelector("#transaction-form [name=csrfmiddlewaretoken]").value;
    if(transactionid != null){
        $("#spinner-container-ini-edit").show();
        $("#selected-transaction-id").val(transactionid);
        $(".modal-title").html("Edit Transation");
        $("#save-btn").html("Save Changes");
        $("#is-confirmed").html('<input class="custom-control-input" type="checkbox" id="is-disabled"><label for="is-disabled" class="custom-control-label">Disabled</label>');
        
        $.ajax({
            "url": hostUrl + "api/en/daco/transaction/" + transactionid,
            "method": "GET",
            "headers": {
            "Authorization": "Token " + auth_user_token
            },
        }).done((response) => {
            console.log(response);
        });
    }
    else{
        var transactionid = "null";
        $("#selected-transaction-id").val(transactionid);
        $("#modal-title").html("Register Transaction");
        $(".save-btn").html("Submit");
        // $("#save-btn").html("Submit");
        $("#is-confirmed").html('');

        /*// Event Dropdown
        $.ajax({
            "url": hostUrl + "api/en/daco/events/",
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
        }).done((response) => {
            console.log(response);
        });

        // Member Dropdown
        $.ajax({
            "url": hostUrl + "api/en/daco/members/",
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
        }).done((response) => {
            console.log(response);
        });

        // Account Dropdown
        $.ajax({
            "url": hostUrl + "api/en/daco/accounts/",
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
        }).done((response) => {
            console.log(response);
        });*/
    }
}

const saveData = (() => {
    var auth_user_id = $("#auth-user-id").val();
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector("#transaction-form [name=csrfmiddlewaretoken]").value;
    var transactionid = $("#selected-transaction-id").val();
    $("#spinner-container-init-edit").show();

    var data = JSON.stringify({
        "txnDate": $("#txnDate-id").val(),
        "event_id": $("#event-id-id").val(),
        "member_id": $("#member-id-id").val(),
        "account_id": $("#account-id-id").val(),
        "Amount": $("#amount-id").val()
    });

    if(transactionid != 'null'){

    }
    else{
        $.ajax({
            "url": hostUrl + "api/en/daco/register/transaction/",
            "method": "POST",
            "headers": {
                "Authorization": "Token " + auth_user_token,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
            "data": data,
          }).done((response) => {
            console.log(response);
            // if (response.status) {
            //     $("#form-alert").html('<div class="alert alert-success alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fas fa-check"></i> Success!</h5>' + response.message + '</div>');
            //     setTimeout(() => {
            //         $("#modal-xl").modal('hide');
            //     }, 2000);
            // } else {
            //     $("#form-alert").html('<div class="alert alert-danger alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><h5><i class="icon fa fa-times"></i> Error!</h5>' + response.message + '</div>');
            // }
            transactions();
        });
    }
})