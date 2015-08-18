/**
 * Created by K on 3/19/14.
 */
$(document).ready(function(){
    function add_select() {
        var group = $("#group_id");
		var city_select = $.parseHTML("<select name='group_id' id='group_id'></select>");
        g_belong_area_id =group.val();
		group.replaceWith(city_select);
	}

	add_select();
    function init_loacation(init_province) {
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
                    if (g_belong_area_id == value[0]){
                        $("#group_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                        $("#group_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }

                });
                group.val(init_province);
                g_belong_area_id = init_province;
            },
            error: function() {
                alert("获取集团资料失败，请刷新网页！");
            }
        });
    }
   // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_area_id != "") {
        init_loacation(g_belong_area_id);
    } else {
        init_loacation("1");
    }
});

