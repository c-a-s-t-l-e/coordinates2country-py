import csv
from PIL import Image
import pkg_resources
from collections import defaultdict
from babel import Locale  # Requires Babel library

class Coordinates2Country:
    def __init__(self):
        # Constants for the equirectangular projection
        self.WIDTH = 2400  # Width of the map image
        self.HEIGHT = 949  # Height of the map image
        self.GREENWICH_X = 939  # X-coordinate of the Greenwich longitude
        self.EQUATOR_Y = 555  # Y-coordinate of the Equator latitude
        self.MIN_LATITUDE = -58.55  # Minimum latitude (South tip of Sandwich Islands)
        self.MAX_LATITUDE = 83.64  # Maximum latitude (North tip of Canada)

        # Load resources
        self.bitmap = self._load_bitmap()
        self.countries_map = self._load_countries_csv()

    def _load_bitmap(self):
        """Load the bitmap image for reverse geocoding."""
        bitmap_path = pkg_resources.resource_filename('coordinates2country', 'resources/countries-8bitgray.png')
        try:
            bitmap = Image.open(bitmap_path)
            # print(f"Bitmap loaded: {bitmap_path}")
            return bitmap
        except Exception as e:
            # print(f"ERROR: Failed to load bitmap: {e}")
            return None

    def _load_countries_csv(self):
        """Load the countries.csv file and map grayscale values to country data."""
        countries = {}
        csv_path = pkg_resources.resource_filename('coordinates2country', 'resources/countries.csv')
        try:
            with open(csv_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header
                for row in reader:
                    grayshade = int(row[0])
                    country_code = row[1]
                    qid = row[2]
                    countries[grayshade] = {
                        'code': country_code,
                        'qid': qid
                    }
            # print(f"Loaded {len(countries)} countries from {csv_path}.")
        except Exception as e:
            print(f"ERROR: Failed to load countries CSV: {e}")
        return countries

    def country(self, latitude: float, longitude: float, language: str = 'en') -> str:
        """Get country name for given coordinates in the specified language."""
        country_code = self.country_code(latitude, longitude)
        if country_code:
            return self.get_country_name(country_code, language)
        return None

    def country_code(self, latitude: float, longitude: float) -> str:
        """Get ISO 3166-1 alpha-2 country code for given coordinates."""
        grayscale = self._get_grayscale_at_coordinates(latitude, longitude)
        if grayscale is not None and grayscale in self.countries_map:
            return self.countries_map[grayscale]['code']
        return None

    def country_qid(self, latitude: float, longitude: float) -> str:
        """Get Wikidata QID for the given coordinates."""
        grayscale = self._get_grayscale_at_coordinates(latitude, longitude)
        if grayscale is not None and grayscale in self.countries_map:
            return self.countries_map[grayscale]['qid']
        return None

    def _get_grayscale_at_coordinates(self, latitude: float, longitude: float) -> int:
        """Convert latitude and longitude to bitmap pixel and return the grayscale value."""
        if longitude < -180 or longitude > 180 or latitude < self.MIN_LATITUDE or latitude > self.MAX_LATITUDE:
            print(f"Coordinates out of bounds: latitude={latitude}, longitude={longitude}")
            return None

        # Convert latitude and longitude to pixel coordinates
        x = (self.WIDTH + int(self.GREENWICH_X + longitude * self.WIDTH / 360)) % self.WIDTH
        y = int(self.EQUATOR_Y - latitude * self.HEIGHT / (self.MAX_LATITUDE - self.MIN_LATITUDE))

        try:
            grayscale_value = self.bitmap.getpixel((x, y))
            # print(f"Pixel ({x}, {y}) has grayscale value: {grayscale_value}")
            return grayscale_value
        except IndexError:
            # print(f"Pixel ({x}, {y}) is out of bounds!")
            return None

    def get_country_name(self, country_code, language='en'):
        """Get the country name for a given ISO country code and language."""
        try:
            locale = Locale(language)
            return locale.territories.get(country_code.upper(), None)
        except Exception as e:
            # print(f"Failed to get country name for {country_code} in {language}: {e}")
            return None
