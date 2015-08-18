/**
 * Created by K on 3/19/14.
 */
$(document).ready(function(){
    function add_select() {
        //替换所属集团
        var group = $("#group_id");
		var group_select = $.parseHTML("<select name='group_id' id='group_id'></select>");
        g_belong_group_id =group.val();
		group.replaceWith(group_select);
        //替换所属品牌
        var brand = $("#brand_id");
		var brand_select = $.parseHTML("<select name='brand_id' id='brand_id'></select>");
        g_belong_brand_id =brand.val();
		brand.replaceWith(brand_select);
        //替换所属省份
        var stores = $("#stores_id");
        var stores_select = $.parseHTML("<select name='stores_id' id='stores_id'></select>");
        g_belong_stores_id = stores.val();
        stores.replaceWith(stores_select);
	}

	add_select();

    function init_group(init_group) {
        var group = $("#group_id");
        // 获取省的json
        $.ajax({
            type: "GET",
            url: "/restful/group",
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                group.empty();
                $.each(json, function(i, value) {
                    if (g_belong_group_id == value[0]){
                        $("#group_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                        $("#group_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }
                });
                group.val(init_group);
                g_belong_group_id = init_group;
            },
            error: function() {
                alert("获取集团资料失败，请刷新网页！");
            }
        });
        get_brand_ajax(init_group)

    }

    function get_brand_ajax(init_group){
        var brand = $("#brand_id");
        // 获取brand的json
        $.ajax({
            type: "GET",
            url: "/restful/brand/" + init_group,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                brand.empty();
                $.each(json, function(i, value) {
                    if (g_belong_brand_id == value[0]){
                        $("#brand_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                         $("#brand_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }
                });
                g_belong_brand_id = brand.val();
            },
            error: function() {
                alert("获取品牌资料失败，请刷新网页！");
            }
        });
        get_stores_ajax(brand.val())
    }
    function get_stores_ajax(init_brand){
        var stores = $("#stores_id");
        // 获取brand的json
        $.ajax({
            type: "GET",
            url: "/restful/stores/" + init_brand,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                stores.empty();
                $.each(json, function(i, value) {
                    if (g_belong_stores_id == value[0]){
                         $("#stores_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                         $("#stores_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }
                });
                g_belong_stores_id = stores.val();
            },
            error: function() {
                alert("获取餐厅资料失败，请刷新网页！");
            }
        });
    }

   // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_group_id != "") {
        init_group(g_belong_group_id);
    } else {
        init_group("1");
    }

    //定义change事件
    var group = $('#group_id');
    group.bind('change',function(){
        var init_group_id = group.val();
        get_brand_ajax(init_group_id)
    });

    //定义省份change事件
    var brand = $("#brand_id");
    brand.bind('change', function(){
        var brand_val = brand.val();
        get_stores_ajax(brand_val);
    });
});

