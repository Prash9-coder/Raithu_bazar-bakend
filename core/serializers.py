from rest_framework import serializers
from .models import User, CowListing, CowImage, Inquiry, Favorite

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'full_name', 'mobile_number', 'village', 'district', 'state', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'mobile_number', 'village', 'district', 'state', 'role')

class CowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CowImage
        fields = ('id', 'image')

class CowListingSerializer(serializers.ModelSerializer):
    images = CowImageSerializer(many=True, read_only=True)
    seller_details = UserProfileSerializer(source='seller', read_only=True)
    
    class Meta:
        model = CowListing
        fields = '__all__'
        read_only_fields = ('seller', 'status', 'created_at', 'updated_at')

class InquirySerializer(serializers.ModelSerializer):
    cow_details = CowListingSerializer(source='cow', read_only=True)
    
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ('buyer', 'created_at')

class FavoriteSerializer(serializers.ModelSerializer):
    cow_details = CowListingSerializer(source='cow', read_only=True)
    
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
