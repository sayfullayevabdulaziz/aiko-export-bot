from collections import defaultdict

from bot.analytics.types import SubCategory, SubCategoryList


async def find_duplicate_codes(sub_category_list: SubCategoryList) -> dict[str, list[SubCategory]]:
    code_map = defaultdict(list)
    
    # Group subcategories by code
    for sub_category in sub_category_list.goods:
        code_map[sub_category.code].append(sub_category)
    
    # Filter out codes that have only one subcategory
    # duplicates = {code: items for code, items in code_map.items()}

    unique_duplicates = [items[0] for items in code_map.values()]
    
    return unique_duplicates
