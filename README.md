# krakenStandingOrder
Create orders on kraken, with the current bid price.

# How To
## Pre-Requirements
This project needs the [krakenConnector](https://github.com/codesie/krakenConnector). For
instructions have a look at the projects README.md file.

Furthermore, a config file needs to exist with the following structure:
```json
{
    "krakenConnector": {
        "api_key": "API-KEY-API-KEY from kraken",
        "secret": "API-SECRET-API-SECRET from kraken"
    },
    "standingOrder": {
        "ADAEUR": 20,
        "XETHZEUR": 20,
        "DOTEUR": 10,
        "XXBTZEUR": 20
    }
}
```
The example file `config-example.json` can be found in this repo.

## Use krakenStandingOrder
The script has two modes. In the demo mode, nothing will be sent to kraken. It just shows,
what it would do.
```commandline
python3 standingOrder.py
```

The `prod` mode will create the orders on kraken:
```commandline
python3 standingOrder.py -m prod
```

### What happens
Each time the script runs, it queries the price(ticker) information for the 
provided pairs and creates a new buy order with the last bid price.

In the config file you can provide below `standingOrder` the currencies, you
want to buy and how much money you want to invest.

#### Log Example after execution in prod mode
```commandline
2021-12-28 11:28:18 INFO --- Order placed on kraken!
2021-12-28 11:28:19 INFO {
  "pair": "XXBTZEUR",
  "type": "buy",
  "ordertype": "limit",
  "price": 43309.6,
  "volume": 0.0004617913811256627,
  "nonce": 1640687298597
}
2021-12-28 11:28:19 INFO --- Order placed on kraken!
2021-12-28 11:28:19 INFO {
  "pair": "XETHZEUR",
  "type": "buy",
  "ordertype": "limit",
  "price": 3448.98,
  "volume": 0.005798815881796937,
  "nonce": 1640687299010
}
2021-12-28 11:28:19 INFO --- Order placed on kraken!
2021-12-28 11:28:20 INFO {
  "pair": "ADAEUR",
  "type": "buy",
  "ordertype": "limit",
  "price": 1.294408,
  "volume": 15.45107879432142,
  "nonce": 1640687299626
}
2021-12-28 11:28:20 INFO --- Order placed on kraken!
2021-12-28 11:28:21 INFO {
  "pair": "DOTEUR",
  "type": "buy",
  "ordertype": "limit",
  "price": 25.9243,
  "volume": 0.38573847702734504,
  "nonce": 1640687300624
}
```