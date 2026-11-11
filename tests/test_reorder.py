import unittest
from reorder.engine import InventoryReorderAutopilot, ItemInventoryParams


class TestInventoryReorderAutopilot(unittest.TestCase):
    def setUp(self):
        self.autopilot = InventoryReorderAutopilot()

    def test_reorder_triggered_with_eoq(self):
        # Stock has fallen to 15 units
        item = ItemInventoryParams(
            item_code="SKU-BEARING-01",
            item_name="Precision Industrial Ball Bearing",
            current_physical_stock=15,
            pending_incoming_po_stock=0,
            reserved_sales_order_stock=5,  # Effective = 10
            annual_demand_units=7300.0,
            average_daily_demand=20.0,
            max_daily_demand=35.0,
            lead_time_days=7,
            max_lead_time_days=10,
            ordering_cost_per_po=600.0,
            holding_cost_per_unit_year=40.0,
            preferred_supplier_id="SUPP-SKF-01"
        )
        rec = self.autopilot.evaluate_item_reorder(item)
        self.assertTrue(rec.is_reorder_triggered)
        self.assertEqual(rec.effective_stock, 10)
        self.assertGreater(rec.reorder_point, 10)
        self.assertGreater(rec.recommended_order_quantity_eoq, 100)
        self.assertEqual(rec.suggested_po_action, "CREATE_PURCHASE_ORDER_DRAFT")

    def test_sufficient_stock_no_trigger(self):
        # Ample stock in warehouse
        item = ItemInventoryParams(
            item_code="SKU-BOLT-M8",
            item_name="Stainless Steel Bolt M8",
            current_physical_stock=5000,
            annual_demand_units=10000.0,
            average_daily_demand=30.0,
            max_daily_demand=50.0,
            lead_time_days=3,
            max_lead_time_days=5,
            preferred_supplier_id="SUPP-FASTENERS"
        )
        rec = self.autopilot.evaluate_item_reorder(item)
        self.assertFalse(rec.is_reorder_triggered)
        self.assertEqual(rec.suggested_po_action, "SUFFICIENT_STOCK")


if __name__ == "__main__":
    unittest.main()
