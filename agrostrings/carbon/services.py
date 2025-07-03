# carbon/services.py
from .models import TreeData, FertilizerData, EnergyData, WasteData, CropData

def calculate_score(record):
    breakdown = {}
    total = 0

    # Trees (max 30 pts)
    try:
        t = record.treedata
        pts = min(t.num_trees // 5, 10)
        pts += min(int(t.avg_height_m), 5)
        pts += min(int(t.avg_age_years * 0.5), 5)
        if t.pct_indigenous >= 50:
            pts += 10
        breakdown['trees'] = pts
        total += pts
    except TreeData.DoesNotExist:
        breakdown['trees'] = 0

    # Fertilizer (max 20)
    try:
        f = record.fertilizerdata
        if f.type == 'organic':
            pts = 20
        elif f.type == 'mixed':
            pts = 10
        else:
            pts = 0
        breakdown['fertilizer'] = pts
        total += pts
    except FertilizerData.DoesNotExist:
        breakdown['fertilizer'] = 0

    # Energy (max 15)
    try:
        e = record.energydata
        pts = 10 if e.uses_solar else 0
        if e.uses_solar:
            pts += min(int(e.pct_solar / 10), 5)
        breakdown['energy'] = pts
        total += pts
    except EnergyData.DoesNotExist:
        breakdown['energy'] = 0

    # Waste (max 15)
    try:
        w = record.wastedata
        pts = 10 if not w.burns_waste else 0
        pts += 5 if w.uses_compost else 0
        pts += 2 if w.waste_separation else 0
        breakdown['waste'] = pts
        total += pts
    except WasteData.DoesNotExist:
        breakdown['waste'] = 0

    # Crops (max 20)
    try:
        c = record.cropdata
        pts = 0
        crop_types = len(c.crop_types.split(',')) if c.crop_types else 0
        if crop_types >= 2:
            pts += 5
        if c.intercropping:
            pts += 5
        pts += 5 if c.pct_land_used >= 70 else 0
        pts += 5 if c.pesticide_type == 'organic' else 0
        breakdown['crops'] = pts
        total += pts
    except CropData.DoesNotExist:
        breakdown['crops'] = 0

    # Determine level
    if total >= 80:
        level = 'High'
    elif total >= 50:
        level = 'Medium'
    else:
        level = 'Low'

    return {
        'total': total,
        'breakdown': breakdown,
        'level': level
    }
