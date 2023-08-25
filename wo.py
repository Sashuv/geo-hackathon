import requests
import string
import math

api_key = 'pk.b7c794e8d8410554aee53afdcb1f906d'
coordinates = [(27.0426424373018, 84.85508199898334),
               (29.04258988019699, 82.85494788854307),
               (27.042685438551093, 84.85458847256307),
               (27.04437203011103, 84.85509809223619)]

class HouseCodeGenerator:
    def __init__(self):
        self.city_names = {}
        self.street_names = {}
        self.alpha_counter = {}  # Store the alphanumeric counter for each street code
    
    def generate_city_code(self, city_name):
        if city_name not in self.city_names:
            code = city_name[:3].upper()
            self.city_names[city_name] = code
        return self.city_names[city_name]

    def generate_street_code(self, street_name):
        if street_name not in self.street_names:
            code = street_name[:3].upper()
            self.street_names[street_name] = code
            self.alpha_counter[code] = 0  
        return self.street_names[street_name]

    def generate_alphanumeric_code(self, street_code):
        code = f"{street_code}{self.alpha_counter[street_code]}"
        self.alpha_counter[street_code] += 1
        return code

    def generate_house_code(self, coordinates, city_name, street_name):
        city_code = self.generate_city_code(city_name)
        street_code = self.generate_street_code(street_name)
        alphanumeric_code = self.generate_alphanumeric_code(street_code)
        return f"{city_code}-{street_code}-{alphanumeric_code}"

# Function to get location information
def get_location_info(latitude, longitude, api_key):
    base_url = "https://us1.locationiq.com/v1/reverse.php"
    params = {
        "format": "json",
        "lat": latitude,
        "lon": longitude,
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'address' in data:
            address = data['address']
            county = address.get('county', '')  # Extract county
            road = address.get('city_district', '')  # Extract city_district

            return county, road  # Return county and road
        else:
            return None, None

    except requests.RequestException as e:
        print("Error:", e)
        return None, None


generator = HouseCodeGenerator()


for coord in coordinates:
    latitude, longitude = coord
    county, road = get_location_info(latitude, longitude, api_key)
    print("City:", county) 
    print("Road:", road)  
    # Use the county and road information to generate the house code
    if county and road:
        house_code = generator.generate_house_code(coord, county, road)
        print("House Code:", house_code)
    else:
        print("Location information not available.")
    print()
