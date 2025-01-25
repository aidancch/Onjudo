import cohere

# Set your Cohere API key and model name here
cohere_api_key = "nz6fdh3FyK7sgrA25T17uyLTu33KNl16azQskw31"
model_name = 'command-r'

# Initialize the Cohere API client
co = cohere.Client(api_key=cohere_api_key)

def get_response(text):
    response = co.chat(
        message=text,
        model = model_name,
        temperature = 0.5
    )
    # Get the model's response
    return response.text

text = input()
res1 = get_response(text)
print(res1)
print(get_response("\n\n given the text response above, can you output ONLY the name of the neighbourhood?"))