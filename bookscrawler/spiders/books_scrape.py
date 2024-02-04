import scrapy

class BooksSpider(scrapy.Spider):
    name='Books'

    
    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/page-1.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        all_books = response.css('article.product_pod')
        for book in all_books:
            
            Source_img = book.css('h3 a::attr(title)').get()
            title = book.css('h3 a::attr(title)').get()
            price = book.css('div.product_price p.price_color::text').get()

            result = {'URL': Source_img,
                      'Title':title,
                      'Price (in £)':price}
            print(result)
            yield result
            
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)