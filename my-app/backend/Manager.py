from RealEstateAgent import RealEstateAgent
from ResponseAnalyzer import ResponseAnalyzer
from harvest import homeharvester
import json

class Manager():
    def __init__(self):
        self.data = []
        self.agent = RealEstateAgent()
        self.analyzer = ResponseAnalyzer()
        self.wanted_columns = set()
        self.location = ''
        self.radius = ''
        self.type = ''
        self.beds = ''
        self.baths = ''
        self.sqft = ''
        self.price = ''
        self.criteria = (
                        "list_price",
                        "full_street_line",
                        "beds",
                        "full_baths",
                        "half_baths",
                        "sqft",
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
        self.agent.get_response(message)
        print("a")
        prompts = self.agent.get_prompts()
        print("b")
        self.analyzer.add_user_prompts(prompts)
        print("c")
        user_responses = self.analyzer.get_response()
        print('d')
        self.process_json(user_responses)
        print('e')
        return prompts[-1]
    
    def get_data(self):
        self.data = self.harvest_request()
        return self.data
        
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
                
        for i in df.iterrows():
            print(i['full_street_line'])
            i['full_street_line'] = i['full_street_line'] + ' ' + i['city'] + ', ' + i['state'] + ' ' + i['zip_code']
            i['list_price'] = self.comma_adder(i['list_price']) if i['list_price'] else 'unknown'
            if i['full_baths'] and i['half_baths']:
                i['full_baths'] = str(float(i['full_baths']) + float(i['half_baths']) * 0.5)
            elif i['full_baths']: 
                i['full_baths'] = str(float(i['full_baths']))
            elif i['full_baths']:
                i['full_baths'] = str(float(i['half_baths']) * 0.5)
            else:
                i['full_baths'] = 'unknown'

        df = df.drop(['city', 'state', 'zip_code', 'half_baths'], axis=1)
        df.rename(columns={'full_street_line': 'address', 'full_baths': 'baths'}, inplace=True)
        data = df.to_json(orient='records')
        data = json.loads(data)
        return data
    
    def comma_adder(self, s):
        s = str(s)
        returns = ''
        cnt = 0
        for i in s[::-1]:
            cnt += 1
            returns += i
            if cnt == 3:
                cnt = 0
                returns += ','
        returns = returns[::-1]
        if returns.startswith(','):
            return returns[1:]
        else:
            return returns
    
if __name__ == '__main__':
    manage = Manager()
    response = manage.get_response('Hi Im trying to find a condo in the San Jose area with a 10 mile radius. I want between 0 and 2000 square feet. I want the price to be between 0 and 1 million dollars')
    print(response)
    data = manage.get_data()
    for i in data:
        print(i['address'])