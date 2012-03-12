$(function () {
    $('#id_telefone').mask('(99) 9999-9999');
    $('#id_data_inicial').mask('99/99/9999');
    $('#id_data_final').mask('99/99/9999');

    var carregarQuartos = function (data) {
        $("#quarto_list tbody").empty();

        for (var _i=0; _i<data.length; _i++) {
            var q = data[_i];

            $("<tr><td><input type=\"radio\" class='quarto' name=\"quarto\" value="+q[0]+" /></td>"+
              "<td>"+q[1]+"</td><td>"+q[2]+"</td><td>"+q[3]+"</td></tr>").appendTo("#quarto_list tbody");
        }
    };

    var buscarQuartos = function () {
        var dataInicial = $('#id_data_inicial').val();
        var dataFinal = $('#id_data_final').val();

        $.getJSON('.', {'data_inicial': dataInicial,
                        'data_final': dataFinal,
                        'acao': 'buscar_quartos'},
                  function (data) {
                      carregarQuartos(data);
                  });
    };

    $('#buscar_quarto').click(function (e) {
        e.preventDefault();
        buscarQuartos();
        return false;
    });
});