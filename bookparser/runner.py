from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from bookparser.spiders.labru import LabruSpider
from bookparser.spiders.bk24ru import Bk24ruSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(LabruSpider)
    runner.crawl(Bk24ruSpider)

    reactor.run()