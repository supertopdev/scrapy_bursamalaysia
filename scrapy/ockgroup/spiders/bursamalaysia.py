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


SQL_DB = 'fareasth_chart'
SQL_TABLE = 'ohlc'
SQL_HOST = 'localhost'
SQL_USER = 'fareasth_chart'
SQL_PASSWD = '142KS(p([i{ZV9Q'


class BursamalaysiaSpider(CrawlSpider):
    name = 'bursamalaysia'
    base_url = 'http://www.bursamalaysia.com'
    allowed_domains = ['www.bursamalaysia.com','announcements.bursamalaysia.com']
    start_urls = ['http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029']
    #start_urls = ['http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172']

    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=True),
    )


    # def parse_start_url(self, response):
    #     return self.parse_item(response)


    def parse(self, response):
	return Request(url="http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029",
	#return Request(url="http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172",
            cookies=self.get_cookies("http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029"),
            #cookies=self.get_cookies("http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172"),
            callback=self.parse_start_url)


    def get_cookies(self,url):
        self.driver = webdriver.PhantomJS(executable_path=r'/home/fareastholdingsb/yo/phantomjs-1.9.2-linux-x86_64/bin/phantomjs', desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
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
            last_update_time = sel.xpath('//div[@class="bm_quad bm_stock_quote"]/p[@class="bm_date bm_delay"]/text()').extract()
            summary_table_lhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/th[@scope="row"]/text()').extract()
            summary_table_rhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/td/text()').extract()
            adjustment_close= sel.xpath('//p[@class="bm_stock_overview"]/descendant::span/text()').extract()

            fehb_open=""
            fehb_close=""
            fehb_high=""
            fehb_low=""
            fehb_adjustment=""
            fehb_volume=""   

            if(len(adjustment_close)>0):
                adjustment_close = adjustment_close[0]
                fehb_close=adjustment_close[0:adjustment_close.index("(",0)].strip()
                fehb_adjustment = adjustment_close[adjustment_close.index("(",0)+1:adjustment_close.index(")",0)].strip()
                print "Close = ",fehb_close
                print "Adjustment = ",fehb_adjustment

            for i in range(len(summary_table_lhs)):
                if summary_table_lhs[i] == "Open":
                    print "Open = ",summary_table_rhs[i]
		    fehb_open = summary_table_rhs[i];
                if summary_table_lhs[i] == "High":
                    print "High = ",summary_table_rhs[i]
		    fehb_high = summary_table_rhs[i];
                if summary_table_lhs[i] == "Low":
                    print "Low = ", summary_table_rhs[i]
		    fehb_low = summary_table_rhs[i];
                if summary_table_lhs[i].startswith("Volume"):
                    print "Volume = ", summary_table_rhs[i]
                    fehb_volume = summary_table_rhs[i].replace(",","");                    


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
            CURSOR.execute("""INSERT into ohlc (open,high,low,close,volume,adj,date) values (%s,%s,%s,%s,%s,%s,%s)""", (fehb_open,fehb_high,fehb_low,fehb_close,fehb_volume,fehb_adjustment,today_date))   
            print "***** Record Inserted *****"
            updated_date_time = time.strftime('%d-%m-%Y %H:%M:%S') 
            f = open('UpdatedTime.txt', 'a')
            f.write('\n\n%s' %updated_date_time)
            f.write('\n%s\nClose=%s\nAdjustment=%s\nOpen=%s\nHigh=%s\nLow=%s\nVolume=%s'%(updated_date_time,fehb_close,fehb_adjustment,fehb_open,fehb_high,fehb_low,fehb_volume))
            traceback.print_exc(file=f)
            f.close()
            CONN.commit() 
	    self.driver.quit()
            return 1
        except Exception as e:

            
	    self.driver.quit()
	    f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()
	    print traceback.format_exc()
            print "Error"

