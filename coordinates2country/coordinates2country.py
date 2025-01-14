import locale
from typing import Optional, Dict
from PIL import Image
import pkg_resources
import csv

class Coordinates2Country:
    def __init__(self):
        self.WIDTH = 2400
        self.HEIGHT = 949
        self.GREENWICH_X = 939
        self.EQUATOR_Y = 555
        self.MIN_LATITUDE = -58.55
        self.MAX_LATITUDE = 83.64
        
        # Load resources
        self.bitmap = Image.open(pkg_resources.resource_filename(
            'coordinates2country', 'resources/countries-8bitgray.png'))
        self.countries_map = self._load_countries_csv()

    def _load_countries_csv(self) -> Dict[int, Dict[str, str]]:
        countries = {}
        csv_path = pkg_resources.resource_filename(
            'coordinates2country', 'resources/countries.csv')
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row and row[0]:
                    grayshade = int(row[0])
                    countries[grayshade] = {
                        'code': row[1],
                        'qid': row[2]
                    }
        return countries

    def country(self, latitude: float, longitude: float, language: str = 'en') -> Optional[str]:
        """Get country name for given coordinates."""
        code = self.country_code(latitude, longitude)
        if code:
            try:
                return locale.Locale(language).display_name(code)
            except KeyError:
                return None
        return None

    def country_code(self, latitude: float, longitude: float) -> Optional[str]:
        """Get ISO 3166-1 alpha-2 country code for given coordinates."""
        if (longitude < -180 or longitude > 180 or 
            latitude < self.MIN_LATITUDE or 
            latitude > self.MAX_LATITUDE):
            return None

        x = (self.WIDTH + int(self.GREENWICH_X + longitude * self.WIDTH / 360)) % self.WIDTH
        y = int(self.EQUATOR_Y - latitude * self.HEIGHT / 
                (self.MAX_LATITUDE - self.MIN_LATITUDE))

        return self._nearest_country(x, y)

    def country_qid(self, latitude: float, longitude: float) -> Optional[str]:
        """Get Wikidata QID for given coordinates."""
        code = self.country_code(latitude, longitude)
        if code:
          for grayshade, data in self.countries_map.items():
            if data['code'] == code:
               return data['qid']
        return None

    def _nearest_country(self, x: int, y: int) -> Optional[str]:
        """Find nearest country starting from given pixel coordinates."""
        country = self._country_from_pixel(x, y)
        if country is None:
            radius = 1
            while country is None:
                country = self._country_at_distance(x, y, radius)
                radius += 1
        return country

    def _country_at_distance(self, centerX: int, centerY: int, radius: int) -> Optional[str]:
        x1 = centerX - radius
        x2 = centerX + radius
        y1 = centerY - radius
        y2 = centerY + radius
        countries_occurrences: Dict[str, int] = {}

        for x in range(x1, x2 + 1):
            for y in (y1, y2):
                country = self._country_from_pixel(x, y)
                if country:
                    countries_occurrences[country] = countries_occurrences.get(country, 0) + 1
        
        for y in range(y1 + 1, y2):
            for x in (x1, x2):
                 country = self._country_from_pixel(x, y)
                 if country:
                    countries_occurrences[country] = countries_occurrences.get(country, 0) + 1
        
        if not countries_occurrences:
            return None
        
        return max(countries_occurrences, key=countries_occurrences.get)


    def _country_from_pixel(self, x: int, y: int) -> Optional[str]:
        try:
          grayshade = self.bitmap.getpixel((x, y))
          return self._country_from_grayshade(grayshade)
        except IndexError:
          return None

    def _country_from_grayshade(self, grayshade: int) -> Optional[str]:
        for shade, data in self.countries_map.items():
             if shade == grayshade:
                return data['code']
        return None
