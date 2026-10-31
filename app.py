
from pathlib import Path

import pandas as pd
import streamlit as st

from src.property_comparison import compare_properties
from src.investment_calculator import calculate_investment_metrics


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real Estate Investment Advisor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "india_housing_prices.csv"
)


# ============================================================
# 3. DATA LOADING AND VALIDATION
# ============================================================

@st.cache_data
def load_property_data(file_path):

    data = pd.read_csv(file_path)

    required_columns = [
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
        "Floor_No",
        "Total_Floors",
        "Age_of_Property",
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

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if data["ID"].isna().any():
        raise ValueError("Property IDs contain missing values.")

    if data["ID"].duplicated().any():
        raise ValueError("Property IDs must be unique.")

    if not pd.api.types.is_numeric_dtype(data["Price_in_Lakhs"]):
        raise ValueError("Price_in_Lakhs must be numeric.")

    if not pd.api.types.is_numeric_dtype(data["Size_in_SqFt"]):
        raise ValueError("Size_in_SqFt must be numeric.")

    return data


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def format_price(value):
    return f"₹{value:,.2f} L"


def make_csv_download(data, filename, label):

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv"
    )


# ============================================================
# 5. APPLICATION HEADER
# ============================================================

st.title("🏠 Real Estate Investment Advisor")

st.markdown(
    """
    Explore property listings, compare properties, analyze market data,
    and evaluate rental investment scenarios.
    """
)


# ============================================================
# 6. LOAD DATASET
# ============================================================

if not DATA_PATH.exists():

    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()


try:

    df = load_property_data(DATA_PATH)

except Exception as error:

    st.error(f"Unable to load dataset: {error}")
    st.stop()


# ============================================================
# 7. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "Property Explorer",
        "Property Comparison",
        "Investment Calculator",
        "Market Analytics"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    f"Total dataset records: {len(df):,}"
)


# ============================================================
# 8. DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Properties",
        f"{len(df):,}"
    )

    col2.metric(
        "Average Price",
        format_price(df["Price_in_Lakhs"].mean())
    )

    col3.metric(
        "Median Price",
        format_price(df["Price_in_Lakhs"].median())
    )

    col4.metric(
        "Cities Covered",
        f"{df['City'].nunique():,}"
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Property Type Distribution")

        property_counts = df["Property_Type"].value_counts()

        st.bar_chart(
            property_counts,
            use_container_width=True
        )

    with right:

        st.subheader("Property Price Distribution")

        price_distribution = (
            pd.cut(
                df["Price_in_Lakhs"],
                bins=20
            )
            .value_counts()
            .sort_index()
        )

        price_distribution.index = (
            price_distribution.index.astype(str)
        )

        st.bar_chart(
            price_distribution,
            use_container_width=True
        )

    st.caption(
        "Price distribution represents the number of dataset records "
        "within each price interval."
    )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Source: Original india_housing_prices.csv. "
        "Statistics describe this dataset and are not verified "
        "real-world market prices."
    )


# ============================================================
# 9. PROPERTY EXPLORER
# ============================================================

