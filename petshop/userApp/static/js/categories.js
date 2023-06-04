
    $(document).ready(function () {
        var category = {};
        var ajaxProperties = {
            url: '/categories',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(category),
            success: function(data){
                category = {};
            },
            complete: function(){
                findCategories("");
            }
        };

        findCategories("");
        findAnimals("");
        function findCategories(filter){
            $.ajax({
                url: '/categories/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'title' }, {name: 'animal_id'}, {name: 'animal_specie'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#categoryDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Название', dataField: 'title', width: 100},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Вид животного', dataField: 'animal_specie', width: 120}
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }
        var animals = [];

        function findAnimals(filter){
            $.ajax({
                url: '/animals/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    animals = data;
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'specie' }],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                   $("#categoryJqxlistbox").jqxListBox({ width: '200px', height: '200px', displayMember: "specie", valueMember: 'id', source: dataAdapter});
                }
            });
        }

        $("#categoryDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#categorySave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#categoryEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#categoryOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#categoryCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#categoryInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Название"});
        $("#categorySearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $('#categoryDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            category['title'] = row["title"];
            category['id'] = row['id'];
            category['animal_id'] = row["animal_id"];
            category['animal_specie'] = row["animal_specie"];
        });
        $("#categorySearch").on('change', function (event){
            var search = $('#categorySearch').val();
            console.log(search);
            findCategories(search);
        });
        $("#categoryInput").on('change', function (event){
            category['title'] = $('#categoryInput').val();
            console.log(category);
        });
        $("#categoryJqxlistbox").on('select', function (event){
            category['animal_id'] = event.args.item.value;
        });

         $("#categoryJqxWindow").jqxWindow({
            title: 'Добавить категорию',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#categorySave').on('click', function() {
            category = {};
            $('#categoryJqxWindow').jqxWindow('open');
            $('#categoryInput').val("");
        });
        $('#categoryEdit').on('click', function() {
            if(category["id"]){
                $('#categoryInput').val(category['title']);

                $('#categoryJqxWindow').jqxWindow('open');

            }
        });
        $('#categoryCancel').on('click', function() {
                    $('#categoryInput').val("");
            $('#categoryJqxWindow').jqxWindow('close');
                        category = {};
        });
        $('#categoryOK').on('click', function() {
            if (!category["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            ajaxProperties['data'] = JSON.stringify(category);
            $.ajax(ajaxProperties);
            $('#categoryJqxWindow').jqxWindow('close');
        });
        $('#categoryDelete').on('click', function () {
            if(category['id']){
                ajaxProperties['method'] = 'delete';
                ajaxProperties['data'] = JSON.stringify(category);
                $.ajax(ajaxProperties);
            }
        });
    });