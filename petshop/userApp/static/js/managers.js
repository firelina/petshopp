$(document).ready(function () {
        var manager = {};
        var ajaxProperties = {
            url: '/managers',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(manager),
            success: function(data){
                manager = {};
            },
            complete: function(){
                findManagers("");
            }
        };

        findManagers("");
        function findManagers(filter){
            console.log(filter);
            $.ajax({
                url: '/manager/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'name' }, {name: 'surname' }, {name: 'lastname'},
                         {name: 'telethon'},  {name: 'birthday'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#managerDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Имя', dataField: 'name', width: 100},
                                { text: 'Фамилия', dataField: 'surname', width: 100},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Отчество', dataField: 'lastname', width: 120},
                                 {text: 'Телефон', dataField: 'telethon', width: 120},
                                 {text: 'Дата рождения', dataField: 'birthday', width: 120},
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }

        $("#managerDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#managerSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#managerEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#managerOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#managerCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#jqxDateTimeInput").jqxDateTimeInput({ width: '250px', height: '25px' });
        $("#managerNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Имя"});
        $("#managerSurNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Фамилия"});
        $("#managerLastNameInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Отчество"});
        $("#jqxMaskedInput").jqxMaskedInput({ width: '250px', height: '25px', mask: '#(###)###-##-##' });
        $("#managerSearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#managerDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            manager['id'] = row['id'];
            manager['name'] = row["name"];
            manager['surname'] = row["surname"];
            manager['lastname'] = row["lastname"];
            manager['telethon'] = row["telethon"];
            manager['birthday'] = row["birthday"];
            console.log(manager['birthday']);
        });
        $("#managerSearch").on('change', function (event){
            var search = $('#managerSearch').val();
//            console.log(search);
            findManagers(search);
        });
        $('#jqxMaskedInput').on('change',
        function (event)
        {
            manager['telethon'] = event.args.value;
            var text = event.args.text;
            // type
            var type = event.args.type; // keyboard or null depending on how the value was changed.
        });
        $("#managerNameInput").on('change', function (event){
            manager['name'] = $('#managerNameInput').val();
        });
        $("#managerSurNameInput").on('change', function (event){
            manager['surname'] = $('#managerSurNameInput').val();
        });
        $("#managerLastNameInput").on('change', function (event){
            manager['lastname'] = $('#managerLastNameInput').val();
        });
        $('#jqxDateTimeInput').on('change', function (event) {
        manager['birthday'] = $('#jqxDateTimeInput').jqxDateTimeInput('value');;
        });
         $("#managerJqxWindow").jqxWindow({
            title: 'Добавить продавца',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#managerSave').on('click', function() {
            manager = {};
            $('#managerJqxWindow').jqxWindow('open');
            $('#managerNameInput').val("");
            $('#managerSurNameInput').val("");
            $('#managerLastNameInput').val("");
            $('#jqxMaskedInput').jqxMaskedInput({value: None });
            $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', None);
        });
        $('#managerEdit').on('click', function() {
            if(manager["id"]){
                $('#managerNameInput').val(manager['name']);
                $('#managerSurNameInput').val(manager['surname']);
                $('#managerLastNameInput').val(manager['lastname']);
                console.log(manager['birthday']);
                $('#jqxDateTimeInput ').jqxDateTimeInput('setDate', new Date(manager['birthday'].split('-')));
                $('#jqxMaskedInput').jqxMaskedInput({value: manager['telethon'] });

//                $('#jqxDateTimeInput').jqxDateTimeInput({ value: customer['birthday']});

                $('#managerJqxWindow').jqxWindow('open');
//                $("#jqxFormattedInput").jqxFormattedInput("open");

            }
        });
        $('#managerCancel').on('click', function() {
            $('#managerNameInput').val("");
            $('#managerSurNameInput').val("");
            $('#managerLastNameInput').val("");
            $('#jqxDateTimeInput').jqxDateTimeInput({ value: manager['birthday']});
            $('#managerJqxWindow').jqxWindow('close');
                        manager = {};
        });
        $('#managerOK').on('click', function() {
            if (!manager["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            console.log(manager);
            ajaxProperties['data'] = JSON.stringify(manager);
            $.ajax(ajaxProperties);
            $('#managerJqxWindow').jqxWindow('close');
        });
        $('#managerDelete').on('click', function () {
            if(manager['id']){
                ajaxProperties['method'] = 'delete';
                console.log(manager);
                ajaxProperties['data'] = JSON.stringify(manager);
                $.ajax(ajaxProperties);
            }
        });
    });