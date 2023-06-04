$(document).ready(function () {
        var customer = {};
        var ajaxProperties = {
            url: '/customers',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(customer),
            success: function(data){
                customer = {};
            },
            complete: function(){
                findCustomers("");
            }
        };

        findCustomers("");
        function findCustomers(filter){
            console.log(filter);
            $.ajax({
                url: '/customers/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'name' }, {name: 'surname' }, {name: 'lastname'},
                         {name: 'discount'},  {name: 'birthday'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#customerDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Имя', dataField: 'name', width: 100},
                                { text: 'Фамилия', dataField: 'surname', width: 100},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Отчество', dataField: 'lastname', width: 120},
                                 {text: 'Скидка', dataField: 'discount', width: 120},
                                 {text: 'Дата рождения', dataField: 'birthday', width: 120},
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }

        $("#customerDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#customerSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#customerEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#customerOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#customerCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#jqxDateTimeInput").jqxDateTimeInput({ width: '250px', height: '25px' });
        $("#customerNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Имя"});
        $("#customerSurNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Фамилия"});
        $("#customerLastNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Отчество"});
        $("#customerSearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#customerDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            customer['id'] = row['id'];
            customer['name'] = row["name"];
            customer['surname'] = row["surname"];
            customer['lastname'] = row["lastname"];
            customer['discount'] = row["discount"];
            customer['birthday'] = row["birthday"];
            console.log(customer['birthday']);
        });
        $("#customerSearch").on('change', function (event){
            var search = $('#customerSearch').val();
//            console.log(search);
            findCustomers(search);
        });
        $("#customerNameInput").on('change', function (event){
            customer['name'] = $('#customerNameInput').val();
        });
        $("#customerSurNameInput").on('change', function (event){
            customer['surname'] = $('#customerSurNameInput').val();
        });
        $("#customerLastNameInput").on('change', function (event){
            customer['lastname'] = $('#customerLastNameInput').val();
        });
        $('#jqxDateTimeInput').on('change', function (event) {
        customer['birthday'] = $('#jqxDateTimeInput').jqxDateTimeInput('value');;
        });
         $("#customerJqxWindow").jqxWindow({
            title: 'Добавить покупателя',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#customerSave').on('click', function() {
            customer = {};
            $('#customerJqxWindow').jqxWindow('open');
            $('#customerNameInput').val("");
            $('#customerSurNameInput').val("");
            $('#customerLastNameInput').val("");
        });
        $('#customerEdit').on('click', function() {
            if(customer["id"]){
                $('#customerNameInput').val(customer['name']);
                $('#customerSurNameInput').val(customer['surname']);
                $('#customerLastNameInput').val(customer['lastname']);
                console.log(customer['birthday']);
                $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(customer['birthday'].split('-')));

//                $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});

                $('#customerJqxWindow').jqxWindow('open');
//                $("#jqxFormattedInput").jqxFormattedInput("open");

            }
        });
        $('#customerCancel').on('click', function() {
            $('#customerNameInput').val("");
            $('#customerSurNameInput').val("");
            $('#customerLastNameInput').val("");
            $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});
            $('#customerJqxWindow').jqxWindow('close');
                        customer = {};
        });
        $('#customerOK').on('click', function() {
            if (!customer["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            console.log(customer);
            ajaxProperties['data'] = JSON.stringify(customer);
            $.ajax(ajaxProperties);
            $('#customerJqxWindow').jqxWindow('close');
        });
        $('#customerDelete').on('click', function () {
            if(customer['id']){
                ajaxProperties['method'] = 'delete';
                console.log(customer);
                ajaxProperties['data'] = JSON.stringify(customer);
                $.ajax(ajaxProperties);
            }
        });
    });