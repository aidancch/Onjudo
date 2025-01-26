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
                        "primary_photo",
                        "city",
                        "state",
                        "zip_code",
                    )
        
    def get_response(self, message):
        #this should only be one message from the user at a time.
        self.agent.get_response(message)
        prompts = self.agent.get_prompts()
        self.analyzer.add_user_prompts(prompts)
        user_responses = self.analyzer.get_response()
        self.process_json(user_responses)
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
        
        addresses = []
        for street, city, state, zip_cope in zip(df['full_street_line'].tolist(), df['city'].tolist(), df['state'].tolist(), df['zip_code'].tolist()):
            addresses.append(street + ' ' + city + ', ' + state + ' ' + zip_cope)
            
        prices = []
        for price in df['list_price']:
            if price:
                prices.append(self.comma_adder(price))
            else:
                price.append('unknown')
                
        baths = []
        for full_bath, half_bath in zip(df['full_baths'], df['half_baths']):
            if full_bath and half_bath:
                baths.append(str(float(full_bath) + float(half_bath) * 0.5))
            elif full_bath:
                baths.append(str(float(full_bath)))
            elif half_bath:
                baths.append(str(float(half_bath) * 0.5))
            else:
                baths.append('unknown')

        df = df.drop(['city', 'state', 'zip_code', 'half_baths', 'full_baths', 'list_price'], axis=1)
        df['address'] = addresses
        df['baths'] = baths
        df['list_price'] = prices
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