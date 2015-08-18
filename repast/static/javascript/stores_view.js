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
        var province = $("#province_id");
        var province_select = $.parseHTML("<select name='province_id' id='province_id'></select>");
        g_belong_province_id = province.val()
        province.replaceWith(province_select)
        //替换所属城市
        var city = $("#city_id");
        var city_select = $.parseHTML("<select name='city_id' id='city_id'></select>");
        g_belong_city_id = city.val();
        city.replaceWith(city_select);
        //替换所有区
        var country = $("#country_id");
        var country_select = $.parseHTML("<select name='country_id' id='country_id'></select>");
        g_belong_country_id = country.val();
        country.replaceWith(country_select);
        // 添加百度地图
		$("#latitude").parent().parent().parent().after("<div id='baidumap' style='width:800px; height:500px; margin-bottom:20px;'></div>");
		// 添加地图搜索
		$("#latitude").parent().parent().parent().after("<div id='float_search_bar'><input type='text' id='keyword' /><span id='search_button' style='margin-left:-45px;' class='btn'>查找</span></div>");
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
        get_brand_ajax(group.val())
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
    function init_location(init_province, init_city, init_country){
        var province = $('#province_id')
        $.ajax({
            type: "GET",
            url: "/restful/province",
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                province.empty();
                $.each(json, function(i, value) {
                    if (g_belong_province_id == value[0]){
                        $("#province_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                         $("#province_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }
                });
                province.val(init_province);
                g_belong_province_id = init_province;
            },
            error: function() {
                alert("获取省资料失败，请刷新网页！");
            }
        });
        get_city(province, init_province, init_city, init_country)

    }
    // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_belong_group_id != "") {
        init_group(g_belong_group_id);
    } else {
        init_group("1");
    }
    if (g_belong_province_id != ""){
        init_location(g_belong_province_id, g_belong_city_id, g_belong_country_id)
    }else{
        init_location("9","75","794")
    }

    function get_city(province, init_province, init_city, init_country){
        var city = $('#city_id');
        $.ajax({
            type: "GET",
            url: "/restful/city/" + init_province,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                city.empty();
                $.each(json, function(i, value) {
                    if (g_belong_city_id == value[0]){
                        $("#city_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                    }else{
                        $("#city_id").append($("<option>").text(value[1]).attr('value', value[0]));
                    }

                });
                city.val(init_city)
                g_belong_city_id = init_city;
            },
            error: function() {
                alert("获取市资料失败，请刷新网页！");
            }
        });
        get_country(province, city, init_city, init_country)
    }
    function get_country(province, city, init_city, init_country){
        var country = $('#country_id');
        $.ajax({
            type: "GET",
            url: "/restful/country/" + init_city,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                country.empty();
                if (json.length == 0){
                     $("#country_id").append($("<option>").text("").attr('value', "0"));
                }else{
                    $.each(json, function(i, value) {
                        if (g_belong_country_id == value[0]){
                            $("#country_id").append($("<option>").text(value[1]).attr('value', value[0]).attr('selected','selected'));
                        }else{
                            $("#country_id").append($("<option>").text(value[1]).attr('value', value[0]));
                        }
                    });
                    if (init_country != ""){
                        country.val(init_country);
                        g_belong_country_id = init_country;
                    }
                }
            },
            error: function() {
                //alert("当前城市没有区！");
            }
        });
        var address = $("#address");
        var temp_city = city.find('option:selected').text();
        var temp_address = "";
        if (temp_city == '市辖区'){
            temp_address = province.find('option:selected').text() + country.find('option:selected').text();
        }else{
            temp_address = province.find('option:selected').text() + city.find('option:selected').text() + country.find('option:selected').text();
        }
        address.val(temp_address)
    }


    // 地图初始化
	function setResult(lng, lat) {
		$("#latitude").val(lat);
		$("#longitude").val(lng);
	}
    //定义change事件
    var group = $('#group_id');
    group.bind('change',function(){
        var init_group_id = group.val();
        get_brand_ajax(init_group_id)
    });

    //定义省份change事件
    var province = $("#province_id");
    province.bind('change', function(){
        var province_val = province.val();
        get_city(province, province_val);
        var city_val = $("#city_id");
        get_country(province, city_val, city_val.val(), "")
    });
    //定义城市cahnge事件
    var city = $("#city_id");
    city.bind('change',function(){
        get_country(province, city, city.val(), "")
    });

	function init_map() {
		createMap();
		setMapEvent(); // 设置地图事件
		addMapControl(); // 向地图添加控件
	}

	function createMap() {
		var map = new BMap.Map("baidumap"); //在百度地图容器中创建一个地图
		var point = new BMap.Point(121.487899, 31.249162);
		map.centerAndZoom(point, 12);
		window.map = map; //将map变量存储在全局
	}

	function setMapEvent() {
        map.enableDragging(); //启用地图拖拽事件，默认启用(可不写)
        map.enableScrollWheelZoom(); //启用地图滚轮放大缩小
        map.enableDoubleClickZoom(); //启用鼠标双击放大，默认启用(可不写)
        map.enableKeyboard(); //启用键盘上下左右键移动地图
	}

	function addMapControl() {
        //向地图中添加缩放控件
		var ctrl_nav = new BMap.NavigationControl({anchor:BMAP_ANCHOR_TOP_LEFT,type:BMAP_NAVIGATION_CONTROL_SMALL});
		map.addControl(ctrl_nav);
        //向地图中添加缩略图控件
		var ctrl_ove = new BMap.OverviewMapControl({anchor:BMAP_ANCHOR_BOTTOM_RIGHT,isOpen:0});
		map.addControl(ctrl_ove);
        //向地图中添加比例尺控件
		var ctrl_sca = new BMap.ScaleControl({anchor:BMAP_ANCHOR_BOTTOM_LEFT});
		map.addControl(ctrl_sca);
	}

	init_map();
    // 百度地图数据部分 start
	var marker_trick = true;
	var marker = new BMap.Marker(new BMap.Point(121.487899, 31.249162), {
		enableMassClear: false,
		raiseOnDrag: true
	});
	marker.enableDragging();
	map.addEventListener("click", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	marker.addEventListener("dragend", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	var local = new BMap.LocalSearch(map, {
		renderOptions: {map: map},
		pageCapacity: 1
	});
	local.setSearchCompleteCallback(function(results) {
		if (local.getStatus() != BMAP_STATUS_SUCCESS) {
			//alert("无结果");
		} else {
			marker.hide();
		}
	});
	local.setMarkersSetCallback(function(pois) {
		for (var i=pois.length; i--; ) {
			var marker = pois[i].marker;
			marker.addEventListener("click", function(e) {
				marker_trick = True;
				var pos = this.getPosition();
				setResult(pos.lng, pos.lat);
			});
		}
	});
    $("#keyword").change(function() {
    	local.search($("#keyword").val());
    });
    $("#keyword").onkeyup = function(e){
        var me = this;
        e = e || window.event;
        var keycode = e.keyCode;
        if(keycode === 13){
            local.search($("#keyword").val());
        }
    };
    //填写酒吧名字自动填写搜索的内容
	$("#name").change(function() {
		$("#keyword").val($("#name").val());
    	local.search($("#keyword").val());
	})
});

