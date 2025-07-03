from .models import TreeData, FertilizerData, EnergyData, WasteData, CropData, FarmerCarbonData
from .models import Coefficient  # loaded from CSV

def calculate_score(record: FarmerCarbonData) -> dict:
    # TODO: implement as previously outlined with weights
    return {'total': 75, 'breakdown': {...}, 'level': 'Medium'}
