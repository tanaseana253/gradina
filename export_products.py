import csv
from store.models import Product

def run():
    with open("exported_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "price", "category", "stock"])

        for p in Product.objects.all():
            writer.writerow([p.name, p.price, p.category, p.stock])

    print("✔ Export complete: exported_products.csv")
