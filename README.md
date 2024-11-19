# receipt-recognition
A package for receipt formatting to improve house accounting.

This library is designed for further connection with application backend, but it can also directly used with
`python main.py --image image_path`

## Samples
### Whole Foods Receipt
![Whole Foods](https://github.com/ralph831005/receipt-recognition/blob/main/sample/whole_foods.jpg)
### Output
```yaml
{
    "store": "WHOLE FOODS MARKET",
    "total_price": 68.99,
    "tax": null,
    "tax_rate": null,
    "items": [
        {"item": "OG GINGER ROOT", "price": 0.48},
        {"item": "PORK OG SHLDR BUTT RST", "price": 16.25},
        {"item": "ANDYT SGL ORIGIN COFFEE", "price": 9.69},
        {"item": "CFWTLB ETHPIA LT RT CFFEE", "price": 14.59},
        {"item": "GRWRKC OG HONDURAS CFFE", "price": 12.59},
        {"item": "SGHTGL ETHIOPIA COFFEE", "price": 15.29},
        {"item": "CARRY OUT BAG CHARGE", "price": 0.1}
    ]
}
```
### Costco Receipt
![Costco](https://github.com/ralph831005/receipt-recognition/blob/main/sample/costco.jpg)
### Output
```yaml
{
    "store": "COSTCO WHOLESALE",
    "total_price": 112.34,
    "tax": 3.97,
    "tax_rate": 9.125,
    "items": [
        {"item": "ORGANIC TOFU", "price": 6.99},
        {"item": "PASTURE EGGS", "price": 8.69},
        {"item": "BNLS/SL BRST", "price": 24.22},
        {"item": "REFRESH MEGA", "price": 28.99},
        {"item": "NEO MAX STR", "price": 14.49},
        {"item": "KS SHORTBRD", "price": 24.99}
    ]
}
```
