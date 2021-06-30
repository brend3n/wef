import wiki_tool as wt

limit = 99999
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

    # Add target to the end/beginning of the list
    path.insert(0, target)

    parents = get_all_parent_links(target,limit)

    # Found path: source -> target with a distance of 1
    if source in parents:
        path.insert(0,source)
        return path

    # Start search for source
    find_path(source, target, path)


def find_path(source, curr_target, path):
    parents = get_all_parent_links(curr_target,limit)

    if source in parents:
        path.insert(0,source)

    path.insert(0, )



