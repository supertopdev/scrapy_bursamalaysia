import sys, traceback
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from ockgroup.items import OckgroupItem
from scrapy.http.cookies import CookieJar
from selenium import webdriver
from urlparse import urljoin
from urlparse import urlparse
import datetime
import MySQLdb
import MySQLdb.cursors
import time
from scrapy.mail import MailSender
import json
import string
import random
import urllib
import re
import smtplib
from scrapy.mail import MailSender
from time import gmtime, strftime
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings

SQL_DB = 'fareasth_ock'
SQL_TABLE = 'nanyang'
SQL_HOST = 'localhost'
#SQL_USER = 'root'
#SQL_PASSWD = ''
SQL_USER = "fareasth_ock"
SQL_PASSWD = "142G#K7ELFW,qAC"


class BursamalaysiaSpider(CrawlSpider):
    mailer = MailSender(smtphost='smtp.mailgun.org', mailfrom='admin@webqom.com', smtpuser='postmaster@sandbox5e7c85e76172478ba660e330ca839a22.mailgun.org', smtppass='bcaf1a6039f6d2e61a4d289fa84f7bd4', smtpport=587)
    name = 'bursamalaysia_nanyang'
    base_url = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=zh_CN&prettyPrint=false&source=gcsc&gss=.com&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&start='
    add_url = '&cx=012605229465411000741:bkqdfrtbckw&q="Far East Holdings"&googlehost=www.google.com&callback=google.search.Search.apiary16952&nocache=1428129005587'
    allowed_domains = ['www.nanyang.com','search.nanyang.com']
    images_prefix = "http://"+allowed_domains[0]
    increment_count = 0
    start_urls = [base_url+str(increment_count)+add_url]
    #http://www.google.com/cse?oe=utf8&ie=utf8&source=uds&q=Far East Holdings&start=10&cx=012605229465411000741:bkqdfrtbckw#gsc.tab=0&gsc.q=Far East Holdings&gsc.page=1
    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=False),
    )
    new_inserted_records = []
    admin_website_url = "http://medianews.fareastholdingsbhd.com"

    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    # def parse(self, response):

    #     # print self.find_between(),"apiary16952","});")
        
    #     return 1
        # return Request(url=self.base_url+str(self.increment_count)+self.add_url,
        #     callback=self.parse_start_url)


    def get_cookies(self,url):
        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
		#self.driver = webdriver.PhantomJS(executable_path='/home/fareastholdingsb/yo/phantomjs-1.9.8-linux-x86_64/bin/phantomjs')
        driver = webdriver.PhantomJS()
        driver.get(url)
        cookies = driver.get_cookies()
        driver.close()
        driver.quit()
        # #reduce(lambda r, d: r.update(d) or r, cookies, {})
        

        return cookies

    def parse_start_url(self, response):
        try:
            string = response.body.decode('utf-8')
            json_obj = json.loads(string[string.index('(')+1:string.index(');')])
            
            count = 0
            CONN = MySQLdb.connect(
			host=SQL_HOST,
                        user=SQL_USER,
                        passwd=SQL_PASSWD,
                        db=SQL_DB,
                        charset='utf8',
                        use_unicode=True)
            CURSOR = CONN.cursor()
	    if not 'results' in json_obj:
		return
            for jObject in json_obj['results']:
                article_url =  jObject['unescapedUrl']
                print "FETCHING =======> ", article_url
                count = count + 1
		if "?tid=" in article_url:
		    article_url = article_url.split("?tid=")[0]
                CURSOR.execute("""SELECT * FROM media_news WHERE link='%s' """%(
                                    str(article_url.strip())
                    ))                    
                if CURSOR.rowcount == 0:
                 	yield Request(url=str(article_url.strip()),callback=self.fetchPage,dont_filter=True)
                

            if count <10:
                return 
            else:
                self.increment_count = self.increment_count + 10
                next_url = self.base_url+str(self.increment_count)+self.add_url
                request = Request(url=next_url,callback=self.parse_start_url,dont_filter=True)
                yield request

        except Exception as e:
           self.logException(e,response)



    
    def fetchPage(self, response):
        try:
            sel = Selector(response)
            article_title = sel.xpath('//title/text()').extract()[0]
	    if len(sel.xpath('//div[@id="inpage_left"]/div[@class="submitted"]/text()').extract())>1:
                article_date = sel.xpath('//div[@id="inpage_left"]/div[@class="submitted"]/text()').extract()[1].strip()
	    else:
                article_date = sel.xpath('//div[@id="inpage_left"]/div[@class="submitted"]/text()').extract()[0].strip()

            article_html = sel.xpath('//div[@id="inpage_left"]/div[@class="node"]').extract()[0]
            article_html = article_html.replace("href=\"/","href=\""+self.images_prefix+"/")
            article_html = article_html.replace("src=\"/","src=\""+self.images_prefix+"/")

            #print "--------->",article_title
            #print "--------->",article_date
            #print "--------->",article_html

	    date_to_timestamp = time.mktime(datetime.datetime.strptime(article_date, "%Y-%m-%d %H:%M").timetuple())
	    footer = "Nanyang"
	    created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	    updated_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            CONN = MySQLdb.connect(
                        host=SQL_HOST,
                        user=SQL_USER,
                        passwd=SQL_PASSWD,
                        db=SQL_DB,
			charset='utf8',
                        use_unicode=True)
            CURSOR = CONN.cursor()
            CURSOR.execute("""INSERT INTO  media_news(title,date,content,link,footer,created_at,updated_at)   
                        VALUES ('%s',%s,'%s','%s','%s','%s','%s')"""%(CONN.escape_string(article_title.encode('utf-8', 'ignore')).decode('utf-8'),
                            date_to_timestamp,
                            CONN.escape_string(article_html.encode('utf-8', 'ignore')).decode('utf-8'),
                            response.url,
			    footer,
			    created_at,
			    updated_at
                            ))

            CONN.commit()
	    self.new_inserted_records.extend([response.url])
            return
        except Exception as e:
            self.logException(e, response)


    def logException(self, e, response):
        f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
        f.write('\n\n%s' %(response.url))
        traceback.print_exc(file=f)
        self.mailer.send(to=["hock@webqom.com"], subject="Nanyang Crawl Failed", body=traceback.format_exc(), cc=[])

        f.close()            


    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)          

    def spider_closed(self, spider):
        try:
            CONN = MySQLdb.connect(
                host=SQL_HOST,
                user=SQL_USER,
                passwd=SQL_PASSWD,
                db=SQL_DB,
                charset='utf8',
                use_unicode=True)
            CURSOR = CONN.cursor()
            all_ids = ""
            email_header = ""
            email_body_master = ""
            email_body = ""
            email_footer = ""



            with open (settings.get('EMAIL_TEMPLATES')+"/email_template_body.html", "r") as myfile:
                email_body_master=myfile.read()

            for i in range(len(self.new_inserted_records)):
                
                CURSOR.execute("""SELECT * FROM media_news WHERE link='%s' """%(
                                        str(self.new_inserted_records[i])
                        ))                    
                if CURSOR.rowcount == 1:
                    data = CURSOR.fetchone()
                    article_id = str(data[0]) 
                    all_ids +=  article_id + ","

                    body = email_body_master
                    body = body.replace("$$$__SERVER_URL__$$$", self.admin_website_url)
                    body = body.replace("$$$__ARTICLE_ID__$$$", article_id)
                    body = body.replace("$$$__ARTICLE_TITLE__$$$", data[3].encode('utf-8').strip())
                    body = body.replace("$$$__ARTICLE_FOOTER__$$$", "Nanyang")
                    body = body.replace("$$$__ARTICLE_BODY__$$$", data[7].encode('utf-8').strip())

                    email_body+=body

            # Remove last ,
            all_ids = all_ids[:-1]

            with open (settings.get('EMAIL_TEMPLATES')+"/email_template_header.html", "r") as myfile:
                email_header=myfile.read()
            email_header = email_header.replace("$$$__SERVER_URL__$$$", self.admin_website_url)
            email_header = email_header.replace("$$$__PUBLISH_ALL__$$$", str(all_ids))
            email_header = email_header.replace("$$$__SOURCE__$$$", "Nanyang")
            email_header = email_header.replace("$$$__DATE__$$$", datetime.datetime.now().strftime('%d %b, %G'))

            with open (settings.get('EMAIL_TEMPLATES')+"/email_template_footer.html", "r") as myfile:
                email_footer=myfile.read()            
            email_footer = email_footer.replace("$$$__SERVER_URL__$$$", self.admin_website_url)

            email = email_header + email_body + email_footer
	    
 	    if len(self.new_inserted_records) > 0 :
            	self.mailer.send(to=["hock@webqom.com","caroline@webqom.com"], subject="Media News: Nanyang", cc=["support@webqom.com"], body=email, mimetype="text/html; charset=UTF-8")
            	#self.mailer.send(to=["hock@webqom.com"], subject="Media News: Nanyang", cc=["hock@webqom.com"], body=email, mimetype="text/html; charset=UTF-8")
        except Exception as e:
            #self.logException(e)
	    print traceback.format_exc()
            
        
