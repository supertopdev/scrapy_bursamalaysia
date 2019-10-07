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



SQL_DB = 'ocknetmy_chart'
SQL_TABLE = 'ohlc'
SQL_HOST = '103.246.89.162'
SQL_USER = 'ocknetmy_chart'
SQL_PASSWD = 'f#792@btWw#c'


class BursamalaysiaSpider(CrawlSpider):
    name = 'bmr'
    base_url = 'http://www.bursamalaysia.com'
    allowed_domains = ['www.bursamalaysia.com','announcements.bursamalaysia.com']
    start_urls = ['http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172']

    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=False),
    )


    # def parse_start_url(self, response):
    #     return self.parse_item(response)



    def parse(self, response):
        import smtplib


        sender = 'alert@ock.net.my'
        receiver = ['hock@webqom.com']

        message = """From: Alert<alert@ock.net.my>
        \r\nTo: Hock<hock@webqom.com>
        \r\nReply-To: <alert@ock.net.my>
        \r\nReturn-Path: <alert@ock.net.my>
        \r\nMessage-ID: <1233543434@ock.net.my>
        \r\nDate: 29-12-2014 23:16:54
        \r\nMIME-Version: 1.0
        \r\nX-Priority: 3
        \r\nX-MSMail-Priority: Normal
        \r\nContent-Type: text/html; charset=iso-8859-1
        \r\nSubject: SMTP e-mail test
        \r\n<html><head><title>Hello</title></head><body>Hi,<br/><br/>
        Greetings!!! <br/><br/>
 
Regards,<br/>
Hock <br/>


</body>
</html>"""

        try:
            print("trying host and port...")

            smtpObj = smtplib.SMTP('mail.ock.net.my', 587)
            smtpObj.login("alert@ock.net.my", "1Xro2$6)V]NB(")

            print("sending mail...")

            smtpObj.sendmail(sender, receiver, message)

            print("Succesfully sent email")

        except smtplib.SMTPException:
            print("Error: unable to send email")
            import traceback
            traceback.print_exc()        
        # mailer = MailSender()
        # print "--------- Sending mail ---------"
        # mailer.send(to=["hock@webqom.com"], subject="Some subject", body="Some body", cc=["hock@webqom.com"])
        # print "--------- Done ---------"
        # return Request(url="http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172",
        #     cookies=self.get_cookies("http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172"),
        #     callback=self.parse_start_url)



    def get_cookies(self,url):
        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
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
            # item = OckgroupItem()

            print "-----------------"
            #Stock Quote Section (bm_quad bm_stock_quote)
            # get stock quote last update time
            last_update_time = sel.xpath('//div[@class="bm_quad bm_stock_quote"]/p[@class="bm_date bm_delay"]/text()').extract()
            summary_table_lhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/th[@scope="row"]/text()').extract()
            summary_table_rhs = sel.xpath('//table[@class="bm_table bm_wspace_bottom"]/descendant::tr/td/text()').extract()
            adjustment_close= sel.xpath('//p[@class="bm_stock_overview"]/descendant::span/text()').extract()
            
            ock_open=""
            ock_close=""
            ock_high=""
            ock_low=""
            ock_adjustment=""
            ock_volume=""   

            if(len(adjustment_close)>0):
                adjustment_close = adjustment_close[0]
                ock_close=adjustment_close[0:adjustment_close.index("(",0)].strip()
                ock_adjustment = adjustment_close[adjustment_close.index("(",0)+1:adjustment_close.index(")",0)].strip()
                print "Close = ",ock_close
                print "Adjustment = ",ock_adjustment
            for i in range(len(summary_table_lhs)):
                if summary_table_lhs[i] == "Open":
                    print "Open = ",summary_table_rhs[i]
                    ock_open = summary_table_rhs[i];
                if summary_table_lhs[i] == "High":
                    print "High = ",summary_table_rhs[i]
                    ock_high = summary_table_rhs[i];
                if summary_table_lhs[i] == "Low":
                    print "Low = ", summary_table_rhs[i]
                    ock_low = summary_table_rhs[i];
                if summary_table_lhs[i].startswith("Volume"):
                    print "Volume = ", summary_table_rhs[i]
                    ock_volume = summary_table_rhs[i].replace(",","");                    

            today_date = time.strftime('%d-%m-%Y') 

            # CONN = MySQLdb.connect(
            #              host=SQL_HOST,
            #              user=SQL_USER,
            #              passwd=SQL_PASSWD,
            #              db=SQL_DB)
            # CURSOR = CONN.cursor()
            # TEST = "SELECT COUNT(1) FROM ohlc WHERE date = %s"
            # CURSOR.execute(TEST,[today_date])
            # if CURSOR.fetchone()[0]:
            #     CURSOR.execute("""UPDATE ohlc set open=%s,high=%s,low=%s,close=%s,volume=%s,adj=%s where date=%s  """, (ock_open,ock_high,ock_low,ock_close,ock_volume,ock_adjustment,today_date))
            #     print "***** Record Updated *****"
            # else:
            #     CURSOR.execute("""INSERT into ohlc (open,high,low,close,volume,adj,date) values (%s,%s,%s,%s,%s,%s,%s)""", (ock_open,ock_high,ock_low,ock_close,ock_volume,ock_adjustment,today_date))   
            #     print "***** Record Inserted *****"
            # CONN.commit()
            self.driver.quit() 
            return 1
        except Exception as e:
            f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
            f.write('\n\n%s' %(response.url))
            traceback.print_exc(file=f)
            f.close()
            self.driver.quit()
            
        
