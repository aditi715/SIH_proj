import sqlite3
import os

# --- Configuration ---
DB_FILE_PATH = "groundwater_from_sql.db"  # The name of the database file to be created

# --- SQL Statements ---

# 1. CREATE TABLE statement from your input
create_table_sql = """
CREATE TABLE IF NOT EXISTS central_report_full (
    S_No INT PRIMARY KEY,
    STATE VARCHAR(255),
    DISTRICT VARCHAR(255),
    ASSESSMENT_UNIT VARCHAR(255),
    Rainfall_mm_Monsoon DECIMAL(10, 2),
    Rainfall_mm_Non_Monsoon DECIMAL(10, 2),
    Rainfall_mm_Total DECIMAL(10, 2),
    Total_Geographical_Area_ha_Recharge_Worthy DECIMAL(10, 2),
    Total_Geographical_Area_ha_Hilly DECIMAL(10, 2),
    Total_Geographical_Area_ha_Total DECIMAL(10, 2),
    Rainfall_Recharge_Monsoon DECIMAL(10, 2),
    Rainfall_Recharge_Non_Monsoon DECIMAL(10, 2),
    Rainfall_Recharge_Total DECIMAL(10, 2),
    Canal_Recharge_ham DECIMAL(10, 2),
    SW_Irrigation_Recharge_ham DECIMAL(10, 2),
    GW_Irrigation_Recharge_ham DECIMAL(10, 2),
    Tanks_Ponds_Recharge_ham DECIMAL(10, 2),
    WCS_Recharge_ham DECIMAL(10, 2),
    Pipelines_Recharge_ham DECIMAL(10, 2),
    Sewage_Flash_Flood_Recharge_ham DECIMAL(10, 2),
    Total_Recharge_Other_Sources_ham DECIMAL(10, 2),
    Total_Annual_GW_Recharge_ham DECIMAL(10, 2),
    Natural_Discharge_ham DECIMAL(10, 2),
    Annual_Extractable_GW_Resource_ham DECIMAL(10, 2),
    Current_GW_Extraction_Irrigation_ham DECIMAL(10, 2),
    Current_GW_Extraction_Industrial_ham DECIMAL(10, 2),
    Current_GW_Extraction_Domestic_ham DECIMAL(10, 2),
    Total_Current_GW_Extraction_ham DECIMAL(10, 2),
    Stage_of_GW_Extraction_percent DECIMAL(5, 2),
    GW_Allocation_Domestic_2025_ham DECIMAL(10, 2),
    Net_Annual_GW_Availability_Future_Use_ham DECIMAL(10, 2)
);
"""

