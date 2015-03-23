<h3>Info for brokers</h3>
<table class="table table-striped">
    <thead>
        <tr>
            <th> Name</th>
            <th> Rating</th>
        </tr>
    </thead>
    <tbody>
        % for broker in brokers:
        <tr>
            <td>
                {{broker['name']}}
            </td>
            <td>
                {{broker['rating']}}
            </td>
        </tr>
        % end
    </tbody>
</table>