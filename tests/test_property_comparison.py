import pandas as pd
import pytest

from src.property_comparison import (
    compare_properties,
    COMPARISON_COLUMNS
)


@pytest.fixture
def sample_properties():
    return pd.DataFrame({
        "ID": [1, 2, 3, 4],
        "State": ["Punjab", "Haryana", "Delhi", "Rajasthan"],
        "City": ["Ludhiana", "Gurugram", "Delhi", "Jaipur"],
        "Locality": ["Locality_1", "Locality_2", "Locality_3", "Locality_4"],
        "Property_Type": ["Apartment", "Villa", "Apartment", "Villa"],
        "BHK": [2, 3, 2, 4],
        "Size_in_SqFt": [1200, 2000, 1500, 2500],
        "Price_in_Lakhs": [80, 150, 110, 200],
        "Price_per_SqFt": [0.067, 0.075, 0.073, 0.080],
        "Year_Built": [2010, 2015, 2012, 2020],
        "Furnished_Status": ["Furnished", "Unfurnished", "Semi-furnished", "Furnished"],
        "Nearby_Schools": [3, 5, 4, 6],
        "Nearby_Hospitals": [2, 3, 1, 4],
        "Public_Transport_Accessibility": ["High", "Medium", "Low", "High"],
        "Parking_Space": ["Yes", "No", "Yes", "Yes"],
        "Security": ["Yes", "Yes", "No", "Yes"],
        "Amenities": ["Gym, Pool", "Garden", "Gym", "Pool, Garden"],
        "Facing": ["North", "South", "East", "West"],
        "Owner_Type": ["Owner", "Builder", "Broker", "Owner"],
        "Availability_Status": [
            "Ready_to_Move",
            "Under_Construction",
            "Ready_to_Move",
            "Ready_to_Move"
        ]
    })


def test_compare_two_properties(sample_properties):
    result = compare_properties([1, 2], sample_properties)

    assert result.shape == (19, 2)
    assert list(result.columns) == [1, 2]


def test_compare_four_properties(sample_properties):
    result = compare_properties([1, 2, 3, 4], sample_properties)

    assert result.shape == (19, 4)


def test_comparison_preserves_source_data(sample_properties):
    original = sample_properties.copy(deep=True)

    compare_properties([1, 2], sample_properties)

    pd.testing.assert_frame_equal(sample_properties, original)


def test_duplicate_ids_rejected(sample_properties):
    with pytest.raises(ValueError):
        compare_properties([1, 1], sample_properties)


@pytest.mark.parametrize(
    "property_ids",
    [
        [1],
        [1, 2, 3, 4, 5],
        [],
        "1,2"
    ]
)
def test_invalid_selection_count_or_type(sample_properties, property_ids):
    with pytest.raises(ValueError):
        compare_properties(property_ids, sample_properties)


def test_nonexistent_id_rejected(sample_properties):
    with pytest.raises(ValueError):
        compare_properties([1, 999], sample_properties)


def test_missing_columns_rejected(sample_properties):
    incomplete_data = sample_properties.drop(columns=["Amenities"])

    with pytest.raises(ValueError):
        compare_properties([1, 2], incomplete_data)


def test_missing_values_are_preserved(sample_properties):
    sample_properties.loc[0, "Nearby_Hospitals"] = None

    result = compare_properties([1, 2], sample_properties)

    assert pd.isna(result.loc["Nearby_Hospitals", 1])
