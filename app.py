import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Monthly Time Tracker", layout="centered")

st.title("⏱️ WakaTime Analyser")
st.markdown("""
A simple application to visualize your WakaTime history beyond the default 14-day limit.
This app processes your exported daily totals file from WakaTime.

To obtain your data:
1. Go to your [WakaTime Account Settings](https://wakatime.com/settings/account).
2. In the Export section, click on "Export my code stats...".
3. Select **Daily totals**, download the file, and upload it below:
""")

# File Upload
uploaded_file = st.file_uploader("Upload WakaTime Export (Daily Totals)", type="json")

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        days = data.get('days', [])

        # Parse JSON to DataFrame
        records = [
            {
                'date': entry['date'],
                'total_seconds': entry.get('grand_total', {}).get('total_seconds', 0.0)
            }
            for entry in days
        ]

        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        df['total_seconds'] = df['total_seconds'].astype(float)
        df['month'] = df['date'].dt.to_period('M')

        # Monthly Aggregation
        monthly_df = (
            df.groupby('month')['total_seconds']
            .sum()
            .reset_index()
            .assign(month=lambda x: x['month'].astype(str),
                    month_dt=lambda x: pd.to_datetime(x['month']))
        )

        # Time Range Selection
        time_ranges = {
            "Last 3 months": 3,
            "Last 6 months": 6,
            "Last 1 year": 12,
            "Last 3 years": 36,
            "All Time": None
        }

        selected_range = st.selectbox("Select Time Range", list(time_ranges))
        months_limit = time_ranges[selected_range]

        if months_limit:
            cutoff = pd.Timestamp.today() - pd.DateOffset(months=months_limit + 1)
            filtered_df = monthly_df[monthly_df['month_dt'] >= cutoff]
        else:
            filtered_df = monthly_df

        # Time Conversion
        filtered_df = filtered_df.assign(
            hours=filtered_df['total_seconds'] / 3600,
            time_hours=(filtered_df['total_seconds'] // 3600).astype(int),
            time_minutes=((filtered_df['total_seconds'] % 3600) // 60).astype(int),
            Total_Time=lambda df: df['time_hours'].astype(str) + 'h ' + df['time_minutes'].astype(str) + 'm'
        )

        # Chart
        st.subheader(f"📈 Time Spent per Month ({selected_range})")
        chart_data = filtered_df[['month', 'hours']].rename(columns={
            'month': 'Month',
            'hours': 'Hours'
        }).set_index('Month')
        st.bar_chart(chart_data)

        # Time Table
        st.subheader("🕒 Breakdown by Hours and Minutes")
        time_table = filtered_df[['month', 'Total_Time']].rename(columns={'month': 'Month'})
        st.dataframe(time_table.sort_values('Month', ascending=False))

    except Exception as e:
        st.error(f"""Error: Invalid export, Parsing Failed.
                 Additional Details: {e}""")
