# A Simple Grocery Inventory App (backend).

It's possible to run the app in development with `python run.py`. To simulate production, use `gunicorn -b 0.0.0.0:8000 wsgi:app`.

## Build the Dockerfile to create image and run:
1. Build the Docker image from the `Dockerfile` with: `docker build -t <dockerhub-username>/<project-name> .`
2. Run the image as container: `docker run -p 8000:8000 <dockerhub-username>/<project-name>`
3. Push the Docker image to Docker Hub: `docker push <dockerhub-username>/<project-name>:latest`

#### In the `Dockerfile` The following command installs development tools (build-essential) and other libraries (libpq-dev, libssl-dev) that might be required by Python packages (like PostgreSQL or cryptography libraries).

```
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \ 
    libpq-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
```

In the example above, `rm -rf /var/lib/apt/lists/*` is used to remove the package list after installation to reduce the size of the final image.

## Using Postgresql Database in production:
1. Use the official dockerhub `postgres` image which will run alongside the flask app container:
   ```
   docker run -d --name tiny_grocery_postgres \
   -e POSTGRES_USER=user \
   -e POSTGRES_PASSWORD=1234$PaSsWoRd \
   -e POSTGRES_DB=tiny_grocery_db \
   -p 5433:5432 \
   -v postgres_data:/var/lib/postgresql/data \
   postgres:17
   ```
      Since locally installed PostgreSQL also listens on PORT 5432, the container will use PORT 5433.
      
      For data persistence, here I'm using a Docker volume named `postgres_data`.

2. Build the docker image: ```docker build -t dockerhub_user/flask-tiny-grocery .```
   
3. Run the Flask app image: ```docker run -d --name flask-tiny-grocery \-e DATABASE_URI="postgresql://user:1234$PaSsWoRd@<UBUNTU/HOST_IP>:5433/tiny_grocery_db" -p 8000:8000 dockerhub_user/flask-tiny-grocery```

4. Since the production database **hasn't been migrated**, get into the flask app container and run migrations:

   1. ```docker exec -it <flask_app_container_id> flask db init```
   2.   ```docker exec -it <flask_app_container_id> flask db migrate -m "Postgres Initial Migration."```
   3.   ```docker exec -it <flask_app_container_id> flask db upgrade```

5.   To get inside the postgres container run: ```docker exec -it tiny_grocery_postgres bash```
   
      Run any command, such as- `ls`.
      
      To run postgres commands, run ```root@<postgres_container_id>:/# psql -U user -d tiny_grocery_db```. Inside you can run any postgresql command. To exit to bash, use `\q`. 

## Deploy to Kubernetes
1. Start `Minikube` with `minikube start`.
2. Check if `Minikube` is running properly with `minikube status`:
	```
   minikube
   type: Control Plane
   host: Running
   kubelet: Running
   apiserver: Running
   kubeconfig: Configured
	```
3. Set `alias='minikube kubectl --'`
4. Apply the YAML files with: </br>
  `kubectl apply -f manifest/deployment.yaml` </br>
  `kubectl apply -f manifest/service.yaml` </br>
  `kubectl apply -f manifest/secret.yaml`
1. Check if pods are deployed with `kubectl get pods`.
	```
      NAME                                            READY   STATUS    RESTARTS   AGE
      flask-tiny-grocery-deployment-c554d9c4d-dkj8f   1/1     Running   0          6m29s
      flask-tiny-grocery-deployment-c554d9c4d-rvk7m   1/1     Running   0          6m47s
	```

2. Check if the service is running with `kubectl get svc`.
	```
      NAME                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
      flask-tiny-grocery-service   NodePort    10.109.247.147   <none>        8000:30000/TCP   31m
      kubernetes                   ClusterIP   10.96.0.1        <none>        443/TCP          40m
	```
3. Obtain the minikube ip with `minikube ip`.
4. In a web browser, access the service with `http://<minikube-ip>:<nodeport>`. Here, nodeport is 30000.

_______________________________________________________________________

### Grocery Store Product Categories and examples:

<em>
Fruits – bananas, apples, grapes, oranges, strawberries, avocados, peaches, pineapple, pears, etc. </br>
Vegetables – potatoes, tomatoes, onions, carrots, lettuce, broccoli, peppers, celery, garlic, cucumbers, etc. </br>
Canned Goods – olives, soup, tuna, veggies, fruit, etc. </br>
Frozen Foods – fish, ice cream, pizza, potatoes, ready meals, etc. </br>
Meat – chicken, beef, pork, sausage, etc. </br>
Fish and shellfish – shrimp, crab, clams, tuna, salmon, tilapia, etc. </br>
Deli – chees, ham, turkey, salami, etc. </br>
Condiments & Spices – salt, sugar, pepper, oregano, cinnamon, ketchup, mayonnaise, mustard , etc. </br>
Sauces & Oils – olive oil, tomato sauce, hot sauce, soy sauce, etc. </br>
Snacks – chips, crackers, pretzels, popcorn, peanuts, nuts, candy, etc. </br>
Bread & Bakery – whole wheat, white, italian, sandwich, tortillas, pies, muffins, bagels, cookies, etc. </br>
Beverages – water, coffe, milk, juice, soda, tea, beer, wine, etc. </br>
Pasta/Rice – spaghetti, macaroni, noodles, white rice, etc. </br>
Cereal – oats, rice, wheat, granola, etc. </br>
Baking – flour, baking powder, butter, milk, eggs, etc. </br>
Personal Care – shampoo, conditioner, soap, deodorant, toothpaste, dental floss, shaving cream, razor blades, etc. </br>
Health Care – band-aid, hydrogen peroxide, alcohol, pain reliever, antacids, etc. </br>
Paper & Wrap – toilet paper, paper towels, tissues, aluminum foil, zip bags, etc. </br>
Household Supplies – detergent, softener, bleach, dish soap, air freshener, gloves, sponge, trash bags, batteries, etc. </br>
Baby Items – baby food, diapers, wet wipes, moisturizing lotion, etc. </br>
Other items – pet food, flowers, tobacco, etc. </br>
</em>
______________________________________________________________________


### Populating data to the SQLite database from Flask shell.
Activate the Python virtual environment with `source env/bin/activate`. Open Flask shell with `flask shell`:
```
>>> from app.models import db, Category, Product, Inventory
>>> p = Product(name="brown bread", retail_price=7.0, manufacturer="alma co", batch_no="ABCB101", unit_of_measure="pouch", weight_per_unit=150.0, category_id=1)
>>> from datetime import datetime
>>> p.mfg_date = datetime(2025, 3, 10, 12, 00, 0)
>>> db.session.commit()
>>> i = Inventory(purchase_price=5.0, max_qty=100.0, available_qty=100.0, reorder_level=20.0, reorder_qty=50.0, shelf_no=3, exp_date=datetime(2025, 3, 17, 12, 00, 00), is_available=True, product_id=1)
>>> db.session.add(i)
>>> db.session.commit()
```
Exit Flask shell by pressing `ctrl+z` or entering `exit()`.

#### Syntax of `JSON` **POST** request for new product:
```
{
	"name": "delicious toast",
	"retail_price": 40.0,
	"description": "toast biscuit",
	"manufacturer": "goodfoods enterprise",
	"supplier": "rhino foods",
	"batch_no": "GHF456",
	"mfg_date": "2025-03-01T00:00:00",
	"exp_date": "2025-09-01T12:00:00",
	"unit_of_measure": "packet",
	"weight_per_unit": 325.0,
	"category_id": 1
}
```
