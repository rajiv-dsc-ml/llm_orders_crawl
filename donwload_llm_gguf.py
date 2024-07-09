from huggingface_hub import hf_hub_download
import os
model_file  = "Phi-3-mini-4k-instruct-q4.gguf"
if not os.path.exists('./'+model_file):  
    model_name = "microsoft/Phi-3-mini-4k-instruct-gguf"
    HF_TOKEN = "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" #Paste here
    model_path = hf_hub_download(model_name,
                                filename=model_file,
                                local_dir='./',
                                token=HF_TOKEN)
    print("My model path: ", model_path)
else:
    print("the model already exists !")
# My model path:  /content/gemma-2b-it.gguf

