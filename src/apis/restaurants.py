from fastapi import FastAPI
from pydantic import BaseModel, Field
import shortuuid


class CreateProductRequest(BaseModel):
    name: str = Field(description="Nombre del producto")
    price: int = Field(description="Precio del producto")
    class Config:
        schema_extra = {
            "example": {
                "name": "Nombre del producto",
                "price": 2700,
            }
        }


class Product(BaseModel):
    id: str = Field(description="ID del producto")
    name: str = Field(description="Nombre del producto")
    price: int = Field(description="Precio del producto")
    class Config:
        schema_extra = {
            "example": {
                "id": "ID del producto",
                "name": "Nombre del producto",
                "price": 2700,
            }
        }


class CreateBeerRequest(BaseModel):
    name: str = Field(description="El nombre de la cerveza")
    brewery: str = Field(description="La cervecería que produce la cerveza")
    style: str = Field(description="El estilo de la cerveza (p. ej., India Pale Ale, Stout)")
    abv: float = Field(description="El porcentaje de alcohol por volumen (ABV) de la cerveza")
    ibu: int = Field(description="La calificación de Unidades Internacionales de Amargor (IBU) de la cerveza")
    price: float = Field(description="El precio de la cerveza")
    class Config:
        schema_extra = {
            "example": {
                "name": "Stone IPA", 
                "brewery": "Stone Brewing", 
                "style": "India Pale Ale", 
                "abv": 6.9, 
                "ibu": 77, 
                "price": 9.99
            }
        }


class Beer(BaseModel):
    id: str = Field(description="ID de la cerveza")
    name: str = Field(description="El nombre de la cerveza")
    brewery: str = Field(description="La cervecería que produce la cerveza")
    style: str = Field(description="El estilo de la cerveza (p. ej., India Pale Ale, Stout)")
    abv: float = Field(description="El porcentaje de alcohol por volumen (ABV) de la cerveza")
    ibu: int = Field(description="La calificación de Unidades Internacionales de Amargor (IBU) de la cerveza")
    price: float = Field(description="El precio de la cerveza")
    class Config:
        schema_extra = {
            "example": {
                "id": "ID del producto",
                "name": "Stone IPA", 
                "brewery": "Stone Brewing", 
                "style": "India Pale Ale", 
                "abv": 6.9, 
                "ibu": 77, 
                "price": 9.99
            }
        }


class CreateMenuRequest(BaseModel):
    name: str = Field(description="Nombre del menú")
    products: list[Product] = Field(description="Productos del menú")
    class Config:
        schema_extra = {
            "example": {
                "name": "Nombre del menu",
                "products": [
                    {
                        "product_id": "9Pv3V7Fif14CkufsiHcW2M",
                        "quantity": 2,
                    }
                ],
            }
        }


class Menu(BaseModel):
    id: str = Field(description="ID del menu")
    name: str = Field(description="Nombre del menú")
    products: list[Product] = Field(description="Productos del menú")
    class Config:
        schema_extra = {
            "example": {
                "id": "ID del menu",
                "name": "Nombre del menu",
                "products": [
                    {
                        "product_id": "9Pv3V7Fif14CkufsiHcW2M",
                        "quantity": 2,
                    }
                ],
            }
        }


class ProductOrder(BaseModel):
    product_id: str = Field(title='Product ID', description='ID del producto asociado al pedido')
    quantity: str = Field(description='Cantidad de productos')


class Order(BaseModel):
    products: ProductOrder = Field(description="Productos asociados a los pedidos")
    observation: str = Field(description="Alguna observación asociado al pedido como alguna peticion especial")
    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "product_id": "9Pv3V7Fif14CkufsiHcW2M",
                        "quantity": 2,
                    }
                ],
                "observation": "Papas fritas sin mostaza porfavor",
            }
        }


class Response(BaseModel):
    message: str = Field(description='Mensaje de la respuesta')
    

