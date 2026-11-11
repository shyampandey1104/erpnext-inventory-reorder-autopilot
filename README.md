# ERPNext Inventory Reorder Autopilot & EOQ 📊📦

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An algorithmic inventory replenishment autopilot implementing **Economic Order Quantity (EOQ)**, dynamic **Safety Stock Buffering**, and statistical **Reorder Point (ROP)** calculation for **ERPNext Stock & Procurement**.

---

## 🚀 Key Features

- **Effective Stock Accounting**: Factors physical warehouse stock, open incoming Purchase Orders, and allocated Sales Order reservations.
- **Demand & Lead-Time Variance Buffering**: Computes safety stock to absorb supplier delays and sudden demand surges.
- **Economic Order Quantity (EOQ)**: Balances annual inventory carrying costs against PO administrative expenses.
- **Direct ERPNext Hooks**: Spawns draft `Purchase Order` documents directly inside ERPNext when stock falls below threshold.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-inventory-reorder-autopilot.git
cd erpnext-inventory-reorder-autopilot
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from reorder.engine import InventoryReorderAutopilot, ItemInventoryParams

autopilot = InventoryReorderAutopilot()

item = ItemInventoryParams(
    item_code="SKU-HYDRAULIC-PUMP",
    item_name="Industrial 100-Bar Pump",
    current_physical_stock=12,
    pending_incoming_po_stock=0,
    reserved_sales_order_stock=4,
    annual_demand_units=1200.0,
    average_daily_demand=4.0,
    max_daily_demand=8.0,
    lead_time_days=10,
    max_lead_time_days=15,
    ordering_cost_per_po=800.0,
    holding_cost_per_unit_year=120.0,
    preferred_supplier_id="SUPP-HYD-LTD"
)

rec = autopilot.evaluate_item_reorder(item)
print(f"Triggered: {rec.is_reorder_triggered} | Action: {rec.suggested_po_action} | EOQ: {rec.recommended_order_quantity_eoq}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
