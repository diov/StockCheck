$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

});

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#receipt-table').bootstrapTable({
            url: '/receipts/details',             //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                    //是否启用排序
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 50,                       //每页的记录行数（*）
            pageList: [20],                        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: false,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            uniqueId: "DISPLAY_ID",                     //每一行的唯一标识，一般为主键列
            showToggle:false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'date',
                title: "日期"
            }, {
                field: 'customer',
                title: '客户'
            }, {
                field: 'receipt_id',
                title: "发票编号"
            }, {
                field: 'maker',
                title: '制单人'
            }, {
                field: 'repository',
                title: "发货仓库"
            }, {
                field: 'balance',
                title: "结算方式"
            }, {
                field: 'product_name',
                title: '商品名称'
            }, {
                field: 'unit',
                title: '单位'
            }, {
                field: 'amount',
                title: '数量'
            }, {
                field: 'sale_price',
                title: '单价'
            }, {
                field: 'price',
                title: "金额"
            }, {
                field: 'comment',
                title: "备注"
            }, {
                field: 'sender',
                title: "发货人"
            }, {
                field: 'handler',
                title: "经手人"
            }, ]
        });
    };

    return oTableInit;
};