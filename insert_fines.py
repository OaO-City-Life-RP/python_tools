import csv
import json
import math

def csv_to_sql(csv_file_path, sql_file_path):
    # Open the CSV file for reading
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header row
        
        # Open the SQL file for writing
        with open(sql_file_path, mode='w', encoding='utf-8') as sql_file:
            # Loop through each row in the CSV file
            for row in csv_reader:
                name = row[0].replace("'", "''")
                description = row[3].replace("'", "''")
                charge_class = row[7].replace("'", "''")
                months = row[8]
                fine = int(row[9])
                
                if months.upper() == "HUT":
                    sentence_json = json.dumps({"default": 99999, "min": 99999, "max": 99999})
                else:
                    months = int(months)
                    new_months = math.ceil(months / 2)
                    new_months_2 = math.ceil(new_months / 2)
                    sentence_json = json.dumps({"default": new_months, "min": new_months_2, "max": months})
                
                # Calculate new_fine, new_fine_2
                new_fine = math.ceil(fine / 2)
                new_fine_2 = math.ceil(new_fine / 2)
                
                # Format fine as JSON
                fine_json = json.dumps({"default": new_fine, "min": new_fine_2, "max": fine})
                points = 0
                
                # Create the SQL insert statement
                sql_insert = (
                    f"INSERT INTO tk_mdt_charges (name, class, description, fine, sentence, points) "
                    f"VALUES ('{name}', '{charge_class}', '{description}', '{fine_json}', '{sentence_json}', {points});\n"
                )
                
                # Write the SQL insert statement to the SQL file
                sql_file.write(sql_insert)

# Example usage
csv_file_path = 'charges.csv'
sql_file_path = 'insert_statements.sql'
csv_to_sql(csv_file_path, sql_file_path)