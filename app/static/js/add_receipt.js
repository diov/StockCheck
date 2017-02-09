$(document).ready(function() {
    var csrftoken = $('meta[name=csrf-token]').attr('content')
    var date_input = $("#receipt_date")[0]
    var warning = $("#warning-block")

    date_input.valueAsDate = new Date();
    warning.hide()
    $('#receipt-form').validator()

    $("#submit").click(function(){
        console.log('enter submit')
        if (!$(this).hasClass('disabled')) {
            var len = $("#product-table")[0].rows.length - 1
            if(len >= 1) {
                $.ajax({
                    url: "#",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    type: "POST",
                    data: $("#receipt-form").serialize(),
                    complete: function(data) {
                        var json = data.responseJSON
                        show_response(json)
                    }
                })
            } else {
                alert("至少需要一个商品")
            }
        }
    })

    $("#remove-add").click(function(){
        $("tr[id^=addr]").remove();
        $("#receipt-form")[0].reset()
    })

    $("#remove-product").click(function(){
        var len = $("#product-table")[0].rows.length - 1
        if(len >= 1) {
            $("#addr"+(len-1)).remove();
        }
    })
});

$(function() {
    $('#product-model').on('show.bs.modal', function() {
        $("#search-btn").bind("click", initTable);
    });
        $("#submit-btn").click(function(){
        var obj = $('#result-table').bootstrapTable('getSelections')[0]
        var len = $("#product-table")[0].rows.length - 1
        var new_tr = ["<tr id=\"addr"+len+"\">",
            "<td><input class=\"form-control\" id=\"products-"+len+"-product_id\" ",
            "name=\"products-"+len+"-product_id\" type=\"text\" value=\""+obj.stock_id+"\" required readonly></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-product_name\" ",
            "name=\"products-"+len+"-product_name\" type=\"text\" value=\""+obj.name+"\" required readonly></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-unit\" ",
            "name=\"products-"+len+"-unit\" type=\"text\" value=\""+obj.unit+"\" readonly></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-amount\" ",
            "name=\"products-"+len+"-amount\" type=\"text\" required></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-univalent\" ",
            "name=\"products-"+len+"-univalent\" type=\"text\" value=\""+obj.sale_price+"\" required></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-price\" "+
            "name=\"products-"+len+"-price\" type=\"text\" required readonly></td>",
            "<td><input class=\"form-control\" id=\"products-"+len+"-comment\" ",
            "name=\"products-"+len+"-comment\" type=\"text\"></td></tr>"].join("");

        $("#product-table tbody").append(new_tr)
        $('#receipt-form').validator('update')
        $('#product-model').modal('hide')
        $("input[id$='amount']").bind('input propertychange', function() {
            amount = $(this).val()
            univalent = $(this).parent().next().children().val()
            $(this).parent().next().next().children().val(amount * 10000 * univalent / 10000)
        });
        $("input[id$='univalent']").bind('input propertychange', function() {
            univalent = $(this).val()
            amount = $(this).parent().prev().children().val()
            $(this).parent().next().children().val(amount * 10000 * univalent / 10000)
        }
        )
    })
});

function initTable() {
    $('#result-table').bootstrapTable('destroy');
    $('#result-table').bootstrapTable({
        url: '/product',                    //请求后台的URL（*）
        method: 'get',                      //请求方式（*）
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: false,                   //是否显示分页（*）
        sortable: false,                    //是否启用排序
        search: false,                      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        strictSearch: true,
        showColumns: false,                  //是否显示所有的列
        showRefresh: false,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        uniqueId: "DISPLAY_ID",                     //每一行的唯一标识，一般为主键列
        showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
        cardView: false,                    //是否显示详细视图
        detailView: false,                  //是否显示父子表
        singleSelect: true,                 //单选
        queryParams: function queryParams(params) {   //设置查询参数
              var param = {
                  search: $("#search-input").val()
              };
              return param;
            },
        columns: [{
            checkbox: true
        }, {
            field: 'stock_id',
            title: "#"
        }, {
            field: 'name',
            title: '商品名称'
        }, {
            field: 'unit',
            title: '单位'
        }, {
            field: 'sale_price',
            title: '出价'
        }, {
            field: 'amount',
            title: '当前库存'
        }, ]
    });
}

function show_response(json) {
    if(null != json) {
        console.log(json)
        switch(json.status) {
            case 0: // 成功
                console.log(0)
                $("#warning-block").removeClass("alert-danger").addClass("alert-success")
                $("#warning-block").children("strong").text(json.message)
                $("#warning-block").show()
                break
            case 1: // 写入失败
                console.log(1)
                $("#warning-block").removeClass("alert-success").addClass("alert-danger")
                $("#warning-block").children("strong").text(json.message)
                $("#warning-block").show()
                break
            case 2: // 验证失败
//                valide_msg = ''
//                Object.keys(json.message).forEach(key => {
//                    msg = json.message[key][0]
//                    valide_msg += (msg+"\n")
//                })
                valide_msg = ""
                json.message.products.forEach(msg => valide_msg += (msg + " "))
                $("#warning-block").removeClass("alert-success").addClass("alert-danger")
                $("#warning-block").children("strong").text(valide_msg)
                $("#warning-block").show()
                break
        }
    }
}