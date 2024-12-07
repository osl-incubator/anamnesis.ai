# anamnesis.ai

### Project Description: AI-Driven Anamnesis Collection System

#### Overview

This project aims to develop an AI-driven anamnesis collection system in the
healthcare domain. The system will leverage the capabilities of FHIR (Fast
Healthcare Interoperability Resources), the ChatGPT API for collecting patient
medical history (anamnesis) through conversational AI.

#### Technical Components

1. **FHIR (Fast Healthcare Interoperability Resources)**:

   - Used for structuring, storing, and retrieving patient anamnesis data.
   - Ensures compliance with healthcare data standards.
   - Facilitates potential future integration with other healthcare systems.
   - BSD: https://github.com/nazrulworld/fhir.resources

2. **ChatGPT API**:

   - Powers the conversational AI interface.
   - Engages with the user to collect symptoms and medical history.
   - Intelligent and natural language processing capabilities enhance user
     experience and data collection accuracy.

3. **Anamnesis Data Handling**:

   - Responses from the user are processed and structured into FHIR-compliant
     formats, specifically using `Observation` resources to record each piece of
     anamnesis.
   - The data is then stored in the SQLite database, maintaining a record of the
     interaction and the medical information gathered.

4. **Data Structure and Retrieval**:

   - Each user interaction generates a series of FHIR `Observation` entities,
     capturing the essence of the patient's current health status and history.
   - These observations are linked to a mock `Patient` resource for the sake of
     the MVP, facilitating a structured and standardized anamnesis record.

## Test Data

The test data was obtained from
https://springernature.figshare.com/collections/A_dataset_of_simulated_patient-physician_medical_interviews_with_a_focus_on_respiratory_cases/5545842/1

Source: Smith, Christopher William; Fareez, Faiha; Parikh, Tishya; Wavell,
Christopher; Shahab, Saba; Chevalier, Meghan; et al. (2022). A dataset of
simulated patient-physician medical interviews with a focus on respiratory
cases. figshare. Collection. https://doi.org/10.6084/m9.figshare.c.5545842.v1

## Conclusion

This project serves as a foundational step towards a more comprehensive
AI-driven healthcare data collection system. By combining the latest in AI
conversational technology with standardized healthcare data protocols, it aims
to streamline the anamnesis process, thereby enhancing patient care and
healthcare data management.
