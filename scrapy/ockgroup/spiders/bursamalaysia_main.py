#!/usr/bin/env python
import time
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
import smtplib
import re
from scrapy.mail import MailSender

SQL_DB = 'fareasth_bursa'
SQL_TABLE = 'corporate_stockinfo'
SQL_HOST = 'localhost'
SQL_USER = 'fareasth_bursa'
SQL_PASSWD = '1410Qf-9Hv.SH(g'


class BursamalaysiaSpider(CrawlSpider):
    mailer = MailSender(smtphost='smtp.mailgun.org', mailfrom='admin@webqom.com', smtpuser='postmaster@sandbox5e7c85e76172478ba660e330ca839a22.mailgun.org', smtppass='bcaf1a6039f6d2e61a4d289fa84f7bd4', smtpport=587)
    name = 'bursamalaysia_main'
    base_url = 'http://www.bursamalaysia.com'
    allowed_domains = ['www.bursamalaysia.com','announcements.bursamalaysia.com']
    start_urls = ['http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029']

    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=True),
    )


    # def parse_start_url(self, response):
    #     return self.parse_item(response)


    def parse(self, response):
	try:
		return Request(url="http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029",
            	cookies=self.get_cookies("http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029"),
            	callback=self.parse_start_url)
        except Exception as e:
            self.mailer.send(to=["hock@webqom.com"], subject="Crawl Failed", body=traceback.format_exc(), cc=[])
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()	


    def get_cookies(self,url):
        self.driver = webdriver.PhantomJS(executable_path='/home/fareastholdingsb/yo/phantomjs-1.9.2-linux-x86_64/bin/phantomjs')
        #self.driver = webdriver.PhantomJS(executable_path='/home/fareastholdingsb/yo/phantomjs-1.9.8-linux-x86_64/bin/phantomjs')
        self.driver.get(url)
        # elem = self.driver.find_element_by_name("Continue")
        # elem.click()
        time.sleep(15)
        cookies = self.driver.get_cookies()
        # #reduce(lambda r, d: r.update(d) or r, cookies, {})

        return cookies

    def parse_start_url(self, response):
        try:
            
        
            sel = Selector(response)
            item = OckgroupItem()

            print "-----------------"
            #Stock Quote Section (bm_quad bm_stock_quote)
            # get stock quote last update time
	
            #last_update_time = sel.xpath('//div[@class="bm_quad bm_stock_quote"]/p[@class="bm_date bm_delay"]/text()').extract()
            summary_table_lhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/th[@scope="row"]/text()').extract()
            summary_table_rhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/td/text()').extract()
            #adjustment_close= sel.xpath('//p[@class="bm_stock_overview"]/descendant::span/text()').extract()

            fehb_stock_code=""
	    fehb_stock_name=""
	    fehb_sector=""
  	    fehb_listing=""   

            fehb_stock_name = sel.xpath('//img[@class="bm_coy_logo"]/@alt').extract()
            #if(len(adjustment_close)>0):
                #adjustment_close = adjustment_close[0]
                #ock_close=adjustment_close[0:adjustment_close.index("(",0)].strip()
                #ock_adjustment = adjustment_close[adjustment_close.index("(",0)+1:adjustment_close.index(")",0)].strip()
                #print "Close = ",ock_close
                #print "Adjustment = ",ock_adjustment
	    if len(fehb_stock_name)>0:
		fehb_stock_name=ock_stock_name[0].split(" ")
		temp_name=""
		for item in fehbstock_name:
			if re.match(r"^[a-zA-Z0-9_]*$",item):
				temp_name+=item+" "
	    	print "Stock Name =", temp_name
		fehb_stock_name=temp_name
            for i in range(len(summary_table_lhs)):
                #if summary_table_lhs[i] == "Open":
                #    print "Open = ",summary_table_rhs[i]
		#    ock_open = summary_table_rhs[i];
                #if summary_table_lhs[i] == "High":
                #    print "High = ",summary_table_rhs[i]
		#    ock_high = summary_table_rhs[i];
                #if summary_table_lhs[i] == "Low":
                #    print "Low = ", summary_table_rhs[i]
		#    ock_low = summary_table_rhs[i];
                #if summary_table_lhs[i].startswith("Volume"):
                #    print "Volume = ", summary_table_rhs[i]
                #    ock_volume = summary_table_rhs[i].replace(",","");                    
                if summary_table_lhs[i] == "Stock Code":
                    print "Stock Code = ", summary_table_rhs[i]
                    fehb_stock_code = summary_table_rhs[i].replace(",","");                    
                if summary_table_lhs[i] == "Sector":
                    print "Sector = ", summary_table_rhs[i]
                    fehb_sector = summary_table_rhs[i].replace(",","");                    
                if summary_table_lhs[i] == "Market":
                    print "Listing = ", summary_table_rhs[i]
                    fehb_listing = summary_table_rhs[i].replace(",","");                    

            today_date = time.strftime('%d-%m-%Y') 

            CONN = MySQLdb.connect(
                         host=SQL_HOST,
                         user=SQL_USER,
                         passwd=SQL_PASSWD,
                         db=SQL_DB)
            CURSOR = CONN.cursor()
            #TEST = "SELECT COUNT(1) FROM ohlc WHERE date = %s"
            #CURSOR.execute(TEST,[today_date])
            #if CURSOR.fetchone()[0]:
            #    CURSOR.execute("""UPDATE ohlc set open=%s,high=%s,low=%s,close=%s,volume=%s,adj=%s where date=%s  """, (ock_open,ock_high,ock_low,ock_close,ock_volume,ock_adjustment,today_date))
            #    print "***** Record Updated *****"
            #else:
            CURSOR.execute("""INSERT into 'corporate_stockinfo' (stock_name,stock_code,listing,sector) values (%s,%s,%s,%s)""", (fehb_stock_name,fehb_stock_code,fehb_listing,fehb_sector))   
            print "***** Record Inserted *****"
            updated_date_time = time.strftime('%d-%m-%Y %H:%M:%S') 
            f = open('UpdatedTime_Main.txt', 'a')
            f.write('\n\n%s' %updated_date_time)
            f.write('\nStock Name=%s\nStock Code=%s\nListing=%s\nSector=%s'%(ock_stock_name,ock_stock_code,ock_listing,ock_sector))
            traceback.print_exc(file=f)
            f.close()
            CONN.commit() 
	    self.driver.quit()
	    #self.mailer.send(to=["hock@webqom.com"], subject="Crawl Success Main", body="", cc=[])
            return 1
        except Exception as e:

            
	    self.driver.quit()
	    f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()
	    print traceback.format_exc()
	    self.mailer.send(to=["hock@webqom.com"], subject="Crawl Failed", body=traceback.format_exc(), cc=[])
            print "Error"

