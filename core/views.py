from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, CowListing, CowImage, Inquiry, Favorite
from .serializers import (
    UserSerializer, UserProfileSerializer, 
    CowListingSerializer, CowImageSerializer, 
    InquirySerializer, FavoriteSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class CowListingViewSet(viewsets.ModelViewSet):
    queryset = CowListing.objects.all().order_by('-created_at')
    serializer_class = CowListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['breed', 'state', 'district', 'status', 'gender']
    search_fields = ['tag_name', 'breed', 'description', 'village']
    ordering_fields = ['price', 'created_at', 'age', 'milk_per_day']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        # Handle multiple images if provided
        images = self.request.FILES.getlist('images')
        for image in images:
            CowImage.objects.create(cow=serializer.instance, image=image)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_listings(self, request):
        listings = CowListing.objects.filter(seller=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_sold(self, request, pk=None):
        listing = self.get_object()
        if listing.seller != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        listing.status = 'sold'
        listing.save()
        return Response({"status": "Marked as sold"})

class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Sellers see inquiries for their cows, buyers see inquiries they sent
        if self.request.user.role == 'seller':
            return Inquiry.objects.filter(cow__seller=self.request.user).order_by('-created_at')
        return Inquiry.objects.filter(buyer=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        cow_id = request.data.get('cow')
        favorite = Favorite.objects.filter(user=request.user, cow_id=cow_id).first()
        if favorite:
            favorite.delete()
            return Response({"status": "removed"})
        Favorite.objects.create(user=request.user, cow_id=cow_id)
        return Response({"status": "added"})
