import requests
import re
import lxml.html as html
import os 
 
  

pattern = re.compile(r'^([\.\.\/\\]{9,9})(.*)$')
SUPPORT_LINK_CATEGORY = 'https://books.toscrape.com/'
SUPPORT_LINK_BOOKS = 'https://books.toscrape.com/catalogue/'
MAIN_LINK        = 'https://books.toscrape.com/index.html'
# $x('//div[@class="image-wrapper"]//img/@src').map(x => x.value)
XPATH_CATEGORIES = '//ul[@class="nav nav-list"]/li/ul/li/a/@href'
XPATH_CATEGORIE_NAME = '//div[@class="page-header action"]/h1/text()'
XPATH_BOOK_LINK  = '//article[@class="product_pod"]/*[3]/a/@href'
XPATH_TITLE      = '//article[@class="product_page"]//div[@class="col-sm-6 product_main"]/h1/text()'
XPATH_PRICE      = '//div[@class="col-sm-6 product_main"]/p[@class="price_color"]/text()'
XPATH_SUMMARY    = '//article[@class="product_page"]/p//text()'
XPATH_STOCK      = '//article[@class="product_page"]/div[@class="row"]/div[@class="col-sm-6 product_main"]/p[@class="instock availability"]/text()'




def regular_expression(string):
    found = re.match(pattern,string)
    return str(found.group(2))



def book(link, category):
    try:
        response = requests.get(link)
        if response.status_code != 200:
            raise ValueError(f'Error:   {response.status_code}    book page')
        
        content = response.content.decode('UTF-8')
        parse_home = html.fromstring(content)
        
        try:
            title = parse_home.xpath(XPATH_TITLE)[0]
            stock = parse_home.xpath(XPATH_STOCK)[1].strip()
            summary = parse_home.xpath(XPATH_SUMMARY)[0]
            price = parse_home.xpath(XPATH_PRICE)[0]
            print(f'{title} \n {stock} \n {summary} \n {price}')
   
        except IndexError:
            print(f'ERROR::   {link} \n   \n ')
            return

        with open(f'{category}/{title}.txt', 'w', encoding='UTF-8') as f:
            f.write(f'{title} \n \n  ')
            f.write(f'stock:{stock} , price:{price} \n \n \n ')
            f.write(f'{summary} \n \n \n ')

          
                         
    except ValueError as ve:
        print(ve)




def category(link):
    try:
        response = requests.get(link)
        if response.status_code != 200:
            raise ValueError(f'Error:   {response.status_code}  category page')
        content = response.content.decode('UTF-8')
        parsed_home = html.fromstring(content)
        
        category_name = parsed_home.xpath(XPATH_CATEGORIE_NAME)[0]
        links_to_books = parsed_home.xpath(XPATH_BOOK_LINK)
        


        if not os.path.isdir(category_name):
            os.mkdir(category_name)
            
        for i in links_to_books:
            i = regular_expression(i)
            i = SUPPORT_LINK_BOOKS + i
            book(i,category_name)
            
        
    except ValueError as ve:
        print(ve)
        print(link)
        return 
    

    
def main():
    try:
        response  = requests.get(MAIN_LINK)
        if response.status_code != 200:
            raise ValueError
        content = response.content.decode('UTF-8')
        parsed_home = html.fromstring(content)
        
        categorys_links = parsed_home.xpath(XPATH_CATEGORIES)

        
        for i in categorys_links:
            i = SUPPORT_LINK_CATEGORY + i
            category(i)
        
    except ValueError:
        print(f'Error:   {response.status_code}  main page')
    

        
if __name__ == '__main__':
    main()