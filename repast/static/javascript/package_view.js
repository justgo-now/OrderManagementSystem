/**
 * Created by K on 3/19/14.
 */
$(document).ready(function(){
    $("input[name='suitable_number']").keyup(function(){  //keyup事件处理
        $(this).val($(this).val().replace(/\D|^0/g,''));
    }).bind("paste",function(){  //CTR+V事件处理
        $(this).val($(this).val().replace(/\D|^0/g,''));
    }).css("ime-mode", "disabled");  //CSS设置输入法不可用
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
        //var checkbox_sort = $.parseHTML("<input type='hidden' name='hidden' id='dish_sort_id'/>");
        var checkbox_sort = $.parseHTML("<label id='dish_sort_id'></label>");
        g_belong_sort_id = dish_sort.val();
        dish_sort.replaceWith(checkbox_sort)
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

   // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_group_id != "") {
        init_group(g_belong_group_id);
    } else {
        init_group("1");
    }
    function init_dish_sort(init_dish_sort_id){
        var bool = true;
        try{
            var dish_sort_array = init_dish_sort_id.split(',')
        }catch(err){
            bool = false;
        }
        var dish_sort = $("#dish_sort_id");
        var brand = $("#brand_id");
        var brand_val = brand.val();
        // 获取brand的json
        $.ajax({
            type: "GET",
            url: "/restful/dish_sort/"+ brand_val,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $(".parentEle").empty();
                $.each(json, function(i, value) {
                    if (bool == true){
                        var number_value = value[0].toString();
                        var index = dish_sort_array.indexOf(number_value);
                        if (index !== -1){
                            $("#dish_sort_id").append($("<input type='checkbox' checked name='dish_sort_id' class='dish_sort' style='float: left' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                                var parentEle = $('#dish_sort_id').parent();
                                parentEle.addClass('parentEle')
                        }else{
                            $("#dish_sort_id").append($("<input type='checkbox' name='dish_sort_id' style='float: left' class='dish_sort' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                            var parentEle = $('#dish_sort_id').parent();
                            parentEle.addClass('parentEle')
                        }
                    }else{
                        if (init_dish_sort_id == value[0].toString()){
                                $("#dish_sort_id").append($("<input type='checkbox' checked name='dish_sort_id' class='dish_sort' style='float: left' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                                var parentEle = $('#dish_sort_id').parent();
                                parentEle.addClass('parentEle')
                            }else{
                                $("#dish_sort_id").append($("<input type='checkbox' name='dish_sort_id' style='float: left' class='dish_sort' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                                var parentEle = $('#dish_sort_id').parent();
                                parentEle.addClass('parentEle')
                            }
                    }
                });

            },
            error: function() {
                alert("获取菜品种类失败，请刷新网页！");
            }
        });
    }
    divEle = $(".controls");
    function change_dish_sort(init_dish_sort_id){
        var bool = true;
        try{
            var dish_sort_array = init_dish_sort_id.split(',')
        }catch(err){
            bool = false;
        }
        var dish_sort = $("#dish_sort_id");
        var brand = $("#brand_id");
        var brand_val = brand.val();
        // 获取brand的json
        $.ajax({
            type: "GET",
            url: "/restful/dish_sort/"+ brand_val,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $(".parentEle").empty();
                $.each(json, function(i, value) {
                    if (bool){
                        var number_value = value[0].toString();
                        var index = dish_sort_array.indexOf(number_value);
                        if (index !== -1){
                            $(".parentEle").append($("<input type='checkbox' checked name='dish_sort_id' class='dish_sort' style='float: left' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                        }else{
                            $(".parentEle").append($("<input type='checkbox' name='dish_sort_id' style='float: left' class='dish_sort' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                        }
                    }else{
                        if (init_dish_sort_id == value[0].toString()){
                            $(".parentEle").append($("<input type='checkbox' checked name='dish_sort_id' class='dish_sort' style='float: left' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                        }else{
                            $(".parentEle").append($("<input type='checkbox' name='dish_sort_id' style='float: left' class='dish_sort' id='dish_sort_id'/>").attr('value', value[0]).after($("<label style='float: left;margin-right: 10px;'>"+value[1]+"</label>")))
                        }
                    }
                });

            },
            error: function() {
                alert("获取菜品种类失败，请刷新网页！");
            }
        });
    }
    //定义change事件
    var group = $('#group_id');
    group.bind('change',function(){
        var init_group_id = group.val();
        get_brand_ajax(init_group_id)
    });
    var brand = $("#brand_id");
    brand.bind('change', function(){
        var brand_id = brand.val();
        change_dish_sort(g_belong_sort_id)
    });
    if (g_belong_sort_id != ''){
        init_dish_sort(g_belong_sort_id)
    }else{
        init_dish_sort(brand.val())
    }
});

