import csv
from store.models import Product

def run():
    file_path = "exported_products.csv"

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name = row["name"].strip()

            product, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "price": row["price"].strip(),
                    "category": row["category"].strip(),
                    "stock": int(row["stock"]) if row["stock"] else 0,
                }
            )

            print(("Created:" if created else "Updated:"), name)

    print("✔ Import completed!")
