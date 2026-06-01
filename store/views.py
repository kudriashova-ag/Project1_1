from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .data import PRODUCTS, ORDERS, VALID_CATEGORIES, CATEGORY_NAMES
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# Доможні функції
def product_to_dict(product_id, product):
    """Перетворює товар у словник для JSON-відповіді."""
    return {
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "stock": product["stock"],
        "available": product["stock"] > 0,
    }


def apply_filters(products_dict, sort=None, in_stock=False):
    """Застосовує фільтри та сортування до словника товарів."""
    items = [product_to_dict(pid, p) for pid, p in products_dict.items()]

    if in_stock:
        items = [p for p in items if p["available"]]

    if sort == "price_asc":
        items.sort(key=lambda p: p["price"])
    elif sort == "price_desc":
        items.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "name":
        items.sort(key=lambda p: p["name"])

    return items


# View функціі
def home(request):
    """ Завдання 2 — Головна сторінка """
    totalProducts = len(PRODUCTS)

    return HttpResponse(f"""
                        <h1>My Store</h1>
                        <p>Товарів: {totalProducts}</p>
                        <a href="/store/">Каталог</a>
                        <a href="/store/search">Пошук</a>
                        <a href="/store/orders">Замовлення</a>
                        """)

def product_list(request):
    """ Завдання 3 — Каталог товарів з фільтрацією """
    sort = request.GET.get("sort", "")
    in_stock = request.GET.get("in_stock") == "1"

    products = apply_filters(PRODUCTS, sort = sort, in_stock = in_stock)

    return JsonResponse({
        "filters":{
            "sort": sort or None,
            "in_stock": in_stock
        },
        "count": len(products),
        "products": products
    }, json_dumps_params = {"ensure_ascii": False, "indent": 2})


def product_detail(request, product_id):
    """Завдання 4 — Деталі товару"""
    product = PRODUCTS.get(product_id)
    if product is None:
        return JsonResponse(
            {"error": "Товар не знайдено"}, 
            status=404, 
            json_dumps_params={"ensure_ascii": False, "indent": 2}
            )
    return JsonResponse(
        product_to_dict(product_id, product),
        json_dumps_params={"ensure_ascii": False, "indent": 2}
    )


@csrf_exempt
def order_views(request, product_id):
    """Завдання 7 — Оформлення замовлення"""
    product = PRODUCTS.get(product_id)
    if product is None:
        return JsonResponse(
            {"error": "Товар не знайдено"}, 
            status=404, 
            json_dumps_params={"ensure_ascii": False, "indent": 2}
            )
    if request.method == "GET":
        return HttpResponse(f"""
                <h1>Оформлення замовлення для {product["name"]}</h1>
                <form method="POST">
                    <input type="text" name="name" placeholder="Ім'я"> <br>
                    <input type="text" name="phone" placeholder="Телефон"> <br>
                    <input type="text" name="quantity" placeholder="Кількість"> <br>
                    <button>Оформити замовлення</button>
                </form>
        """)
    if request.method == "POST":
        if product["stock"] == 0:
            return JsonResponse(
                {"error": "Товара немає на складі"}, 
                status=400, 
                json_dumps_params={"ensure_ascii": False, "indent": 2}
                )
        # валідація

        order = {
            "order_id": len(ORDERS) + 1,
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": request.POST.get("quantity"),
            "total_price": int(request.POST.get("quantity")) * product["price"],
            "customer_name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            }
        ORDERS.append(order)
        return redirect("order_list")
    

def order_list(request):
    """Завдання 8 — Список замовлень"""    
    if not ORDERS:
        return JsonResponse(
            {"message": "Замовлень поки немає", "orders": []}, 
            json_dumps_params={"ensure_ascii": False, "indent": 2})
    return JsonResponse(
        {
            "count": len(ORDERS),
            "orders": ORDERS
        },
        json_dumps_params={"ensure_ascii": False, "indent": 2}
    )

    