class RestaurantService:
    products: list[Product] = []
    orders: list[Order] = []
    menus: list[Menu] = []
    beers = []

    def create_order(self, order: Order):
        print(f'Create order {order}')
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def create_product(self, new_product: CreateProductRequest) -> Product:
        product = Product(id=shortuuid.uuid(), **new_product.dict())
        print(f'Create product {product}')
        self.products.append(product)
        return product
    
    def create_beer(self, new_beer: CreateBeerRequest) -> Beer:
        beer = Beer(id=shortuuid.uuid(), **new_beer.dict())
        print(f'Create beer {beer}')
        self.beers.append(beer)
        return beer
    
    def get_product_beer(self):
        return self.beers
    
    def get_products(self):
        return self.products

    def create_menu(self, new_menu: CreateMenuRequest) -> Menu:
        menu = Menu(id=shortuuid.uuid(), ** new_menu.dict())
        print(f'Create menu {menu}')
        self.menus.append(menu)
        return menu

    def get_menu_by_id(self, menu_id: str):
        for menu in self.menus:
            if menu.id == menu_id:
                return menu
        return ValueError("El menú con el ID especificado no existe")
    

service = RestaurantService()
macdonalds_products = [    {"name": "Big Mac", "price": 5.49},    {"name": "Quarter Pounder with Cheese", "price": 5.79},    {"name": "Double Quarter Pounder with Cheese", "price": 7.79},    {"name": "Filet-O-Fish", "price": 4.79},    {"name": "McChicken", "price": 4.19},    {"name": "10-piece McNuggets", "price": 6.49},    {"name": "20-piece McNuggets", "price": 10.99},    {"name": "French Fries (medium)", "price": 2.99},    {"name": "Soft Drink (medium)", "price": 1.79},    {"name": "Apple Pie", "price": 1.99}]
drinks = [{"name": "Margarita", "type": "trago", "price": 8.99},    {"name": "Piña Colada", "type": "trago", "price": 9.99},    {"name": "Mojito", "type": "trago", "price": 7.99},    {"name": "Daiquiri", "type": "trago", "price": 8.99},    {"name": "Negroni", "type": "trago", "price": 10.99},    {"name": "Cosmopolitan", "type": "trago", "price": 9.99},    {"name": "Corona Extra", "type": "cerveza", "price": 5.99},    {"name": "Heineken", "type": "cerveza", "price": 6.99},    {"name": "Budweiser", "type": "cerveza", "price": 4.99},    {"name": "Merlot", "type": "vino", "price": 12.99},    {"name": "Chardonnay", "type": "vino", "price": 13.99},    {"name": "Pinot Noir", "type": "vino", "price": 14.99},    {"name": "Soda", "type": "bebida sin alcohol", "price": 1.99},    {"name": "Agua Mineral", "type": "bebida sin alcohol", "price": 2.99},    {"name": "Jugo de Naranja", "type": "bebida sin alcohol", "price": 3.99},    {"name": "Té Helado", "type": "bebida sin alcohol", "price": 2.49},    {"name": "Limonada", "type": "bebida sin alcohol", "price": 3.49},    {"name": "Coca Cola", "type": "bebida sin alcohol", "price": 1.99},    {"name": "Sprite", "type": "bebida sin alcohol", "price": 1.99},    {"name": "Fanta Naranja", "type": "bebida sin alcohol", "price": 1.99}]
foods = [{"name": "Pizza Margherita", "price": 12.99},    {"name": "Hamburguesa de Ternera", "price": 9.99},    {"name": "Pollo Frito", "price": 8.99},    {"name": "Ensalada de Pollo", "price": 10.99},    {"name": "Sopa de Tomate", "price": 5.99},    {"name": "Hot Dog", "price": 6.99},    {"name": "Nachos con Queso", "price": 4.99},    {"name": "Palitos de Queso", "price": 3.99},    {"name": "Alitas de Pollo", "price": 8.99},    {"name": "Hummus con Pita", "price": 6.99},    {"name": "Rollito de Primavera", "price": 4.99},    {"name": "Sandwich de Jamón y Queso", "price": 7.99},    {"name": "Sandwich de Pavo y Aguacate", "price": 8.99},    {"name": "Bocadillo de Carne Asada", "price": 9.99},    {"name": "Wrap Vegano", "price": 6.99},    {"name": "Empanada de Carne", "price": 2.99},    {"name": "Croquetas de Jamón", "price": 3.99},    {"name": "Pan de Ajo", "price": 2.99},    {"name": "Gyozas de Cerdo", "price": 5.99},    {"name": "Tacos de Pescado", "price": 11.99},    {"name": "Rollitos de Huevo", "price": 4.99},    {"name": "Sándwich de Carne Ahumada", "price": 10.99},    {"name": "Quesadilla de Pollo", "price": 8.99},    {"name": "Calamares Fritos", "price": 9.99},    {"name": "Papas Fritas con Queso", "price": 6.99},    {"name": "Tortilla Española", "price": 7.99},    {"name": "Chili con Carne", "price": 8.99},    {"name": "Sándwich de Pollo", "price": 6.99},    {"name": "Tostada de Aguacate", "price": 5.99},    {"name": "Ensalada César", "price": 9.99}]
beers = [    
    {"name": "Stone IPA", "brewery": "Stone Brewing", "style": "India Pale Ale", "abv": 6.9, "ibu": 77, "price": 9.99},    {"name": "Dirty Bastard", "brewery": "Founders Brewing Co.", "style": "Scotch Ale", "abv": 8.5, "ibu": 50, "price": 10.99},    {"name": "Hennepin Farmhouse Saison", "brewery": "Ommegang", "style": "Saison", "abv": 7.7, "ibu": 24, "price": 12.99},    {"name": "Westmalle Tripel", "brewery": "Westmalle Brewery", "style": "Belgian Tripel", "abv": 9.5, "ibu": 38, "price": 14.99},    {"name": "Dragon's Milk Bourbon Barrel Stout", "brewery": "New Holland Brewing", "style": "Imperial Stout", "abv": 11.0, "ibu": 31, "price": 11.99},    {"name": "Rodenbach Grand Cru", "brewery": "Rodenbach Brewery", "style": "Flanders Red Ale", "abv": 6.0, "ibu": 17, "price": 13.99},    {"name": "Ten Fidy Imperial Stout", "brewery": "Oskar Blues Brewery", "style": "Russian Imperial Stout", "abv": 10.5, "ibu": 98, "price": 10.99},    {"name": "Sierra Nevada Pale Ale", "brewery": "Sierra Nevada Brewing Co.", "style": "American Pale Ale", "abv": 5.6, "ibu": 38, "price": 8.99},    {"name": "Maudite Belgian Strong Ale", "brewery": "Unibroue Brewery", "style": "Belgian Strong Ale", "abv": 8.0, "ibu": 22, "price": 11.99},    {"name": "Samuel Smith's Nut Brown Ale", "brewery": "Samuel Smith Old Brewery", "style": "English Brown Ale", "abv": 5.0, "ibu": 28, "price": 9.99},
  {"name": "Hopslam Ale", "brewery": "Bell's Brewery", "style": "Double IPA", "abv": 10.0, "ibu": 70, "price": 15.99},    {"name": "La Fin Du Monde", "brewery": "Unibroue Brewery", "style": "Belgian Tripel", "abv": 9.0, "ibu": 19, "price": 12.99},    {"name": "Old Rasputin Russian Imperial Stout", "brewery": "North Coast Brewing Co.", "style": "Russian Imperial Stout", "abv": 9.0, "ibu": 75, "price": 11.99},    {"name": "Orval Trappist Ale", "brewery": "Orval Brewery", "style": "Belgian Pale Ale", "abv": 6.2, "ibu": 25, "price": 13.99},    {"name": "Stone Coffee Milk Stout", "brewery": "Stone Brewing", "style": "Milk Stout", "abv": 5.0, "ibu": 40, "price": 9.99},    {"name": "The Abyss Bourbon Barrel-Aged Stout", "brewery": "Deschutes Brewery", "style": "Imperial Stout", "abv": 12.4, "ibu": 80, "price": 16.99},    {"name": "Chimay Blue Grande Réserve", "brewery": "Chimay Brewery", "style": "Belgian Strong Dark Ale", "abv": 9.0, "ibu": 30, "price": 14.99},    {"name": "Pliny the Elder", "brewery": "Russian River Brewing Company", "style": "Double IPA", "abv": 8.0, "ibu": 100, "price": 19.99},    {"name": "Troegenator Double Bock", "brewery": "Tröegs Independent Brewing", "style": "Doppelbock", "abv": 8.2, "ibu": 25, "price": 10.99},    {"name": "Duvel Belgian Golden Ale", "brewery": "Duvel Moortgat Brewery", "style": "Belgian Strong Pale Ale", "abv": 8.5, "ibu": 32, "price": 13.99}
]


