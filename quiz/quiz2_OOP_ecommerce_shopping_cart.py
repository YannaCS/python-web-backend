from abc import ABC, abstractclassmethod
from datetime import datetime

class Product(ABC):
    _id_counter = 1
    def __init__(self, name: str, price: int, stock: int):
        self.id = Product._id_counter
        Product._id_counter += 1

        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self) -> str:
        return f'product {self.id}: {self.name}'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Product):
            return self.id == other.id
        return False

    @abstractclassmethod
    def get_product_info(self):
        pass

    @abstractclassmethod
    def get_category(self):
        pass

    def is_in_stock(self, quantity: int) -> bool:
        return self.stock >= quantity
    
    def reduce_stock(self, quantity) -> bool:
        if quantity > self.stock:
            return False
        self.stock -= quantity
        return True
    
class ClothingProduct(Product):
    def __init__(self, name: str, price: int, stock: int, size: str, color: str):
        super().__init__(name, price, stock)
        self.size = size
        self.color = color

    def get_product_info(self):
        return f"size: {self.size} color: {self.color}"
    
    def get_category(self):
        return "Clothing"
    
class FoodProduct(Product):
    def __init__(self, name: str, price: int, stock: int, expiration_date: str):
        super().__init__(name, price, stock)
        self.expiration_date = expiration_date

    def get_product_info(self):
        return f"expiration_date: {self.expiration_date}"
    
    def is_expired(self):
        expiration_date = datetime.strptime(self.expiration_date, '%Y-%m-%d').date()
        now = datetime.now().date()
        if expiration_date < now:
            return True
        
        return False

    def get_category(self):
        return "Food"
    

class ShoppingCart():
    def __init__(self):
        self.items = {}  # product_id: (product, quantity)
    
    def add_item(self, product: Product, quantity: int):
        if quantity > product.stock:
            raise ValueError(f"Insufficient stock for {product.name}. "
                             f"Requested: {quantity}, Available: {product.stock}")
        
        if product.id in self.items:
            _, current_qty = self.items[product.id]
            new_quantity = current_qty + quantity
            if new_quantity > product.stock:
                raise ValueError(f"Insufficient stock for {product.name}. "
                             f"Requested: {new_quantity}, Available: {product.stock}")
            self.items[product.id] = (product, new_quantity)
        else:
            self.items[product.id] = (product, quantity)
    
    def remove_item(self, product: Product):
        if product.id in self.items:
            del self.items[product.id]
            return True
        return False
    
    def get_total(self):
        total = 0
        for product_id, (product, quantity) in self.items.items():
            total += product.price * quantity
        return total
    
    def get_items(self):
        return [(product, quantity) for product, quantity in self.items.values()]
    
    def clear_cart(self):
        self.items.clear()

    def checkout(self):
        """
        Steps:
        1. Display order summary
        2. Update inventory
        3. Clear cart
        """
        if not self.items:
            print('Cart is empty. Nothing to checkout.')
            return
        
        # Display Order Summary
        print("=" * 50)
        print("ORDER SUMMARY")
        print("=" * 50)

        for product_id, (product, quantity) in self.items.items():
            item_total = product.price * quantity
            print(f"{product.name} x {quantity} @ ${product.price:.2f} = ${item_total:.2f}")
        
        print("-" * 50)
        print(f"TOTAL: ${self.get_total():.2f}")
        print("=" * 50)

        # Update Inventory
        for product_id, (product, quantity) in self.items.items():
            product.reduce_stock(quantity)

        # Clear Cart
        self.clear_cart()
        
        print("\nOrder processed successfully!")
        print("Thank you for your purchase!")

    def __len__(self) -> int:
        return len(self.get_items())



 #========== TEST CASES ==========

def test_basic_cart_operations():
    print("\n" + "="*60)
    print("TEST 1: Basic Cart Operations")
    print("="*60)
    
    # Create products
    shirt = ClothingProduct("T-Shirt", 25, 10, "M", "Blue")
    jeans = ClothingProduct("Jeans", 60, 5, "L", "Black")
    apple = FoodProduct("Apple", 2, 50, "2025-12-31")
    
    # Create cart
    cart = ShoppingCart()
    
    # Add items
    print(f"\nAdding 2 {shirt.name} to cart...")
    cart.add_item(shirt, 2)
    print(f"Cart length: {len(cart)}")
    
    print(f"\nAdding 1 {jeans.name} to cart...")
    cart.add_item(jeans, 1)
    print(f"Cart length: {len(cart)}")
    
    print(f"\nAdding 5 {apple.name} to cart...")
    cart.add_item(apple, 5)
    print(f"Cart length: {len(cart)}")
    
    # Display cart
    print("\nCurrent cart items:")
    for product, quantity in cart.get_items():
        print(f"  - {product.name}: {quantity} x ${product.price} = ${product.price * quantity}")
    
    print(f"\nTotal: ${cart.get_total():.2f}")


