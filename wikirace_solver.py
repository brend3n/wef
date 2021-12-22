import wiki_tool as wt

limit = 99999

# Path not found
found_path = False

def get_all_parent_links(title, limit):
    page = f'https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/{title}&namespace=0&limit={limit}'

    soup = wt.get_soup(page)

    p_links = wt.get_all_links(soup)
    p_links = list(set(p_links))

    for link in p_links:
        print(link)

    print(f"\n\n\nNumber of pages: {len(p_links)}")

    return p_links


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




def main():
    source = input("Enter starting page: ")
    target = input("Enter target page: ")
    find_path_exec(source, target)
  


if __name__=="__main__":
    main()
