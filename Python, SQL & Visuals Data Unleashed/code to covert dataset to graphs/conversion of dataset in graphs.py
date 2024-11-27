######################################If you have dont have kaggle account then run this uncommented code code and run#####################
import os
import pandas as pd
import sqlite3
import plotly.express as px

# Step 1: Set up base directory dynamically
base_dir = os.path.dirname(os.path.abspath(__file__))

# Dataset and output directories
dataset_path = os.path.join(base_dir, "..", "dataset", "pokedex.csv")
converted_csv_path = os.path.join(base_dir, "..", "converted_csv", "pokedex_data.csv")
database_path = os.path.join(base_dir, "..", "database", "pokedex.db")
sql_file_path = os.path.join(base_dir, "..", "sql_files", "create_table_pokedex.sql")
graphs_dir = os.path.join(base_dir, "..", "graphs")

# Ensure directories exist
os.makedirs(os.path.dirname(converted_csv_path), exist_ok=True)
os.makedirs(os.path.dirname(database_path), exist_ok=True)
os.makedirs(os.path.dirname(sql_file_path), exist_ok=True)
os.makedirs(graphs_dir, exist_ok=True)

# Debug: Print paths
print("Dataset path:", dataset_path)
print("Converted CSV path:", converted_csv_path)
print("Database path:", database_path)
print("SQL file path:", sql_file_path)
print("Graphs directory:", graphs_dir)

# Step 2: Verify the dataset file exists
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

# Load dataset
df = pd.read_csv(dataset_path, sep=';', header=0)

# Step 3: Save the cleaned data to a CSV file
df.to_csv(converted_csv_path, index=False)

# Step 4: Create SQLite database and table
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS pokedex (
    POKEID INTEGER,
    NAME TEXT,
    TYPE TEXT,
    TOTAL INTEGER
);
'''
cursor.execute(create_table_query)

# Insert data into the table
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO pokedex (POKEID, NAME, TYPE, TOTAL) VALUES (?, ?, ?, ?);",
        (row['POKEID'], row['NAME'], row['TYPE'], row['TOTAL'])
    )

conn.commit()
conn.close()

# Step 5: Generate SQL file with table creation and insertion statements
with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
    sql_file.write(create_table_query)
    for _, row in df.iterrows():
        sql_file.write(
            f"INSERT INTO pokedex (POKEID, NAME, TYPE, TOTAL) VALUES ({row['POKEID']}, "
            f"'{row['NAME']}', '{row['TYPE']}', {row['TOTAL']});\n"
        )

# Step 6: Generate graphs using Plotly
fig1 = px.bar(df.head(10), x='POKEID', y='TOTAL', title='Top 10 Pokémon by Total Stat')
fig2 = px.scatter(df, x='POKEID', y='TOTAL', title='Total Stat vs. Pokémon ID')
fig3 = px.line(df, x='POKEID', y='TOTAL', color='TYPE', title='Line Plot by Type')
fig4 = px.histogram(df, x='POKEID', y='TOTAL', color='TYPE', title='Histogram by Type')

# Save graphs as HTML files
fig1.write_html(os.path.join(graphs_dir, "bargraph.html"))
fig2.write_html(os.path.join(graphs_dir, "scatter.html"))
fig3.write_html(os.path.join(graphs_dir, "line.html"))
fig4.write_html(os.path.join(graphs_dir, "histogram.html"))

print("Data processing and visualization complete.")


######################################If you have  have kaggle account,KaggleApi(), api.authenticate()then fill it and run this uncommented code code#####################
############If you are running this code comment upper code##################################
# import os
# import pandas as pd
# import sqlite3
# import plotly.express as px
# from kaggle.api.kaggle_api_extended import KaggleApi

# # Step 1: Set up base directory dynamically
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # Directories for dataset, converted CSV, database, SQL file, and graphs
# dataset_dir = os.path.join(base_dir, "..", "dataset")
# converted_csv_dir = os.path.join(base_dir, "..", "converted_csv")
# database_dir = os.path.join(base_dir, "..", "database")
# sql_dir = os.path.join(base_dir, "..", "sql_files")
# graphs_dir = os.path.join(base_dir, "..", "graphs")

# # Ensure directories exist
# os.makedirs(dataset_dir, exist_ok=True)
# os.makedirs(converted_csv_dir, exist_ok=True)
# os.makedirs(database_dir, exist_ok=True)
# os.makedirs(sql_dir, exist_ok=True)
# os.makedirs(graphs_dir, exist_ok=True)

# # Paths for individual files
# csv_file_path = os.path.join(converted_csv_dir, "pokedex_data.csv")
# database_path = os.path.join(database_dir, "pokedex.db")
# sql_file_path = os.path.join(sql_dir, "create_table_pokedex.sql")

# # Debug: Print paths
# print("Dataset directory:", dataset_dir)
# print("Converted CSV path:", csv_file_path)
# print("Database path:", database_path)
# print("SQL file path:", sql_file_path)
# print("Graphs directory:", graphs_dir)

# # Step 2: Authenticate and download the Kaggle dataset
# api = KaggleApi()
# api.authenticate()

# # Specify the dataset you want to download
# kaggle_dataset = "itambs/pokemons"

# try:
#     api.dataset_download_files(kaggle_dataset, path=dataset_dir, unzip=True)
#     print(f'Dataset "{kaggle_dataset}" downloaded to "{dataset_dir}"')
# except Exception as e:
#     print(f"Error downloading dataset: {str(e)}")
#     exit()

# # Step 3: Load dataset
# dataset_path = os.path.join(dataset_dir, "pokedex.csv")
# if not os.path.exists(dataset_path):
#     raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

# df = pd.read_csv(dataset_path, sep=';', header=0)

# # Step 4: Save the cleaned data to a CSV file
# df.to_csv(csv_file_path, index=False)

# # Step 5: Create SQLite database and table
# conn = sqlite3.connect(database_path)
# cursor = conn.cursor()

# create_table_query = '''
# CREATE TABLE IF NOT EXISTS pokedex (
#     POKEID INTEGER,
#     NAME TEXT,
#     TYPE TEXT,
#     TOTAL INTEGER
# );
# '''
# cursor.execute(create_table_query)

