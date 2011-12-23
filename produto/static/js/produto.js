/*
 * Trabalho de conclusão de curso
 * Alunos
 *
 * Wilson Pinto Júnior <wilsonpjunior@gmail.com>
 * Mateus Fedrigo de Moura <mateusfedrigo@gmail.com>
 * Jonathas Peixoto <jonathas.peixoto@gmail.com>
 *
 * Este programa é um software livre; você pode redistribui-lo e/ou 
 * modifica-lo dentro dos termos da Licença Pública Geral GNU como 
 * publicada pela Fundação do Software Livre (FSF); na versão 2 da 
 * Licença, ou (na sua opnião) qualquer versão.

 * Este programa é distribuido na esperança que possa ser  util, 
 * mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
 * MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
 * Licença Pública Geral GNU para maiores detalhes.
 *
 * Você deve ter recebido uma cópia da Licença Pública Geral GNU
 * junto com este programa, se não, escreva para a Fundação do Software
 * Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

$(function () {
    var Produto = Backbone.Model.extend({});
    var Produtos = Backbone.Collection.extend({
        model: Produtos,
        url: '/produto/'
    });

    var ProdutoView = Backbone.View.extend({
        className: "produto",
        tagName: "tr",
        template: _.template($('#produtoview-template').html()),
        events: {
            "click": "onClickEvent",
        },
        render: function() {
            $(this.el).html(this.template({object: this.model}));
            return this;
        },
        onClickEvent: function () {
            if ($(this.el).hasClass('selected')) {
                $('tr.produto.selected').removeClass('selected');
                $(this.el).removeClass('selected');
            } else {
                $('tr.produto.selected').removeClass('selected');
                $(this.el).addClass('selected');
            }
        }
    });

    window.produtos = new Produtos();

    var ProdutosView = Backbone.View.extend({
        id: "produtos",
        tagName:  "div",
        className: "ui-widget-content ui-corner-all",
        template: _.template($('#produtosview-template').html()),
        events: {
            "click #add_produto": "addProduto",
        },
        initialize: function () {
            produtos.bind('add',   this.addOne, this);
            produtos.bind('reset', this.addAll, this);
            produtos.fetch();
        },
        addOne: function (produto) {
            var view = new ProdutoView({model: produto});
            $("#produtos table tbody").append(view.render().el);
        },
        addAll: function () {
            produtos.each(this.addOne);
        },
        render: function () {
            $(this.el).html(this.template());
            $(this.el).find(".toolbar").buttonset();
            return this;
        },
        addProduto: function (e) {
            e.preventDefault();

            var view = new AddProdutoView();
            view.render()

            return false;
        }
    });

    var AddProdutoView = Backbone.View.extend({
        id: "add_produto",
        tagName: "div",
        template: _.template($('#adddprodutoview-tmpl').html()),
        
        initialize: function () {
            console.info(this, arguments);
        },
        render: function () {
            var _this = this;

            $(this.el).html(this.template());
            $(this.el).dialog({
                title: "Adicionando novo produto",
                modal: true,
                buttons: {
                    "Salvar": function () {
                        _this.save();
                        $(this).dialog('destroy');
                        _this.remove();
                    },
                    "Cancelar": function (){
                        $(this).dialog('destroy');
                        _this.remove();
                    }
                },
                close: function () {
                    _this.remove();
                }
            });
            return this;
        },
        save: function () {
            var f = $("#addproduto-form");
            var p = new Produto();
            
            produtos.create({
                nome: f.find('input[name="nome"]').val(),
                qtde: f.find('input[name="qtde"]').val(),
                valor: f.find('input[name="valor"]').val()
            });
        }
    });

    var ProdutoRouter = Backbone.Router.extend({
        routes: {
            "produtos/": "index",
        },
        index: function () {
            $('#container').empty();
            var view = new ProdutosView();
            $(view.render().el).appendTo('#container');
        },
    });

    window.Produto = Produto;
    window.produtoRouter = new ProdutoRouter();
    
});