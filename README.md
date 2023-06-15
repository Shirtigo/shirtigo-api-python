# shirtigo-api-python
A python implementation of a client for the shirtigo print API.
Check out our [REST-API documentation](https://cockpit.shirtigo.com/docs/rest-api/) for a full list of all features.

# Basic usage
## Client object initialization
```
BASE_URL = "https://cockpit.shirtigo.com/api/"
API_TOKEN = "YOUR_API_TOKEN"
client = ApiClient(API_TOKEN, BASE_URL)
```
## Access your shirtigo user data
```
    data = client.get("user")
    print(data["firstname"], data["lastname"])
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

# Create a product collection
Products are organized into collections, with each baseProduct being assignable to a collection/ project only once. To create a new product, first create a project, and then, in a subsequent step, assign the desired products to that project.

## Create a project
```
    data = {'name' : "My test project " + random_string() }
    project = client.post('projects', data=data)
```

## Add a product to the project
In this example we will add a black Organic Shirt with a one-sided print to our project. The processing specifications define the design, its placement, dimensions, and other relevant details needed for customizing the BaseProduct. Please not, that you can add custom processings for each color.
```
data = {
    "project_id": project.reference,
    "base_product_id": 235,
    "processings": [
        {
            "processingarea_type": "front",
            "processingmethod": "dtg",
            "design_reference": design.reference,
            "offset_top": 50,
            "offset_center": 0,
            "width": 250,
            "is_customizable": False,
            "force_position": False,
            "colors": [
                {
                    "colorId": 326,
                    "price": 2195,
                    "sortPosition": 1
                }
            ]
        }
    ]
}

$product = client.post('customized-product', data=data)
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
