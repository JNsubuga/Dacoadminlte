var protocol = window.location.protocol
//////////////////////////////////////////////////////////
var hostUrl = protocol + "//" + window.location.host +"/"

$(() => {
    members();
})

const members = () => {
    const csrftoken = document.querySelector('#global-auth-form [name=csrfmiddlewaretoken]').value;
    $("spinner-container").show();
    var auth_user_token = $("#auth-user-token").val();
    
    $.ajax({
        "url": hostUrl +"api/en/daco/members/",
        "method": "GET",
        "headers": {
            "Authorization": "Token " + auth_user_token
        },
        onerror:(error) => {
            $("#spinner-container").hide();
            console.log(error.responseText)
        }
    })
    .done((response) => {
        $("#spinner-container").hide();
        // console.log(response);
        var allMembers = [];
        for(let i=0; i< response.length; i++){
            var member = response[i];
            allMembers.push({
                names: member.names,
                code: member.code,
                phone_contact: member.phone_contact,
                Actions: '<button type="button" onclick="memberForm(' + member.id + ')" class="btn btn-default btn-sm"><i class="fa fa-edit"></i> Edit</button> <button type="button" onclick="deleteMember(' + member.id + ')" type="button" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> Delete</button>'
            }) 
        }
        const dataSet = allMembers.map(({names, code, phone_contact, Actions}) => [names, code, phone_contact, Actions]);
        $("#member-data-table").DataTable({
            data: dataSet,
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            bDestroy: true,
            buttons: ["copy", "csv", "excel", "pdf", "print", "colvis"],
            columns: [
                {title: "Member Names"},
                {title: "Member Code"},
                {title: "Member Contact"},
                {title: "Action(s)", className: 'dt-center'},
            ]
        })
        .buttons()
        .container()
        .appendTo("#member-data-tablewrapper .col-md-6:eq(0)")
    });
}

// Display Data Form
const memberForm = (memberid = null) => {
    $("#modal-xl").modal('show');
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector("#member-form [name=csrfmiddlewaretoken").value;
    if(memberid != null){
        $("#spinner-container-init-edit").show();
        $("#selected-account-id").val(memberid);
        $(".modal-title").html("Edit Account");
        $("#save-btn").html("Save Changes");
        $("#is-active").html('<input class="custom-control-input" type="checkbox" id="is-active"><label for="is-disabled" class="custom-control-label">Disabled</label>');
        /////////////////
        $.ajax({
            "url": hostUrl + "api/en/daco/member/"+ memberid,
            "method": "GET",
            "headers": {
                "Authorization": "Token " + auth_user_token
            },
            onerror:(error) =>{
                $("#spinner-container-init-edit").hide();
                console.log(error.responseText);
            }
        }).done((response) => {
            // console.log(response);
            $("#member-id").val(response.id);
            $("#member-names-id").val(response.names);
            $("#member-code-id").val(response.code);
            $("#member-phone-contact-id").val(response.phone_contact);
        });
    }
    else{
        var memberid = "null";
        $("#selected-member-id").val(memberid);
        $(".modal-title").html("Register Member");
        $("#save-btn").html("Submit");
        $("#is-active").html('')
    }

}

// Save Form Data
const saveData = () => {
    var auth_user_id = $("#auth-user-id").val();
    var auth_user_token = $("#auth-user-token").val();
    const csrftoken = document.querySelector("#member-form [name=csrfmiddlewaretoken]").value;
    var memberid = $("#selected-member-id").val();
    $("#spinner-container-init-edit").show();

    var data = JSON.stringify({
        "names": $("#member-names-id").val(),
        "code": $("#member-code-id").val(),
        "phone_contact": $("#member-phone-contact-id").val(),
        // "created_by_id": 
    });
    
    
    if(memberid != 'null'){
        // console.log(data);
    }
    else{
        // console.log(data);
        $.ajax({
            "url": hostUrl +"api/en/daco/register/member/",
            "method": "POST",
            "headers": {
                "Authorization": "Token "+ auth_user_token,
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
            "data": data
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
            members();
        });
    }
}