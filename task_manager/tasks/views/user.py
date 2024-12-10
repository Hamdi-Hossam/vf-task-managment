from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Subscription
from ..serializers import SubscriptionSerializer
from users.permissions import IsUser

@api_view(['POST'])
@permission_classes([IsUser])
def subscribe_to_reports(request):
    if request.method == 'POST':
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription, created = Subscription.objects.update_or_create(
                user=request.user,
                defaults=serializer.validated_data
            )
            message = "Subscription created." if created else "Subscription updated."
            return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsUser])
def unsubscribe_from_reports(request):
    if request.method == 'DELETE':
        try:
            subscription = Subscription.objects.get(user=request.user)
            subscription.delete()
            return Response({'message': 'Unsubscribed successfully.'}, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response({'message': 'No active subscription found.'}, status=status.HTTP_404_NOT_FOUND)