products = beers
for p in products:
    service.create_product(CreateProductRequest(**p))
    service.create_beer(CreateBeerRequest(**p))

app = FastAPI(
    title="Restaurant API",
    description="Operaciones de pedidos y estado de pedidos de restaurantes.",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "ordenes",
            "description": "Operaciones asociadas a las ordenes de **productos**.",
        },
        {
        "name": "menus",
        "description": "Operaciones asociadas a los **menus** y sus **productos** asociados.",
        }
    ],
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Servidor local"
        }
    ]
)

@app.post("/products", tags=["menus"])
async def create_product(product: CreateProductRequest) -> Product:
    """
    Crea un nuevo producto asociado al restaurante.

    - **name**: Nombre del producto.
    - **price**: Precio del producto.

    ```
    """
    return service.create_product(product)


@app.get("/products", tags=["menus"])
async def get_products() -> list[Product]:
    """
    Obtiene una lista de todos los productos.

    - **id**: ID del producto.
    - **name**: Nombre del producto.
    - **price**: Precio del producto.

    ```
    """
    return service.get_products()


@app.post("/products/beers", tags=["menus"])
async def create_beer(beer: CreateBeerRequest) -> Beer:
    """
    Crea un item de cerveza.

    - **name**: Nombre de la cerveza.
    - **price**: Precio de la cerveza.
    - **brewery**: La cervecería que produce la cerveza.
    - **style**: El estilo de la cerveza (p. ej., India Pale Ale, Stout).
    - **abv**: El porcentaje de alcohol por volumen (ABV) de la cerveza.
    - **ibu**: La calificación de Unidades Internacionales de Amargor (IBU) de la cerveza.
    
    """
    return service.create_beer(beer)


