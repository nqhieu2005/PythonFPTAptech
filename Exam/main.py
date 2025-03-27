import pymongo
from datetime import datetime

class MedicalServiceSystem:
    def __init__(self):
        # Database connection method
        self.client = self.connect_to_database()
        self.db = self.client['medical_service']
        
        # Initialize collections
        self.patients_collection = self.db['patients']
        self.doctors_collection = self.db['doctors']
        self.appointments_collection = self.db['appointments']

    def connect_to_database(self):
        """
        Establish connection to MongoDB database
        """
        try:
            # Replace with your MongoDB connection string
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            print("Database connection successful!")
            return client
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB database: {e}")
            return None

    def add_patients(self):
        """
        Add 3 patients from keyboard input
        """
        patients = []
        for i in range(3):
            print(f"\nEnter details for Patient {i+1}:")
            patient = {
                'full_name': input("Full Name: "),
                'date_of_birth': input("Date of Birth (YYYY-MM-DD): "),
                'gender': input("Gender: "),
                'address': input("Address: "),
                'phone_number': input("Phone Number: "),
                'email': input("Email: ")
            }

            try:
                result = self.patients_collection.insert_one(patient)
                patients.append(result.inserted_id)
                print(f"Patient {patient['full_name']} added successfully!")
            except Exception as e:
                print(f"Error adding patient: {e}")
        
        return patients

    def add_doctors(self):
        """
        Add 5 doctors from keyboard input
        """
        doctors = []
        for i in range(5):
            print(f"\nEnter details for Doctor {i+1}:")
            doctor = {
                'full_name': input("Full Name: "),
                'specialization': input("Specialization: "),
                'phone_number': input("Phone Number: "),
                'email': input("Email: "),
                'years_of_experience': int(input("Years of Experience: "))
            }

            try:
                result = self.doctors_collection.insert_one(doctor)
                doctors.append(result.inserted_id)
                print(f"Doctor {doctor['full_name']} added successfully!")
            except Exception as e:
                print(f"Error adding doctor: {e}")
        
        return doctors

    def add_appointments(self, patients, doctors):
        """
        Add 3 appointments for 3 patients
        """
        for i in range(3):
            print(f"\nEnter details for Appointment {i+1}:")
            
            # Select patient and doctor
            patient_id = patients[i]
            doctor_id = doctors[i]
            
            # Get appointment details
            appointment = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': datetime.strptime(input("Appointment Date (YYYY-MM-DD HH:MM:SS): "), "%Y-%m-%d %H:%M:%S"),
                'reason': input("Reason for Appointment: "),
                'status': 'pending'
            }
            
            try:
                self.appointments_collection.insert_one(appointment)
                print(f"Appointment added successfully!")
            except Exception as e:
                print(f"Error adding appointment: {e}")

    def generate_report(self):
        """
        Generate a report of appointments with specific template
        """
        try:
            # Aggregate appointments with patient and doctor details
            pipeline = [
                {
                    '$lookup': {
                        'from': 'patients',
                        'localField': 'patient_id',
                        'foreignField': '_id',
                        'as': 'patient_details'
                    }
                },
                {
                    '$lookup': {
                        'from': 'doctors',
                        'localField': 'doctor_id',
                        'foreignField': '_id',
                        'as': 'doctor_details'
                    }
                },
                {
                    '$unwind': '$patient_details'
                },
                {
                    '$unwind': '$doctor_details'
                }
            ]
            
            results = list(self.appointments_collection.aggregate(pipeline))
            
            # Print report header
            print("\nMedical Service Appointments Report")
            print("=" * 80)
            print("{:<5} {:<15} {:<10} {:<10} {:<15} {:<15} {:<20} {:<20}".format(
                'No', 'Patient name', 'Birthday', 'Gender', 
                'Address', 'Doctor name', 'Reason', 'Date'
            ))
            
            # Print report rows
            for idx, appointment in enumerate(results, 1):
                patient = appointment['patient_details']
                doctor = appointment['doctor_details']
                
                # Handle date_of_birth formatting
                if isinstance(patient['date_of_birth'], datetime):
                    birth_year = patient['date_of_birth'].year
                else:
                    birth_year = patient['date_of_birth'][:4]  # Assume it's a string
                
                # Handle appointment_date formatting
                if isinstance(appointment['appointment_date'], str):
                    appointment_date = datetime.strptime(appointment['appointment_date'], "%Y-%m-%d %H:%M:%S")
                else:
                    appointment_date = appointment['appointment_date']
                
                print("{:<5} {:<15} {:<10} {:<10} {:<15} {:<15} {:<20} {:<20}".format(
                    idx, 
                    patient['full_name'], 
                    birth_year,  # Use the extracted year
                    patient['gender'], 
                    patient['address'], 
                    doctor['full_name'], 
                    appointment['reason'], 
                    appointment_date.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
                ))
        
        except Exception as e:
            print(f"Error generating report: {e}")

    def get_todays_appointments(self):
        """
        Get all appointments for today and show them to the screen
        """
        try:
            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Aggregate appointments with patient and doctor details for today
            pipeline = [
                {
                    '$match': {
                        'appointment_date': {
                            '$gte': datetime.strptime(today + " 00:00:00", "%Y-%m-%d %H:%M:%S"),
                            '$lt': datetime.strptime(today + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                        }
                    }
                },
                {
                    '$lookup': {
                        'from': 'patients',
                        'localField': 'patient_id',
                        'foreignField': '_id',
                        'as': 'patient_details'
                    }
                },
                {
                    '$lookup': {
                        'from': 'doctors',
                        'localField': 'doctor_id',
                        'foreignField': '_id',
                        'as': 'doctor_details'
                    }
                },
                {
                    '$unwind': '$patient_details'
                },
                {
                    '$unwind': '$doctor_details'
                }
            ]
            
            results = list(self.appointments_collection.aggregate(pipeline))
            
            # Print report header
            print("\nToday's Appointments")
            print("=" * 60)
            print("{:<15} {:<5} {:<15} {:<10} {:<10} {:<15} {:<10}".format(
                'Address', 'No', 'Patient name', 'Birthday', 'Gender', 
                'Doctor name', 'Status'
            ))
            
            # Print report rows
            for idx, appointment in enumerate(results, 1):
                patient = appointment['patient_details']
                doctor = appointment['doctor_details']
                
                print("{:<15} {:<5} {:<15} {:<10} {:<10} {:<15} {:<10}".format(
                    patient['address'], 
                    idx, 
                    patient['full_name'], 
                    patient['date_of_birth'][:4],  # Extract year 
                    patient['gender'], 
                    doctor['full_name'], 
                    appointment.get('status', 'Pending')
                ))
        
        except Exception as e:
            print(f"Error retrieving today's appointments: {e}")

    def close_connection(self):
        """
        Close the MongoDB connection
        """
        if self.client:
            self.client.close()
            print("Database connection closed.")

def main():
    # Create an instance of the Medical Service System
    medical_system = MedicalServiceSystem()

    try:
        # Add patients
        print("\n--- Adding Patients ---")
        patients = medical_system.add_patients()

        # Add doctors
        print("\n--- Adding Doctors ---")
        doctors = medical_system.add_doctors()

        # Add appointments
        print("\n--- Adding Appointments ---")
        medical_system.add_appointments(patients, doctors)

        # Generate report
        print("\n--- Generating Appointment Report ---")
        medical_system.generate_report()

        # Get today's appointments
        print("\n--- Today's Appointments ---")
        medical_system.get_todays_appointments()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close database connection
        medical_system.close_connection()

if __name__ == "__main__":
    main()