def test_stock_validation():
    print("\n" + "="*60)
    print("TEST 2: Stock Validation")
    print("="*60)
    
    # Create product with limited stock
    jacket = ClothingProduct("Jacket", 100, 3, "XL", "Red")
    cart = ShoppingCart()
    
    print(f"\n{jacket.name} has {jacket.stock} items in stock")
    
    # Try to add more than available
    try:
        print(f"\nAttempting to add 5 {jacket.name} (more than stock)...")
        cart.add_item(jacket, 5)
    except ValueError as e:
        print(f"❌ Error caught: {e}")
    
    # Add valid quantity
    print(f"\nAdding 2 {jacket.name} (within stock)...")
    cart.add_item(jacket, 2)
    print(f"✓ Success! Cart has {len(cart)} items")
    
    # Try to add more that would exceed stock
    try:
        print(f"\nAttempting to add 2 more {jacket.name} (total would be 4, exceeds stock of 3)...")
        cart.add_item(jacket, 2)
    except ValueError as e:
        print(f"❌ Error caught: {e}")
    
    print(f"\nFinal cart quantity: {len(cart)} items")


def test_remove_item():
    print("\n" + "="*60)
    print("TEST 3: Remove Item")
    print("="*60)
    
    # Create products and cart
    banana = FoodProduct("Banana", 1, 100, "2025-11-25")
    orange = FoodProduct("Orange", 2, 80, "2025-11-30")
    cart = ShoppingCart()
    
    # Add items
    cart.add_item(banana, 10)
    cart.add_item(orange, 5)
    
    print(f"\nCart has {len(cart)} items")
    print("Items:")
    for product, quantity in cart.get_items():
        print(f"  - {product.name}: {quantity}")
    
    # Remove an item
    print(f"\nRemoving {banana.name}...")
    result = cart.remove_item(banana)
    print(f"Remove successful: {result}")
    print(f"Cart now has {len(cart)} items")
    
    # Try to remove non-existent item
    print(f"\nTrying to remove {banana.name} again...")
    result = cart.remove_item(banana)
    print(f"Remove successful: {result}")


def test_checkout_process():
    print("\n" + "="*60)
    print("TEST 4: Checkout Process")
    print("="*60)
    
    # Create products
    hoodie = ClothingProduct("Hoodie", 45, 8, "L", "Gray")
    socks = ClothingProduct("Socks", 8, 20, "M", "White")
    bread = FoodProduct("Bread", 3, 15, "2025-11-22")
    
    print("\nInitial stock levels:")
    print(f"  - {hoodie.name}: {hoodie.stock}")
    print(f"  - {socks.name}: {socks.stock}")
    print(f"  - {bread.name}: {bread.stock}")
    
    # Create cart and add items
    cart = ShoppingCart()
    cart.add_item(hoodie, 2)
    cart.add_item(socks, 3)
    cart.add_item(bread, 2)
    
    print(f"\nCart has {len(cart)} items")
    
    # Checkout
    print("\nProcessing checkout...")
    cart.checkout()
    
    print("\nStock levels after checkout:")
    print(f"  - {hoodie.name}: {hoodie.stock}")
    print(f"  - {socks.name}: {socks.stock}")
    print(f"  - {bread.name}: {bread.stock}")
    
    print(f"\nCart after checkout: {len(cart)} items")


def test_empty_cart_checkout():
    print("\n" + "="*60)
    print("TEST 5: Empty Cart Checkout")
    print("="*60)
    
    cart = ShoppingCart()
    print(f"\nCart has {len(cart)} items")
    print("\nAttempting to checkout empty cart...")
    cart.checkout()


def test_food_expiration():
    print("\n" + "="*60)
    print("TEST 6: Food Product Expiration")
    print("="*60)
    
    expired_milk = FoodProduct("Milk", 4, 10, "2025-01-01")
    fresh_milk = FoodProduct("Fresh Milk", 4, 10, "2025-12-31")
    
    print(f"\n{expired_milk.name} (expires: {expired_milk.expiration_date})")
    print(f"  Is expired: {expired_milk.is_expired()}")
    
    print(f"\n{fresh_milk.name} (expires: {fresh_milk.expiration_date})")
    print(f"  Is expired: {fresh_milk.is_expired()}")


def test_product_info():
    print("\n" + "="*60)
    print("TEST 7: Product Information")
    print("="*60)
    
    dress = ClothingProduct("Summer Dress", 75, 5, "S", "Yellow")
    cheese = FoodProduct("Cheese", 6, 12, "2025-12-15")
    
    print(f"\n{dress}")
    print(f"  Category: {dress.get_category()}")
    print(f"  Info: {dress.get_product_info()}")
    print(f"  Price: ${dress.price}")
    print(f"  Stock: {dress.stock}")
    
    print(f"\n{cheese}")
    print(f"  Category: {cheese.get_category()}")
    print(f"  Info: {cheese.get_product_info()}")
    print(f"  Price: ${cheese.price}")
    print(f"  Stock: {cheese.stock}")


# Run all tests
if __name__ == "__main__":
    print("\n" + "🛒 SHOPPING CART SYSTEM TESTS 🛒".center(60))
    
    test_basic_cart_operations()
    test_stock_validation()
    test_remove_item()
    test_checkout_process()
    test_empty_cart_checkout()
    test_food_expiration()
    test_product_info()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")