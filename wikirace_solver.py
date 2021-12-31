import wiki_tool as wt
import requests
from bs4 import BeautifulSoup

limit = 99999

# Path not found
found_path = False

def get_all_parent_links(title, limit):
    page = f'https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/{title}&namespace=0&limit={limit}'

    soup = wt.get_soup(page)

    p_links = wt.get_all_links(soup)
    p_links = list(set(p_links))

    #for link in p_links:
    #    print(link)

    # print(f"\n\n\nNumber of pages: {len(p_links)}")

    return p_links

# This is a backtracking solution
"""
def find_path_exec(source, target):
    path = []
    cache = []

    # Add target to the end/beginning of the list
    path.insert(0, target)
    cache.append(target)

    # Working backwards -> starting from the target and working backwards
    parents = get_all_parent_links(target,limit)

    # Found path: [source -> target] with a distance of 1
    if source in parents:
        # Add source to path
        path.insert(0, source)
        return path

    # Start search for source
    find_path(source, target, path, cache)


def find_path(source, curr_target, path, cache):

    # Get all parents of curr_target
    parents = get_all_parent_links(curr_target, limit)

    # Source is what we are looking for since we're working backwards
    if source in parents:
        path.insert(0,source)
        print(f"Path found: {path}")
        found_path = True
        return
    else:
        # If we don't find what we are looking for it
        for parent in parents:
            # Don't repeat old links
            if parent not in cache:
                # Cache the parent page so we dont visit it again
                cache.append(parent)
                # Add it to the path
                path.insert(0, parent)
                find_path(source, parent, path, cache)
                # Remove from path if not
                path.pop(0)
                cache.remove(parent)
"""

def get_soup(url):
    # print(f"get_soup({url})")
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_all_links(page_title):

	page_title = str(page_title).replace(" ","_")
	url = f"https://en.wikipedia.org/wiki/{page_title}"
	soup = get_soup(url)
	links = []
	for link in soup.find_all('a'):
		l = link.get('href')
		l = str(l)
		if ("/wiki/" in l) and (":" not in l) and (".svg" not in l) and (".org" not in l) and ("Main_Page" not in l):
			l = l[6:]
			links.append(l)
	return links


def find_shortest_path_helper(s,t):
    wiki_search = []
    reconstructed_path = []
    source_links = get_all_links(s)
    
    if t in source_links:
        print(f"Found path {s}->{t}")
        return [s,t]
    data = {
        "parent":s,
        "children":source_links
    }
    data_test = {
        "test": 1,
        "test2":2
    }
    wiki_search.append([data])
    
    path = find_shortest_path(s,t,wiki_search,reconstructed_path)
    print(f"Path: {path}")
    return path

# Source is the starting node and the target is the ending node.
def find_shortest_path(source, target, wiki_search,re_path):
    index = len(wiki_search) - 1
    # print(f"wiki_search: {wiki_search}")
    # print(f"index: {index}")
    # print(f"wiki_search[{index}]: {wiki_search[index]}")

    # Look for target    
    for ele in wiki_search[index]:
        if target in ele['children']:
            print(f"Found target: {target}")
            # re_path = reconstruct_path(source, target, wiki_search, re_path)
            return re_path
        else:
            print("Target not found.")
    # Target was not found, so get new data and update wiki_search
    new_level = []
    for parent in wiki_search[index]:
        print(f"Parent: {parent}")
        for child in parent["children"]:
            print(f"child: {child}")
            data = {
                "parent": child,
                "children": get_all_links(child)
            }
            new_level.append(data)
    wiki_search.append(new_level)
    find_shortest_path(source, target, wiki_search, re_path)

def reconstruct_path(source, target, wiki_search, re_path):
    pass		

def main():
    # source = str(input("Enter starting page: "))
    # target = str(input("Enter target page: "))

    
    # print(f"Looking for path from {source} to {target}")
    # find_shortest_path_helper(source, target)
    
    find_shortest_path_helper("Taiwan", "SARS")
  


if __name__=="__main__":
    main()
