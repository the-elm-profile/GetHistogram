# Histogram Maker

A small terminal-based Python tool to load CSV files, inspect numeric columns, and generate histograms with a guided interactive workflow.

## What it does

- loads data from CSV files
- lists numeric columns and missing value warnings
- lets you customize:
  - title
  - axis labels
  - number of bins
  - bar color and edge color
  - alpha/transparency
  - log-scale Y axis
  - output PNG file name
- shows basic column statistics before plotting
- optionally saves the chart as a PNG

## Requirements

- Python 3.8+
- pandas
- matplotlib

## Install

```bash
pip install pandas matplotlib
```

## Run

```bash
python histogram_maker.py
```

## Workflow

1. Start the script
2. Choose how to load a CSV file:
   - manually enter a file path
   - auto-search current folder for `.csv`
3. Select a numeric column
4. Configure histogram settings
5. Plot the chart
6. Optionally save to PNG
7. Repeat as needed or load another CSV

## Key commands

- `1` / `2` — choose menu options
- `p` — plot with current settings
- `e` — cancel or exit
- `y` / `n` — yes / no prompts

## Example Session

1. Launch the app
2. Choose `2` to auto-search the current folder
3. Pick the CSV file index
4. Choose `1` to configure and plot
5. Change title, labels, bins, color, etc.
6. Press `p` to plot
7. Save the chart with a file name
8. Choose whether to reuse settings or load another file

## Notes

- Only numeric columns can be used for histograms
- Missing values are ignored for plotting
- Output PNG files are saved with `.png` extension

## Helpful tips

- Run the script from the folder containing your CSV files for faster auto-search
- Use standard matplotlib color names or hex codes for color inputs
- If the script cannot read a file, check the path and file format
