


def getdietplan(response_data):
    monthly_total = response_data.get("monthly_total")
    monthly_summary = response_data.get("monthly_summary")

    monthly_summary_text = "" 

    for item in monthly_summary:
        monthly_summary_text += f".{item.get("meal_type")} - ₹ {item.get("total")} \n"

    print(monthly_summary_text)


# {
#   "monthly_total": 9500,
#   "monthly_summary": [
#     {
#       "meal_type": "Lunch",
#       "total": 6200
#     },
#     {
#       "meal_type": "Snacks",
#       "total": 3300
#     }
#   ]
# }