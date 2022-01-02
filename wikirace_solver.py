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
        self.children = []
        
    def add_child(self, child_data):
        # Create child node object with its data
        child = Node(child_data)
        # Set the parent of this child
        child.parent = self
        self.children.append(child)
    
    def set_children_from_links(self, data):
        
        # Get links
        links = get_all_links(self.data)
        
        # Create new node and assign to parent node
        for link in links:
            self.add_child(link)

    
    def get_parent(self):
        return self.parent

class Wiki_Race_Tree():
    
    # Initializes the tree data structure
    def __init__(self, source, target):
        self.path = None
        self.root = Node(source)
        self.target = target
        pass
    
    # Prints the contents of the tree
    def print_tree(self):
        pass
    
    
    
    def construct_tree_helper(self):
        curr_node = self.root
        self.root.set_children_from_links()
        
        if self.target in self.root.children:
            print("Found target.")
            return

        self.construct_tree(self.root)
        print("Done building tree.")
            
    # Creates the tree that represents the possible paths from a source
    # page to its children pages and grandchildren pages and so on.
    def construct_tree(self, curr_node):
        # Keep adding children until target page is found
        
        for child in curr_node.children:
            child.set_children_from_links(child.data)
            
            if self.target in child.children:
                print("Found target.")
                return
            
                
            
        
        pass
    
    # Reconstructs the path take to get to the source to target nodes
    def reconstruct_path(self):
        path = []
        
        
        self.path = path    
        
    # Runs the algorithm to find the path from the source node to the
    # target node.
    def run(self):
        self.construct_tree_helper()
        self.reconstruct_path()
            
        pass
    
    # Use selenium to complete the race
    def do_wiki_race(self):
        self.run()
        path = self.path
        for link in path:
            # click on link with that title (selenium)
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

def main():
    
    tree = Wiki_Race_Tree("University_of_Central_Florida", "Harvard_University")
    tree.run()
    # tree.do_wiki_race()
  


if __name__=="__main__":
    main()
