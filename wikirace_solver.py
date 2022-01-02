import wiki_tool as wt
import requests
from bs4 import BeautifulSoup

wiki_search = []
reconstructed_path = []

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


# Works as expected
def nice_print(dict_list):
    index = 0
    for i in range(len(dict_list)):
        print(f"\n\n~~~~Level: {i}~~~~\n\n")
        for j in range(len(dict_list[i])):
            parent = dict_list[i][j]["parent"]
            children = dict_list[i][j]["children"]
            print(f"Parent: {parent}\nChildren: {children}\n\n")
        print("\n")
            
# Test data to see if logic is correct
def test_links():
    wiki_search = [
        [{"parent":"apple","children": ["phone","orange","pear"]}],
        [{"parent":"phone","children":[]},
         {"parent":"orange","children":["color", "fruit"]},
         {"parent":"pear","children":["dollar", "fish"]}
        ]
    ]
    nice_print(wiki_search)
    return wiki_search

def find_shortest_path_helper(s,t):
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
    find_shortest_path(s,t, 0)
    
    path = []
    # path = reconstruct_path(s,t)
    
    print(f"Path: {path}")
    return path


# Able to find existence of target page but cannot reconstruct path nor
# is the data structured properly.
'''
# ! Need to check if the data structured properly
# Source is the starting node and the target is the ending node.
def find_shortest_path(source, target, wiki_search,re_path):
    
    index = len(wiki_search) - 1

    # Look for target    
    for ele in wiki_search[index]:
        if target in ele['children']:
            print(f"Found target: {target}")
            re_path = reconstruct_path(source, target, wiki_search, re_path)
            return re_path
        else:
            print("Target not found.")
            
            
    # Target was not found, so get new data and update wiki_search
    new_level = []
    for parent in wiki_search[index]:
        print(f"Parent: {parent['parent']}")
        for child in parent["children"]:
            print(f"child: {child}")
            data = {
                "parent": child,
                "children": get_all_links(child)
            }
            if target in data["children"]:
                print("Found target.")
                re_path = reconstruct_path(source, target, wiki_search, re_path)
                return re_path
            new_level.append(data)
            
    wiki_search.append(new_level)
    find_shortest_path(source, target, wiki_search, re_path)
'''
# # Source is the starting node and the target is the ending node.
# def find_shortest_path(source, target, wiki_search,re_path):
    
    
#     new_level = []
#     for i in range(len(wiki_search)):
#         for j in range(len(wiki_search[i])):
#             parent = wiki_search[i][j]["parent"]
#             children_list = wiki_search[i][j]["children"]
            
#             # Get links for each child of page
#             for child in children_list:
#                 data = {
#                     "parent": child,
#                     "children": get_all_links(child)
#                 }
#                 # Check if found target
#                 if target in data["children"]:
#                     print("Found target.")
#                     re_path = reconstruct_path(source, target, wiki_search, re_path)
#                     return re_path
#                 new_level.append(data)
#         wiki_search.append(new_level)
    
#     find_shortest_path(source, target, data, re_path)   
    
    
# Source is the starting node and the target is the ending node.
def find_shortest_path(source, target, index):
    flag_f = False
    print("\nBefore\n")
    nice_print(wiki_search)
    new_level = []
    for element in wiki_search[index]:
        parent = element["parent"]
        for child in element["children"]:
            data = {
                "parent":child,
                "children": get_all_links(child)
            }
            new_level.append(data)
            if target in data["children"]:
                print("Found target.")
                flag_f = True
                break
            
        if flag_f == True:
            break
    wiki_search.append(new_level)
    size = len(wiki_search)
    print(f"wiki_search size: {size}")
    print("\nAfter\n")
    nice_print(wiki_search)
    
    if flag_f == True:
        return
    
    find_shortest_path(source,target, index+1)
    pass    
    
    
# Not finding the nodes in the middle
def reconstruct_path(source, target):
    found_flag = False
    path = [target]
    # Start at the last level in wiki_search
    index = len(wiki_search) - 1
    # print("Printing wiki_search to see that it isnt fucked")
    # print(wiki_search)
    print(f"index: {index}")
    while index >= 0:
        for page_dict in wiki_search[index]:
            # print(f"page_dict: {page_dict} ")
            if target in page_dict["children"]:
                parent = page_dict["parent"]
                print(f"parent: {parent}")
                path.append(page_dict["parent"])
                index -= 1
                found_flag = True
                break
            else:
                print("Not found ...")
    path.append(source)
    # print(f"path: {path}")
    path.reverse()
    # print(f"path: {path}")
    return path

def main():
    # source = str(input("Enter starting page: "))
    # target = str(input("Enter target page: "))

    
    # print(f"Looking for path from {source} to {target}")
    # find_shortest_path_helper(source, target)
    
    find_shortest_path_helper("Claude_R._Kirk_Jr.", "Toluca")
    # test_links()
  


if __name__=="__main__":
    main()