# 2. A list of all INSERT statements from your input
insert_statements = [
    "INSERT INTO central_report_full VALUES (1, 'ANDAMAN AND NICOBAR ISLANDS', 'N & M ANDAMAN', NULL, 3015.7, 0, 3015.7, 58040, 286106, 344146, 16376.36, 0, 16376.36, 0, 0, 0, 151.9, 0, 0, 0, 151.9, 16528.26, 1652.84, 14875.42, 0.8, 83.24, 262.06, 346.11, 2.33, 269.19, 14522.18);",
    "INSERT INTO central_report_full VALUES (2, 'ANDAMAN AND NICOBAR ISLANDS', 'NICOBAR', NULL, 2805.2, 0, 2805.2, 38075, 156091, 194166, 11344.64, 0, 11344.64, 0, 0, 0, 16.14, 0, 0, 0, 16.14, 11360.78, 1136.09, 10224.69, 0.25, 0.95, 88.29, 92.6, 0.9, 90.68, 9819.28);",
    "INSERT INTO central_report_full VALUES (3, 'ANDAMAN AND NICOBAR ISLANDS', 'SOUTH ANDAMAN', NULL, 3015.7, 0, 3015.7, 31524, 215321, 246845, 10777.26, 0, 10777.26, 0, 0, 0, 20.46, 0, 0, 0, 20.46, 10797.72, 1079.76, 9717.96, 10.65, 13.61, 322.86, 347.12, 3.57, 331.62, 9362.07);",
    "INSERT INTO central_report_full VALUES (4, 'ARUNACHAL PRADESH', 'ANJAW', NULL, 0, 0, 0, 0, 619000, 619000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);",
    "INSERT INTO central_report_full VALUES (5, 'ARUNACHAL PRADESH', 'CHANGLANG', NULL, 2222.9, 0, 2222.9, 53000, 413200, 466200, 19742.16, 10336.2, 30078.36, 0, 0, 29.16, 0, 0, 0, 0, 29.16, 30107.52, 3010.77, 27096.75, 64.8, 0, 182.82, 247.62, 0.91, 225.59, 26806.36);",
    "INSERT INTO central_report_full VALUES (6, 'ARUNACHAL PRADESH', 'DIBANG VALLEY', NULL, 0, 0, 0, 0, 912900, 912900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);",
    "INSERT INTO central_report_full VALUES (7, 'ARUNACHAL PRADESH', 'EAST KAMENG', NULL, 2026.3, 0, 2026.3, 31250, 382150, 413400, 11144.66, 6383.14, 17527.8, 0, 0, 32.47, 0, 5.68, 0, 0, 38.15, 17565.95, 1756.59, 15809.36, 94.1, 0, 14.72, 108.82, 0.69, 23.5, 15691.77);",
    "INSERT INTO central_report_full VALUES (8, 'ARUNACHAL PRADESH', 'EAST SIANG', NULL, 4398.6, 0, 4398.6, 110100, 250200, 360300, 70296.68, 9924.6, 80221.28, 0, 0, 40.16, 0, 5, 0, 0, 45.16, 80266.44, 8026.64, 71985, 110.42, 4.2, 64.4, 179.02, 0.25, 75.08, 71795.3);",
    "INSERT INTO central_report_full VALUES (9, 'ARUNACHAL PRADESH', 'KURUNG KUMEY', NULL, 0, 0, 0, 0, 604000, 604000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);",
    "INSERT INTO central_report_full VALUES (10, 'ARUNACHAL PRADESH', 'LOHIT', NULL, 2998.2, 0, 2998.2, 200000, 321200, 521200, 105536.64, 17398.2, 122934.84, 0, 0, 15.32, 0, 0, 0, 0, 15.32, 122950.16, 12295.03, 109376.97, 34.36, 8.4, 230.97, 273.73, 0.25, 279.47, 109054.75);",
    "INSERT INTO central_report_full VALUES (11, 'ARUNACHAL PRADESH', 'LOWER DIBANG VALLEY', NULL, 3996.1, 0, 3996.1, 120000, 270000, 390000, 77315.63, 2235.73, 79551.36, 0, 0, 74.13, 0, 0, 0, 0, 74.13, 79625.49, 7962.55, 71662.94, 216.5, 0, 31.62, 248.12, 0.35, 34.28, 71412.15);",
    "INSERT INTO central_report_full VALUES (12, 'ARUNACHAL PRADESH', 'LOWER SUBANSIRI', NULL, 1444.4, 0, 1444.4, 10135, 340665, 350800, 2643.04, 2591.35, 5234.39, 0, 0, 7.05, 0, 0, 0, 0, 7.05, 5241.44, 524.15, 4485.54, 16.83, 0, 22.95, 39.78, 0.89, 43.11, 4425.59);",
    "INSERT INTO central_report_full VALUES (13, 'ARUNACHAL PRADESH', 'PAPUM PARE', NULL, 3199.6, 0, 3199.6, 17819, 328381, 346200, 9018.4, 3283.09, 12301.49, 0, 0, 5.96, 0, 0, 0, 0, 5.96, 12307.45, 1230.75, 9593.23, 15.36, 25.29, 108.03, 148.68, 1.55, 190.73, 9361.85);",
    "INSERT INTO central_report_full VALUES (14, 'ARUNACHAL PRADESH', 'TAWANG', NULL, 0, 0, 0, 0, 217200, 217200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);",
    "INSERT INTO central_report_full VALUES (15, 'ARUNACHAL PRADESH', 'TIRAP', NULL, 2907.3, 0, 2907.3, 12500, 223700, 236200, 6396.06, 2269.39, 8665.45, 0, 0, 2.47, 1.03, 0.02, 0, 0, 3.52, 8668.97, 866.9, 7802.07, 6.25, 0, 49.29, 55.54, 0.71, 56.2, 7739.62);",
    "INSERT INTO central_report_full VALUES (16, 'ARUNACHAL PRADESH', 'UPPER SIANG', NULL, 0, 0, 0, 0, 640000, 640000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);",
    "INSERT INTO central_report_full VALUES (17, 'ARUNACHAL PRADESH', 'UPPER SUBANSIRI', NULL, 1735.4, 0, 1735.4, 700, 702700, 703400, 185.7, 2294.35, 2480.05, 0, 0, 0, 0, 0, 0, 0, 0, 2480.05, 248, 2232.05, 0, 0, 13.92, 13.92, 0.62, 19.98, 2210.98);",
    "INSERT INTO central_report_full VALUES (18, 'ARUNACHAL PRADESH', 'WEST KAMENG', NULL, 1500, 0, 1500, 520, 759280, 759800, 225, 4106.8, 4331.8, 0, 0, 5.06, 0, 0, 0, 0, 5.06, 4336.86, 433.69, 3903.17, 12.6, 0.05, 59.81, 72.46, 1.86, 70.83, 3816.92);",
    "INSERT INTO central_report_full VALUES (19, 'ARUNACHAL PRADESH', 'WEST SIANG', NULL, 2390.8, 0, 2390.8, 77700, 757800, 835500, 29019.26, 32470.18, 61489.44, 0, 0, 0, 0, 0, 0, 0, 0, 61489.44, 6148.94, 55340.5, 0, 0, 129.56, 129.56, 0.23, 145.48, 55190.28);",
    "INSERT INTO central_report_full VALUES (20, 'ASSAM', 'BAKSA', 'BAKSA', 2140.2, 0, 2140.2, 245900, 0, 245900, 118432.89, 0, 118432.89, 0, 0, 21.09, 0, 0, 0, 0, 21.09, 118453.98, 11845.4, 106608.58, 48.77, 0, 856.9, 905.67, 0.85, 940.6, 105658.26);",
    "INSERT INTO central_report_full VALUES (21, 'ASSAM', 'BARPETA', 'BARPETA', 2140.2, 0, 2140.2, 230700, 0, 230700, 111116.63, 0, 111116.63, 0, 0, 156.41, 0, 0, 0, 0, 156.41, 111273.04, 11127.3, 100145.74, 347.58, 0, 1404.75, 1752.33, 1.75, 1542.41, 98357.38);",
    "INSERT INTO central_report_full VALUES (22, 'ASSAM', 'BONGAIGAON', 'BONGAIGAON', 2140.2, 0, 2140.2, 109800, 0, 109800, 52890.35, 0, 52890.35, 0, 0, 0.05, 0, 0, 0, 0, 0.05, 52890.4, 5289.04, 47601.36, 0.1, 0, 818.15, 818.25, 1.72, 898.3, 46781.99);",
]

def create_database():
    """Creates and populates the SQLite database from SQL statements."""
    
    # Remove the old database file if it exists to start fresh
    if os.path.exists(DB_FILE_PATH):
        os.remove(DB_FILE_PATH)
        print(f"Removed existing database file: {DB_FILE_PATH}")
        
    try:
        # Connect to the SQLite database (this creates the file)
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        print(f"Database file created: {DB_FILE_PATH}")

        # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)
        print("Table 'central_report_full' created successfully.")

        # Execute all the INSERT statements
        for statement in insert_statements:
            cursor.execute(statement)
        
        # Commit the changes to the database
        conn.commit()
        print(f"Successfully inserted {len(insert_statements)} rows of data.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()
            print("Database connection closed.")

# --- Main Execution ---
if __name__ == "__main__":
    create_database()