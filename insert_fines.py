import csv

def csv_to_sql(csv_file_path, sql_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header row
        
        # Open the SQL file for writing
        with open(sql_file_path, mode='w', encoding='utf-8') as sql_file:
            # Loop through each row in the CSV file
            for row in csv_reader:
                title = row[0].replace("'", "''")
                description = row[3].replace("'", "''")
                charge_type = row[7].replace("'", "''")
                months = row[8]
                fine = row[9]
                
                # Create the SQL insert statement
                sql_insert = (
                    f"INSERT INTO mdt_charges (title, description, fine, months, type) "
                    f"VALUES ('{title}', '{description}', {fine}, {months}, '{charge_type}');\n"
                )
                
                # Write the SQL insert statement to the SQL file
                sql_file.write(sql_insert)

# Example usage
csv_file_path = 'charges.csv'
sql_file_path = 'insert_statements.sql'
csv_to_sql(csv_file_path, sql_file_path)
