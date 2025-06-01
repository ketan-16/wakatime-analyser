# WakaTime Analyzer

**WakaTime Analyzer** is a simple Streamlit application that helps you visualize your coding activity history by parsing the WakaTime daily totals export file.

## Features

* 📊 Monthly aggregated charts of your coding time
* 📅 Time range filtering (3 months, 6 months, 1 year, etc.)
* 🕒 Human-readable breakdown of hours and minutes per month

## Getting Started

1. Go to your [WakaTime Account Settings](https://wakatime.com/settings/account).
2. Under the Export section, click on **"Export my code stats..."**.
3. Choose **Daily totals**.
4. Download the JSON file and upload it into the app.

## Live Site

You can access the application here: [https://wakatime-analyzer.streamlit.app/](https://wakatime-analyzer.streamlit.app/)

## Tech Stack

* Python 🐍
* Streamlit 📈
* Pandas 🐼

## Development

To run locally:

```bash
pip install streamlit pandas
streamlit run app.py
```

## License

MIT License
