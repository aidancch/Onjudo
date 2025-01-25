import cohere

# Set your Cohere API key and model name here
class RealEstateAgent:
    cohere_api_key = "nz6fdh3FyK7sgrA25T17uyLTu33KNl16azQskw31"
    co = cohere.ClientV2(api_key=cohere_api_key)
    def __init__(self):
        self.prompt = [
                {"role": "system", "content": '''You are a knowledgeable and friendly real estate property searcher chatbot named Shizuka. Your role is to assist clients in buying or renting properties within the United States. You provide accurate, up-to-date information on property listings, market trends, and neighborhoods. You answer questions clearly and offer helpful advice to guide clients through every step of the real estate process. Communicate in a polite, professional manner, ensuring clients feel supported and well-informed at all times.'''}
            ]

    # Initialize the Cohere API client
    def get_response(self, message):
        self.prompt.append({'role': 'user', 'content': message})
        model = self.co.chat_stream(
            model="command-r-plus-08-2024",
            temperature=0.5,
            messages=self.prompt,
        )
        return model

    def start_prompting(self):
        user_input = ''
        print('''Hi, I'm Shizuka, your dedicated real estate expert. I'm here to help you find the perfect property. With a deep understanding of the market and a passion for making the process as smooth as possible, I'm committed to ensuring your real estate journey is seamless and stress-free. What are you looking for in your dream home?''')
        while user_input != 'Q':
            user_input = input()
            if user_input == 'Q':
                return self.prompt
            model = self.get_response(user_input)
            response = ''
            for event in model:
                if event.type == "content-delta":
                    response += event.delta.message.content.text
                    print(event.delta.message.content.text, end="")
            self.prompt.append({'role': 'assistant', 'content': response})
        return self.prompt
    
if __name__ == "__main__":
    bot = RealEstateAgent()
    bot.start_prompting()