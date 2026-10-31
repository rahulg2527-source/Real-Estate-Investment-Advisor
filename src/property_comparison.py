


COMPARISON_COLUMNS = [
    "ID",
    "State",
    "City",
    "Locality",
    "Property_Type",
    "BHK",
    "Size_in_SqFt",
    "Price_in_Lakhs",
    "Price_per_SqFt",
    "Year_Built",
    "Furnished_Status",
    "Nearby_Schools",
    "Nearby_Hospitals",
    "Public_Transport_Accessibility",
    "Parking_Space",
    "Security",
    "Amenities",
    "Facing",
    "Owner_Type",
    "Availability_Status"
]


def compare_properties(property_ids, data):
    """
    Compare between 2 and 4 properties using their dataset IDs.

    Returns a transposed DataFrame with properties as columns.
    Original dataset is not modified.
    """

    if not isinstance(property_ids, (list, tuple)):
        raise ValueError("Provide property IDs as a list or tuple.")

    if not 2 <= len(property_ids) <= 4:
        raise ValueError("Select between 2 and 4 properties.")

    try:
        if len(set(property_ids)) != len(property_ids):
            raise ValueError("Duplicate property IDs are not allowed.")
    except TypeError as exc:
        raise ValueError("Property IDs must be hashable values.") from exc

    missing_columns = [
        column for column in COMPARISON_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing comparison columns: {missing_columns}"
        )

    selected = data[data["ID"].isin(property_ids)].copy()

    if len(selected) != len(property_ids):
        raise ValueError("One or more property IDs were not found.")

    return selected[COMPARISON_COLUMNS].set_index("ID").T
