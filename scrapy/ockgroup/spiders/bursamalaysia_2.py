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
import xml.sax.saxutils as saxutils
import MySQLdb
import MySQLdb.cursors
import re

SQL_DB = 'fareasth_bursa'
SQL_HOST = 'localhost'
# SQL_USER = 'root'
# SQL_PASSWD = ''
SQL_USER = 'fareasth_bursa'
SQL_PASSWD = '1410Qf-9Hv.SH(g'


class BursamalaysiaSpider(CrawlSpider):
  name = 'bursamalaysia2'
  base_url = 'http://www.bursamalaysia.com'
  allowed_domains = ['www.bursamalaysia.com', 'announcements.bursamalaysia.com']
  start_urls = [
    'http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029']

  rules = (
    Rule(SgmlLinkExtractor(allow=(), deny=()), callback='parse_start_url', follow=True),
  )

  # def parse_start_url(self, response):
  #     return self.parse_item(response)


  def parse(self, response):
    page_count = 1
    base_crawl_url = "http://www.bursamalaysia.com/market/listed-companies/list-of-companies/plc-profile.html?stock_code=5029"
    try:
      return Request(url=base_crawl_url,
                     cookies=self.get_cookies(base_crawl_url),
                     meta={'page_count': page_count, 'base_crawl_url': base_crawl_url},
                     callback=self.parse_start_url)
    except Exception as e:
      f = open(BursamalaysiaSpider.name + '-log.txt', 'a')
      f.write('\n\n%s' % (response.url))
      traceback.print_exc(file=f)
      f.close()

  def get_cookies(self, url):
    self.driver = webdriver.PhantomJS(executable_path='/home/fareastholdingsb/yo/phantomjs-1.9.2-linux-x86_64/bin/phantomjs')
    self.driver.get(url)
    # elem = self.driver.find_element_by_name("Continue")
    # elem.click()
    # time.sleep(15)
    cookies = self.driver.get_cookies()
    # #reduce(lambda r, d: r.update(d) or r, cookies, {})

    return cookies

  def parse_start_url(self, response):
    page_count = response.meta['page_count']
    base_crawl_url = response.meta['base_crawl_url']
    try:
      records = response.xpath('//table[contains(@class, "bm_center")]')[0].xpath('.//tbody//tr')
      for record in records:
        column = record.xpath("td")
        date_of_publishing = column[0].xpath("text()").extract()[0]
        company_name = column[1].xpath("a/text()").extract()[0]
        link_to_announcement = column[1].xpath("a/@href").extract()[0]
        crawl_url = ''.join(["http://www.bursamalaysia.com", link_to_announcement])

        yield Request(url=crawl_url, callback=self.fetchPage,
                          meta={'date_of_publishing': date_of_publishing, 'company_name': company_name})

      next_page = response.xpath('//a[@class="bm_next"]').extract()[0]

      if next_page:
        print "FETCHING NEXT PAGE "
        page_count = page_count + 1
        actual_crawl_url = str(base_crawl_url) + str(page_count)
        yield Request(dont_filter=True, url=actual_crawl_url, callback=self.getAnnouncements,
                      meta={'page_count': page_count, 'base_crawl_url': base_crawl_url},
                      cookies=self.get_cookies(actual_crawl_url)
                      )
    except Exception as e:
      f = open(BursamalaysiaSpider.name + '-log.txt', 'a')
      f.write('\n\n%s' % (response.url))
      traceback.print_exc(file=f)
      f.close()

  def fetchPage(self, response):
    try:
      print "FETCHED PAGE ", response.url
      sel = Selector(response)
      iframe_src = sel.xpath('//iframe[@id="bm_ann_detail_iframe"]/@src').extract()[0]
      yield Request(dont_filter=True, url=iframe_src,
                    meta={'date_of_publishing': response.meta['date_of_publishing'],
                          'linktoarticle_on_indexpage': response.url},
                    cookies=self.get_cookies(iframe_src),
                    callback=self.fetchAnnouncementIframe)

    except Exception as e:
      f = open(BursamalaysiaSpider.name + '-log.txt', 'a')
      f.write('\n\n%s' % (response.url))
      traceback.print_exc(file=f)
      f.close()

  def fetchAnnouncementIframe(self, response):
    try:
      sel = Selector(response)
      content = sel.xpath('//div[@id="main"]').extract()
      title = sel.xpath('//div[@id="main"]/h3/text()').extract()
      if type(title) in [list, tuple]:
          if not title:
              print "TITLE -------", title
              title = ""
          else:
              title = title[0]

      # find category of announcement
      table_lhs = sel.xpath(
          '//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentLabelH"]/text()').extract()
      table_rhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentDataH"]')
      category_of_announcement = ""
      referenceno_of_announcement = ""
      for i in range(len(table_lhs)):
          print "", table_lhs[i], "-", table_rhs[i]
          if table_lhs[i] == "Category":
              category_of_announcement = table_rhs[i].xpath('text()').extract()[0]
          if table_lhs[i] == "Reference No" or table_lhs[i] == "Reference Number":
              referenceno_of_announcement = table_rhs[i].xpath('text()').extract()[0]

      table_lhs = sel.xpath(
          '//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentLabel"]/text()').extract()
      table_rhs = sel.xpath('//div[@class="ven_announcement_info"]/table/descendant::td[@class="formContentData"]')
      for i in range(len(table_lhs)):
          print "", table_lhs[i], "-", table_rhs[i]
          if table_lhs[i] == "Category":
              category_of_announcement = table_rhs[i].xpath('text()').extract()[0]
          if table_lhs[i] == "Reference No" or table_lhs[i] == "Reference Number":
              referenceno_of_announcement = table_rhs[i].xpath('text()').extract()[0]

      print "----------------RECORD INSERTED--------------------------"
      pdf = sel.xpath('//div[@class="attachment fixed"]/descendant::p[@class="att_download_pdf"]/a/@href')
      domain = urlparse(response.url)
      # fullurl = urljoin(domain.scheme,domain.hostname)


      print "Getting URL  ", pdf
      file_location = ""
      if len(content) > 0:
        html_content = content[0].strip()
      else:
        html_content = ""

        if len(pdf) > 0:
            hostname = urlparse(response.url).hostname
            filelist = []
            filelist.append(''.join([domain.scheme, "://", domain.netloc, pdf.extract()[0].strip()]))
            file_location = pdf.extract()[0].strip().encode('ascii', 'ignore')
            path_to_file_on_disk = ''.join(
            [response.meta['date_of_publishing'], "_", file_location.rsplit('=', 1)[1]])
            path_to_file_on_disk = "_".join(path_to_file_on_disk.split())
            path_to_file_on_disk = "".join([path_to_file_on_disk, ".pdf"])
            # file_location_urlencoded = urllib.quote(file_location.encode('ascii', 'ignore').strip())
            # file_location = urllib.quote(file_location.strip())
            path_to_file_on_disk = path_to_file_on_disk.strip()
            print "Replacing [", file_location, "] with [", path_to_file_on_disk, "]"
            html_content = html_content.replace(saxutils.escape(file_location), path_to_file_on_disk)

            yield OckgroupItem(
            file_urls=[{"file_url": ''.join([domain.scheme, "://", domain.netloc, file_location]),
                        "file_name": path_to_file_on_disk}])
          # print "Store path =>" ,myitem['files'][0]['path']

      CONN = MySQLdb.connect(
          host=SQL_HOST,
          user=SQL_USER,
          passwd=SQL_PASSWD,
          db=SQL_DB,
          charset='utf8'
      )
      CURSOR = CONN.cursor()
      CURSOR.execute("""INSERT INTO  announcements(title,date_of_publishing,html,direct_linktoarticle_iframe,linktoarticle_on_indexpage,category,attachment_location_ondisk,reference_no, short_description, company_name)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s', '', '')""" % (
      CONN.escape_string(str(title.encode('ascii', 'ignore').decode('ascii'))),
      response.meta['date_of_publishing'],
      CONN.escape_string(str(html_content.encode('ascii', 'ignore').decode('ascii'))),
      CONN.escape_string(str(response.url.encode('ascii', 'ignore').decode('ascii'))),
      response.meta['linktoarticle_on_indexpage'],
      CONN.escape_string(str(category_of_announcement.encode('ascii', 'ignore').decode('ascii'))),
      path_to_file_on_disk,
      CONN.escape_string(str(referenceno_of_announcement.encode('ascii', 'ignore').decode('ascii')))))

      CONN.commit()
          # print "Content = ",content
    except Exception as e:
      f = open(BursamalaysiaSpider.name + '-log.txt', 'a')
      f.write('\n\n%s' % (response.url))
      traceback.print_exc(file=f)
      f.close()