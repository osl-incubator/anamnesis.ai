### What is LLama-2?

LLama-2 represents a significant advancement in the development of large language models tailored for dialogue applications, offering state-of-the-art performance and encouraging responsible research practices within the community. It is a comprehensive collection of large language models (LLMs) developed and released by a team of researchers led by Hugo Touvron and Louis Martin. These models vary in scale, ranging from 7 billion to 70 billion parameters, and are specifically optimized for dialogue applications. Referred to as LLama 2-Chat, these fine-tuned LLMs have demonstrated superior performance compared to existing open-source chat models across various benchmarks.

The research team conducted human evaluations focusing on the models' helpfulness and safety, indicating that LLama 2-Chat could serve as a viable alternative to closed-source models. They emphasize the importance of transparency and responsible development in the field of large language models, providing detailed descriptions of their fine-tuning process and safety enhancements to facilitate further research and community contributions.

### Steps to install Llama-2 models

To install Llama-2 models, follow these steps:

1. Visit the Llama [download form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) on the official website and accept the License Agreement.

2. Once your request is approved, you will receive a signed URL over email. Check your email inbox (including spam/junk folders) for the email containing the signed URL.

3. Clone the Llama 2 repository from the provided link. You can typically do this using a Git command like:

   ```
   git clone <repository_url>
   ```

   Replace `<repository_url>` with the URL of the Llama 2 repository provided to you.

4. Navigate to the directory where you cloned the Llama 2 repository.

5. Run the `download.sh` script from the terminal, passing the signed URL provided in the email when prompted to start the download. You can run the script using the following command:

   ```
   bash download.sh
   ```

   Follow the on-screen instructions and paste the signed URL when prompted.

6. Keep in mind that the signed URLs provided for downloading the models expire after 24 hours and have a limited number of downloads. If you encounter errors such as "403: Forbidden" during the download process, it likely means that the URL has expired or reached its download limit.

7. If you encounter such errors, you can always re-request a new signed URL by going through the download form and accepting the License Agreement again. Once you receive the new signed URL via email, repeat steps 3 to 5 to download the models.

Following these steps should allow you to successfully install Llama-2 models for your blog.

### Starter Code

```
from transformers import AutoTokenizer
import transformers
import torch

model = "/kaggle/input/llama-2/pytorch/7b-chat-hf/1"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

sequences = pipeline(
    'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=200,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
```
