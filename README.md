<p>A Simple Grocery Inventory backend. Monolith.</p>

<code>
>>> p = Product(name="brown bread", retail_price=7.0, manufacturer="alma co", batch_no="ABCB101", unit_of_measure="pouch", weight_per_unit=150.0, category_id=1)
>>>from datetime import datetime
>>> p.mfg_date = datetime(2025, 3, 10, 12, 00, 0)
>>> db.session.commit()
>>>i = Inventory(purchase_price=5.0, max_qty=100.0, available_qty=100.0, reorder_level=20.0, reorder_qty=50.0, shelf_no=3, exp_date=datetime(2025, 3, 17, 12, 00, 00), is_available=True, product_id=1)
>>> db.session.add(i)
>>> db.session.commit()
</code>
