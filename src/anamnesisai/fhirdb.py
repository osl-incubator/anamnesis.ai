import sqlite3

class FHIRDatabase:
    def __init__(self, db_path='fhir_database.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE fhir_database 
                            (patient, practitioner, encounter, observation, diagnostic_report, condition,
                             medication_request, care_plan, procedure, allergy_intolerance, clinical_impression)
                            ''')
        self.connection.commit()

    def save_resource(self, resource):
        resource_type = resource.resource_type
        resource_data = resource.as_json()
        self.cursor.execute(f"INSERT INTO fhir_database ({resource_type}) VALUES (?)", (resource_data,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
