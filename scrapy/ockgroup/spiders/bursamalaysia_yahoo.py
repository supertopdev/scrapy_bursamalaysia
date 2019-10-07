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
import smtplib
from scrapy.mail import MailSender


# SQL_DB = 'ocknetmy_chart'
# SQL_TABLE = 'ohlc'
# SQL_HOST = '103.246.89.162'
# SQL_USER = 'ocknetmy_chart'
# SQL_PASSWD = 'f#792@btWw#c'

class BursamalaysiaSpider(CrawlSpider):
    SQL_DB = 'fareasth_yahoo'
    SQL_TABLE = 'yahoo'
    SQL_HOST = 'localhost'
    SQL_USER = 'fareasth_bursa'
    SQL_PASSWD = '1410Qf-9Hv.SH(g'

    name = 'bursamalaysia_yahoo'
    base_url = 'http://www.finance.yahoo.com'
    allowed_domains = ['www.finance.yahoo.com']
    start_urls = ['https://finance.yahoo.com/quote/FEHS.KL?p=FEHS.KL']
  # start_urls = ['https://finance.yahoo.com/q;_ylc=X1MDMjE0MjQ3ODk0OARfcgMyBGZyA3VoM19maW5hbmNlX3dlYgRmcjIDc2EtZ3AEZ3ByaWQDBG5fZ3BzAzkEb3JpZ2luA2ZpbmFuY2UueWFob28uY29tBHBvcwM3BHBxc3RyAwRxdWVyeQMwMTcyLktMLARzYWMDMQRzYW8DMQ--?p=http%3A%2F%2Ffinance.yahoo.com%2Fq%3Fs%3D5029.KL%26ql%3D0&fr=uh3_finance_web&uhb=uh3_finance_vert&s=5029.KL']

    mailer = MailSender(smtphost='smtp.mailgun.org', mailfrom='admin@webqom.com', smtpuser='postmaster@sandbox5e7c85e76172478ba660e330ca839a22.mailgun.org', smtppass='bcaf1a6039f6d2e61a4d289fa84f7bd4', smtpport=587)

    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse', follow=False),
    )


    def parse(self, response):
        try:
            sel = Selector(response)
            today_date = time.strftime('%Y-%m-%d %H:%M:%S') 

            prev_close =""
            open_ = ""
            bid = ""
            ask = ""
            one_yr_target = ""
            beta = ""
            next_earnings_date = ""

            volume =""
            avg_volume = ""
            days_range = ""
            fiftytwo_wk_range = ""
            market_cap = ""
            p_e = ""
            eps = ""
            div_yield = ""
            summary_table_lhs = sel.xpath('//div[@id="yfi_quote_summary_data"]/table[@id="table2"]/descendant::tr')
            summary_table_rhs = sel.xpath('//div[@id="yfi_quote_summary_data"]/table[@id="table2"]/descendant::td')
            for i in range(len(summary_table_lhs)):
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Day's Range:"):
                    str = "-";
                    days_range = summary_table_rhs[i].xpath("span/span/text()").extract()
                    days_range = str.join(days_range)
                    print "---> Range => ", days_range
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("52wk Range:"):
                    str = "-";
                    fiftytwo_wk_range = summary_table_rhs[i].xpath("span/text()").extract()
                    fiftytwo_wk_range = str.join(fiftytwo_wk_range)
                    print "---> Range => ", fiftytwo_wk_range
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Volume:"):
                    volume = summary_table_rhs[i].xpath("span/text()").extract()[0]
                    print "----> Volume => ",volume
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Avg Vol"):
                    avg_volume = summary_table_rhs[i].xpath("text()").extract()[0]
                    print "----> Avg Volume => ", avg_volume
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Market Cap:"):
                    market_cap = summary_table_rhs[i].xpath("span/text()").extract()[0]
                    print "---> Market Cap => ", market_cap
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("P/E"):
                    p_e = summary_table_rhs[i].xpath("text()").extract()[0]
                    print "---> P_E => ", p_e
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("EPS"):
                    eps = summary_table_rhs[i].xpath("text()").extract()[0]
                    print "---> EPS => ", eps
                if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Div & Yield:"):
                    div_yield = summary_table_rhs[i].xpath("text()").extract()[0]
                    print "---> Div & Yield => ", div_yield  


            summary_table_lhs = sel.xpath('//div[@id="yfi_quote_summary_data"]/table[@id="table1"]/descendant::tr')
            summary_table_rhs = sel.xpath('//div[@id="yfi_quote_summary_data"]/table[@id="table1"]/descendant::td')
            for i in range(len(summary_table_lhs)):
                try:
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Prev Close:"):
                        print "----> Prev Close: => ",summary_table_rhs[i].xpath("text()").extract()[0]
                        prev_close = summary_table_rhs[i].xpath("text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Open:"):
                        print "----> Open: => ",summary_table_rhs[i].xpath("text()").extract()[0]
                        open_ = summary_table_rhs[i].xpath("text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Bid:"):
                        print "----> Bid: => ",summary_table_rhs[i].xpath("span/text()").extract()[0]
                        bid = summary_table_rhs[i].xpath("span/text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Ask:"):
                        print "----> Ask: => ",summary_table_rhs[i].xpath("span/text()").extract()[0]
                        ask = summary_table_rhs[i].xpath("span/text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("1y Target Est:"):
                        print "----> 1 yr target: => ",summary_table_rhs[i].xpath("text()").extract()[0]
                        one_yr_target = summary_table_rhs[i].xpath("text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Beta:"):
                        print "----> Beta: => ",summary_table_rhs[i].xpath("text()").extract()[0]
                        beta = summary_table_rhs[i].xpath("text()").extract()[0]
                    if summary_table_lhs[i].xpath("th/text()").extract()[0].startswith("Next Earnings Date:"):
                        print "----> Next Earnings Date: => ",summary_table_rhs[i].xpath("text()").extract()[0]
                        next_earnings_date = summary_table_rhs[i].xpath("text()").extract()[0]
                except:
                    pass
                    
            CONN = MySQLdb.connect(
                            host=self.SQL_HOST,
                            user=self.SQL_USER,
                            passwd=self.SQL_PASSWD,
                            db=self.SQL_DB,
                            charset='utf8')
            CURSOR = CONN.cursor()
            CURSOR.execute("""INSERT INTO %s (volume, avg_volume, prev_close, open, bid, ask, 1y_target_est, beta, next_earnings_date, days_range, 52wk_range, market_cap, p_e, eps, div_yield, created_date)   
                            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(self.SQL_TABLE,volume,avg_volume,prev_close,open_,bid,ask,one_yr_target,beta,next_earnings_date,days_range,fiftytwo_wk_range,market_cap,p_e,eps,div_yield,today_date))

            CONN.commit()
            return 1
        except Exception as e:
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
	    self.mailer.send(to=["hock@webqom.com"], subject="Yahoo Crawl Failed", body=traceback.format_exc(), cc=[])
            f.close()
            return 0


    def get_cookies(self,url):
        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
		#self.driver = webdriver.PhantomJS(executable_path='/home/fareastholdingsb/yo/phantomjs-1.9.8-linux-x86_64/bin/phantomjs')
        driver = webdriver.PhantomJS()
        driver.get(url)
        # elem = self.driver.find_element_by_name("Continue")
        # elem.click()
        # time.sleep(15)
        cookies = driver.get_cookies()
        driver.close()
        driver.quit()
        # #reduce(lambda r, d: r.update(d) or r, cookies, {})
        

        return cookies

    def parse_start_url(self, response):
        try:
            
            sel = Selector(response)
            # item = OckgroupItem()

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

        except Exception as e:
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()

        # self.driver.close()            
        # return item                


    def fetchPage(self, response):
        try:
            sel = Selector(response)
            iframe_src=sel.xpath('//iframe[@id="bm_ann_detail_iframe"]/@src').extract()[0]
            yield(Request(url=iframe_src,
                        meta={'date_of_publishing':response.meta['date_of_publishing'],
                        'linktoarticle_on_indexpage':response.url},
                        callback=self.fetchIframe))
            
        except Exception as e:
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()


    def fetchIframe(self, response):
        try:
            
            sel = Selector(response)
            content = sel.xpath('//div[@id="main"]').extract()
            title = sel.xpath('//div[@id="main"]/h3/text()').extract()

            # print "------------------------------------------"
            # print "",response.meta['date_of_publishing']
            # print "",content[0].strip()

            #find category of announcement
            table_lhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentLabelH"]/text()').extract()
            table_rhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentDataH"]')
            category_of_announcement = ""
            referenceno_of_announcement = ""
            for i in range(len(table_lhs)):
                if table_lhs[i] == "Category":
                    category_of_announcement = table_rhs[i].xpath('text()').extract()[0]
                if table_lhs[i] == "Reference No":
                    referenceno_of_announcement = table_rhs[i].xpath('text()').extract()[0]




            print "----------------RECORD NOT - INSERTED--------------------------"

            pdf = sel.xpath('//div[@class="attachment fixed"]/descendant::p/a/@href')
            domain = urlparse(response.url)
            path_to_file_on_disk = ""
            # fullurl = urljoin(domain.scheme,domain.hostname)

            print "Getting URL  ",pdf
            file_location = ""
            html_content = content[0].strip()
            

            if len(pdf) >0:
                file_location = pdf.extract()[0].strip().encode('ascii', 'ignore')
                path_to_file_on_disk = ''.join([response.meta['date_of_publishing'],"_",file_location.rsplit('/',1)[1]])
                path_to_file_on_disk="_".join(path_to_file_on_disk.split())
                hostname = urlparse(response.url).hostname
                
                
                file_location = urllib.quote(file_location.strip())
                path_to_file_on_disk = path_to_file_on_disk.strip()
                print "Replacing [",file_location,"] with [",path_to_file_on_disk,"]"
                html_content = html_content.replace(file_location,path_to_file_on_disk)
                # 

                
                print "======================================"
                print html_content
                # filelist = []
                # filelist.append(''.join([domain.scheme,"://",domain.netloc,pdf.extract()[0].strip()]))
                # myitem = OckgroupItem()
                # myitem["file_urls"] = filelist
                yield OckgroupItem(file_urls=[{"file_url":''.join([domain.scheme,"://",domain.netloc,file_location]),
                                    "file_name":path_to_file_on_disk}])

            CONN = MySQLdb.connect(
                        host="127.0.0.1",
                        port=8889,
                        user="root",
                        passwd="root",
                        db="fareasth_ock",
                        charset='utf8')
            CURSOR = CONN.cursor()
            CURSOR.execute("""INSERT INTO  announcements(title,date_of_publishing,html,direct_linktoarticle_iframe,linktoarticle_on_indexpage,category,attachment_location_ondisk,reference_no)   
                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"""%(CONN.escape_string(str(title[0].encode('ascii', 'ignore').decode('ascii'))),response.meta['date_of_publishing'],CONN.escape_string(html_content.encode('ascii', 'ignore').decode('ascii')),
                            CONN.escape_string(str(response.url.encode('ascii', 'ignore').decode('ascii'))),
                            response.meta['linktoarticle_on_indexpage'],
                            CONN.escape_string(str(category_of_announcement.encode('ascii', 'ignore').decode('ascii'))),
                            path_to_file_on_disk,
                            CONN.escape_string(str(referenceno_of_announcement.encode('ascii', 'ignore').decode('ascii')))))

            CONN.commit()

        except Exception as e:
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()
            self.driver.quit()
            
        
