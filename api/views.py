from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Patient, Doctor, Mapping
from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class MappingListCreateView(generics.ListCreateAPIView):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]


class MappingDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        patient = get_object_or_404(Patient, id=id)
        if patient.created_by != request.user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        mappings = Mapping.objects.filter(patient=patient)
        doctors = [mapping.doctor for mapping in mappings]
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def delete(self, request, id):
        mapping = get_object_or_404(Mapping, id=id)
        if mapping.patient.created_by != request.user:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
