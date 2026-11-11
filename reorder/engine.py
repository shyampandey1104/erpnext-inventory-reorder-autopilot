"""Inventory Reorder Point (ROP), Safety Stock & Economic Order Quantity (EOQ) Autopilot."""

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ItemInventoryParams(BaseModel):
    item_code: str
    item_name: str
    current_physical_stock: int
    pending_incoming_po_stock: int = 0
    reserved_sales_order_stock: int = 0
    annual_demand_units: float
    average_daily_demand: float
    max_daily_demand: float
    lead_time_days: int
    max_lead_time_days: int
    ordering_cost_per_po: float = 500.0   # Fixed PO administrative cost (S)
    holding_cost_per_unit_year: float = 50.0  # Annual carrying / warehousing cost (H)
    preferred_supplier_id: str


class ReorderRecommendation(BaseModel):
    item_code: str
    effective_stock: int
    safety_stock_buffer: int
    reorder_point: int
    is_reorder_triggered: bool
    recommended_order_quantity_eoq: int
    suggested_po_action: str
    rationale: str


class InventoryReorderAutopilot:
    """Computes scientific Safety Stock, Reorder Points, and Economic Order Quantities."""

    def evaluate_item_reorder(self, item: ItemInventoryParams) -> ReorderRecommendation:
        # Effective Available Stock = Physical + Incoming PO - Reserved SO
        effective_stock = item.current_physical_stock + item.pending_incoming_po_stock - item.reserved_sales_order_stock

        # Safety Stock formula: (Max Daily Demand * Max Lead Time) - (Avg Daily Demand * Avg Lead Time)
        max_usage = item.max_daily_demand * item.max_lead_time_days
        avg_usage = item.average_daily_demand * item.lead_time_days
        safety_stock = max(0, int(math.ceil(max_usage - avg_usage)))

        # Reorder Point (ROP) = (Avg Daily Demand * Avg Lead Time) + Safety Stock
        rop = int(math.ceil(avg_usage + safety_stock))

        # Economic Order Quantity (EOQ) formula: sqrt((2 * D * S) / H)
        if item.holding_cost_per_unit_year > 0:
            eoq_raw = math.sqrt((2.0 * item.annual_demand_units * item.ordering_cost_per_po) / item.holding_cost_per_unit_year)
            eoq = max(1, int(round(eoq_raw)))
        else:
            eoq = int(item.average_daily_demand * 30)

        is_triggered = effective_stock <= rop

        if is_triggered:
            deficit = rop - effective_stock
            order_qty = max(eoq, deficit + safety_stock)
            action = "CREATE_PURCHASE_ORDER_DRAFT"
            rationale = (f"Effective stock ({effective_stock}) fell below Reorder Point ({rop}). "
                         f"Safety stock buffer: {safety_stock} units. Recommended replenishment: {order_qty} units.")
        else:
            order_qty = 0
            action = "SUFFICIENT_STOCK"
            rationale = f"Effective stock ({effective_stock}) is above Reorder Point ({rop}). No PO required."

        return ReorderRecommendation(
            item_code=item.item_code,
            effective_stock=effective_stock,
            safety_stock_buffer=safety_stock,
            reorder_point=rop,
            is_reorder_triggered=is_triggered,
            recommended_order_quantity_eoq=order_qty,
            suggested_po_action=action,
            rationale=rationale
        )
