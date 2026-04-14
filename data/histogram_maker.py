import os
import glob
import pandas as pd
import platform as pl
import matplotlib.pyplot as plt
import matplotlib.colors as clr

# UX and abbreviations #

cend = '\033[0m'
bold = '\033[1m'
bred = '\033[1;31m'
bblue = '\033[1;34m'
bgreen = '\033[1;32m'
byellow = '\033[1;33m'
inval = f'{bred}Invalid! {cend}'

# Useful defs #

def clear_screen():
    os.system('cls' if pl.system() == 'Windows' else 'clear')

def logo(prompt):
        print(f'{bblue}Histogram Maker{cend}\n{byellow}{prompt}{cend}\nType "e" to leave.\n\n')

def ask_str(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.lower() == 'e':
            return None
        else:
            return str(answer)

def ask_int(prompt, min_val, max_val):
    while True:
        answer = input(prompt).strip()
        if answer.lower() == 'e':
            return None
        if answer.isdigit():
            val = int(answer)
            if val >= min_val and (max_val is None or val <= max_val):
                return val
        limit = f'between {min_val} and {max_val}' if max_val else f'>= {min_val}'
        print(f'\n{inval}"{answer}" is not {limit}')

def ask_color(prompt):
     while True:
          color = input(prompt).strip()
          if color.lower() == 'e':
              return None
          if clr.is_color_like(color):
                return color
          else:
               print(f'\n{inval}"{color}" is not a color.')

def ask_yes_no(prompt):
    while True:
         answer = input(prompt).strip().lower()
         if answer == 'e':
             return None
         if answer == 'y':
            return True
         elif answer == 'n':
            return False
         else:
            print(f'\n{inval}"{answer}" is not y nor n.')

# Defs for csv

def load_csv_manu():
    clear_screen()
    logo('Manual selection')
    path = input(f'Enter the path to the {bold}.csv{cend} file: ').strip()
    try: 
        df = pd.read_csv(path)
        print(f'{bgreen}Loaded {cend}{len(df)} rows.')
        return df, path
    except FileNotFoundError:
        print(f'\n{inval}Path not found.')
    except pd.errors.EmptyDataError:
        print(f'\n{inval}This is an empty file.')
    except Exception as e:
        print(f'\n{inval}Could not read file: {e}')
    return None, None

def load_csv_auto():
    clear_screen()
    logo('Automatic selection')
    files = glob.glob('*.csv')
    if not files:
        print(f'\n{inval}No .csv files found in this folder: {os.getcwd()}')
        return None, None
    if len(files) == 1:
        print(f'{bgreen}Found: {cend}{files[0]}')
        if ask_yes_no('Load this file? [y/n]: '):
            return pd.read_csv(files[0]), files[0]
        return None, None
    print(f'Found {bold}multiple{cend} .csv files: ')
    for i, f in enumerate(files):
        print(f'{i}: {f}')
    choice = ask_int(f'Which one? (0-{len(files)-1}): ', 0, len(files)-1)
    if choice is None: return None, None
    try:
        df = pd.read_csv(files[choice])
        print(f'{bgreen}Loaded {cend} {len(df)} rows.')
        return df, files[choice]
    except Exception as e:
        clear_screen()
        logo('Automatic selection')
        print(f'\n{inval}Could not read file: {e}')
        return None, None
    
def load_csv():
    while True:
        clear_screen()
        logo('Load .csv')
        sniffcsv = input(
            f'Type {bold}1{cend} to enter file path manually\n'
            f'Type {bold}2{cend} to auto-search in this folder ({os.getcwd()})'
            f'\nAnswer: '
            ).strip()
        if sniffcsv == '1':
            df, filename = load_csv_manu()
        elif sniffcsv == '2':
            df, filename = load_csv_auto()
        elif sniffcsv.lower() == 'e':
            return None, None
        else:
            continue
        if df is not None:
            return df, filename
        input(f'\nPress {bold}Enter{cend} to continue... ')

# Defs to histogram #

def get_histogram_config(df):
    config = {
        'title': 'Histogram',
        'xlabel': 'Value',
        'ylabel': 'Frequency',
        'column': 0,
        'bins': 10,
        'color': 'steelblue',
        'edgecolor': 'black',
        'alpha': 0.85,
        'logscale': False,
        'save': None
    }

    while True:
        clear_screen()
        logo('Configure Histogram')
        col_name = df.columns[config['column']]
        print(
            f"{bold}1{cend} - Title: {config['title']}\n"
            f"{bold}2{cend} - X label: {config['xlabel']}\n"
            f"{bold}3{cend} - Y label: {config['ylabel']}\n"
            f"{bold}4{cend} - Column: {col_name}\n"
            f"{bold}5{cend} - Bins: {config['bins']}\n"
            f"{bold}6{cend} - Log scale (y): {config['logscale']}\n"
            f"{bold}7{cend} - Bar color: {config['color']}\n"
            f"{bold}8{cend} - Edge color: {config['edgecolor']}\n"
            f"{bold}9{cend} - Alpha (transparency): {int(config['alpha']*100)}\n"
            f"{bold}10{cend} - Save: {config['save'] or 'not saving'}\n"
            f"\n{bgreen}p{cend} - Plot with this settings\n"
            f"{bred}e{cend} - Cancel and go back\n"
        )
        choice = input('What to edit? ').strip().lower()
        if choice == '1':
            new_title = ask_str('Type the title of your histogram: ')
            if new_title is None: return None
            config['title'] = new_title
        elif choice == '2':
            new_xlabel = ask_str('What is the x label: ')
            if new_xlabel is None: return None
            config['xlabel'] = new_xlabel
        elif choice == '3':
            new_ylabel = ask_str('What is the y label: ')
            if new_ylabel is None: return None
            config['ylabel'] = new_ylabel
        elif choice == '4':    
            while True:
                print('\nAvailable columns: ')
                for i, col in enumerate(df.columns):
                    if pd.api.types.is_numeric_dtype(df[col]):
                        missing = df[col].isna().sum()
                        missing_note = f'({byellow}{missing}{cend} is missing)' if missing > 0 else ''
                        print(f'{i}: {col} {missing_note}')
                    else:
                        print(f'{i}: {col} {bred}(text - unusable){cend}')
                new_column = ask_int('Which column to use: ', 0, len(df.columns) - 1)
                if new_column is None: return None
                if not pd.api.types.is_numeric_dtype(df.iloc[:, new_column]):
                    print(f'\n{inval}That column contains text, not numbers. Pick another.')
                    continue
                config['column'] = new_column
                break
        elif choice == '5':
            new_bins = ask_int('How many bins: ', 1, None)
            if new_bins is None: return None
            config['bins'] = new_bins
        elif choice == '6':
            if ask_yes_no('Toggle log scale on Y axis? [y/n]: '):
                config['logscale'] = not config['logscale']
                print(f"Log scale: {config['logscale']}")
        elif  choice == '7':      
            new_color = ask_color('Bar color: ')
            if new_color is None: return None
            config['color'] = new_color
        elif choice == '8':
            edgecolor = ask_color('Edge color: ')
            if edgecolor is None: return None
            config['edgecolor'] = edgecolor
        elif choice == '9':
            new_alpha = ask_int("Alpha (bars transparency 1-100): ", 1, 100)
            if new_alpha is None: return None
            config['alpha'] = new_alpha/100
        elif choice == '10':
            if ask_yes_no('Save the chart to a file?\n[y/n]: '):
                new_save = ask_str('File name (without extension): ')
                if new_save is None: return None
                config['save'] = new_save
        elif choice == 'p':
            return config
        elif choice == 'e': 
            return None        

def print_status(df, column):
    data = df.iloc[:, column].dropna()
    col_name = df.columns[column]
    print(f'\n{byellow}Statistics for:{cend} "{col_name}"')
    print(f'  Count:  {len(data)}')
    print(f'  Mean:   {data.mean():.4f}')
    print(f'  Median: {data.median():.4f}')
    print(f'  Std:    {data.std():.4f}')
    print(f'  Min:    {data.min():.4f}')
    print(f'  Max:    {data.max():.4f}')
    missing = df.iloc[:, column].isna().sum()
    if missing > 0:
        print(f'{byellow}Warning: {cend}{missing} missing values were ignored.')

def plt_histogram(df, config):
    clear_screen()
    print_status(df, config['column'])
    data = df.iloc[:, config['column']].dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=config['bins'], color=config['color'], edgecolor=config['edgecolor'], alpha=config['alpha'])
    ax.set_title(config['title'])
    ax.set_xlabel(config['xlabel'])
    ax.set_ylabel(config['ylabel'])
    if config['logscale']:
        ax.set_yscale('log')
    ax.grid(True, axis='y', alpha=0.4)
    ax.set_axisbelow(True)
    plt.tight_layout()
    if config['save']:
        fig.savefig(f"{config['save']}.png", dpi=250)
        print(f"{bgreen}Saved as {config['save']}.png{cend}") 
    plt.show()
    plt.close(fig)

# Main # 

def main():
    df, filename = load_csv()
    if df is None:
        return
    while True:
        clear_screen()
        logo('Main Menu')
        print(
            f'{bgreen}Loaded: {cend}{filename}\n'
            f'{bold}1{cend} - Configure and plot histogram\n'
            f'{bold}2{cend} - Load different .csv'
            )
        choice = input('Answer: ').strip().lower()
        if choice == '1':
            config = get_histogram_config(df)
            if config is None:
                continue
            plt_histogram(df, config)
            while True:
                again = ask_yes_no('Use the same settings again? [y/n]: ')
                if again is None or again is False:
                    break
                plt_histogram(df, config)
        elif choice == '2':
            new_df, new_filename = load_csv()
            if new_df is not None:
                df = new_df
                filename = new_filename
        elif choice == 'e':
            print(f'{bgreen}Goodbye.{cend}\nExiting...')
            break

# Histogram Maker #

if __name__ == '__main__':
    main()