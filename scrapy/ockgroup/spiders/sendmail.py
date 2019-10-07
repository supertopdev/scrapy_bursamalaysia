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
from scrapy.mail import MailSender
import smtplib



class SendMail(CrawlSpider):
    mailer = MailSender(smtphost='smtp.mailgun.org', mailfrom='admin@webqom.com', smtpuser='postmaster@sandbox5e7c85e76172478ba660e330ca839a22.mailgun.org', smtppass='bcaf1a6039f6d2e61a4d289fa84f7bd4', smtpport=587)
    name = 'sendmail'
    base_url = 'http://www.bursamalaysia.com'
    allowed_domains = ['www.bursamalaysia.com','announcements.bursamalaysia.com']
    start_urls = ['http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=0172']
    admin_website_url = "http://medianews.fareastholdingsbhd.com"

    rules = (
        Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=True),
    )

    # def parse_start_url(self, response):
    #     return self.parse_item(response)


    def parse(self, response):
        data = "<html><body><p>Hello</p></body></html>"
        # with open ("../email_template.html", "r") as myfile:
        #     data=myfile.read()
        # print data
        self.mailer.send(to=["hock@webqom.com"], subject="Test Mail", body=data, mimetype="text/html")
        return 1
