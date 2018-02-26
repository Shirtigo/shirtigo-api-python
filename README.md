# shirtigo-api-python
A python implementation of a client for the shirtigo print API.
Check out our [REST-API documentation](https://cockpit.shirtigo.de/docs/rest-api/) for a full list of all features.

# Basic usage
## Client object initialization
```
BASE_URL = "https://testing.cockpit.shirtigo.de/api/"
API_TOKEN = "YOUR_API_TOKEN"
client = ApiClient(API_TOKEN, BASE_URL)
```
## Access your shirtigo user data
```
    data = client.get("user")
    print(data["firstname"], data["lastname"])
```

## Create a project
```
    data = {'name' : "My test project " + random_string() }
    project = client.post('projects', data=data)
```

## Uploading a design
 The product creation reqires to upload a design first.
### From file:
```
    design_path = './test_design.png'
    design = client.post("designs/file", files={"file": (os.path.basename(design_path),
                                                        open(design_path, 'rb').read())
                                                })
```
### From URL:
```
    data = {"url" : "https:/my-web-storage/my-design.png"}
    design = client.post("designs/url", data=data)
```

## Get a list of your existing designs
```
    designs = client.get('designs')['data']
```

## Add a processing area to a project
```
    data= {
          "area": "front",
          "position": "center",
          "method": "print",
          "design": design['reference'],
          "offset_top": 300,
          "offset_center": 10,
          "width": 200,
          # "base_products" : [ ids]
    }
    client.post("projects/" + project['reference'] + "/processings", data=data)
```

## Get a list of available base products to process (print)
```
    base_products = client.get('base-products')['data']
```

we select the last one for our test
```
    base_product = base_products[-1]
    colors = [color['id'] for color in base_product['colors']['data']]
    test_sizes = [color['sizes'][0]['id'] for color in base_product['colors']['data']]
```

## Create a product
Product creation combines a base product, and a project.
Let's create a product with our design on the shirt front
```
    data = {
    "project_id": project['reference'],
    "base_product_id": base_product['id'],
    "colors": colors
    }
    product = client.post('products', data = data)
```

## Publish finished project
 Finished projects need to be published before products can be ordered from a project
```
    data = {'project-reference' : project['reference']}
    response = client.post('projects/' + project['reference'] + '/publish')
```

## Order a list of products
```
    products = []
    for color_id, size_id in zip(colors,test_sizes):
        products.append( {
                          "productId": product['id'],
                          "colorId": color_id,
                          "sizeId": size_id,
                          "amount": random.randint(1, 4)
                        })
    order_data = {
                "delivery": {
                "title": "Dr.",
                "company": "Shirtigo GmbH",
                "firstname": "Max",
                "lastname": "Mustermann",
                "street": "Musterstraße 12",
                "postcode": "12345",
                "city": "Köln",
                "country": "Deutschland"
                },
                "sender": {
                "title": "Dr.",
                "company": "Shirtigo GmbH",
                "firstname": "Max",
                "lastname": "Mustermann",
                "street": "Musterstraße 12",
                "postcode": "12345",
                "city": "Köln",
                "country": "Deutschland"
                },
                "products": products
    }
```
## Check the current price for a planned order
```
    prices = client.post('orders/predict-price', data=order_data)
```
## Post order request
```
    order = client.post('orders', data=order_data)
```
