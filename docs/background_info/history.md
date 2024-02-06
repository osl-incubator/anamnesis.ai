## Platform used:

- We are currently using **Kaggle notebooks** for implementing Llama-2
- TBN: We are not using google collab since terminal option and GPU P100 is only available as a premium feature.
- The model being used is : **Llama-2-chat-7b-hf / Llama-2-chat-gglm**
- Accelerator : GPU T4 x2, GPU P100

## Dataset

### Test dataset 1:

- Hospital-triage-and-patient-history-data
- Dataset Link : [dataset1](https://www.kaggle.com/datasets/maalona/hospital-triage-and-patient-history-data)
- Accelerator : None
- Dataset size : 1.56 GB
- Rows : 560486
- Columns : 972
- Data is in rdata format it has to be converted to Pydata. Check patients_data.csv for pydata.
- Notebook Link : [notebook1](https://www.kaggle.com/code/satarupadeb/converting-rdata-to-pydata)

## Model :

#### Test 2 (In-progress)

- Model Used : Llama-2-chat-7b-hf
- Dataset : Patients.pdf (dummy data)
- Technique used : RAG
- Accelerator : GPU T4 x2
- issue #1: Output limit exceeded (19.5 / 19.5)
