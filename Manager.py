from RealEstateAgent import RealEstateAgent
from ResponseAnalyzer import ResponseAnalyzer
from harvest import homeharvester
import json
import time

class Manager():
    def __init__(self):
        self.agent = RealEstateAgent()
        self.analyzer = ResponseAnalyzer()
        self.wanted_columns = set()
        self.location = None
        self.radius = None
        self.type = None
        self.beds = None
        self.baths = None
        self.sqft = None
        self.price = None
        self.criteria = (
                        "list_price",
                        "full_street_line",
                        "beds",
                        "full_baths",
                        "half_baths",
                        "sqft",
                        "address",
                        "text",
                        "property_url",
                        "status",
                        "list_date",
                        "neighborhoods",
                        "agent_id",
                        "agent_name",
                        "agent_email",
                        "agent_phones",
                        "broker_id",
                        "office_name",
                        "office_email",
                        "nearby_schools",
                        "primary_photo",
                        "latitude",
                        "longitude",
                        "primary_photo"
                    )
        
    def get_response(self, message):
        #this should only be one message from the user at a time.
        self.start_time = time.perf_counter()
        self.agent.get_response(message)
        prompts = self.agent.get_prompts()
        self.analyzer.add_user_prompts(prompts)
        data = self.analyzer.get_response()
        self.process_json(data)
        self.elapsed_time = time.perf_counter() - self.start_time
        return self.harvest_request()
        
    def process_json(self, data):
        data = json.loads(data)
        self.location = data['location']
        self.radius = data['radius']
        self.type = data['propertyType']
        self.beds = data['beds']
        self.baths = data['baths']
        self.sqft = data['radius']
        self.price = data['price']     
        
    def harvest_request(self):
        scraper = homeharvester()
        df = scraper.get_houses(self.location, self.radius)
        for i in df.columns:
            if i not in self.criteria:
                df = df.drop(i, axis=1)
        return df.to_json(orient='records')
    
if __name__ == '__main__':
    manage = Manager()
    data = manage.get_response('Hi Im trying to find a condo in the San Jose area with a 10 mile radius. I want between 0 and 2000 square feet. I want the price to be between 0 and 1 million dollars')
    data = json.loads(data)