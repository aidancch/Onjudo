from RealEstateAgent import RealEstateAgent
from ResponseAnalyzer import ResponseAnalyzer
from harvest import homeharvester
import json
import re
import pandas

class Manager():
    def __init__(self):
        self.data = []
        self.agent = RealEstateAgent()
        self.analyzer = ResponseAnalyzer()
        self.wanted_columns = set()
        self.location = ''
        self.radius = ''
        self.beds = ''
        self.baths = ''
        self.sqft = [0, float('inf')]
        self.price = [0, float('inf')]
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
        return prompts[-1]
    
    def get_data(self):
        user_responses = self.analyzer.get_response()
        self.process_json(user_responses)
        self.data = self.harvest_request()
        return self.data
        
    def process_json(self, data):
        print("Cohere data: " + data)
        data = json.loads(data)
        self.location = data['location']
        self.radius = data['radius']
        self.beds = data['beds']
        self.baths = data['baths']
        self.sqft = data['size']
        self.price = data['price']     

        
    def harvest_request(self):
        scraper = homeharvester()
        df = scraper.get_houses(self.location, self.radius)
        df.fillna(" ")
        
        if self.sqft:
            if type(self.sqft) == str or len(self.sqft) != 2 or self.sqft == '':
                self.sqft = [0, float('inf')]
            if self.sqft[0] == '' and self.sqft[1] == '':
                self.sqft = [0, float('inf')]
            elif self.sqft[1] == '':
                self.sqft = [float(self.sqft[0]), float('inf')]    
            elif self.sqft[0] == '':
                self.sqft = [float('inf'), float(self.sqft[1])]    
            in_range_mask1 = (float(self.sqft[0]) <= df['sqft']) & (df['sqft'] <= float(self.sqft[1]))
            df = df[in_range_mask1]

        if self.price:
            if type(self.price) == str or len(self.price) != 2 or self.price == '':
                self.price = [0, float('inf')]
            if self.price[0] == '' and self.price[1] == '':
                self.price = [0, float('inf')]
            elif self.price[1] == '':
                self.price = [float(self.price[0]), float('inf')]
            elif self.price[0] == '':
                self.price = [float('inf'), float(self.price[1])]   
            in_range_mask2 = (float(self.price[0]) <= df['list_price']) & (df['list_price'] <= float(self.price[1]))
            df = df[in_range_mask2]

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
            if type(full_bath) == pandas._libs.missing.NAType:
                full_bath = 0
            if type(half_bath) == pandas._libs.missing.NAType:
                half_bath = 0
            if full_bath and half_bath:
                baths.append(str(float(full_bath) + float(half_bath) * 0.5))
            elif full_bath:
                baths.append(str(float(full_bath)))
            elif half_bath:
                baths.append(str(float(half_bath) * 0.5))
            else:
                baths.append('unknown')
                
                    
        phone_numbers = []        
        for number in df['agent_phones'].tolist():
            if type(number) == pandas._libs.missing.NAType or number is None or "None" in number:
                phone_numbers.append('N/A')
            else:
                number = number[0]['number']
                phone_numbers.append(self.pretty_number(number))
    

        df = df.drop(['city', 'state', 'zip_code', 'half_baths', 'full_baths', 'list_price', 'agent_phones'], axis=1)
        df['address'] = addresses
        df['baths'] = baths
        df['list_price'] = prices
        df['agent_phones'] = phone_numbers
        
        if self.beds:
            in_range_mask3 = (int(self.beds) == df['beds']) | (int(self.beds) - 1 == df['beds']) | (int(self.beds) + 1 == df['beds'])
            df = df[in_range_mask3]
            
        if self.baths:
            in_range_mask4 = (int(self.beds) == df['baths']) | (int(self.beds) - 1 == df['baths']) | (int(self.beds) + 1 == df['baths'])
            df = df[in_range_mask4]
        
        data = df.to_json(orient='records')
        data = json.loads(data)
        return data
    
    def pretty_number(self, phone):
        if not phone: return "N/A"
        digits = re.sub(r'\D', '', phone)
    
        # Check if the input is already formatted correctly
        if re.match(r'^\(\d{3}\)\s\d{3}-\d{4}$', phone):
            return phone
        
        # Check if we have the correct number of digits
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        else:
            return "N/A"
    
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
    response = manage.get_response('Give me houses that are 1 mil to 3 mil in irvine')
    print(response)
    print(manage.price)
    print(manage.sqft)
    data = manage.get_data()
    # print(data)
    # for i in data:
    #     print(i['list_price'])