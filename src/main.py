from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import users, products, auth, categories

app = FastAPI(root_path='/api')

app.add_middleware(CORSMiddleware,  # type: ignore
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(users.router)


@app.get("/")
async def index():
    return {"message": "Добро пожаловать на стартовый эндопинт этого API\n\n"
                       "Документация доступна по эндпоинту /docs"}
