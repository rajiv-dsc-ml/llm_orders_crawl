# llm_orders_crawl
crawling of an ecommerce website orders detail of a given user of that ecommerce

Flow to execute : 
1. pull the repository
2. Make a virtual environment : 
   If you have conda : 

   conda create --name venv_name python==3.11

   #activate the virtual environment which has name , say, venv_name
   conda activate venv_name

   #after its activation , install all the required libraries mentioned in the requirements.txt by
   pip install -r requirements.txt   

3. run the download_llm_gguf.py file that downloads the gguf file of an llm (https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)
i.e : go inside the repository in terminal and execute the command : python download_llm_gguf.py

4. start login.py by executing this command in the terminal .
   Make sure the pwd is the repository address. 
   uvicorn login:app --host 0.0.0.0 --port 8000

------------------------------------------------------------------------------------------------------

Design : 
Components : 
Three important components : 
# 1.Function calling with llm
This component relies on the quality of llm in terms of understandiing which function out of all should be called given the prompt.
Such llmm should also have the ability to extract the function arguments' values from the given prompt

# 2.llm "brain"
Since the function calling llm was not so bright to recognize some html element values, so I am using another llm (https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf) to do that . 
For example, given html unstructured texts , it was hard for the function calling llm to recognize the html tag responsible for username , html tag responsible for password and finally the button responsible for sign in action

# 3. Preprocessing
Some preprocessing functions have been written that use regex to shorten the given html text so that the focus can be held on the tags where the required information can be present 

# 4. Selenium
While I did later experimented with langchain for web scraping, I could not find the neat way to actually take actions like signIn or clicking a button without using library like requests or selenium
My way to approach the problem was to first manually solve the scraping problem and then feeding the agentic capabilities like llm function calling and llm answering to a question-prompt.
So, shifting to function calling by langchain was avoided because open source chat-llm like mistral-7B-instruct , was also not performing well in terms of final task of extracting orders data 

And I could not afford to experiment with openai keys. 
I have added those files also as a proof of my experimentations. They are under the folder named experiments .



