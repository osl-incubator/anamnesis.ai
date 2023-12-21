# anamnesis.ai

### Project Description: AI-Driven Anamnesis Collection System

#### Overview

This project aims to develop a Minimum Viable Product (MVP) for an AI-driven anamnesis collection system in the healthcare domain. The system will leverage the capabilities of FHIR (Fast Healthcare Interoperability Resources), the ChatGPT API, Flask (a micro web framework written in Python), and SQLite (a lightweight database) to facilitate an interactive, user-friendly platform for collecting patient medical history (anamnesis) through conversational AI.

#### Technical Components

1. **FHIR (Fast Healthcare Interoperability Resources)**:
   - Used for structuring, storing, and retrieving patient anamnesis data.
   - Ensures compliance with healthcare data standards.
   - Facilitates potential future integration with other healthcare systems.
   - BSD: https://github.com/nazrulworld/fhir.resources

2. **ChatGPT API**:
   - Powers the conversational AI interface.
   - Engages with the user to collect symptoms and medical history.
   - Intelligent and natural language processing capabilities enhance user experience and data collection accuracy.

3. **Flask (Python Web Framework)**:
   - Serves as the backend framework for the web application.
   - Manages HTTP requests, routing, and web page rendering.
   - Lightweight and easy to integrate with Python-based tools like SQLite and the ChatGPT API.

4. **SQLite (Database)**:
   - Stores user interactions and anamnesis data.
   - Lightweight database, ideal for the MVP stage of the project.
   - Easy integration with Flask, facilitating seamless data operations.

#### Business Logic

1. **User Interface**:
   - A simple, intuitive web interface developed using Flask.
   - No user login required for the MVP phase; designed for a single user interaction.
   - Provides a chat window where the user can interact with the ChatGPT-powered bot.

2. **Conversational Data Collection**:
   - The user initiates a conversation by describing symptoms or medical concerns.
   - The ChatGPT bot responds with follow-up questions to gather detailed anamnesis information (e.g., symptom onset, severity, duration, associated conditions).

3. **Anamnesis Data Handling**:
   - Responses from the user are processed and structured into FHIR-compliant formats, specifically using `Observation` resources to record each piece of anamnesis.
   - The data is then stored in the SQLite database, maintaining a record of the interaction and the medical information gathered.

4. **Data Structure and Retrieval**:
   - Each user interaction generates a series of FHIR `Observation` entities, capturing the essence of the patient's current health status and history.
   - These observations are linked to a mock `Patient` resource for the sake of the MVP, facilitating a structured and standardized anamnesis record.

5. **Future Expansion Potential**:
   - While initially designed for a single user, the system architecture allows for scalability to handle multiple users with authentication and more complex data management.
   - The use of FHIR ensures that future developments could integrate with broader healthcare systems and EHR (Electronic Health Records) platforms.

#### Conclusion

This MVP serves as a foundational step towards a more comprehensive AI-driven healthcare data collection system. By combining the latest in AI conversational technology with standardized healthcare data protocols, it aims to streamline the anamnesis process, thereby enhancing patient care and healthcare data management.
