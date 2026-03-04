from fastapi import FastAPI

app = FastAPI()

# Products list
products = [
    {"id": 1, "name": "Smartphone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Headphones", "price": 2000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Mouse", "price": 800, "category": "Accessories", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 300, "category": "Accessories", "in_stock": False},

    # New products added
    {"id": 5, "name": "Laptop Stand", "price": 1500, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 4500, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 2500, "category": "Electronics", "in_stock": True}
]

# API endpoint
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    
    filtered_products = [
        product for product in products
        if product["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products
    }
@app.get("/products/instock")
def get_instock_products():

    instock_products = [
        product for product in products
        if product["in_stock"] == True
    ]

    return {
        "products": instock_products,
        "count": len(instock_products)
    }
@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])

    out_of_stock_count = total_products - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_products": in_stock_count,
        "out_of_stock_products": out_of_stock_count,
        "categories": categories
    }
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = [
        product for product in products
        if keyword.lower() in product["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matches": matched_products,
        "total_matches": len(matched_products)
    }
@app.get("/products/deals")
def product_deals():

    best_deal = min(products, key=lambda x: x["price"])

    premium_pick = max(products, key=lambda x: x["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