@app.get("/products/beers")
async def get_beers() -> list[Beer]:
    """
    Obtiene una lista de cervezas

    - **name**: Nombre de la cerveza.
    - **price**: Precio de la cerveza.
    - **brewery**: La cervecería que produce la cerveza.
    - **style**: El estilo de la cerveza (p. ej., India Pale Ale, Stout).
    - **abv**: El porcentaje de alcohol por volumen (ABV) de la cerveza.
    - **ibu**: La calificación de Unidades Internacionales de Amargor (IBU) de la cerveza.
    
    """
    return service.get_product_beer()


@app.post("/menus", tags=["menus"])
async def create_menu(menu: CreateMenuRequest) -> Menu:
    """
    Crea un nuevo menú.
    - **id**: ID del menú.
    - **name**: Nombre del menú.
    - **products**: Productos que incluye el menú.
    ```
    """
    return service.create_menu(menu)


@app.get("/menus/{menu_id}", tags=["menus"])
async def get_menu_by_id(menu_id: str) -> Menu:
    """
    Obtener un menú por su ID.
    """
    return service.get_menu_by_id(menu_id)


@app.post("/orders", tags=["ordenes"])
async def create_order(order: Order) -> Response:
    """
    Crea un pedido de productos al restaurante
    - **products**: Productos asociados al pedido.
    - **observation**: Observación especial sobre el pedido como algun ingrediente extra o opciones especiales por algun producto.
    """
    service.create_order(order)
    return Response(message="Orden Creada")


@app.get("/orders", tags=["ordenes"])
async def get_order() -> list[Order]:
    """
    Obtiene una lista de las ordenes creadas, cada item tiene las siguientes caracteristicas:
    - **products**: Productos asociados al pedido.
    - **observation**: Observación especial sobre el pedido como algun ingrediente extra o opciones especiales por algun producto.
    """
    orders = service.get_orders()
    return orders
