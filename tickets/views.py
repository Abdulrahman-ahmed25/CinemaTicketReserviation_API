from django import http
from rest_framework.serializers import Serializer
from tickets import serializers
from django.shortcuts import render
from .models import Guest, Movie, Reservation
# Create your views here.
from django.http.response import Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status, filters, mixins, generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GuestSerialization, MovieSerialization, ReservationSerialization
from rest_framework.authentication import TokenAuthentication
#for searching process
from django_filters import rest_framework as filters
from .paginations import CustomPagination
#1 without REST framework and no model query
def no_rest_no_model(request):
    guest={
        'name':'samir',
        'mobile':256324
    }
    return JsonResponse(guest, safe=False)

#2 without REST framework with model query
def no_rest_yes_model(request):
    data = Guest.objects.all()
    context={
        'guests':list(data.values())
    }
    return JsonResponse(context)

#3 function based views
#3.1 GET POST
@api_view(['GET','POST'])
def fbv_list(request):
    #GET 
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerialization(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = GuestSerialization(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)

#3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def fbv_pk(request, pk): 
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    #GET 
    if request.method == 'GET':
        serializer = GuestSerialization(guest)
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerialization(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    #DELETE 
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#4 Class based views
#4.1 GET POST
class CBV_list(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerialization(guests, many= True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerialization(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)

#4.2 GET PUT DELETE
class CBV_bk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerialization(guest)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerialization(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT )


#5 using mixins
#5.1 GET POST
class MixinsList(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerialization

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#5.2 GET PUT DELETE
class MixinsBk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerialization

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#6 using generics
#6.1 GET POST
class GenericsList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerialization
    pagination_class = CustomPagination

#6.2 GET PUT DELETE
class GenericsBk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerialization

#7 viewsets
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerialization
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'mobile')
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerialization
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['movie']
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialization
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]



#7 new reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    ## for create new reservation with exist guests
    try:
        guest= Guest.objects.get(
            name = request.data['name'],
            mobile = request.data['mobile']
            )
    except Guest.DoesNotExist:
        raise Http404

    # for create new reservation with creating new guest
    # guest = Guest()
    # guest.name = request.data['name']
    # guest.mobile = request.data['mobile']
    # guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    # serializer = ReservationSerialization(reservation, data = request.data)
    # if serializer.is_valid():
    #     serializer.save()
    return Response(status=status.HTTP_202_ACCEPTED)
    
