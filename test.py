from multiprocessing.dummy import Process

import requests

from 模板.crawler_template import Runner


DEBUG = False
HEADLESS = True
RAISE_EXCEPTION = False
KEYWORDS = ['望城县', '长沙市望城区', '望城区档案']
DRIVER_PATH = '/Users/mac/Downloads/chromedriver'


# 人民日报
class RenMinRiBaoRunner(Runner):
    def get_page_item_links(self, kw, page=1, previous_links=None, total_links=None):
        if not total_links:
            total_links = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }
        self.url_template = 'http://search.people.cn/api-search/front/search'
        json = {"key": kw, "page": page, "limit": 10, "hasTitle": True, "hasContent": True, "isFuzzy": True, "type": 0,
                "sortType": 2, "startTime": 0, "endTime": 0}
        content = requests.post(self.url_template, headers=headers, json=json).json()
        records = content.get('data').get('records')
        links = [record.get('url') for record in records]
        # print('links', links)
        # links = html.xpath(self.links_xpath)
        if not links:
            return total_links

        for link in links:
            # print('put %s into queue' % link)
            self.queue.put(link)

        # print('links', links)
        total_links += links
        return self.get_page_item_links(kw, page=page + 1, previous_links=links[:], total_links=total_links[:])


rmrb = RenMinRiBaoRunner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='',
    paragraph_xpath_list=[
        '//div[@class="rm_txt_con cf"]/p//text()',
        '//div[@class="clearfix w1000_320 text_con"]//p/text()',
        '//div[contains(@class, "clearfix")]//p/text()',
    ],
    debug=DEBUG,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
        '//h2/text()',
    ]
    # test_links=['http://society.people.com.cn/n1/2020/1219/c1008-31972132.html', 'http://hb.people.com.cn/n2/2020/1219/c194063-34483122.html', 'http://hn.people.com.cn/n2/2021/0506/c356887-34711408.html', 'http://hn.people.com.cn/n2/2021/0722/c356886-34832796.html', 'http://hn.people.com.cn/n2/2020/1229/c356887-34500737.html', 'http://gz.people.com.cn/n2/2021/0423/c361324-34691384.html', 'http://finance.people.com.cn/n1/2021/0619/c1004-32134821.html', 'http://hn.people.com.cn/n2/2021/0218/c356886-34581110.html', 'http://hn.people.com.cn/n2/2021/0727/c336521-34840279.html', 'http://hn.people.com.cn/n2/2021/0714/c356886-34819827.html']
)


# 望城门户
wcmh = Runner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='http://searching.hunan.gov.cn/hunan/971206000/news?q={kw}&searchfields=&sm=1&columnCN=&iszq=&aggr_iszq=&p={page}&timetype=timeqb',
    links_xpath='//div[@class="title "]/a/@href',
    paragraph_xpath_list=[
        '//div[@class="pages_content TRS_Editor"]/div//p//text()'
    ],
    debug=DEBUG,
    headless=HEADLESS,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
    ]
)


# 清廉长沙
class SelfRunner(Runner):
    def get_page_item_links(self, kw, page=0, total_links=None):
        if not total_links:
            total_links = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Cookie': '_gscu_2138955816=32544007ji8gtf25; _gscbrs_2138955816=1; ICMS_VISIT_FLAG_COOKIE=2021-9-25_39009615; Hm_lvt_1addf79e03854c60736c4faedb476b73=1632544007; Hm_lpvt_1addf79e03854c60736c4faedb476b73=1632544007; _gscs_2138955816=32544007dgkyxx25|pv:4',
            'Referer': 'http://www.ljcs.gov.cn/search.html?searchkey=%E6%9C%9B%E5%9F%8E%E5%8E%BF',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://www.ljcs.gov.cn'
        }
        self.url_template = 'http://www.ljcs.gov.cn/default.php?client=client&mod=document_news&f=interface&a=news_list'
        data = {
            'search_key': kw,
            'siteid': '1',
            'channel_id': '',
            'state': '30',
            'p': '%s' % page,
            'ps': '20',
            'is_encrypt': '0',
            'only_client': '0',
            'haschild': '0',
            'skip_index': '0'
        }
        res = requests.post(self.url_template, headers=headers, data=data).json()
        result = res.get('result')
        links = ['http://www.ljcs.gov.cn/' + item.get('DocumentNewsUrl') for item in result or []]
        print('links', links)
        # links = html.xpath(self.links_xpath)
        if not links:
            return total_links

        for link in links:
            # print('put %s into queue' % link)
            self.queue.put(link)

        # print('links', links)
        total_links += links
        return self.get_page_item_links(kw, page=page + 1, total_links=total_links[:])


qlcs = SelfRunner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='',
    paragraph_xpath_list=['//div[@class="rm_txt_con cf"]/p//text()',
                          '//div[@class="am-article-bd"]/div[contains(@style, "align") or @align!=""]',
                          '//div[@class="article"]//p//text()'
                          ],
    debug=DEBUG,
    headless=HEADLESS,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
        '//div[@class="maintitle"]/text()'
    ]
    # test_links=['']
)


# 湖南日报
hnrb = Runner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='http://so.voc.com.cn/cse/search?q={kw}&p={page}&s=7639422230623402302&sti=1440',
    # url_template='http://so.voc.com.cn/cse/search?q={kw}&p={page}&s=7639422230623402302',
    links_xpath='//h3[@class="c-title"]/a/@href',
    paragraph_xpath_list=[
        '//div[@id="content"]//p/text()',
        '//div[@class="nei"]/ct/p//text()',
    ],
    debug=DEBUG,
    headless=HEADLESS,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
    ],
    start_page=0
)


# 湖南红网
hnhw = Runner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='https://news-search.rednet.cn/Search?q={kw}&p={page}',
    links_xpath='//div[@class="result-footer"]/a/@href',
    paragraph_xpath_list=[
        '//article//p/text()',
        '//div[@class="nei"]/ct/p//text()',
    ],
    debug=DEBUG,
    headless=HEADLESS,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
    ]
)


# 长沙晚报
cswb = Runner(
    keywords=KEYWORDS,
    driver_path=DRIVER_PATH,
    url_template='https://so.icswb.com/default.php?mod=search&m=no&syn=no&f=_all&s=s_show_date_DESC&temp=&p={page}&ps=20&site_id=2&range=&search_target=1&search_key={kw}&search_column=&search_channel_id=0',
    links_xpath='//h3/a/@href',
    paragraph_xpath_list=[
        '//article[@class="am-article"]//p/text()',
        '//div[@class="nei"]/ct/p//text()',
    ],
    debug=DEBUG,
    headless=HEADLESS,
    raise_exception=RAISE_EXCEPTION,
    title_xpath_list=[
        '//h1/text()',
    ]
)


if __name__ == '__main__':
    targets = [rmrb.run, wcmh.run, qlcs.run, hnrb.run, hnhw.run, cswb.run]
    processes = []

    for t in targets:
        processes.append(Process(target=t))

    for p in processes:
        p.daemon = False

    for p in processes:
        p.start()

    for p in processes:
        p.join()
