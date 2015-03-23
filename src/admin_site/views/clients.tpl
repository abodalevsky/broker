<h3>Details</h3>
<table class="table table-striped">
    <thead>
        <tr>
            <th> Broker</th>
            <th> Name</th>
            <th> Balance</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
        % for client in clients:
        <tr>
            <td>
                {{client['broker']}}
            </td>
            <td>
                {{client['name']}}
            </td>
            <td>
                {{client['balance']}}
            </td>
            <td>
                 <button onclick="showClient({{client['idclient']}});" class="btn btn-primary">
                    <span class="glyphicon glyphicon-briefcase"></span> More...
                 </button>
            </td>
        </tr>
        % end
    </tbody>
</table>


