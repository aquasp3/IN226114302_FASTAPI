from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

products=[
{"id":1,"name":"Wireless Mouse","category":"Electronics","price":499,"in_stock":True},
{"id":2,"name":"Notebook","category":"Stationery","price":99,"in_stock":True},
{"id":3,"name":"USB Hub","category":"Electronics","price":799,"in_stock":False},
{"id":4,"name":"Pen Set","category":"Stationery","price":49,"in_stock":True}
]

feedback=[]
orders=[]

@app.get("/products/filter")
def filter_products(category:Optional[str]=None,max_price:Optional[int]=None,min_price:Optional[int]=None):
    result=[]
    for p in products:
        if category and p["category"].lower()!=category.lower():
            continue
        if max_price is not None and p["price"]>max_price:
            continue
        if min_price is not None and p["price"]<min_price:
            continue
        result.append(p)
    return result

@app.get("/products/{product_id}/price")
def get_price(product_id:int):
    for p in products:
        if p["id"]==product_id:
            return {"name":p["name"],"price":p["price"]}
    return {"error":"Product not found"}

class CustomerFeedback(BaseModel):
    customer_name:str=Field(...,min_length=2)
    product_id:int=Field(...,gt=0)
    rating:int=Field(...,ge=1,le=5)
    comment:Optional[str]=Field(None,max_length=300)

@app.post("/feedback")
def submit_feedback(data:CustomerFeedback):
    feedback.append(data.dict())
    return {"message":"Feedback submitted successfully","feedback":data,"total_feedback":len(feedback)}

@app.get("/products/summary")
def product_summary():
    total=len(products)
    in_stock=sum(1 for p in products if p["in_stock"])
    out_stock=total-in_stock
    most=max(products,key=lambda x:x["price"])
    least=min(products,key=lambda x:x["price"])
    cats=list(set(p["category"] for p in products))
    return {"total_products":total,"in_stock_count":in_stock,"out_of_stock_count":out_stock,"most_expensive":{"name":most["name"],"price":most["price"]},"cheapest":{"name":least["name"],"price":least["price"]},"categories":cats}

class OrderItem(BaseModel):
    product_id:int=Field(...,gt=0)
    quantity:int=Field(...,ge=1,le=50)

class BulkOrder(BaseModel):
    company_name:str=Field(...,min_length=2)
    contact_email:str=Field(...,min_length=5)
    items:List[OrderItem]=Field(...,min_items=1)

@app.post("/orders/bulk")
def bulk_order(order:BulkOrder):
    confirmed=[]
    failed=[]
    total=0
    for item in order.items:
        prod=next((p for p in products if p["id"]==item.product_id),None)
        if not prod:
            failed.append({"product_id":item.product_id,"reason":"Product not found"})
            continue
        if not prod["in_stock"]:
            failed.append({"product_id":item.product_id,"reason":prod["name"]+" is out of stock"})
            continue
        subtotal=prod["price"]*item.quantity
        total+=subtotal
        confirmed.append({"product":prod["name"],"qty":item.quantity,"subtotal":subtotal})
    return {"company":order.company_name,"confirmed":confirmed,"failed":failed,"grand_total":total}

class SimpleOrder(BaseModel):
    product_id:int
    quantity:int

@app.post("/orders")
def create_order(data:SimpleOrder):
    order_id=len(orders)+1
    order={"id":order_id,"product_id":data.product_id,"quantity":data.quantity,"status":"pending"}
    orders.append(order)
    return order

@app.get("/orders/{order_id}")
def get_order(order_id:int):
    for o in orders:
        if o["id"]==order_id:
            return o
    return {"error":"Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id:int):
    for o in orders:
        if o["id"]==order_id:
            o["status"]="confirmed"
            return o
    return {"error":"Order not found"}
