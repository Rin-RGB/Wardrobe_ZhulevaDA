from wardrobe.models import Category, ClothingItem


def wardrobe_context(request):
    """
    Контекстный процессор: передаёт в каждый шаблон
    список категорий и общее количество вещей.
    Критерий 23.
    """
    categories = Category.objects.all()
    total_items = ClothingItem.objects.count()

    return {
        'all_categories': categories,
        'total_items_count': total_items,
    }