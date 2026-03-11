import requests as http_requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Staff
from .serializers import StaffSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get_queryset(self):
        qs = Staff.objects.all()
        department = self.request.query_params.get('department')
        is_active = self.request.query_params.get('is_active')
        if department:
            qs = qs.filter(department=department)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return qs

    def _find_manager(self, username):
        mgr_url = settings.SERVICE_URLS['MANAGER_SERVICE']
        resp = http_requests.get(f"{mgr_url}/api/manager/", timeout=5)
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        for manager in results:
            if manager.get('username') == username:
                return manager
        return None

    def _sync_manager(self, staff, raw_password=None):
        """Đồng bộ sang Manager Service khi role=admin."""
        if staff.role != 'admin':
            return

        mgr_url = settings.SERVICE_URLS['MANAGER_SERVICE']
        payload = {
            'username': staff.username,
            'email': staff.email,
            'full_name': staff.full_name,
            'phone_number': staff.phone_number,
            'date_of_birth': str(staff.date_of_birth) if staff.date_of_birth else None,
            'gender': staff.gender,
            'employee_code': staff.employee_code,
            'department': staff.department,
            'access_level': 10,
            'is_active': staff.is_active,
        }
        if raw_password:
            payload['password'] = raw_password

        try:
            existing = self._find_manager(staff.username)
            if existing:
                http_requests.patch(
                    f"{mgr_url}/api/manager/{existing['id']}/",
                    json=payload,
                    timeout=5,
                )
            else:
                http_requests.post(
                    f"{mgr_url}/api/manager/",
                    json=payload,
                    timeout=5,
                )
        except http_requests.RequestException:
            pass

    def _delete_manager(self, username):
        mgr_url = settings.SERVICE_URLS['MANAGER_SERVICE']
        try:
            existing = self._find_manager(username)
            if existing:
                http_requests.delete(
                    f"{mgr_url}/api/manager/{existing['id']}/",
                    timeout=5,
                )
        except http_requests.RequestException:
            pass

    def perform_create(self, serializer):
        raw_password = self.request.data.get('password')
        staff = serializer.save()
        self._sync_manager(staff, raw_password)

    def perform_update(self, serializer):
        previous_staff = serializer.instance
        previous_role = previous_staff.role
        previous_username = previous_staff.username
        raw_password = self.request.data.get('password')
        staff = serializer.save()
        if previous_role == 'admin' and previous_username != staff.username:
            self._delete_manager(previous_username)
        if staff.role == 'admin':
            self._sync_manager(staff, raw_password)
        elif previous_role == 'admin':
            self._delete_manager(previous_username)

    def perform_destroy(self, instance):
        username = instance.username
        role = instance.role
        instance.delete()
        if role == 'admin':
            self._delete_manager(username)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            staff = Staff.objects.get(username=username, is_active=True)
        except Staff.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not check_password(password, staff.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(StaffSerializer(staff).data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        staff = self.get_object()
        staff.is_active = False
        staff.save()
        self._sync_manager(staff)
        return Response({'status': 'deactivated'})
