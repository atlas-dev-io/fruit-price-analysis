import matplotlib.pyplot as plt
import pandas as pd


FRUIT_LABELS = {
    "Apple": "Apple",
    "Banana": "Banana",
    "Orange": "Orange",
    "Grape": "Grape",
    "Pear": "Pear",
}


def save_price_chart(df: pd.DataFrame, output_path) -> None:
    plt.figure(figsize=(10, 6))
    for fruit_name, group in df.groupby("fruit_name"):
        ordered = group.sort_values("date")
        label = FRUIT_LABELS.get(fruit_name, fruit_name)
        plt.plot(ordered["date"], ordered["price"], marker="o", label=label)

    plt.title("Fruit Price Trends")
    plt.xlabel("Date")
    plt.ylabel("Price (yuan/kg)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
