import pytest
from pathlib import Path

from poe_helper.parsers import item_parser

data_folder = Path("tests/data/")

def test_item_parser():
    with open(data_folder / "test_item_parser_data.txt", "r") as f:
        read_data = f.read()
    assert item_parser(read_data) == {
        'Requirements': {
            'Level': '17', 
            'Dex': '62'
        },
        'type': 'Basket Rapier',
        'name': 'Death Scalpel',
        'corrupted': True,
        'Rarity': 'Rare',
        'properties': {
            'Physical Damage': '13-30 (augmented)', 
            'Elemental Damage': '1-4 (augmented), 2-25 (augmented)',
            'Critical Strike Chance': '5.50%', 
            'Attacks per Second': '1.55', 
            'Weapon Range': '14'
        },
        'Sockets': 'R-G-R',
        'Item Level': '17',
        'implicitMods': [
            '+25% to Global Critical Strike Multiplier (implicit)'
        ],
        'Note': '~price 1 jewellers',
        'explicitMods': [
            '+8 to Dexterity',
            '21% increased Physical Damage',
            'Adds 1 to 4 Fire Damage',
            'Adds 2 to 25 Lightning Damage', 
            '+7% to Fire Resistance', 
            '+8% to Chaos Resistance', 
            '+32 to Accuracy Rating'
        ]
    }