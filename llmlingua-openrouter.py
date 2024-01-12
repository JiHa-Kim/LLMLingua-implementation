from openai import OpenAI
from os import getenv
from llmlingua import PromptCompressor

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

# Setup LLMLingua
llm_lingua = PromptCompressor()

def rolling_window(text, window_size, overlap):
    """
    This function returns a generator that can iterate over the input text,
    yielding consecutive chunks of tokens of size 'window_size' with an overlap.
    """
    start = 0
    while start < len(text):
        yield text[start:start + window_size]
        start += window_size - overlap

# Define your compression ratio
compression_ratio = 0.5  # adjust this value as needed

# Input prompt here
contexts = input("Enter your contexts: ")

# Split the contexts into chunks using the rolling window function
contexts_chunks = list(rolling_window(contexts.split("\n"), 2000, 500))  # adjust window size and overlap as needed

for contexts in contexts_chunks:
    # Calculate the input length
    input_length = len(contexts)

    # Calculate the target_token based on the input length and compression ratio
    target_token = int(input_length * compression_ratio)

    # Input question here
    question = input("Enter your question: ")

    # Use the calculated target_token in the compress_prompt function
    compressed_prompt = llm_lingua.compress_prompt(
        contexts,
        instruction="",
        question=question,
        target_token=target_token,  # use the calculated target_token
        condition_compare=True,
        condition_in_question='after',
        rank_method='longllmlingua',
        use_sentence_level_filter=False,
        context_budget="+100",
        dynamic_context_compression_ratio=0.4,  # enable dynamic_context_compression_ratio
        reorder_context="sort"
    )

    # Generate completion
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": $YOUR_SITE_URL, # Optional, for including your app on openrouter.ai rankings.
        "X-Title": $YOUR_APP_NAME, # Optional. Shows in rankings on openrouter.ai.
      },
      model="openchat/openchat-7b", #FREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
      messages=[
        {
          "role": "user",
          "content": compressed_prompt,
        },
      ],
    )

    print(completion.choices[0].message.content)
