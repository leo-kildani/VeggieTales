from . import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 

    product_memory = {

        "Apple": {
            "type": "Fruit", 
            "price $": 1.0,
            "quantity": 100,
            "time": 12.25,
            "climate": 70,
        },
        "Banana": {
            "type": "Fruit",
            "price $": 1.0,
            "quantity": 200,
            "time": 12.25,
            "climate": 70,
        },
        "Carrot": {
            "type": "Vegetable",
            "price $": 1.0,
            "quantity": 150,
            "time": 12.25,
            "climate": 70,
        }, 
        "Broccoli": {
            "type": "Vegetable",
            "price $": 1.0,
            "quantity": 50,
            "time": 12.25,
            "climate": 70,
        },
        "Orange": {
            "type": "Fruit",
            "price $": 1.0,
            "quantity": 120,
            "time": 12.25, 
            "climate": 70,
        },
    }

    # product_memory = {
    #     "Selected produce": {
    #         "Fruit": "Apple",    
    #         "price $:": 1.0,
    #         "quantity -->": 100
    #     },
    #}

#displaying the information in a more story like - simple to read
description = """
This produce is a {type} with a price of ${price} and a quantity of {quantity} this came from the farm to the store in {time} minutes and had a {climate} freiheit degrees climate during its trip. 
It took {gallons} gallones of water for it to grow and was spreayed with {pesticiles} 
""".format(
    fruit=product_memory["Selected produce"]["Fruit"],
    fruit=product_memory["Apple"]["type"],
    price=product_memory["Apple"]["price $"],
    quantity=product_memory["Apple"]["quantity"])
print(description)