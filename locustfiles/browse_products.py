from locust import HttpLocust, HttpUser, task, between
from random import randint

class WebsiteUSer(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def view_products(self):
        print('viewing products...')
        collection_id = randint(1,10)
        self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='store/products')
 
    @task(4) 
    def view_product(self):
        print('viewing products details...')
        product_id = randint(1,500)
        self.client.get(
            f'/store/products/{product_id}',
            name='store/products/:id')
        

    @task(1)
    def add_to_cart(self):
        print('adding to cart...')
        product_id = randint(1,10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name ='store/carts/items',
            json={'product_id' : product_id, 'quantity' : 1}
            )
 

    def on_start(self) -> None:
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']
        return super().on_start()

 