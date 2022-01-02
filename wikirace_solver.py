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
        print(f"Child: {child.data}")
        return child
    
    def set_children_from_links(self, data):
        # Get links
        links = get_all_links(data)
        children_nodes = []
        
        print(f"Parent: {data}")
        # Create new node and assign to parent node
        for link in links:
            children_nodes.append(self.add_child(link))
        
        print("\n")
        
        return links, children_nodes
    
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
        # Set children for root node
        pages_seen, children = self.root.set_children_from_links(self.root.data)
        
        
        if self.target in pages_seen:
            print("Found target.")
            return

        self.construct_tree(children, pages_seen)
        print("Done building tree.")
            
    # Creates the tree that represents the possible paths from a source
    # page to its children pages and grandchildren pages and so on.
    def construct_tree(self, children_node_list, pages_seen):
        
        # Stores all children (Node) on current level
        new_children = []
        
        # Keep adding children until target page is found
        for child_node in children_node_list:
            page_data, new_children_temp = child_node.set_children_from_links(child_node.data)
            
            # Keep track of the titles of the pages seen so we know
            # when we find the target page
            pages_seen.append(page_data)
            
            # Keep track of child nodes
            new_children.append(new_children_temp)
            
            if self.target in pages_seen:
                print("Found target.")
                return
        
        self.construct_tree(new_children, pages_seen) 
    
    # Reconstructs the path take to get to the source to target nodes
    def reconstruct_path(self):
        path = []
        
        print(f"reconstruct_path()")
        
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
