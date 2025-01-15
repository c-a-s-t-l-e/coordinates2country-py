# coordinates2country-py

A Python port of the excellent [coordinates2country](https://github.com/coordinates2country/coordinates2country) Java library.

What country is at a particular latitude/longitude? This Python library tells you quickly, without using the Internet and without requiring any permission.

- Fast reverse geocoding
- Never needs an Internet connection, not even the first time
- Less than 100kB

## Installation

```bash
pip install coordinates2country-py
```

## Usage

```python
from coordinates2country.coordinates2country import Coordinates2Country

c2c = Coordinates2Country()

# Get country name in English
print(c2c.country(50.1, 10.2))  # Output: Germany

# Get ISO country code
print(c2c.country_code(50.1, 10.2))  # Output: DE

# Get Wikidata QID
print(c2c.country_qid(50.1, 10.2))  # Output: 183
```
## Credits

This is a Python port of the coordinates2country Java library. All credit for the original implementation and data goes to the original authors.
