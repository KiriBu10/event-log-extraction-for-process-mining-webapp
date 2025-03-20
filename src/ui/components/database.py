import sqlite3
import re
import os
import sqlite3
import pandas as pd
import numpy as np





# Function to safely quote identifiers
def quote_identifier(identifier):
    return f'"{identifier}"'
    #return f"'{identifier}'" 

# Discover and Load CSV Files
def discover_csv_files_and_structure(directory):
    files_structure = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            table_name = filename.split('.')[0]
            df = pd.read_csv(os.path.join(directory, filename))
            files_structure[table_name] = {
                'columns': df.columns.tolist(),
                'data': df
            }
    return files_structure

# Discover csv schema
def read_csv_schema_from_excel(csv_schema_excel_path):
    """Read relationships and structure information from an Excel file."""
    relationships_df = pd.read_excel(csv_schema_excel_path)
    relationships = {}
    column_types = {}
    for _, row in relationships_df.iterrows():
        table_name = row['table_name']
        column_name = row['column']
        column_data_type = row['data_type']
        column_type = row['type']

        column_details = {
            'type': column_type,
            'data_type':column_data_type,
            'target_table': row['target_table'] if (pd.notna(column_type) and 'FK' in column_type) else None,
            'target_column': row['target_column'] if (pd.notna(column_type) and 'FK' in column_type) else None
        }
        column_types.setdefault(table_name, {})[column_name] = column_details
        if pd.notna(column_type) and 'FK' in column_type:
            relationships[(table_name, column_name)] = row['target_table']#(row['target_table'], row['target_column'])
    return relationships, column_types

def sort_tables_by_dependency(relationships):
    # Initialize containers for tracking table relationships
    all_tables = set()
    dependency_map = {}
    
    # Populate the dependency map and all_tables set
    for (table_name, column), ref_table in relationships.items():
        all_tables.add(table_name)
        all_tables.add(ref_table)
        if table_name not in dependency_map:
            dependency_map[table_name] = set()
        dependency_map[table_name].add(ref_table)
    
    # Identify independent tables (those not depending on other tables)
    independent_tables = {table for table in all_tables if table not in dependency_map}
    
    # The sorted list starts with independent tables
    sorted_tables = list(independent_tables)
    
    # Add dependent tables to the sorted list
    for table in dependency_map:
        if table not in sorted_tables:
            sorted_tables.append(table)
    
    return sorted_tables


def create_database_and_tables(files_structure, sorted_table_names, column_types, db_output_dir='example.db'):
    """Create a database and tables based on the defined CSV structure and relationships from the Excel file."""
    # Remove the existing database file if it exists
    if os.path.exists(db_output_dir):
        os.remove(db_output_dir)

    conn = sqlite3.connect(db_output_dir)
    cur = conn.cursor()

    # Enable foreign key support 
    cur.execute("PRAGMA foreign_keys = ON")
    
    # Create tables using schema information from the Excel file
    for table_name, details in files_structure.items():
        column_defs = []
        primary_keys = []
        foreign_keys_sql = []

        for col in details['columns']:
            col_type_info = column_types.get(table_name, {}).get(col, {})
            col_type = col_type_info.get('type', 'TEXT')
            data_type = col_type_info.get('data_type', 'TEXT') if col_type_info.get('data_type', np.nan) is not np.nan else 'TEXT'
            
            if col_type == 'PK':
                primary_keys.append(quote_identifier(col))
                col_definition = f"{quote_identifier(col)} {data_type}"
            elif col_type == 'DATETIME':
                col_definition = f"{quote_identifier(col)} DATETIME"
            elif col_type == 'FK':
                target_table = col_type_info['target_table']
                target_column = col_type_info['target_column']
                col_definition = f"{quote_identifier(col)} {data_type}"
                foreign_keys_sql.append(
                    f"FOREIGN KEY ({quote_identifier(col)}) REFERENCES {quote_identifier(target_table)}({quote_identifier(target_column)})"
                )
            else:
                col_definition = f"{quote_identifier(col)} {data_type}"

            column_defs.append(col_definition)

        if primary_keys:
            primary_keys_sql = f"PRIMARY KEY ({', '.join(primary_keys)})"
            column_defs.append(primary_keys_sql)
        
        create_table_sql = f"CREATE TABLE {quote_identifier(table_name)} ({', '.join(column_defs + foreign_keys_sql)})"
        print(create_table_sql)
        cur.execute(create_table_sql)
    
    def insert_data_into_db(table_name):
        details = files_structure[table_name]
        details['data'].to_sql(table_name, conn, if_exists='append', index=False, method="multi")
        print(f"Data inserted into table {table_name}")

    # Insert data in sorted order
    for table_name in sorted_table_names+list(set(list(files_structure.keys()))-set(sorted_table_names)):
        insert_data_into_db(table_name)

    conn.commit()
    conn.close()
    
    print('Database created: ' + db_output_dir)
    return conn

def get_database_schema_execute_all(path_to_csv_files,path_to_csv_schema_file, db_output_dir):
    # Main execution flow
    files_structure = discover_csv_files_and_structure(path_to_csv_files)
    #print(files_structure)
    #print('1-----------------------')
    relationships, column_types = read_csv_schema_from_excel(path_to_csv_schema_file)
    #print(relationships)
    #print('2-----------------------')
    #print(column_types)
    #print('3-----------------------')
    sorted_table_names = sort_tables_by_dependency(relationships)
    #print(sorted_table_names)
    #print('4-----------------------')
    conn = create_database_and_tables(files_structure, sorted_table_names,column_types, db_output_dir = db_output_dir)
    return get_database_schema(path_to_db=db_output_dir), conn




def get_database_schema(path_to_db):
    conn = sqlite3.connect(path_to_db)
    schema = []
    cur = conn.cursor()
    for row in cur.execute("SELECT type, name, sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        schema.append(f"{row[0].upper()} {row[1]}:\n{row[2]};\n")
    conn.close()  
    return "\n".join(schema)
















def create_db(event_log):
    # Create an in-memory SQLite database
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    # Store the DataFrame as a SQL table
    event_log.to_sql('eventlog', conn, index=False, if_exists='replace')
    return conn

# # def run_query(conn, query = "SELECT * FROM eventlog"):
# #     cursor = conn.cursor()
# #     cursor.execute(query)
# #     return cursor.fetchall()

def run_query(conn, query="SELECT * FROM eventlog"):
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Fetch column names
    column_names = [description[0] for description in cursor.description]
    
    # Fetch the data
    data = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in data]
    return result

# def get_database_schema(conn):
#     #conn = sqlite3.connect(path_to_db)
#     schema = []
#     cur = conn.cursor()
#     for row in cur.execute("SELECT type, name, sql FROM sqlite_master WHERE type='table' ORDER BY name"):
#         schema.append(f"{row[0].upper()} {row[1]}:\n{row[2]};\n")
#     #conn.close()  
#     return "\n".join(schema)

def extract_sql_statement(text):
    sql_pattern = re.compile(r"(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|GRANT|REVOKE|TRUNCATE|MERGE|CALL|EXPLAIN|SHOW|USE)\b.*?;", re.IGNORECASE | re.DOTALL)
    match = sql_pattern.search(text)
    # If a match is found, return the matched string
    if match:
        return match.group(0)
    else:
        return None
    