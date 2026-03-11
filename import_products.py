import csv
from store.models import Product

def run():
    file_path = "exported_products.csv"

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Normalize keys (strip whitespace)
            row = {k.strip(): v for k, v in row.items()}

            name = row.get("name")
            price = row.get("price")
            category = row.get("category")
            stock = row.get("stock") or 0

            if not name:
                print("Skipping row: missing name")
                continue

            obj, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "price": price,
                    "category": category,
                    "stock": int(stock),
                }
            )

            print(("Created: " if created else "Updated: ") + name)

    print("✔ Import completed!")
