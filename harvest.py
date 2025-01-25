from homeharvest import scrape_property

# Generate filename based on current timestamp
class homeharvester():
  def __init__(self):
    self.x = 0
  
  def get_houses(self, location, radius):
    properties = scrape_property(
      location=location,
      radius=radius,
      listing_type="for_sale",
      past_days=30
    )
    
    return properties


if __name__ == '__main__':
  scraper = homeharvester()
  properties = scraper.get_houses('Irvine, CA', 10)
  for index, row in properties.iterrows():
    print(row['agent_name'])