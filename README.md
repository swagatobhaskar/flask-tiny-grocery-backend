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

<p>
Fruits – bananas, apples, grapes, oranges, strawberries, avocados, peaches, pineapple, pears, etc. </br>
Vegetables – potatoes, tomatoes, onions, carrots, lettuce, broccoli, peppers, celery, garlic, cucumbers, etc.</br>
Canned Goods – olives, soup, tuna, veggies, fruit, etc.</br>
Frozen Foods – fish, ice cream, pizza, potatoes, ready meals, etc.</br>
Meat – chicken, beef, pork, sausage, etc.</br>
Fish and shellfish – shrimp, crab, clams, tuna, salmon, tilapia, etc.</br>
Deli – chees, ham, turkey, salami, etc.</br>
Condiments & Spices – salt, sugar, pepper, oregano, cinnamon, ketchup, mayonnaise, mustard , etc.</br>
Sauces & Oils – olive oil, tomato sauce, hot sauce, soy sauce, etc.</br>
Snacks – chips, crackers, pretzels, popcorn, peanuts, nuts, candy, etc.</br>
Bread & Bakery – whole wheat, white, italian, sandwich, tortillas, pies, muffins, bagels, cookies, etc.</br>
Beverages – water, coffe, milk, juice, soda, tea, beer, wine, etc.</br>
Pasta/Rice – spaghetti, macaroni, noodles, white rice, etc.</br>
Cereal – oats, rice, wheat, granola, etc.</br>
Baking – flour, baking powder, butter, milk, eggs, etc.</br>
Personal Care – shampoo, conditioner, soap, deodorant, toothpaste, dental floss, shaving cream, razor blades, etc.</br>
Health Care – band-aid, hydrogen peroxide, alcohol, pain reliever, antacids, etc.</br>
Paper & Wrap – toilet paper, paper towels, tissues, aluminum foil, zip bags, etc.</br>
Household Supplies – detergent, softener, bleach, dish soap, air freshener, gloves, sponge, trash bags, batteries, etc.</br>
Baby Items – baby food, diapers, wet wipes, moisturizing lotion, etc.</br>
Other items – pet food, flowers, tobacco, etc.</br>
</p>
