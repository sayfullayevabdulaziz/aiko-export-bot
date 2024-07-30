from bot.core.loader import redis_client


class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cart_id = f"cart:{user_id}"
        self.redis_client = redis_client

    async def async_initilize(self):
        if not await self.redis_client.exists(self.cart_id):
            await self.redis_client.hset(self.cart_id, mapping={"_dummy": 0})
        
    async def add_item(self, item_id, quantity, price):
        """Add an item to the shopping cart."""
        await self.async_initilize()
        
        if await self.redis_client.hexists(self.cart_id, "_dummy"):
            await self.redis_client.hdel(self.cart_id, "_dummy")
        await self.redis_client.hset(self.cart_id, item_id, f"{quantity}:{price}")

    async def remove_item(self, item_id):
        """Remove an item from the shopping cart."""
        await self.redis_client.hdel(self.cart_id, item_id)

    async def get_items(self):
        """Get the current items in the shopping cart."""
        # await self.async_initilize()
        items = await self.redis_client.hgetall(self.cart_id)
        # items = {k.decode('utf-8'): int(v.decode('utf-8')) for k, v in items.items() if int(v.decode('utf-8')) != 0}
        result = {}

        if not items:
            return result

        for artikul, value in items.items():
            artikul = artikul.decode('utf-8')
            quantity, price = map(int, value.decode('utf-8').split(':'))
            if quantity != 0:
                result[artikul] = {'quantity': quantity, 'price': price}
        
        result.pop("_dummy", None)
        return result

    async def get_item(self, item_id):
        """Get the quantity of a specific item in the shopping cart."""
        await self.async_initilize()
        
        item = await self.redis_client.hget(self.cart_id, item_id)
        if item:
            quantity, price = map(int, item.decode('utf-8').split(':'))
            return (quantity, price)# {'quantity': quantity, 'price': price}
        return (None, None)
    
    async def clear_cart_from_redis(self):
        """Clear all items from the shopping cart."""
        await self.redis_client.delete(self.cart_id)

    def get_total(self, item_prices):
        """Calculate the total price of items in the cart."""
        cart_items = self.get_items()
        total = 0
        for item_id, quantity in cart_items.items():
            total += int(quantity) * item_prices.get(item_id, 0)
        return total