elif page == "Property Explorer":

    st.header("Property Explorer")

    st.markdown(
        "Search and filter properties using available dataset attributes."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        states = ["All"] + sorted(
            df["State"].dropna().unique().tolist()
        )

        selected_state = st.selectbox(
            "Select State",
            states
        )

    if selected_state == "All":
        city_data = df
    else:
        city_data = df[
            df["State"] == selected_state
        ]

    with col2:

        cities = ["All"] + sorted(
            city_data["City"].dropna().unique().tolist()
        )

        selected_city = st.selectbox(
            "Select City",
            cities
        )

    with col3:

        property_types = ["All"] + sorted(
            df["Property_Type"].dropna().unique().tolist()
        )

        selected_type = st.selectbox(
            "Property Type",
            property_types
        )

    col4, col5 = st.columns(2)

    with col4:

        bhk_values = sorted(
            df["BHK"].dropna().unique().tolist()
        )

        selected_bhk = st.selectbox(
            "BHK Configuration",
            ["All"] + bhk_values
        )

    with col5:

        min_price = float(df["Price_in_Lakhs"].min())
        max_price = float(df["Price_in_Lakhs"].max())

        selected_price = st.slider(
            "Price Range (₹ Lakhs)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=5.0
        )

    st.divider()

    filtered_df = df.copy()

    if selected_state != "All":
        filtered_df = filtered_df[
            filtered_df["State"] == selected_state
        ]

    if selected_city != "All":
        filtered_df = filtered_df[
            filtered_df["City"] == selected_city
        ]

    if selected_type != "All":
        filtered_df = filtered_df[
            filtered_df["Property_Type"] == selected_type
        ]

    if selected_bhk != "All":
        filtered_df = filtered_df[
            filtered_df["BHK"] == selected_bhk
        ]

    filtered_df = filtered_df[
        filtered_df["Price_in_Lakhs"].between(
            selected_price[0],
            selected_price[1]
        )
    ]

    st.subheader("Search Results")

    result_col1, result_col2, result_col3 = st.columns(3)

    result_col1.metric(
        "Matching Properties",
        f"{len(filtered_df):,}"
    )

    if not filtered_df.empty:

        result_col2.metric(
            "Average Property Price",
            format_price(filtered_df["Price_in_Lakhs"].mean())
        )

        result_col3.metric(
            "Average Property Size",
            f"{filtered_df['Size_in_SqFt'].mean():,.0f} Sq Ft"
        )

        display_columns = [
            "ID",
            "State",
            "City",
            "Locality",
            "Property_Type",
            "BHK",
            "Size_in_SqFt",
            "Price_in_Lakhs",
            "Furnished_Status",
            "Year_Built",
            "Availability_Status"
        ]

        st.subheader("Available Properties")

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(filtered_df):,} matching properties."
        )

    else:

        st.warning(
            "No properties match the selected filters. "
            "Try changing your selections."
        )


# ============================================================
# 10. PROPERTY COMPARISON
# ============================================================

elif page == "Property Comparison":

    st.header("Property Comparison")

    st.markdown(
        "Compare two to four properties side by side using their IDs."
    )

    st.info(
        "Enter Property IDs from the dataset preview or Property Explorer."
    )

    st.divider()

    property_id_input = st.text_input(
        "Enter Property IDs separated by commas",
        placeholder="Example: 1, 36, 47"
    )

    if st.button("Compare Properties", type="primary"):

        if not property_id_input.strip():

            st.warning("Please enter at least two Property IDs.")

        else:

            try:

                selected_ids = [
                    int(value.strip())
                    for value in property_id_input.split(",")
                ]

                comparison_df = compare_properties(
                    selected_ids,
                    df
                )

                st.success(
                    f"Successfully compared {len(selected_ids)} properties."
                )

                st.subheader("Property Comparison Results")

                st.dataframe(
                    comparison_df,
                    use_container_width=True
                )

                st.caption(
                    "Each column represents one property. "
                    "Each row represents a property attribute. "
                    "Missing source values are preserved."
                )

                st.divider()

                st.subheader("Price and Size Overview")

                selected_properties = df[
                    df["ID"].isin(selected_ids)
                ].copy()

                metric_columns = st.columns(len(selected_ids))

                for index, (_, property_row) in enumerate(
                    selected_properties.iterrows()
                ):

                    with metric_columns[index]:

                        st.markdown(
                            f"**Property ID: {property_row['ID']}**"
                        )

                        st.metric(
                            "Price",
                            format_price(property_row["Price_in_Lakhs"])
                        )

                        st.metric(
                            "Size",
                            f"{property_row['Size_in_SqFt']:,.0f} Sq Ft"
                        )

                        st.metric(
                            "BHK",
                            str(property_row["BHK"])
                        )

            except ValueError as error:

                st.error(
                    f"Invalid property selection: {error}"
                )

            except Exception as error:

                st.error(
                    f"Unable to compare properties: {error}"
                )


