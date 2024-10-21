class Asset:
    def __init__(self, asset_id, quantity, unit_price, owner_id, purchase_date):
        self.asset_id = asset_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.owner_id = owner_id
        self.purchase_date = purchase_date

    def __eq__(self, other):
        if isinstance(other, Asset):
            return (self.owner_id == other.owner_id
                    and self.asset_id == other.asset_id
                    and self.quantity == other.quantity
                    and self.unit_price == other.unit_price
                    and self.purchase_date == other.purchase_date
                    )
        return False

    def __hash__(self):
        return hash((self.asset_id, self.quantity, self.unit_price, self.owner_id))

    def __str__(self):
        return (f'id: {self.asset_id}, '
                f'quantity: {self.quantity}, '
                f'unit_price: {self.unit_price}, '
                f'owner_id: {self.owner_id}, '
                f'purchase_date: {self.purchase_date}')