# # Insert data into the table
# for _, row in df.iterrows():
#     cursor.execute(
#         "INSERT INTO pokedex (POKEID, NAME, TYPE, TOTAL) VALUES (?, ?, ?, ?);",
#         (row['POKEID'], row['NAME'], row['TYPE'], row['TOTAL'])
#     )

# conn.commit()
# conn.close()

# # Step 6: Generate SQL file
# with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
#     sql_file.write(create_table_query)
#     for _, row in df.iterrows():
#         sql_file.write(
#             f"INSERT INTO pokedex (POKEID, NAME, TYPE, TOTAL) VALUES ({row['POKEID']}, "
#             f"'{row['NAME']}', '{row['TYPE']}', {row['TOTAL']});\n"
#         )

# # Step 7: Generate graphs using Plotly
# fig1 = px.bar(df.head(10), x='POKEID', y='TOTAL', title='Top 10 Pokémon by Total Stat')
# fig2 = px.scatter(df, x='POKEID', y='TOTAL', title='Total Stat vs. Pokémon ID')
# fig3 = px.line(df, x='POKEID', y='TOTAL', color='TYPE', title='Line Plot by Type')
# fig4 = px.histogram(df, x='POKEID', y='TOTAL', color='TYPE', title='Histogram by Type')

# # Save graphs as HTML files
# fig1.write_html(os.path.join(graphs_dir, "bargraph.html"))
# fig2.write_html(os.path.join(graphs_dir, "scatter.html"))
# fig3.write_html(os.path.join(graphs_dir, "line.html"))
# fig4.write_html(os.path.join(graphs_dir, "histogram.html"))

# print("Data processing and visualization complete.")
