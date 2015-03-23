var timerForDataRequest = null;

function showClient(id) {
    $('#mainContext').load('static/client_full.html', function (){
        loadClient(id);
    })

};

function loadClient(id_client){
    var client_data = {
        id: id_client
    };

    timerForDataRequest = setInterval(getClient, 30000);

    getClient();

    function getClient(){
        $.getJSON("ajax/get_client", client_data, function (data){
            var actives = "<b>name</b>: " + data.name + "<br><b>balance</b>: " + data.balance;
            actives += "<ul>";
            $.each(data.actives, function (){
                actives += "<li>code: " + this.details.name + " quantity: " + this.quantity;
            });
            actives += "</ul>";
            $('#client_all').html(actives);
        })
    }
};



