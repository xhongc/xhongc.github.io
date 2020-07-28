title: PDF.js跨域（django后端处理数据流方法）
date: 2020-07-28
author: charles
Tags: django
Slug: pdf_js_django_cors
Category: python

## 前言
PDF.js is a Portable Document Format (PDF) viewer that is built with HTML5.
下载地址[https://github.com/mozilla/pdf.js/releases](https://github.com/mozilla/pdf.js/releases)

## 跨域
网上也有一些设置nginx服务器实现跨域，这里只考虑是把pdf文件请求到后端返回数据流的形式来实现

- 首先
1. 修改viewer.js
```js
function webViewerLoad() {
  var config = getViewerConfiguration();
  window.PDFViewerApplication = pdfjsWebApp.PDFViewerApplication;
  window.PDFViewerApplicationOptions = pdfjsWebAppOptions.AppOptions;
  var event = document.createEvent('CustomEvent');
  event.initCustomEvent('webviewerloaded', true, true, {});
  document.dispatchEvent(event);
  pdfjsWebApp.PDFViewerApplication.run(config);
}
```
改成
```js
window.webViewerLoad=function webViewerLoad(fileUrl) {//调整了此行
  var config = getViewerConfiguration();
  window.PDFViewerApplication = pdfjsWebApp.PDFViewerApplication;
  window.PDFViewerApplicationOptions = pdfjsWebAppOptions.AppOptions;
  var event = document.createEvent('CustomEvent');
  event.initCustomEvent('webviewerloaded', true, true, {});
  document.dispatchEvent(event);
  //调整了if 语句
  if(fileUrl){
    config.defaultUrl=fileUrl;
  }
  pdfjsWebApp.PDFViewerApplication.run(config);
}
```
2. 注释
```js
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  webViewerLoad();
} else {
  document.addEventListener('DOMContentLoaded', webViewerLoad, true);
}
```
3. 修改viewer.js
```js
run(config) {
    this.initialize(config).then(webViewerInitialized);
  }
```
改成
```js
run(config) {
    //添加if语句
    if(config.defaultUrl){
      _app_options.AppOptions.set('defaultUrl',config.defaultUrl)

   }    
   this.initialize(config).then(webViewerInitialized);
  },
```
4. 添加代码viewer.html
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
```js
<script>
    function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            if (pair[0] == variable) {
                return pair[1];
            }
        }
        return (false);
    }

    $(document).ready(function () {

        //获取要跨域访问的pdf地址
        var pdfUrl = getQueryVariable("pdfurl")

        if (pdfUrl) {
            xhrPdf(pdfUrl, function (href) {

                //调用viewer.js方法预览pdf
                webViewerLoad(href)
            })
        }

    });

    //添加xhrPdf函数
    function xhrPdf(url, callback) {
        $.ajax({
            type: "get",
            async: false,
            mimeType: 'text/plain; charset=x-user-defined',
            url: "/api/g_pdf?pdfurl=" + url, //请求服务器数据 获取pdf数据流
            success: function (data) {
                var rawLength = data.length;
                //转换成pdf.js能直接解析的Uint8Array类型,见pdf.js-4068    
                var array = new Uint8Array(new ArrayBuffer(rawLength));
                for (var i = 0; i < rawLength; i++) {
                    array[i] = data.charCodeAt(i) & 0xff;
                }
                var href = window.URL.createObjectURL(new Blob([array]));//数据流转换成createObjectURL能解析的Blob类型
                callback(href)   //返回url         
            }
        });
    }

</script>
```
### 然后
- django 接口代码 来处理文件流
```python
class PDFstreamViewsets(mixins.ListModelMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        url = request.query_params.get('pdfurl', None)
        if not url:
            return JsonResponse({'status': '0000'})
        try:
            r = requests.get(url, stream=True)
        except:
            r = ''
        fd = io.BytesIO()
        for chunk in r.iter_content(2000):
            fd.write(chunk)
        return StreamingHttpResponse(streaming_content=(fd.getvalue(),), content_type='application/octet-stream')
```

urls.py
```python
# 注册URL路径，要求添加template文件目录，这里不再赘述
path('pdf_viewer/', TemplateView.as_view(template_name='viewer.html'), name='test'),
```
### 最后
访问 http://127.0.0.1:8088/pdf_viewer/?pdfurl=http://www.mee.gov.cn/image20010518/5295.pdf
可以看到效果了

