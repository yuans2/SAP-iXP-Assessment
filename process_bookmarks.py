import requests
def get_real_domain(url):
    http_headers = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    rs = requests.get(url,headers=http_headers,timeout=10)    
    return get_domain(rs.url)

def get_domain(url):
    #remove http or https
    url = url.split('://')[-1]
    #get first domain
    domain = url.split('/')[0]
    return domain

def arrange_urls(urls):
    #store urls
    domain_dict = { }
    for url in urls:
        domain = get_real_domain(url)
        #print(url, ' get domain: ' , domain)
        if domain in domain_dict:
            domain_dict[domain].append(url)
        else:
            domain_dict[domain] = [url]
    #get
    for domain in domain_dict:
        my_urls = domain_dict[domain]
        http_urls = [url for url in my_urls if url.startswith('http://')]
        https_urls = [url for url in my_urls if url.startswith('https://')]

        def length(url):
            return len(url)
        #sort by length
        http_urls.sort(key = length)
        https_urls.sort(key = length)
        #sort by alph
        http_urls.sort()
        https_urls.sort()

        domain_dict[domain] = https_urls + http_urls

    #restore
    return domain_dict

def valid_url(url):
    #check if url is a real url
    if ' ' in url or '.' not in url:
        return False
    if not url.startswith('http://') and not url.startswith('https://'):
        return False
    return True

def load_bookmarks(filename):
    urls = []
    #read out all urls
    with open(filename, 'r') as input_file:
        for line in input_file:
            url = line.strip()
            if url not in urls and valid_url(url):
                urls.append(url)
    #arrange    
    domain_dict = arrange_urls(urls)
    #print by alphelebt
    domain_sort = list(domain_dict.keys())
    domain_sort.sort()
    for domain in domain_sort:
        my_urls = domain_dict[domain]
        output = '['
        for url in my_urls[:-1]:
            output += url + ','
        output += my_urls[-1] + ']'
        print(output)

if __name__ == '__main__':
    load_bookmarks('bookmarks.txt')
    #print(get_real_domain('https://news.google.com/news/'))