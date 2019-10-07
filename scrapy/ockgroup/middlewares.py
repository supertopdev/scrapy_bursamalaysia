# import gtk
#import webkit
#import jswebkit
import os
import random
from scrapy.conf import settings
from scrapy.http import HtmlResponse



class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)
 
class ProxyMiddleware(object):
    def process_request(self, request, spider):
    	request.meta['proxy'] = settings.get('HTTP_PROXY')


# class WebkitDownloader( object ):
#     def stop_gtk(self, v, f):
#         gtk.main_quit()

#     def _get_webview(self):
#         webview = webkit.WebView()
#         props = webview.get_settings()
#         props.set_property('enable-java-applet', False)
#         props.set_property('enable-plugins', False)
#         props.set_property('enable-page-cache', False)
#         return webview

#     def process_request( self, request, spider ):
#         if 'renderjs' in request.meta:
#             webview = self._get_webview()
#             webview.connect('load-finished', self.stop_gtk)
#             webview.load_uri(request.url)
#             gtk.main()
#             ctx = jswebkit.JSContext(webview.get_main_frame().get_global_context())
#             url = ctx.EvaluateScript('window.location.href')
#             html = ctx.EvaluateScript('document.documentElement.innerHTML')
#             return HtmlResponse(url, encoding='utf-8', body=html.encode('utf-8'))
