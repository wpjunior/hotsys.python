$(document).ready(function (e) {

    var anexaHospede = function (data) {
        $('#hospede_list').slideDown();
        var i = $('<tr><td><input type="hidden" name="hospede" value="'+data.id+'" />'+data.nome+'</td>'+
                  '<td>'+data.cpf+'</td></tr>');
        
        i.appendTo('#hospede_list tbody');
    }

    var cadastraHospede = function (cpf) {
        alert('CPF não cadastrado');
    }

    var addHospede = function (cpf) {
        $.getJSON(
            '.', {'cmd': 'getHospede', 'cpf': cpf},
            function (data) {
                if ($.isEmptyObject(data)) {
                    cadastraHospede(cpf);
                } else {
                    anexaHospede(data)
                }
            });
    };
    
    $('#id_data_inicial').datepicker();
    $('#id_data_final').datepicker();
    $('#hospede_cpf').mask('999.999.999-99');
    $('#hospede_list').hide();

    $('#add_hospede').click(function (e) {
        e.preventDefault();
        var cpf = $('#hospede_cpf').val();
        addHospede(cpf);
        $('#hospede_cpf').val('');
        return false;
    });
});