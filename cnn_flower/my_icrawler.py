import sys
from icrawler.builtin import GoogleImageCrawler
if(len(sys.argv) == 3) :
    google_crawler = GoogleImageCrawler(storage={'root_dir': sys.argv[1]})
    google_crawler.crawl(keyword=sys.argv[2], max_num=300)
else :
    print("フォルダ名 検索ワード")
