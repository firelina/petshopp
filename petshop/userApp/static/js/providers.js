
    $(document).ready(function () {
        var provider = {};
        var ajaxProperties = {
            url: '/providers',
            contentType: "application/json",
            method: 'post',
            dataType: 'json',
            data: JSON.stringify(provider),
            success: function(data){
                provider = {};
            },
            complete: function(){
                findProviders("");
            }
        };

        findProviders("");
        function findProviders(filter){
            $.ajax({
                url: '/providers/search',
                contentType: "application/json",
                method: 'post',
                data: JSON.stringify(filter),
                dataType: 'json',
                success: function(data){
                    var source = {
                        dataType: "json",
                        dataFields: [{ name: 'id' }, { name: 'title' }, {name: 'telethon'}],
                        localData: data
                    };
                    var dataAdapter = new $.jqx.dataAdapter(source);
                    $("#providerDataTable").jqxDataTable(
                        {
                            source: dataAdapter,
                            columns: [
                                { text: 'id', dataField: 'id', width: 100 },
                                { text: 'Название', dataField: 'title', width: 100},
//                                 {text: 'id животного', dataField: 'animal_id', width: 100},
                                 {text: 'Телефон', dataField: 'telethon', width: 120}
                            ],
                            theme: 'darkblue'
                        });
                }
            });
        }

        $("#providerDelete").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#providerSave").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#providerEdit").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#providerOK").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#providerCancel").jqxButton({ width: '120px', height: '35px', theme: 'darkblue' });
        $("#providerInput").jqxInput({ width: '250px', height: '25px', placeHolder: "Название"});
        $("#providerSearch").jqxInput({ width: '250px', height: '25px', placeHolder: "Поиск" });
        $("#jqxMaskedInput").jqxMaskedInput({ width: '250px', height: '25px', mask: '#(###)###-##-##' });
        $('#providerDataTable').on('rowClick',function (event)
        {
            const row = event.args.row;
            provider['title'] = row["title"];
            provider['id'] = row['id'];
            provider['telethon'] = row["telethon"];
        });
        $("#providerSearch").on('change', function (event){
            var search = $('#providerSearch').val();
            console.log(search);
            findProviders(search);
        });
        $("#providerInput").on('change', function (event){
            provider['title'] = $('#providerInput').val();
        });
        $('#jqxMaskedInput').on('change',
        function (event)
        {
            provider['telethon'] = event.args.value;
        });

         $("#providerJqxWindow").jqxWindow({
            title: 'Добавить поставщика',
            height:500,
            width: 400,
            theme: 'darkblue',
            showCloseButton: true,
            isModal: true,
            autoOpen: false
        });
        $('#providerSave').on('click', function() {
            category = {};
            $('#providerJqxWindow').jqxWindow('open');
            $('#providerInput').val("");
        });
        $('#providerEdit').on('click', function() {
            if(provider["id"]){
                $('#providerInput').val(provider['title']);
                $('#jqxMaskedInput').jqxMaskedInput({value: provider['telethon'] });
                $('#providerJqxWindow').jqxWindow('open');

            }
        });
        $('#providerCancel').on('click', function() {
                    $('#providerInput').val("");
            $('#providerJqxWindow').jqxWindow('close');
                        provider = {};
        });
        $('#providerOK').on('click', function() {
            if (!provider["id"])
                ajaxProperties['method'] = 'post';
            else
                ajaxProperties['method'] = 'put';
            ajaxProperties['data'] = JSON.stringify(provider);
            $.ajax(ajaxProperties);
            $('#providerJqxWindow').jqxWindow('close');
        });
        $('#providerDelete').on('click', function () {
            if(provider['id']){
                ajaxProperties['method'] = 'delete';
                ajaxProperties['data'] = JSON.stringify(provider);
                $.ajax(ajaxProperties);
            }
        });
    });