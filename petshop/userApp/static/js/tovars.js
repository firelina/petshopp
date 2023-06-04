$(document).ready(function () {
        var tovar = {};
        var ajaxProperties = {
            url: '/tovars',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(tovar),
            success: function(data){
                tovar = {};
            },
            complete: function(){
                findTovars("");
            }
        };

        findTovars("");
        findCategories("");
        function findTovars(filter){
            console.log(filter);
            $.ajax({
                url: '/tovars/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'title' }, {name: 'cost' }, {name: 'category_id'},
                         {name: 'category_title'},  {name: 'animal_id'}, {name: 'animal_specie'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#tovarDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Название', dataField: 'title', width: 100},
                                { text: 'Цена', dataField: 'cost', width: 100},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Категория', dataField: 'category_title', width: 120},
                                 {text: 'Животное', dataField: 'animal_specie', width: 120}
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }
        var categories = [];

        function findCategories(filter){
            $.ajax({
                url: '/categories/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    animals = data;
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'title' }],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                   $("#tovarJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "title", valueMember: 'id', source: dataAdapter});
                }
            });
        }

        $("#tovarDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#tovarSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#tovarEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#tovarOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#tovarCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#tovarInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Название"});
        $("#jqxFormattedInput").jqxFormattedInput({ width: 250, height: 25, radix: "decimal", value: "100", spinButtons: true, dropDown: true });
        $("#tovarSearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#tovarDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            tovar['title'] = row["title"];
            tovar['id'] = row['id'];
            tovar['cost'] = row['cost'];
            tovar['category_id'] = row["category_id"];
            tovar['category_title'] = row["category_title"];
        });
        $("#tovarSearch").on('change', function (event){
            var search = $('#tovarSearch').val();
//            console.log(search);
            findTovars(search);
        });
        $("#tovarInput").on('change', function (event){
            tovar['title'] = $('#tovarInput').val();
//            console.log(tovar);
        });
        $('#jqxFormattedInput').on('change', function (event) {
            tovar['cost'] = $('#jqxFormattedInput').val();
        });
        $("#tovarJqxlistbox").on('select', function (event){
            tovar['category_id'] = event.args.item.value;
        });

         $("#tovarJqxWindow").jqxWindow({
            title: 'Добавить товар',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#tovarSave').on('click', function() {
            tovar = {};
            $('#tovarJqxWindow').jqxWindow('open');
            $('#tovarInput').val("");
        });
        $('#tovarEdit').on('click', function() {
            if(tovar["id"]){
                $('#tovarInput').val(tovar['title']);
                $('#jqxFormattedInput').val(tovar['cost']);

                $('#tovarJqxWindow').jqxWindow('open');
//                $("#jqxFormattedInput").jqxFormattedInput("open");

            }
        });
        $('#tovarCancel').on('click', function() {
                    $('#tovarInput').val("");
            $('#tovarJqxWindow').jqxWindow('close');
                        tovar = {};
        });
        $('#tovarOK').on('click', function() {
            if (!tovar["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            console.log(tovar);
            ajaxProperties['data'] = JSON.stringify(tovar);
            $.ajax(ajaxProperties);
            $('#tovarJqxWindow').jqxWindow('close');
        });
        $('#tovarDelete').on('click', function () {
            if(tovar['id']){
                ajaxProperties['method'] = 'delete';
                console.log(tovar);
                ajaxProperties['data'] = JSON.stringify(tovar);
                $.ajax(ajaxProperties);
            }
        });
    });