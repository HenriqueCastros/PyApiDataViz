# PyApiDataViz

## Overview
This project was developed for a Data Science course I'm currently taking. The assignment was to build an API in python that extracts data from a public dataset (either a CSV file or via an API). 

After extracting data from the chosen dataset, it must launch an endpoint that serves the data grouped into a category. The API must also save in memory the last request as CSV and plot related graphs.

The dataset, the category to be grouped by and the graphs were arbitrarily  chosen by me.

For the dataset, I chose the Pokemon dataset, available at https://pokeapi.co/, I decided to import only the First Genaration Pokemon (first 151, up to Mew). The group-by category is the Pokemon's type. The plots are a Boxplot that displays the distibution of the stats for each categoty, a scatterplot for the correlation between Pokemons' attack and defense and a pairplot for defense, attack and speed.

## Install
For this project you will need some packages. All the necessary packages are listed in requirements.txt.

To install them run the following command:

```bash
pip install -r /path/to/requirements.txt
```

## Usage
Run the **app.py** file and wait for it to load all the dataset. Once all the data is loaded it should automatically lauch the api. Logging is implemented so just keep an eye on terminal.

```bash
python app.py
```

## Endpoints

| Endpoint |  |
| ------------- |:-------------:|
| /pokemon     | List all pokemons on the dataset   |
| /pokemon/<id>      | Retrives a specific Pokemon     |
| /pokemon_stats      | Retrives stats for each type of pokemon and plots graphs    |

## To be developed
- [ ] Allow filtering for one specific pokemon type.
- [ ] Allow filtering for one pokemon stat.
