import random
from loguru import logger

# Country archetypes with PMESII-based strengths and weaknesses
COUNTRY_ARCHETYPES = {
    "Narco-State": {
        "Political": 30,
        "Military": 70,
        "Economic": 50,
        "Social": 40,
        "Information": 60,
        "Infrastructure": 30
    },
    "Social Democracy": {
        "Political": 80,
        "Military": 40,
        "Economic": 70,
        "Social": 90,
        "Information": 60,
        "Infrastructure": 85
    },
    "Techno-State": {
        "Political": 60,
        "Military": 50,
        "Economic": 80,
        "Social": 50,
        "Information": 90,
        "Infrastructure": 95
    },
    "Militarized State": {
        "Political": 50,
        "Military": 90,
        "Economic": 40,
        "Social": 50,
        "Information": 50,
        "Infrastructure": 60
    },
    "Resource-Based State": {
        "Political": 40,
        "Military": 60,
        "Economic": 80,
        "Social": 55,
        "Information": 45,
        "Infrastructure": 75
    },
    "Failed State": {
        "Political": 20,
        "Military": 30,
        "Economic": 25,
        "Social": 15,
        "Information": 30,
        "Infrastructure": 10
    }
}

logger.info("Initializing country generator")

def generate_countries(num_countries=6):
    try:
        countries = []
        archetype_names = list(COUNTRY_ARCHETYPES.keys())
        random.shuffle(archetype_names)

        for i in range(num_countries):
            archetype = archetype_names[i % len(archetype_names)]
            country = {
                "name": f"Country {i+1}",
                "archetype": archetype,
                "resources": COUNTRY_ARCHETYPES[archetype]
            }
            countries.append(country)
        
        logger.info("Country generation complete")
        return countries
    except Exception as e:
        logger.error(f"Error generating countries: {e}")
        return []

if __name__ == "__main__":
    generated_countries = generate_countries()
    for country in generated_countries:
        logger.info(country)