# ============================================================
# 11. INVESTMENT CALCULATOR
# ============================================================

elif page == "Investment Calculator":

    st.header("Real Estate Investment Calculator")

    st.markdown(
        """
        Calculate rental income, investment costs, rental yields,
        monthly cash flow and hypothetical five-year appreciation scenarios.
        """
    )

    st.info(
        "Calculations are based on your inputs, not verified rental-market data."
    )

    st.divider()

    st.subheader("Investment Details")

    col1, col2 = st.columns(2)

    with col1:

        purchase_price_lakhs = st.number_input(
            "Property Purchase Price (₹ Lakhs)",
            min_value=0.01,
            value=50.0,
            step=1.0
        )

        monthly_rent_rupees = st.number_input(
            "Expected Monthly Rental Income (₹)",
            min_value=0.0,
            value=25000.0,
            step=1000.0
        )

        annual_expenses_rupees = st.number_input(
            "Annual Expenses (₹)",
            min_value=0.0,
            value=30000.0,
            step=1000.0
        )

    with col2:

        one_time_costs_rupees = st.number_input(
            "One-Time Acquisition Costs (₹)",
            min_value=0.0,
            value=300000.0,
            step=10000.0
        )

        vacancy_rate_pct = st.slider(
            "Expected Annual Vacancy Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=1.0
        )

        appreciation_rate_pct = st.number_input(
            "Your Assumed Annual Appreciation (%)",
            min_value=-99.0,
            max_value=100.0,
            value=5.0,
            step=0.5
        )

    st.divider()

    if st.button(
        "Calculate Investment Returns",
        type="primary",
        use_container_width=True
    ):

        try:

            results = calculate_investment_metrics(
                purchase_price_lakhs=purchase_price_lakhs,
                monthly_rent_rupees=monthly_rent_rupees,
                annual_expenses_rupees=annual_expenses_rupees,
                one_time_costs_rupees=one_time_costs_rupees,
                vacancy_rate_pct=vacancy_rate_pct,
                appreciation_rate_pct=appreciation_rate_pct
            )

            st.session_state["investment_results"] = results

            st.session_state["investment_inputs"] = {
                "purchase_price_lakhs": purchase_price_lakhs,
                "monthly_rent_rupees": monthly_rent_rupees,
                "annual_expenses_rupees": annual_expenses_rupees,
                "one_time_costs_rupees": one_time_costs_rupees,
                "vacancy_rate_pct": vacancy_rate_pct,
                "appreciation_rate_pct": appreciation_rate_pct
            }

        except (ValueError, TypeError) as error:

            st.error(f"Unable to calculate investment: {error}")

    if "investment_results" in st.session_state:

        results = st.session_state["investment_results"]
        saved_inputs = st.session_state["investment_inputs"]

        st.divider()

        st.subheader("Investment Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Purchase Price",
            f"₹{results['purchase_price_rupees']:,.0f}"
        )

        col2.metric(
            "Total Acquisition Cost",
            f"₹{results['total_acquisition_cost']:,.0f}"
        )

        col3.metric(
            "Gross Annual Rent",
            f"₹{results['gross_annual_rent']:,.0f}"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Effective Annual Rent",
            f"₹{results['effective_annual_rent']:,.0f}"
        )

        col5.metric(
            "Net Annual Rent",
            f"₹{results['net_annual_rent']:,.0f}"
        )

        col6.metric(
            "Monthly Net Cash Flow",
            f"₹{results['monthly_net_cash_flow']:,.0f}"
        )

        st.divider()

        st.subheader("Rental Yield Analysis")

        yield_col1, yield_col2 = st.columns(2)

        yield_col1.metric(
            "Gross Rental Yield",
            f"{results['gross_rental_yield_pct']:.2f}%"
        )

        yield_col2.metric(
            "Net Rental Yield",
            f"{results['net_rental_yield_pct']:.2f}%"
        )

        if results["monthly_net_cash_flow"] < 0:

            st.warning("Estimated monthly rental cash flow is negative.")

        elif results["monthly_net_cash_flow"] == 0:

            st.warning("Estimated monthly rental cash flow is zero.")

        else:

            st.success("Estimated monthly rental cash flow is positive.")

        st.divider()

        st.subheader("Your Five-Year Appreciation Scenario")

        five_year_value = results["five_year_scenario_value"]

        current_value = results["purchase_price_rupees"]

        scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

        scenario_col1.metric(
            "Current Purchase Price",
            f"₹{current_value:,.0f}"
        )

        scenario_col2.metric(
            "Five-Year Scenario Value",
            f"₹{five_year_value:,.0f}"
        )

        scenario_col3.metric(
            "Estimated Change",
            f"₹{five_year_value - current_value:,.0f}"
        )

        st.divider()

        st.subheader("Five-Year Appreciation Scenarios")

        standard_scenarios = {
            "Conservative": 3.0,
            "Moderate": 5.0,
            "Optimistic": 8.0
        }

        scenario_rows = []

        for scenario_name, annual_rate in standard_scenarios.items():

            scenario_result = calculate_investment_metrics(
                purchase_price_lakhs=saved_inputs["purchase_price_lakhs"],
                monthly_rent_rupees=0,
                appreciation_rate_pct=annual_rate
            )

            scenario_value = scenario_result["five_year_scenario_value"]

            scenario_rows.append({
                "Scenario": scenario_name,
                "Annual Appreciation (%)": annual_rate,
                "Five-Year Scenario Value (₹)": scenario_value,
                "Estimated Change (₹)": (
                    scenario_value
                    - scenario_result["purchase_price_rupees"]
                )
            })

        scenario_df = pd.DataFrame(scenario_rows)

        st.dataframe(
            scenario_df.style.format({
                "Annual Appreciation (%)": "{:.2f}%",
                "Five-Year Scenario Value (₹)": "₹{:,.0f}",
                "Estimated Change (₹)": "₹{:,.0f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "This is not a complete investment ROI model. "
            "Loan EMI, income tax, capital gains tax, selling costs "
            "and changes in rent are excluded."
        )

        if st.button("Clear Investment Results"):

            st.session_state.pop("investment_results", None)
            st.session_state.pop("investment_inputs", None)

            st.rerun()


# ============================================================
# 12. MARKET ANALYTICS
# ============================================================

elif page == "Market Analytics":

    st.header("Market Analytics")

    st.markdown(
        """
        Explore property distribution, price statistics and
        descriptive comparisons across states, cities and property categories.
        """
    )

    st.warning(
        "These results describe the supplied dataset only. "
        "They should not be interpreted as verified real-world market rankings."
    )

    st.divider()

    # --------------------------------------------------------
    # ANALYTICS FILTERS
    # --------------------------------------------------------

    st.subheader("Analytics Filters")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        states = ["All"] + sorted(
            df["State"].dropna().unique().tolist()
        )

        analytics_state = st.selectbox(
            "Filter by State",
            states,
            key="analytics_state"
        )

    if analytics_state == "All":

        analytics_city_data = df

    else:

        analytics_city_data = df[
            df["State"] == analytics_state
        ]

    with filter_col2:

        cities = ["All"] + sorted(
            analytics_city_data["City"].dropna().unique().tolist()
        )

        analytics_city = st.selectbox(
            "Filter by City",
            cities,
            key="analytics_city"
        )

    analytics_df = df.copy()

    if analytics_state != "All":

        analytics_df = analytics_df[
            analytics_df["State"] == analytics_state
        ]

    if analytics_city != "All":

        analytics_df = analytics_df[
            analytics_df["City"] == analytics_city
        ]

    if analytics_df.empty:

        st.warning("No records found for the selected filters.")
        st.stop()

    st.divider()

    # --------------------------------------------------------
    # MARKET KPI METRICS
    # --------------------------------------------------------

    st.subheader("Market Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Properties",
        f"{len(analytics_df):,}"
    )

    col2.metric(
        "Average Price",
        format_price(analytics_df["Price_in_Lakhs"].mean())
    )

    col3.metric(
        "Median Price",
        format_price(analytics_df["Price_in_Lakhs"].median())
    )

    col4.metric(
        "Average Size",
        f"{analytics_df['Size_in_SqFt'].mean():,.0f} Sq Ft"
    )

    st.divider()

    # --------------------------------------------------------
    # STATE-WISE ANALYSIS
    # --------------------------------------------------------

    st.subheader("State-Wise Property Analysis")

    state_summary = (
        analytics_df.groupby("State", as_index=False)
        .agg(
            Property_Count=("ID", "count"),
            Average_Price=("Price_in_Lakhs", "mean"),
            Median_Price=("Price_in_Lakhs", "median"),
            Average_Size=("Size_in_SqFt", "mean"),
            Unique_Cities=("City", "nunique")
        )
        .sort_values(
            "Property_Count",
            ascending=False
        )
    )

    state_chart_col, state_table_col = st.columns(2)

    with state_chart_col:

        st.markdown("**Properties by State**")

        state_chart_data = (
            state_summary
            .set_index("State")[["Property_Count"]]
            .sort_values("Property_Count", ascending=False)
        )

        st.bar_chart(
            state_chart_data,
            use_container_width=True
        )

    with state_table_col:

        st.markdown("**State Price Summary**")

        state_price_chart = (
            state_summary
            .set_index("State")[["Average_Price"]]
            .sort_values("Average_Price", ascending=False)
        )

        st.bar_chart(
            state_price_chart,
            use_container_width=True
        )

    with st.expander("View complete state-wise table"):

        st.dataframe(
            state_summary.style.format({
                "Average_Price": "₹{:.2f} L",
                "Median_Price": "₹{:.2f} L",
                "Average_Size": "{:,.0f} Sq Ft"
            }),
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            state_summary,
            "state_wise_market_analysis.csv",
            "Download State Analysis CSV"
        )

    st.divider()

    # --------------------------------------------------------
    # CITY-WISE ANALYSIS
    # --------------------------------------------------------

    st.subheader("City-Wise Property Analysis")

    city_summary = (
        analytics_df.groupby(["State", "City"], as_index=False)
        .agg(
            Property_Count=("ID", "count"),
            Average_Price=("Price_in_Lakhs", "mean"),
            Median_Price=("Price_in_Lakhs", "median"),
            Average_Size=("Size_in_SqFt", "mean")
        )
        .sort_values(
            "Property_Count",
            ascending=False
        )
    )

    top_cities = city_summary.head(15)

    city_chart_col, city_price_col = st.columns(2)

    with city_chart_col:

        st.markdown("**Top 15 Cities by Record Count**")

        city_count_chart = (
            top_cities
            .set_index("City")[["Property_Count"]]
        )

        st.bar_chart(
            city_count_chart,
            use_container_width=True
        )

    with city_price_col:

        st.markdown("**Top 15 Cities by Average Price**")

        top_price_cities = (
            city_summary
            .sort_values("Average_Price", ascending=False)
            .head(15)
            .set_index("City")[["Average_Price"]]
        )

        st.bar_chart(
            top_price_cities,
            use_container_width=True
        )

    with st.expander("View complete city-wise table"):

        st.dataframe(
            city_summary.style.format({
                "Average_Price": "₹{:.2f} L",
                "Median_Price": "₹{:.2f} L",
                "Average_Size": "{:,.0f} Sq Ft"
            }),
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            city_summary,
            "city_wise_market_analysis.csv",
            "Download City Analysis CSV"
        )

    st.divider()

    # --------------------------------------------------------
    # PROPERTY TYPE ANALYSIS
    # --------------------------------------------------------

    st.subheader("Property Type Analysis")

    property_type_summary = (
        analytics_df.groupby("Property_Type", as_index=False)
        .agg(
            Property_Count=("ID", "count"),
            Average_Price=("Price_in_Lakhs", "mean"),
            Median_Price=("Price_in_Lakhs", "median"),
            Average_Size=("Size_in_SqFt", "mean")
        )
        .sort_values("Property_Count", ascending=False)
    )

    type_col1, type_col2 = st.columns(2)

    with type_col1:

        st.markdown("**Property Type Distribution**")

        type_counts = (
            property_type_summary
            .set_index("Property_Type")[["Property_Count"]]
        )

        st.bar_chart(
            type_counts,
            use_container_width=True
        )

    with type_col2:

        st.markdown("**Average Price by Property Type**")

        type_prices = (
            property_type_summary
            .set_index("Property_Type")[["Average_Price"]]
        )

        st.bar_chart(
            type_prices,
            use_container_width=True
        )

    st.dataframe(
        property_type_summary.style.format({
            "Average_Price": "₹{:.2f} L",
            "Median_Price": "₹{:.2f} L",
            "Average_Size": "{:,.0f} Sq Ft"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # FURNISHING STATUS ANALYSIS
    # --------------------------------------------------------

    st.subheader("Furnishing Status Analysis")

    furnishing_summary = (
        analytics_df.groupby("Furnished_Status", as_index=False)
        .agg(
            Property_Count=("ID", "count"),
            Average_Price=("Price_in_Lakhs", "mean"),
            Median_Price=("Price_in_Lakhs", "median")
        )
        .sort_values("Property_Count", ascending=False)
    )

    furnish_col1, furnish_col2 = st.columns(2)

    with furnish_col1:

        st.markdown("**Properties by Furnishing Status**")

        st.bar_chart(
            furnishing_summary.set_index("Furnished_Status")[
                ["Property_Count"]
            ],
            use_container_width=True
        )

    with furnish_col2:

        st.markdown("**Average Price by Furnishing Status**")

        st.bar_chart(
            furnishing_summary.set_index("Furnished_Status")[
                ["Average_Price"]
            ],
            use_container_width=True
        )

    st.dataframe(
        furnishing_summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # AVAILABILITY ANALYSIS
    # --------------------------------------------------------

    st.subheader("Property Availability Analysis")

    availability_summary = (
        analytics_df.groupby("Availability_Status", as_index=False)
        .agg(
            Property_Count=("ID", "count"),
            Average_Price=("Price_in_Lakhs", "mean"),
            Median_Price=("Price_in_Lakhs", "median")
        )
        .sort_values("Property_Count", ascending=False)
    )

    availability_col1, availability_col2 = st.columns(2)

    with availability_col1:

        st.markdown("**Properties by Availability**")

        st.bar_chart(
            availability_summary.set_index("Availability_Status")[
                ["Property_Count"]
            ],
            use_container_width=True
        )

    with availability_col2:

        st.markdown("**Average Price by Availability**")

        st.bar_chart(
            availability_summary.set_index("Availability_Status")[
                ["Average_Price"]
            ],
            use_container_width=True
        )

    st.dataframe(
        availability_summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # PRICE DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("Property Price Distribution")

    price_bins = pd.cut(
        analytics_df["Price_in_Lakhs"],
        bins=20
    )

    price_histogram = (
        price_bins
        .value_counts()
        .sort_index()
    )

    price_histogram.index = price_histogram.index.astype(str)

    st.bar_chart(
        price_histogram,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # DESCRIPTIVE PRICE STATISTICS
    # --------------------------------------------------------

    st.subheader("Price Statistics")

    price_statistics = (
        analytics_df["Price_in_Lakhs"]
        .describe()
        .to_frame(name="Price_in_Lakhs")
    )

    st.dataframe(
        price_statistics.style.format(
            "₹{:.2f} L"
        ),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # DOWNLOAD ANALYTICS DATA
    # --------------------------------------------------------

    st.subheader("Download Analytics")

    make_csv_download(
        analytics_df,
        "filtered_property_market_data.csv",
        "Download Filtered Property Data"
    )

    st.caption(
        "All tables and charts are descriptive summaries of the "
        "provided dataset. They do not establish actual market values, "
        "investment returns or future appreciation."
    )
