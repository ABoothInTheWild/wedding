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
        checkAdminLogin();
        return (false);
    });
});

function getTable() {
    payload = {}

    $.ajax({
        type: 'POST',
        url: "/getAllData/",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(data) {
            //Describe
            let data_rows = data.map(entry => [entry["id"], entry["name"], entry["email"], entry["phone"], entry["address1"], entry["address2"], entry["city"], entry["state"], entry["zip"], entry["last_updated"]]);
            //reinit datatable
            dt = $('#info').DataTable({
                data: data_rows,
                responsive: {
                    details: {
                        display: $.fn.dataTable.Responsive.display.modal({
                            header: function(row) {
                                var data = row.data();
                                return 'Description for Submitted Contact Information';
                            }
                        }),
                        renderer: $.fn.dataTable.Responsive.renderer.tableAll({
                            tableClass: 'table'
                        })
                    }
                },
                dom: "<'row'<'col-sm-12 col-md-6'B><'col-sm-12 col-md-6'fl>>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'row'<'col-sm-12 col-md-12'ip>>",
                order: [
                    [0, "desc"]
                ],
                pageLength: 10,
                lengthMenu: [10, 20, 50, 100],
                buttons: [
                    { extend: 'copyHtml5' },
                    { extend: 'csvHtml5' },
                    {
                        extend: 'pdfHtml5',
                        title: function() { return 'Description for Submitted Contact Information'; },
                        orientation: 'portrait',
                        pageSize: 'A3',
                        text: 'PDF',
                        titleAttr: 'PDF'
                    }
                ]
            });

            $('.dt-buttons button').each(function() {
                $(this).removeClass("btn-secondary");
                $(this).addClass("btn-primary");
            })
        }
    });
}

function checkAdminLogin() {
    var payload = {
        "login": $('#admin_user').val(),
        "password": $('#pwd').val()
    };

    $.ajax({
        type: 'POST',
        url: "/adminLoginAttempt/",
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ "data": payload }),
        success: function(data) {
            if (data["success"] === true) {
                $("#data-info").show();
                $("#admin-check").hide();

                getTable();
            } else {
                $('#admin_user').val("");
                $('#pwd').val("");
                $('#admin_user').text("");
                $('#pwd').text("");
                alert("Incorrect Credentials. Are you really an Admin?");
            }
        }
    });
}