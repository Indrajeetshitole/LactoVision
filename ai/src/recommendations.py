def generate_recommendations(input_data, predicted_yield):
    rec=[]; alerts=[]
    feed=float(input_data.get("feed_quantity_kg_dm",0)); water=float(input_data.get("water_intake_l",0)); thi=float(input_data.get("thi",0)); bcs=float(input_data.get("body_condition_score",0)); health=str(input_data.get("health_status",""))
    if feed < 14: rec.append("Review dry-matter feed quantity with a qualified dairy nutritionist.")
    if water < 40: rec.append("Review water availability and intake; ensure clean water is continuously available.")
    if thi >= 72: alerts.append("Heat-stress risk: THI is elevated. Review shade, ventilation and cooling practices.")
    if bcs < 2.75: rec.append("Body condition is low; review energy balance and nutrition with a qualified professional.")
    if health.lower() not in {"healthy","normal"}: alerts.append("Health status needs attention; use this as a decision-support alert and consult a veterinarian.")
    if not rec: rec.append("Current inputs do not trigger a basic rule-based recommendation; continue monitoring milk, feed, water and health trends.")
    return rec, alerts
