/**
 * Created by K on 3/24/14.
 */

   document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
       WeixinJSBridge.call('showToolbar');
    });
    function weixinSendAppMessage(title,desc,link,imgUrl){
        WeixinJSBridge.invoke('sendAppMessage',{
        //"appid":appId,
        "img_url":imgUrl,
        //"img_width":"640",
        //"img_height":"640",
        "link":link,
        "desc":desc,
        "title":title
        });
    }

