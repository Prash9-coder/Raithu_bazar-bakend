import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cattle_market.settings')
django.setup()

from core.models import User, CowListing

def seed():
    # Create a seller
    if not User.objects.filter(username='farmer_ramu').exists():
        seller = User.objects.create_user(
            username='farmer_ramu',
            password='password123',
            full_name='Ramu Rao',
            mobile_number='9848012345',
            village='Kanchikacherla',
            district='Krishna',
            state='Andhra Pradesh',
            role='seller'
        )
        print("Created seller: Ramu Rao")
    else:
        seller = User.objects.get(username='farmer_ramu')

    # Create dummy listings
    listings = [
        {
            'tag_name': 'Lakshmi',
            'breed': 'Ongole',
            'age': 4,
            'gender': 'Female',
            'milk_per_day': 12,
            'health_condition': 'Excellent',
            'vaccination_details': 'All done',
            'pregnant_status': True,
            'price': 45000,
            'negotiable': True,
            'village': 'Kanchikacherla',
            'district': 'Krishna',
            'state': 'Andhra Pradesh',
            'description': 'High quality Ongole breed cow. Very healthy and good milk yield.'
        },
        {
            'tag_name': 'Gauri',
            'breed': 'Punganur',
            'age': 3,
            'gender': 'Female',
            'milk_per_day': 5,
            'health_condition': 'Good',
            'vaccination_details': 'Updated',
            'pregnant_status': False,
            'price': 120000,
            'negotiable': False,
            'village': 'Punganur',
            'district': 'Chittoor',
            'state': 'Andhra Pradesh',
            'description': 'Rare Punganur dwarf cow. Best for household and organic farming.'
        }
    ]

    for item in listings:
        if not CowListing.objects.filter(tag_name=item['tag_name']).exists():
            CowListing.objects.create(seller=seller, **item)
            print(f"Created listing: {item['tag_name']}")

if __name__ == '__main__':
    seed()
