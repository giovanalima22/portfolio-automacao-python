from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("output")
OUT.mkdir(exist_ok=True)

def load_files():
    files = sorted(RAW.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No CSV files found. Run generate_data.py first.")
    return pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

def transform(df):
    df = df.copy()

    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["customer"] = df["customer"].fillna("Cliente não informado").str.strip()
    df["product"] = df["product"].str.strip().str.title()

    for col in ["quantity", "unit_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["sale_id", "sale_date", "product_id", "quantity", "unit_price"]
    )
    df = df.drop_duplicates(subset=["sale_id"])

    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["sale_date"].dt.to_period("M").astype(str)
    return df

def create_outputs(df):
    monthly = (
        df.groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("sale_id", "nunique"),
            items=("quantity", "sum"),
        )
    )
    monthly["average_order_value"] = monthly["revenue"] / monthly["orders"]

    products = (
        df.groupby(["product_id", "product"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("sale_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )

    excel_path = OUT / "relatorio_vendas.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Vendas", index=False)
        monthly.to_excel(writer, sheet_name="Resumo Mensal", index=False)
        products.to_excel(writer, sheet_name="Produtos", index=False)

    monthly.to_csv(OUT / "resumo_mensal.csv", index=False)
    print(f"Created: {excel_path}")
    print(f"Records processed: {len(df)}")

def main():
    raw = load_files()
    clean = transform(raw)
    create_outputs(clean)

if __name__ == "__main__":
    main()
