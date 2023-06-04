$(document).ready(function () {
        var supply = {};
        var tovars = [];
        var ajaxProperties = {
            url: '/supplies',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(supply),
            success: function(data){
                supply = {};
            },
            complete: function(){
                findSupplies("");
            }
        };

        findSupplies("");
        function findSupplies(filter){
            console.log(filter);
            $.ajax({
                url: '/supplies/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'supply_number' }, {name: 'created_date' }, {name: 'provider'},
                         {name: 'manager_id'}, {name: 'manager'}, {name: 'tovars'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#supplyDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Номер поставки', dataField: 'supply_number', width: 100},
                                { text: 'Дата создания поставки', dataField: 'created_date', width: 180},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Поставщик', dataField: 'provider', width: 120},
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
        $("#supplyAddTovarDataTable").jqxDataTable(
        {
             source: dataAdapter,
             columns: [
             { text: 'Id товара', dataField: 'tovar_id', width: 100 },
             { text: 'Название товара', dataField: 'title', width: 100 },
             { text: 'Количество товара', dataField: 'amount', width: 100}],
                            theme: 'darkblue'
                        });
        }

        var providers = [];

        function findProviders(filter){
            $.ajax({
                url: '/providers/search',
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
                   $("#supplyJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "title", valueMember: 'id', source: dataAdapter});
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
                   $("#supplyAddTovarJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "title", valueMember: 'id', source: dataAdapter});
                }
            });
        }
        function findAmounts(id){
            $.ajax({
                url: '/supplies/amounts',
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

        $("#supplyDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplySave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyAddTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyEditTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyDeleteTovar").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyAddTovarOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#supplyAddTovarCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#jqxMaskedInput").jqxMaskedInput({ width: '250px', height: '25px', mask: '######' });
        $("#jqxDateTimeInput").jqxDateTimeInput({ width: '250px', height: '25px' });
        $("#supplyAddTovarJqxFormattedInput").jqxFormattedInput({ width: 250, height: 25, radix: "decimal", value: "100", spinButtons: true, dropDown: true })
        $("#supplySearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#supplyDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            supply['id'] = row['id'];
            supply['supply_number'] = row["supply_number"];
            supply['created_date'] = row["created_date"];
            supply['provider_id'] = row["provider_id"];
            supply['manager_id'] = row["manager_id"];
            supply['tovars'] = row["tovars"];
        });
        $('#supplyAddTovarDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            tovar['tovar_id'] = row["tovar_id"];
            tovar['title'] = row["title"];
            tovar['amount'] = row["amount"];
        });
        $("#supplySearch").on('change', function (event){
            var search = $('#supplySearch').val();
//            console.log(search);
            findSupplies(search);
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
         $("#supplyJqxWindow").jqxWindow({
            title: 'Добавить поставку',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $("#supplyAddTovarJqxWindow").jqxWindow({
            title: 'Добавить товар в поставку',
            height:300,
            width: 300,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#supplySave').on('click', function() {
            supply = {};
            findProviders("");
            $('#supplyJqxWindow').jqxWindow('open');
        });
        $('#supplyAddTovar').on('click', function() {
            tovar = {};
            findTovars("");
            $('#supplyAddTovarJqxWindow').jqxWindow('open');
        });
        $('#supplyEditTovar').on('click', function() {
            if (tovar['tovar_id']){
                tovars.splice(tovars.indexOf(tovar), 1);
                findTovars("");
                $('#supplyAddTovarJqxWindow').jqxWindow('open');
                $('#supplyAddTovarJqxFormattedInput').val(tovar['amount']);

            }


        });
        $('#supplyDeleteTovar').on('click', function() {
            if (tovar['tovar_id']){
                tovars.splice(tovars.indexOf(tovar), 1);
                console.log(tovars);
                tableTovars(tovars);
            }
        });
        $('#supplyAddTovarOK').on('click', function() {
            tovars.push(tovar);
            tableTovars(tovars);
            $('#supplyAddTovarJqxWindow').jqxWindow('close');
        });
         $("#supplyAddTovarJqxlistbox").on('select', function (event){
            tovar['tovar_id'] = event.args.item.value;
            tovar['title'] = event.args.item.label;
        });
        $('#supplyAddTovarJqxFormattedInput').on('change', function (event) {
            tovar['amount'] = $('#supplyAddTovarJqxFormattedInput').val();
        });
        $('#jqxMaskedInput').on('change',
        function (event)
        {
            supply['supply_number'] = event.args.value;
        });
        $('#jqxDateTimeInput').on('change', function (event) {
        supply['created_date'] = $('#jqxDateTimeInput').jqxDateTimeInput('value');;
        });
        $("#supplyJqxlistbox").on('select', function (event){
            supply['provider_id'] = event.args.item.value;
        });
        $('#supplyEdit').on('click', function() {
            if(supply["id"]){
            findProviders('');
            $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(supply['created_date'].split('-')));
            $('#jqxMaskedInput').jqxMaskedInput({value: supply['supply_number'] });
            findAmounts(supply["id"]);

//                $('#customerNameInput').val(customer['name']);
//                $('#customerSurNameInput').val(customer['surname']);
//                $('#customerLastNameInput').val(customer['lastname']);
//                console.log(customer['birthday']);
//                $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(customer['birthday'].split('-')));

//                $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});

              $('#supplyJqxWindow').jqxWindow('open');
//                $("#jqxFormattedInput").jqxFormattedInput("open");

            }
        });
        $('#supplyCancel').on('click', function() {
//            $('#customerNameInput').val("");
//            $('#customerSurNameInput').val("");
//            $('#customerLastNameInput').val("");
//            $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});
            $('#supplyJqxWindow').jqxWindow('close');
                        supply = {};
        });
        $('#supplyOK').on('click', function() {
            supply['tovars'] = tovars
            if (!supply["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            ajaxProperties['data'] = JSON.stringify(supply);
            $.ajax(ajaxProperties);
            $('#supplyJqxWindow').jqxWindow('close');
            supply = {};
        });
        $('#supplyDelete').on('click', function () {
            if(supply['id']){
                ajaxProperties['method'] = 'delete';
                ajaxProperties['data'] = JSON.stringify(supply);
                $.ajax(ajaxProperties);
            }
        });
    });