import wiki_tool as wt
import requests
from bs4 import BeautifulSoup

limit = 99999

# Path not found
found_path = False

# Simple Node class
class Node(object):
    
    def __init__(self,data):
        self.data = data
        self.parent = None
        self.children = None
        
    def add_child(self, obj):
        self.children.append(obj)
        
    def set_parent(self, parent):
        self.parent = parent
    
    def get_parent(self):
        return self.parent

class Wiki_Race_Tree():
    
    # Initializes the tree data structure
    def __init__(self, source, target):
        self.path = None
        self.root = source
        pass
    
    # Prints the contents of the tree
    def print_tree(self):
        pass
    
    # Creates the tree that represents the possible paths from a source
    # page to its children pages and grandchildren pages and so on.
    def construct_tree(self):
        pass
    
    # Reconstructs the path take to get to the source to target nodes
    def reconstruct_path(self):
        path = []
        
        
        self.path = path    
    
    # Use selenium to complete the race
    def do_wiki_race(self, path):
        pass
    
    
        
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


      
# Test data to see if logic is correct
def get_test_links(ele):
    wiki_search = [
        [{"parent":"apple","children": ["phone","orange","pear"]}],
        [{"parent":"phone","children":[]},
         {"parent":"orange","children":["color", "fruit"]},
         {"parent":"pear","children":["dollar", "fish"]}
        ]
    ]
    # nice_print(wiki_search)
    return wiki_search

def find_shortest_path_helper(s,t):
    wiki_search = []
    reconstructed_path = []
    source_links = get_all_links(s)
    
    # Check if target is already found on source page.
    if t in source_links:
        print(f"Found path {s}->{t}")
        return [s,t]

    # Source page data
    data = {
        "parent":s,
        "children":source_links
    }
    
    wiki_search.append([data])
    
    path = find_shortest_path(s,t,wiki_search,reconstructed_path)
    
    print(f"Path: {path}")
    return path


# Source is the starting node and the target is the ending node.
def find_shortest_path(source, target, wiki_search,re_path):
    index = len(wiki_search) - 1
    
    new_level = []
    for j in range(len(wiki_search[index])):
        parent = wiki_search[index][j]["parent"]
        children_list = wiki_search[index][j]["children"]
        
        # Get links for each child of page
        for child in children_list:
            data = {
                "parent": child,
                "children": get_all_links(child)
            }
            print(f"Data for {child}:\n{get_all_links(child)}\n\n\n")
            new_level.append(data)
            print(f"new_level: {new_level}")
            
            # Check if found target
            if target in data["children"]:
                print("Found target.")
                size_tt = len(wiki_search)
                print(f"Size wiki_search: {size_tt}")
                print_levels(wiki_search)
                nice_print(wiki_search)
                re_path = []    
                re_path = reconstruct_path(source, target, wiki_search, re_path)
                return re_path
        wiki_search.append(new_level)
    
    find_shortest_path(source, target, wiki_search, re_path)   

# ! Working on reconstruction 
# Not finding the nodes in the middle
def reconstruct_path(source, target, wiki_search, re_path):
    return	

def main():
    # source = str(input("Enter starting page: "))
    # target = str(input("Enter target page: "))

    
    # print(f"Looking for path from {source} to {target}")
    # find_shortest_path_helper(source, target)
    
    find_shortest_path_helper("University_of_Central_Florida", "Harvard_Law_School")
    # test_links()
  


if __name__=="__main__":
    main()
