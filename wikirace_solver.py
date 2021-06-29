import wiki_tool as wt







def get_all_parent_links(title, limit):
    page = f'https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/{title}&namespace=0&limit={limit}'

    soup = wt.get_soup(page)
    # print(soup)

    p_links = wt.get_all_links(soup)
    # print(p_links)
    # for link in p_links:
    #     # print(link)
    print(f"\n\n\nNumber of pages: {len(p_links)}")
    return p_links



get_all_parent_links("Lemon",9999999)

