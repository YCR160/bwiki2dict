def all_titles(all_data):
    all_pages = all_data.get("query", {}).get("pages", {})

    # 所有标题
    all_titles = set()
    for _, page in all_pages.items():
        all_titles.add(page.get("title", ""))

    return all_titles


def filter_titles(all_data, part_categories):
    all_pages = all_data.get("query", {}).get("pages", {})

    # 构建 分类: [标题1, 标题2, ...] 的字典
    category_to_pages = {}
    for _, page in all_pages.items():
        categories = page.get("categories", [])
        for category in categories:
            category_title = category.get("title", "")
            if category_title not in category_to_pages:
                category_to_pages[category_title] = []
            category_to_pages[category_title].append(page.get("title", ""))

    # 构建 部分分类: [标题1, 标题2, ...] 的字典
    part_category_to_pages = {}
    for category in part_categories:
        part_category_to_pages[category] = category_to_pages.get(category, [])

    # 部分标题
    part_titles = set()
    for category, pages in part_category_to_pages.items():
        for page in pages:
            part_titles.add(page)

    return part_titles


if __name__ == "__main__":
    from fetch import fetch_all_titles

    api_url = "https://wiki.biligame.com/sr/api.php"
    all_data = fetch_all_titles(api_url)

    all_pages = all_data.get("query", {}).get("pages", {})
    # print(all_pages)
    all_categories = set()
    for page_id, page in all_pages.items():
        # print(page)
        categories = page.get("categories", [])
        # print(categories)
        for category in categories:
            category_title = category.get("title", "")
            # print(category_title)
            all_categories.add(category_title)

    print(all_categories)
