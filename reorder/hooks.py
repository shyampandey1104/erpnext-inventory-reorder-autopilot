# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "reorder"
app_title = "Erpnext Inventory Reorder Autopilot"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Inventory Reorder Autopilot for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/reorder/css/reorder.bundle.css"
app_include_js = "/assets/reorder/js/reorder.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "reorder.engine.on_document_submit",
        "on_cancel": "reorder.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "reorder.engine.daily_scheduled_sync"
    ]
}
