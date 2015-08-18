/**
 * Created by K on 3/19/14.
 */
$(document).ready(function(){
    //文本框只能输入数字
    $("#list_price").keyup(function(){
            $(this).val($(this).val().replace(/[^0-9.]/g,''));
        }).bind("paste",function(){  //CTR+V事件处理
            $(this).val($(this).val().replace(/[^0-9.]/g,''));
        }).css("ime-mode", "disabled"); //CSS设置输入法不可用


    $("#price").keyup(function(){
            $(this).val($(this).val().replace(/[^0-9.]/g,''));
        }).bind("paste",function(){  //CTR+V事件处理
            $(this).val($(this).val().replace(/[^0-9.]/g,''));
        }).css("ime-mode", "disabled"); //CSS设置输入法不可用
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
        var dish_sort = $("#dish_sort_id");
        var dish_sort_select = $.parseHTML("<select name='dish_sort_id' id='dish_sort_id'></select>");
        g_belong_sort_id = dish_sort.val();
        dish_sort.replaceWith(dish_sort_select);
        var packageEle = $("#package_id");
        var package_select = $.parseHTML("<select name='package_id' id='package_id'></select>");
        packageEle.replaceWith(package_select);
        packageEle.append($("<option>").text("请选择套餐").attr('value', "0").attr('selected','selected'));
        g_belong_package_id = packageEle.val();
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
    }

    function init_package(init_package_id){
        var packageEle = $("#package_id");
        var brand = $("#brand_id");
        $.ajax({
            type: "GET",
            url: "/restful/package/"+ brand.val(),
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                packageEle.empty();
                $.each(json, function(i, value) {
                     if (init_package_id == value[0].toString()){
                          packageEle.append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                     }else{
                          packageEle.append($("<option>").text(value[1]).attr('value', value[0]));
                     }
                });
                g_belong_package_id = packageEle.val();
            },
            error: function() {
                alert("获取菜品种类失败，请刷新网页！");
            }
        });
    }

    function init_dish_sort(init_brand){
        var dish_sort = $("#dish_sort_id");
        var brand = $("#package_id").val();
        var packageVal = "0";
        if (brand !== null){
            packageVal = brand
        }
        // 获取brand的json
        $.ajax({
            type: "GET",
            url: "/restful/sort/"+ packageVal,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                dish_sort.empty();
                $.each(json, function(i, value) {
                     if (init_brand == value[0].toString()){
                          dish_sort.append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                     }else{
                          dish_sort.append($("<option>").text(value[1]).attr('value', value[0]));
                     }
                });
                g_belong_sort_id = dish_sort.val();
            },
            error: function() {
                alert("获取菜品种类失败，请刷新网页！");
            }
        });
    }

   // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_group_id != "") {
        init_group(g_belong_group_id);
    } else {
        init_group("1");
    }
    if (g_belong_package_id != ""){
        init_package(g_belong_package_id)
    }else{
        init_package("0")
    }
    if (g_belong_sort_id != ''){
        init_dish_sort(g_belong_sort_id)
    }else{
        init_dish_sort("0")
    }

    //定义change事件
    var group = $('#group_id');
    group.bind('change',function(){
        var init_group_id = group.val();
        get_brand_ajax(init_group_id)
    });
    var brand = $("#brand_id")
    brand.bind('change', function(){
       var init_brand_id = brand.val();
       init_package(init_brand_id);
       init_dish_sort("0")
    });
    var packageEle = $("#package_id");
    packageEle.bind('change', function(){
        var packageVal = packageEle.val();
        init_dish_sort(packageVal)
    })
});

