import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Manager, AuditLog
from .serializers import ManagerSerializer, AuditLogSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            mgr = Manager.objects.get(username=username, is_active=True)
        except Manager.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, mgr.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(ManagerSerializer(mgr).data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Aggregate dashboard data from other services."""
        data = {'staff_count': None, 'order_stats': None}
        try:
            resp = requests.get(f"{settings.SERVICE_URLS['STAFF_SERVICE']}/api/staff/", timeout=5)
            if resp.status_code == 200:
                data['staff_count'] = resp.json().get('count', 0)
        except requests.RequestException:
            pass
        try:
            resp = requests.get(f"{settings.SERVICE_URLS['ORDER_SERVICE']}/api/orders/stats/", timeout=5)
            if resp.status_code == 200:
                data['order_stats'] = resp.json()
        except requests.RequestException:
            pass
        return Response(data)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
