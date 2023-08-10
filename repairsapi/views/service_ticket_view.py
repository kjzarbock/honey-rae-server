"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket


class ServiceTicketView(ViewSet):
    """Honey Rae API customers view"""

    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """
        if request.auth.user.is_staff:
            serviceTickets = ServiceTicket.objects.all()
        else:
            serviceTickets = ServiceTicket.objects.filter(customer=request.auth.user.customer)
        serialized = ServiceTicketSerializer(serviceTickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer record
        """

        serviceTicket = ServiceTicket.objects.get(pk=pk)
        serialized = ServiceTicketSerializer(serviceTicket, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""
    class Meta:
        model = ServiceTicket
        fields = ('id', 'description', 'emergency', 'date_completed', 'customer', 'employee')
        depth = 1