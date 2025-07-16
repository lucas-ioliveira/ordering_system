from fastapi import FastAPI

from api.endpoints.auth.router import router as auth_router
from api.endpoints.orders.router import router as orders_router
from api.endpoints.order_items.router import router as order_items_router

app = FastAPI(
    title='FastAPI',
    description='API para gerenciamento de pedidos',
    version='0.1.0',
)

app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(order_items_router)