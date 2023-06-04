
    $(document).ready(function () {
//        var row = null;

        var ajaxProperties = {
            url: '/animals',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(animal),
            success: function(data){
                console.log(data);
                animal = {};
            },
            complete: function(){
                findAnimals("");
            }
        };
        var animal = {};

        $("#animalDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#animalSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#animalEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#OK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#Cancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#input").jqxInput({ width: '250px', height: '25px', placeHolder: "Название"});
        $("#search").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $("#input").on('change', function (event){
            animal['specie'] = $('#input').val();
            console.log(animal);
        });
        $("#search").on('change', function (event){
            var search = $('#search').val();
            console.log(search);
            findAnimals(search);
        });
        $("#jqxWindow").jqxWindow({
            title: 'Добавить животное',
            height:120,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#animalSave').on('click', function() {
            $('#jqxWindow').jqxWindow('open');
            $('#input').val("");
//            row = {};
        });
        $('#animalEdit').on('click', function() {
            if(animal["id"]){
                $('#input').val(animal['specie']);
                $('#jqxWindow').jqxWindow('open');
            }
        });
        $('#Cancel').on('click', function() {
                    $('#input').val("");
            $('#jqxWindow').jqxWindow('close');
                        animal = {};
        });
        $('#OK').on('click', function() {
            if (!animal["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            ajaxProperties['data'] = JSON.stringify(animal);
            $.ajax(ajaxProperties);

        });
        $('#animalDelete').on('click', function () {
            if(animal['id']){
                ajaxProperties['method'] = 'delete';
                $.ajax(ajaxProperties);
            }
        });

        function findAnimals(filter){
            $.ajax({
                url: '/animals/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'specie' }],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#dataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Вид', dataField: 'specie', width: 100 }
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }

        $('#dataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            animal['specie'] = row["specie"];
            animal['id'] = row['id'];
        });

        findAnimals("");
    });







//    function onSaveAnimal(){
//        $.ajax({
//            url: '/animal/tst',
//            contentType: "application/json",
//            method: 'post',
//            dataType: 'json',
//            data: JSON.stringify(animal),
//            success: function(data){
//                console.log(data);
//            }
//        });
//    }


