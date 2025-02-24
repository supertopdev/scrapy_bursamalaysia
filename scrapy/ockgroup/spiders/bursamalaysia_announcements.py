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
#import pytz
from scrapy.mail import MailSender
import json
import string
import random
import urllib
import xml.sax.saxutils as saxutils

SQL_DB = 'fareasth_bursa'
SQL_HOST = 'localhost'
# SQL_USER = 'root'
# SQL_PASSWD = 'mugen1996'
SQL_USER = 'fareasth_bursa'
SQL_PASSWD = '1410Qf-9Hv.SH(g'


class BursamalaysiaSpider(CrawlSpider):

	name = 'bursamalaysia_announcements'
	base_url = 'http://www.bursamalaysia.com'
	allowed_domains = ['www.bursamalaysia.com','announcements.bursamalaysia.com','ws.bursamalaysia.com']
	start_urls = ['http://ws.bursamalaysia.com/market/listed-companies/company-announcements/#/?=&company=5029&page=1']

	rules = (
		Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=False),
	)

	drive = None

	def parse(self, response):
		try:
			page_count=1
			base_crawl_url="http://ws.bursamalaysia.com/market/listed-companies/company-announcements/#/?=&company=5029&page="
			actual_crawl_url = str(base_crawl_url) + str(page_count)
			yield Request(url=actual_crawl_url,callback=self.getAnnouncements, meta={'page_count':page_count,'base_crawl_url':base_crawl_url})
		except Exception as e:
			f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
			f.write('\n\n%s' %(response.url))
			traceback.print_exc(file=f)
			f.close()


	def get_cookies(self,url):
		#self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
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


	def getAnnouncements(self, response):
		try:

			base_crawl_url = response.meta['base_crawl_url']
			page_count = response.meta['page_count']
			actual_crawl_url = str(base_crawl_url) + str(page_count)
			
			string = response.body.decode('utf-8')
			json_obj = json.loads(string)

			dataTable = Selector(text = json_obj["html"])
			for record in dataTable.css("table.bm_dataTable > tbody > tr"):
				column = record.xpath("td")
				date_of_publishing =  column[1].xpath("text()").extract()[0]
				company_name = column[2].xpath("a/text()").extract()[0]
				link_to_announcement = column[3].xpath("a/@href").extract()[0]
				crawl_url = ''.join(["http://www.bursamalaysia.com",link_to_announcement])

				CONN = MySQLdb.connect(host=SQL_HOST, user=SQL_USER, passwd=SQL_PASSWD, db=SQL_DB, charset='utf8')
				CURSOR = CONN.cursor()
				CURSOR.execute("""SELECT * FROM announcements WHERE date_of_publishing='%s' and linktoarticle_on_indexpage='%s'"""%(str(date_of_publishing),
								str(crawl_url)
				))				   
				if CURSOR.rowcount == 0:
					print " CALLING FETCH PAGE FOR URL ", str(crawl_url)
					yield Request(url=crawl_url, callback=self.fetchPage, meta={'date_of_publishing':date_of_publishing, 'company_name':company_name})
				else:
					print "SKIPED: ", crawl_url

			sel = Selector(text = json_obj["pagination"])
			next_page = sel.xpath('//a[@class="bm_next"]')

			if next_page :
				print "FETCHING NEXT PAGE "
				page_count=page_count+1
				actual_crawl_url = str(base_crawl_url) + str(page_count)
				yield Request(dont_filter=True, url=actual_crawl_url,callback=self.getAnnouncements, meta={'page_count':page_count,'base_crawl_url':base_crawl_url})
		#return 1
			
		except Exception as e:
			f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
			f.write('\n\n%s' %(response.url))
			traceback.print_exc(file=f)
			f.close()

	def fetchPage(self, response):
		try:
			print "FETCHED PAGE ", response.url
			sel = Selector(response)
			iframe_src=sel.xpath('//iframe[@id="bm_ann_detail_iframe"]/@src').get()
			yield Request(dont_filter=True, url=iframe_src,
						meta={'date_of_publishing':response.meta['date_of_publishing'],
						'linktoarticle_on_indexpage':response.url},
						callback=self.fetchIframe)
			
		except Exception as e:
			f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
			f.write('\n\n%s' %(response.url))
			traceback.print_exc(file=f)
			f.close()


	def fetchIframe(self, response):
		try:
			# Using Selenium webdrive
			options = webdriver.ChromeOptions()
			options.add_argument('--headless')
			driver = webdriver.Chrome(chrome_options=options)
		
			driver.get(response.url)
			# #reduce(lambda r, d: r.update(d) or r, cookies, {})
			print "FETCHED IFRAME ", response.url
			sel = Selector(text=driver.page_source.encode('utf-8'))
			content = sel.xpath('//div[@id="main"]').extract()
			title = sel.xpath('//div[@id="main"]/h3/text()').extract()
			f = open(BursamalaysiaSpider.name+'-logHtml.txt', 'a')
			f.write('\n\n%s' %(response.body))
			f.close()
			if type(title) in [list,tuple]:
				if not title:
					print "TITLE -------", title
					title = ""
				else:
					title = title[0]


			#find category of announcement
			table_lhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentLabelH"]/text()').extract()
			table_rhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentDataH"]')
			category_of_announcement = ""
			referenceno_of_announcement = ""
			for i in range(len(table_lhs)):
				print "",table_lhs[i],"-",table_rhs[i]
				if table_lhs[i] == "Category":
					category_of_announcement = table_rhs[i].xpath('text()').extract()[0]
				if table_lhs[i] == "Reference No" or table_lhs[i] == "Reference Number":
					referenceno_of_announcement = table_rhs[i].xpath('text()').extract()[0]

			table_lhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentLabel"]/text()').extract()
			table_rhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentData"]')
			for i in range(len(table_lhs)):
				print "",table_lhs[i],"-",table_rhs[i]
				if table_lhs[i] == "Category":
					category_of_announcement = table_rhs[i].xpath('text()').extract()[0]
				if table_lhs[i] == "Reference No" or table_lhs[i] == "Reference Number":
					referenceno_of_announcement = table_rhs[i].xpath('text()').extract()[0]


			print "----------------RECORD INSERTED--------------------------"

			pdf = sel.xpath('//div[@class="attachment fixed"]/descendant::p/a/@href')
			domain = urlparse(response.url)
			path_to_file_on_disk = ""
			# fullurl = urljoin(domain.scheme,domain.hostname)

			print "Getting URL  ",pdf
			file_location = ""
			if len(content)>0:
					html_content = content[0].strip()
			else:
				html_content = ""

				if len(pdf) >0:
					file_location = pdf.extract()[0].strip().encode('ascii', 'ignore')
					path_to_file_on_disk = ''.join([response.meta['date_of_publishing'],"_",file_location.rsplit('=',1)[1]])
					path_to_file_on_disk="_".join(path_to_file_on_disk.split())
					path_to_file_on_disk="".join([path_to_file_on_disk,".pdf"])
					hostname = urlparse(response.url).hostname
					#file_location_urlencoded = urllib.quote(file_location.encode('ascii', 'ignore').strip())
					#file_location = urllib.quote(file_location.strip())
					path_to_file_on_disk = path_to_file_on_disk.strip()
					print "Replacing [",file_location,"] with [",path_to_file_on_disk,"]"
					html_content = html_content.replace(saxutils.escape(file_location),path_to_file_on_disk)

					yield OckgroupItem(file_urls=[{"file_url":''.join([domain.scheme,"://",domain.netloc,file_location]),
										"file_name":path_to_file_on_disk}])

			CONN = MySQLdb.connect(
						host=SQL_HOST,
						user=SQL_USER,
						passwd=SQL_PASSWD,
						db=SQL_DB,
						charset='utf8'				
						)
			CURSOR = CONN.cursor()
			CURSOR.execute("""INSERT INTO  announcements(title,date_of_publishing,html,direct_linktoarticle_iframe,linktoarticle_on_indexpage,category,attachment_location_ondisk,reference_no, short_description, company_name)   
						VALUES ('%s','%s','%s','%s','%s','%s','%s','%s', '', '')"""%(CONN.escape_string(str(title.encode('ascii', 'ignore').decode('ascii'))),response.meta['date_of_publishing'],CONN.escape_string(str(html_content.encode('ascii', 'ignore').decode('ascii'))),
							CONN.escape_string(str(response.url.encode('ascii', 'ignore').decode('ascii'))),
							response.meta['linktoarticle_on_indexpage'],
							CONN.escape_string(str(category_of_announcement.encode('ascii', 'ignore').decode('ascii'))),
							path_to_file_on_disk, CONN.escape_string(str(referenceno_of_announcement.encode('ascii', 'ignore').decode('ascii')))))

			CONN.commit()

		except Exception as e:
			f = open(BursamalaysiaSpider.name+'-log.txt', 'a')
			f.write('\n\n%s' %(response.url))
			traceback.print_exc(file=f)
			f.close()
		finally:
			driver.quit()
		
