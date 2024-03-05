class EnergyMarketplace:
    def __init__(self):
        self.listings = []
        self.orders = []
        self.filled_orders = []

    def list_energy(self, producer_id, energy_amount, price, type, location):
        listing = {
            'producer_id': producer_id,
            'energy_amount': energy_amount,
            'price': price,
            'type': type,
            'location': location
        }
        self.listings.append(listing)
    
    def place_order(self, consumer_id, listing_id, energy_amount):
        listing = self.find_listing(listing_id)
        if listing and listing['energy_amount'] >= energy_amount:
            order = {
                'consumer_id': consumer_id,
                'listing_id': listing_id,
                'energy_amount': energy_amount,
                'price': listing['price'] * energy_amount
            }
            self.orders.append(order)
            listing['energy_amount'] -= energy_amount  # Update listing amount
            print(f"Order placed: {order}")
        else:
            print("Listing not found or insufficient energy amount")

    def find_listing(self, listing_id):
        for listing in self.listings:
            if listing['producer_id'] == listing_id:
                return listing
        return None
