def getpage(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)
	
def crawl_web(seed,maxpages):
  
    tocrawl = [seed]
    crawled = [] 
    index = {}
    graph = {}
    
    #While there are more pages to crawl
    while tocrawl:
        page = tocrawl.pop()

        if page not in crawled and len(crawled) < maxpages:

            content = getpage(page)
            #Adds all the link targets on this page to tocrawl
            add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            #Adds the page to the list of crawled pages
            crawled.append(page)
    return index, graph


#--------------------------------building index-----------------------------------
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

    
#---------------------------------page rank algorithm---------------------------------

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def quick_sort(url_lst,ranks):
    url_sorted_worse=[]
    url_sorted_better=[]
    if len(url_lst)<=1:
        return url_lst
    pivot=url_lst[0]
    for url in url_lst[1:]:
        if ranks[url]<=ranks[pivot]:
            url_sorted_worse.append(url)
        else:
            url_sorted_better.append(url)
    return quick_sort(url_sorted_better,ranks)+[pivot]+quick_sort(url_sorted_worse,ranks)

        
def ordered_search(index, ranks, keyword):
    if keyword in index:
        all_urls=index[keyword]
    else:
        return None
    return quick_sort(all_urls,ranks)


#---------------------------------example-----------------------------------



index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html',10)
ranks = compute_ranks(graph)
print ordered_search(index, ranks, 'Hummus')
