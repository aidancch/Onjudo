import cohere

class ResponseAnalyzer:
    cohere_api_key = "nz6fdh3FyK7sgrA25T17uyLTu33KNl16azQskw31"
    co = cohere.ClientV2(api_key=cohere_api_key)
    def __init__(self):
        self.prompt = [
                {"role": "system", "content": '''tell me what data you need'''}
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
    
    
    '''
    location OR location estimate (midpoint, radius) (e.g. SF, radius=100mi)
    listing_type
    past_days
    price range
    property_type: single_family, multi_family, condos, condo_townhome_rowhome_coop, condo_townhome, townhomes, duplex_triplex, farm, land, mobile
    
    i want a dictionary output, with each of those above
    e.g.
    return {"location": ("San Francisco, CA", 20), "listing_type": "for_sale", "past_days": 30 , "property_type": "multi_family"}
    '''