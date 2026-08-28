from django.shortcuts import render, redirect, get_object_or_404
from . forms import CustomUserForm, ProfileForm, DestinationImageForm
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Destinations, DestinationImages, Profile, FavDestination
from .serializers import DestinationsSerializer, DestinationImageSerializer, ProfileSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView


class CreateProfile(CreateAPIView):
    queryset=Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser,FormParser]
    lookup_field = 'id'

@api_view(['GET'])
def get_user(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many = True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_profile(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many = True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_user_id(request, pid):
    try:
        user = User.objects.get(id=pid)
    except User.DoesNotExist:
        return Response('Not found',status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)

class UpdateProfile(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser,FormParser]
    lookup_field = 'id'

@api_view(['GET','DELETE'])
def delete_profile(request,pid):
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(id =pid)
        except Profile.DoesNotExist:
            return Response({'error' : 'Profile not found'},status=404)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)
    if request.method == 'DELETE': 
        try:
            profile = Profile.objects.get(id =pid)
        except Profile.DoesNotExist:
            return Response({'error' : 'Profile not found'},status=404)
        profile.delete()
        return Response({'message' : 'Profile Deleted successfully'})

class CreateDestView(CreateAPIView):
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    parser_classes = [MultiPartParser, FormParser]

@api_view(['GET'])
def get_dest(request):
    destinations = Destinations.objects.all()
    serializer = DestinationsSerializer(destinations, many=True)
    return Response(serializer.data)
    
class UpdateDest(UpdateAPIView):
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'
    
@api_view(['GET','DELETE'])
def delete_dest(request,pid):
    if request.method == 'GET':
        try:
            destination = Destinations.objects.get(id = pid)
        except Destinations.DoesNotExist:
            return Response({'error' : 'destination not found'},status=404)
        serializer = DestinationsSerializer(destination)

        return Response(serializer.data,status=200)
    
    if request.method == 'DELETE':
        try:
            destination = Destinations.objects.get(id =pid)
        except Destinations.DoesNotExist:
            return Response({'error' : 'Destination not found'},status=status.HTTP_404_NOT_FOUND)
        
        destination.delete()
        return Response({'Message' : 'Deleted successfully'})
    

class CreateDestImage(CreateAPIView):
    queryset = DestinationImages.objects.all()
    serializer_class = DestinationImageSerializer
    parser_classes=[MultiPartParser,FormParser]
    lookup_field='id'

@api_view(['GET'])
def get_dest_image(request):
    dest_image = DestinationImages.objects.all()
    serializer = DestinationImageSerializer(dest_image, many = True)
    return Response(serializer.data)

class UpdateDestImage(UpdateAPIView):
    queryset = DestinationImages.objects.all()
    serializer_class = DestinationImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'id'

@api_view(['GET','DELETE'])
def delete_image(request, pid):
    if request.method =='GET':
        try:
            dest_image = DestinationImages.objects.get(id = pid)
        except DestinationImages.DoesNotExist:
            return Response({'error' : 'destination image not found'},status=404)
        serializer = DestinationImageSerializer(dest_image)
        return Response(serializer.data, status=200)

    if request.method == 'DELETE':
        try:
            dest_image = DestinationImages.objects.get(id=pid)
        except DestinationImages.DoesNotExist:
            return Response({'error' : 'Destination images not found'},status=404)
        dest_image.delete()
        return Response({'message' : 'Destination image deleted successfully'})



def home(request):
    destination = Destinations.objects.all()
    return render(request,'tour/index.html', {'destination' : destination})

def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successfully')
            return redirect('login')
    else:
        form = CustomUserForm()   # Create empty form on GET request

    return render(request, 'tour/register.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username =name, password = pwd)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully')
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
    return render(request, 'tour/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('/')

def view_profile(request):
    if request.user.is_authenticated:
        profile,create = Profile.objects.get_or_create(user = request.user)
        dest_image = DestinationImages.objects.filter(user = profile.user).order_by('-updated_at')
        return render(request, 'tour/view_profile.html', {'profile': profile, 'dest_image':dest_image})
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')
    
def update_profile(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user = request.user)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            profile_form = form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('/view_profile')
        else:
            form = ProfileForm(instance=profile)
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')
    return render(request, 'tour/edit_profile.html', {'form':form ,'profile' : profile})
    
def view_all_dest(request):
    if request.user.is_authenticated:
        destination = Destinations.objects.all()
        return render(request, 'tour/view_all_dest.html', {'destination' : destination})
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')

def view_each_dest(request, pname):
    if request.user.is_authenticated:
        destination = Destinations.objects.filter(place_name=pname).first()
        image_review = DestinationImages.objects.filter(destination = destination).order_by('-updated_at')
        if destination:
            return render(request, 'tour/view_each_dest.html', {'destination':destination , 'image_review' : image_review})
        else:
            messages.warning(request, 'No destination found')
            return redirect('/view_all_dest')
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')

    
def add_image(request,pid):
    if request.user.is_authenticated:
        try:
            destination = Destinations.objects.get(id =pid)
        except Destinations.DoesNotExist:
            messages.error(request, 'Destination not found')

        if request.method == 'POST':
            form = DestinationImageForm(request.POST, request.FILES)
            if form.is_valid():
                image_review = form.save(commit=False)
                image_review.user = request.user
                image_review.destination = destination
                image_review.save()
                messages.success(request, 'Destination added Successfully')
                return redirect('/view_all_dest')
        else:
            form = DestinationImageForm()
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')
    return render(request, 'tour/add_image.html',{'form' : form, 'destination' : destination})

def edit_image(request, pid):
    if request.user.is_authenticated:
        dest_image = DestinationImages.objects.get(id =pid)
        if request.method == 'POST':
            form = DestinationImageForm(request.POST, request.FILES, instance=dest_image)
            if form.is_valid():
                form.save()
                messages.success(request, 'Destination added Successfully')
                return redirect('/view_all_dest')
        else:
            form = DestinationImageForm(instance=dest_image)
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')
    return render(request, 'tour/add_image.html',{'form' : form, 'dest_image' : dest_image})
    
def delete_dest_image(request,pid):
    if request.user.is_authenticated:
        image_review = DestinationImages.objects.get(id = pid, user = request.user)
        dest_name = image_review.destination.place_name
        image_review.delete()
        messages.success(request, 'Reviews deleted Successfully')
        return redirect(f'/view_each_dest/{dest_name}')
    else:
        messages.error(request, 'You must be logged in')
        return redirect('/login')
    
def add_to_fav(request):
    if request.headers.get('X-Requested-With')==('XMLHttpRequest'):
        if request.user.is_authenticated:
            data = json.load(request)
            dest_id = data['pid']
            dest_status = Destinations.objects.get(id = dest_id)
            if dest_status:
                if FavDestination.objects.filter(user = request.user, destination = dest_status).exists():
                    return JsonResponse({'status' : 'Destination already added in favorites'},status = 200)
                else:
                    FavDestination.objects.create(user = request.user, destination = dest_status)
                    return JsonResponse({'status' : 'Destination added in favorites list'},status = 200)
            else:
                return JsonResponse({'status' : 'Destination not found'},status =404)
        else:
            return JsonResponse({'status' : 'Login to add favorites'},status = 400)
    else:
        return JsonResponse({'status' : 'Invalid Access'},status=400)
    
def fav_page(request):
    if request.user.is_authenticated:
        fav = FavDestination.objects.filter(user = request.user)
        return render(request, 'tour/fav_page.html',{'fav':fav})
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')
    
def remove_fav(request,pid):
    if request.user.is_authenticated:
        fav = FavDestination.objects.filter(id = pid)
        fav.delete()
        return redirect('/fav_page')
    
def search_dest(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '').strip()

        if query == '':
            messages.warning(request, 'Enter the destination')
            return redirect('/')
        
        dest = Destinations.objects.filter(place_name__iexact = query)

        if dest.exists():
            place = dest.first()
            return redirect(f'/view_each_dest/{place.place_name}')
        else:
            messages.warning(request, 'Destination not found')
            return redirect('/')
    else:
        messages.warning(request, 'You must be logged in')
        return redirect('/login')