import cohere

class ResponseAnalyzer:
    cohere_api_key = "nz6fdh3FyK7sgrA25T17uyLTu33KNl16azQskw31"
    co = cohere.ClientV2(api_key=cohere_api_key)
    def __init__(self):
        self.prompt = None
        self.user_responses = {}
        with open('backend/analyzer_prompt.txt') as f:
            self.prompt = [
                    {"role": "system", "content": ''.join(f.readlines())},
                ]

    # Initialize the Cohere API client
    def get_response(self):
        message = self.prompt[:]
        message.append(self.user_responses)
        model = self.co.chat(
            model="command-r-plus-08-2024",
            temperature=0,
            messages=message,
        )
        return model.message.content[0].text
    
    def add_user_prompts(self, prompts):
        user_prompts = ''
        for dictionary in prompts:
            if dictionary['role'] == 'user':
                user_prompts += dictionary['content']
        
        self.user_responses = {'role': 'user', 'content': user_prompts}
    
if __name__ == '__main__':
    info_extractor = ResponseAnalyzer()
    info_extractor.add_user_prompts([{'role': 'user', 'content': 'Im looking for a condo in san Jose in about a 10 mile radius.'}])
    print(info_extractor.get_response())