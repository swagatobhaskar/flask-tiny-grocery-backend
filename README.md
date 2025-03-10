<h3>A Simple Grocery Inventory backend. Monolith.</h3>

<p>

`from app.models import db, Category, Product, Inventory`

`p = Product(name="brown bread", retail_price=7.0, manufacturer="alma co", batch_no="ABCB101", unit_of_measure="pouch", weight_per_unit=150.0, category_id=1)`

`from datetime import datetime`

`p.mfg_date = datetime(2025, 3, 10, 12, 00, 0)`

`db.session.commit()`

`i = Inventory(purchase_price=5.0, max_qty=100.0, available_qty=100.0, reorder_level=20.0, reorder_qty=50.0, shelf_no=3, exp_date=datetime(2025, 3, 17, 12, 00, 00), is_available=True, product_id=1)`

`db.session.add(i)`

`db.session.commit()`

</p>

<p>
JSON new product:
<code>
{
	"name": "voja toast",
	"retail_price": 40.0,
	"description": "toast biscuit",
	"manufacturer": "voja enterprise",
	"supplier": "rino foods",
	"batch_no": "GHF456",
	"mfg_date": "2025-03-01T00:00:00",
	"exp_date": "2025-09-01T12:00:00",
	"unit_of_measure": "packet",
	"weight_per_unit": 325.0,
	"category_id": 1
}
</code>
</p>
