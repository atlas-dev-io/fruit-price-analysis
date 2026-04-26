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


def save_risk_comparison_chart(risk_df: pd.DataFrame, output_path) -> None:
    ordered = risk_df.sort_values("composite_risk_score", ascending=False).reset_index(drop=True)
    colors = {"high": "#c0392b", "medium": "#f39c12", "low": "#27ae60"}

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        ordered["fruit_name"],
        ordered["composite_risk_score"],
        color=[colors.get(level, "#7f8c8d") for level in ordered["risk_level"]],
    )
    plt.title("Composite Risk Comparison by Fruit")
    plt.xlabel("Fruit")
    plt.ylabel("Composite Risk Score")

    for bar, level in zip(bars, ordered["risk_level"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            level,
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_seasonality_chart(profile_df: pd.DataFrame, output_path) -> None:
    plt.figure(figsize=(12, 7))
    for fruit_name, group in profile_df.groupby("fruit_name"):
        plt.plot(group["month"], group["avg_price"], marker="o", label=fruit_name)

    plt.title("Monthly Seasonality Profiles by Fruit")
    plt.xlabel("Month")
    plt.ylabel("Average Price")
    plt.xticks(range(1, 13))
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
