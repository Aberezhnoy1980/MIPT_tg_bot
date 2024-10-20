class Asset:
    def __init__(self, asset_id, quantity, unit_price, owner_id, purchase_date):
        self.asset_id = asset_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.owner_id = owner_id
        self.purchase_date = purchase_date

    def __eq__(self, other):
        if isinstance(self, other):
            return (self.owner_id == other.owner_id
                    and self.asset_id == other.asset_id
                    and self.quantity == other.quantity
                    and self.unit_price == other.unit_price
                    and self.purchase_date == other.purchase_date
                    )
        return False
