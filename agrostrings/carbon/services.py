import csv
import os
from django.conf import settings
from .models import TreeData, FertilizerData, EnergyData, WasteData, CropData

# Load CSV once and cache it
def load_coefficients():
    csv_path = os.path.join(settings.BASE_DIR, 'carbon', 'natural_element.csv')
    data = {}
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data[row['element']] = float(row['value'])
    except FileNotFoundError:
        print("⚠️ Coefficient file not found!")
    return data

COEFFICIENTS = load_coefficients()

def calculate_score(record):
    c = COEFFICIENTS
    breakdown = {}
    total = 0

    # Trees
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

    # Fertilizer
    try:
        f = record.fertilizerdata
        if f.type == 'organic':
            pts = int(20 * c.get('fertilizer_organic_factor', 1))
        elif f.type == 'mixed':
            pts = 10
        else:
            pts = int(20 * c.get('fertilizer_chemical_factor', 1))
        breakdown['fertilizer'] = pts
        total += pts
    except FertilizerData.DoesNotExist:
        breakdown['fertilizer'] = 0

    # Energy
    try:
        e = record.energydata
        pts = 10 if e.uses_solar else 0
        if e.uses_solar:
            pts += min(int(e.pct_solar / 10), 5)
        breakdown['energy'] = pts
        total += pts
    except EnergyData.DoesNotExist:
        breakdown['energy'] = 0

    # Waste
    try:
        w = record.wastedata
        pts = 10 if not w.burns_waste else -int(5 * c.get('waste_burn_factor', 1))
        pts += 5 if w.uses_compost else 0
        pts += 2 if w.waste_separation else 0
        breakdown['waste'] = pts
        total += pts
    except WasteData.DoesNotExist:
        breakdown['waste'] = 0

    # Crops
    try:
        cdata = record.cropdata
        pts = 0
        crop_types = len(cdata.crop_types.split(',')) if cdata.crop_types else 0
        if crop_types >= 2:
            pts += 5
        if cdata.intercropping:
            pts += 5
        pts += 5 if cdata.pct_land_used >= 70 else 0
        pts += 5 if cdata.pesticide_type == 'organic' else 0
        breakdown['crops'] = pts
        total += pts
    except CropData.DoesNotExist:
        breakdown['crops'] = 0

    # Final level
    level = 'High' if total >= 80 else 'Medium' if total >= 50 else 'Low'

    return {
        'total': total,
        'breakdown': breakdown,
        'level': level
    }
