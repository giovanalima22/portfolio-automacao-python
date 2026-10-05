from pathlib import Path
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)
OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)

products = [
    (101, "Notebook Pro", "Eletrônicos", 4200),
    (102, "Monitor 24", "Eletrônicos", 950),
    (103, "Teclado Mecânico", "Periféricos", 420),
    (104, "Mouse Sem Fio", "Periféricos", 180),
    (105, "Headset", "Periféricos", 310),
    (106, "Webcam HD", "Periféricos", 260),
]

rows = []
start = date(2026, 1, 1)

for i in range(1, 301):
    d = start + timedelta(days=random.randint(0, 89))
    pid, name, category, price = random.choice(products)
    rows.append({
        "sale_id": i,
        "sale_date": d.isoformat(),
        "customer": f"Cliente {random.randint(1, 80):03d}",
        "product_id": pid,
        "product": name,
        "category": category,
        "quantity": random.randint(1, 5),
        "unit_price": price,
        "seller": random.choice(["Ana", "Bruno", "Carla", "Diego"]),
    })

df = pd.DataFrame(rows)
df.loc[10, "product"] = " notebook pro "
df.loc[20, "customer"] = None
df = pd.concat([df, df.iloc[[30]]], ignore_index=True)

for month, part in df.groupby(pd.to_datetime(df["sale_date"]).dt.month):
    part.to_csv(OUT / f"vendas_2026_{month:02d}.csv", index=False)

print(f"Generated {len(df)} raw records in {OUT}")
