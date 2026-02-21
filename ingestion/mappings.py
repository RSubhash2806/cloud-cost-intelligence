# ingestion/mappings.py

CORE_FOCUS_FIELDS = {
    "costRecordId": "CostRecord.costRecordId",
    "effectiveCost": "CostRecord.effectiveCost",
    "billedCost": "CostRecord.billedCost",
    "listCost": "CostRecord.listCost",
    "contractedCost": "CostRecord.contractedCost",
    "currency": "CostRecord.currency",
    "consumedQuantity": "CostRecord.consumedQuantity",
    "consumedUnit": "CostRecord.consumedUnit",
}

RESOURCE_FIELDS = {
    "resourceId": "Resource.resourceId",
    "resourceName": "Resource.resourceName",
    "resourceType": "Resource.resourceType",
}

SERVICE_FIELDS = {
    "serviceName": "Service.serviceName",
    "serviceCategory": "Service.serviceCategory",
}

TIME_FIELDS = {
    "chargePeriodStart": "TimeFrame.chargePeriodStart",
    "chargePeriodEnd": "TimeFrame.chargePeriodEnd",
}

ACCOUNT_FIELDS = {
    "billingAccountId": "Account.billingAccountId",
    "billingAccountName": "Account.billingAccountName",
}

LOCATION_FIELDS = {
    "regionId": "Location.regionId",
    "regionName": "Location.regionName",
}

def derive_cost_intent(charge_category: str) -> str:
    if charge_category is None:
        return "Unknown"

    category = charge_category.lower()

    if "usage" in category:
        return "Usage"
    if "commitment" in category or "reservation" in category:
        return "CommitmentPurchase"
    if "discount" in category or "credit" in category:
        return "Adjustment"
    if "tax" in category:
        return "Tax"

    return "Other"
