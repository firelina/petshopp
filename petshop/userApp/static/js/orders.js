$(document).ready(function () {
        var order = {};
        var tovars = [];
        var ajaxProperties = {
            url: '/orders',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(order),
            success: function(data){
                order = {};
            },
            complete: function(){
                findOrders("");
            }
        };

        findOrders("");
        function findOrders(filter){
            console.log(filter);
            $.ajax({
                url: '/orders/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'order_number' }, {name: 'created_date' },
                        {name: 'customer_id'}, {name: 'customer'}, {name: 'manager_id'}, {name: 'manager'}, {name: 'tovars'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#orderDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Номер заказа', dataField: 'order_number', width: 100},
                                { text: 'Дата создания заказа', dataField: 'created_date', width: 180},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Покупатель', dataField: 'customer', width: 120},
                                 {text: 'Менеджер', dataField: 'manager', width: 120},
                                 {text: 'Товары', dataField: 'tovars', width: 150},
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }

        function tableTovars(data){
        var source = {
                        dataType: "json",
                        dataFields: [{ name: 'tovar_id' }, { name: 'title' }, {name: 'amount' }],
                        localData: data
                    };
        var dataAdapter = new $.jqx.dataAdapter(source);
        $("#orderAddTovarDataTable").jqxDataTable(
        {
             source: dataAdapter,
             columns: [
             { text: 'Id товара', dataField: 'tovar_id', width: 100 },
             { text: 'Название товара', dataField: 'title', width: 100 },
             { text: 'Количество товара', dataField: 'amount', width: 100}],
                            theme: 'darkblue'
                        });
        }

        var customers = [];

        function findCustomers(filter){
            $.ajax({
                url: '/customers/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    customers = data;
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'fullname'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                   $("#orderJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "fullname", valueMember: 'id', source: dataAdapter});
                }
            });
        }
        var tovars = [];

        function findTovars(filter){
            $.ajax({
                url: '/tovars/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    providers = data;
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'title' }],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                   $("#orderAddTovarJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "title", valueMember: 'id', source: dataAdapter});
                }
            });
        }
        function findAmounts(id){
            $.ajax({
                url: '/orders/amounts',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(id),
                dataType: 'json',
                success: function(data){
                    tovars = data;
                    tableTovars(tovars);
                }
            });
        }

        $("#orderDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderAddTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderEditTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderDeleteTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderAddTovarOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#orderAddTovarCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#jqxMaskedInput").jqxMaskedInput({ width: '250px', height: '25px', mask: '######' });
        $("#jqxDateTimeInput").jqxDateTimeInput({ width: '250px', height: '25px' });
        $("#orderAddTovarJqxFormattedInput").jqxFormattedInput({ width: 250, height: 25, radix: "decimal", value: "100", spinButtons: true, dropDown: true })
        $("#orderSearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#orderDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            order['id'] = row['id'];
            order['order_number'] = row["order_number"];
            order['created_date'] = row["created_date"];
            order['customer_id'] = row["customer_id"];
            order['manager_id'] = row["manager_id"];
            order['tovars'] = row["tovars"];
        });
        $('#orderAddTovarDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            tovar['tovar_id'] = row["tovar_id"];
            tovar['title'] = row["title"];
            tovar['amount'] = row["amount"];
        });
        $("#orderSearch").on('change', function (event){
            var search = $('#orderSearch').val();
//            console.log(search);
            findOrders(search);
        });
//        $("#supplyNameInput").on('change', function (event){
//            customer['name'] = $('#customerNameInput').val();
//        });
//        $("#customerSurNameInput").on('change', function (event){
//            customer['surname'] = $('#customerSurNameInput').val();
//        });
//        $("#customerLastNameInput").on('change', function (event){
//            customer['lastname'] = $('#customerLastNameInput').val();
//        });
//        $('#jqxDateTimeInput').on('change', function (event) {
//        customer['birthday'] = $('#jqxDateTimeInput').jqxDateTimeInput('value');;
//        });
         $("#orderJqxWindow").jqxWindow({
            title: 'Добавить заказ',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $("#orderAddTovarJqxWindow").jqxWindow({
            title: 'Добавить товар в заказ',
            height:300,
            width: 300,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#orderSave').on('click', function() {
            order = {};
            tovar = {};
            findCustomers("");
            $('#orderJqxWindow').jqxWindow('open');
        });
        $('#orderAddTovar').on('click', function() {
            tovar = {};
            findTovars("");
            $('#orderAddTovarJqxWindow').jqxWindow('open');
        });
        $('#orderEditTovar').on('click', function() {
            if (tovar['tovar_id']){
                tovars.splice(tovars.indexOf(tovar), 1);
                findTovars("");
                $('#orderAddTovarJqxWindow').jqxWindow('open');
                $('#orderAddTovarJqxFormattedInput').val(tovar['amount']);

            }


        });
        $('#orderDeleteTovar').on('click', function() {
            if (tovar['tovar_id']){
                tovars.splice(tovars.indexOf(tovar), 1);
                console.log(tovars);
                tableTovars(tovars);
            }
        });
        $('#orderAddTovarOK').on('click', function() {
            tovars.push(tovar);
            tableTovars(tovars);
            $('#orderAddTovarJqxWindow').jqxWindow('close');
        });
         $("#orderAddTovarJqxlistbox").on('select', function (event){
            tovar['tovar_id'] = event.args.item.value;
            tovar['title'] = event.args.item.label;
        });
        $('#orderAddTovarJqxFormattedInput').on('change', function (event) {
            tovar['amount'] = $('#orderAddTovarJqxFormattedInput').val();
        });
        $('#jqxMaskedInput').on('change',
        function (event)
        {
            order['order_number'] = event.args.value;
        });
        $('#jqxDateTimeInput').on('change', function (event) {
        order['created_date'] = $('#jqxDateTimeInput').jqxDateTimeInput('value');;
        });
        $("#orderJqxlistbox").on('select', function (event){
            order['customer_id'] = event.args.item.value;
        });
        $('#orderEdit').on('click', function() {
            if(order["id"]){
            tovar = {};
            findCustomers('');
            $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(order['created_date'].split('-')));
            $('#jqxMaskedInput').jqxMaskedInput({value: order['order_number'] });
            findAmounts(order["id"]);

//                $('#customerNameInput').val(customer['name']);
//                $('#customerSurNameInput').val(customer['surname']);
//                $('#customerLastNameInput').val(customer['lastname']);
//                console.log(customer['birthday']);
//                $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(customer['birthday'].split('-')));

//                $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});

              $('#orderJqxWindow').jqxWindow('open');
//                $("#jqxFormattedInput").jqxFormattedInput("open");

            }
        });
        $('#orderCancel').on('click', function() {
//            $('#customerNameInput').val("");
//            $('#customerSurNameInput').val("");
//            $('#customerLastNameInput').val("");
//            $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});
            $('#orderJqxWindow').jqxWindow('close');
                        order = {};
        });
        $('#orderOK').on('click', function() {
            order['tovars'] = tovars
            if (!order["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            ajaxProperties['data'] = JSON.stringify(order);
            $.ajax(ajaxProperties);
            $('#orderJqxWindow').jqxWindow('close');
            order = {};
        });
        $('#orderDelete').on('click', function () {
            if(order['id']){
                ajaxProperties['method'] = 'delete';
                ajaxProperties['data'] = JSON.stringify(order);
                $.ajax(ajaxProperties);
            }
        });
    });