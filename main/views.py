from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserMap, Pin, Bookmarks
from users.forms import CreateMap, UpdateMap, CreatePin
from django.contrib import messages
from django.contrib.auth.models import User

#navigation bar views
@login_required
def index(response):

    form = CreateMap()

    #get current user
    current_user = response.user

    #create new map
    if response.method == "POST":
        print("Post Request Sent")
        form = CreateMap(response.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            p = form.cleaned_data['private']

            #check if the map name already exists, if it does throw an error
            if not UserMap.objects.filter(name=n).exists():
                m = UserMap(name = n, private = p)    
                m.save()        

                #set map to current user
                response.user.usermap.add(m)
            else: 
                #throw error if map already exists
                messages.error(response, f'Map name already exists.')

            return redirect('main-home')
    else:
        form = CreateMap()

    context = {
        #get all of users maps
        'user_maps': UserMap.objects.all(),
        'form': form,
        'current_user': current_user,
        'bookmarks': Bookmarks.objects.filter(user=response.user),
        'bookmarks_count': Bookmarks.objects.filter(user=response.user).count()

    }

    return render(response, 'index.html', context)

#search page functionality
def search(request):
    query = ''
    users = User.objects.none()
    
    if request.method == 'POST':
        query = request.POST.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query)

    return render(request, 'search.html', {'users': users, 'query': query})


#views not on navigation bar
def map(request, username, map_name):


    #variable to get username from URL
    general_user = User.objects.get(username=username)

    #variable to get the current user
    user = User.objects.get(username=request.user)
    username = user.username

    #get id of map and select pins
    selected_map = UserMap.objects.get(user=general_user, name=map_name)

    #get current likes from the map
    likers = selected_map.likes.all()  
    #like counts
    likes_count = likers.count()  

    #check to see if current map is bookmarked or not
    is_bookmarked = Bookmarks.objects.filter(user=request.user, creator = general_user, map_name=map_name).exists()

    #get pins of the selected user map to retrieve data 
    pins = Pin.objects.filter(usermap=selected_map)

    #get all the pins from the selected map to generate the count
    pins_all = selected_map.pin.all()

    #generate form to create pin
    create_pin_form = CreatePin()

    #generate form to update map
    update_map_form = UpdateMap(instance = selected_map)

    #toggle between private and public
    #if togglePrivate submit button is clicked in map.html
    if request.method == 'POST' and 'togglePrivate' in request.POST:
        #toggle variable 
        selected_map.private = not selected_map.private
        selected_map.save()

    #update map form
    elif request.method == 'POST' and 'updateMap' in request.POST:
        update_map_form = UpdateMap(request.POST, instance=selected_map)
        if update_map_form.is_valid():
            n = update_map_form.cleaned_data['name']

            #check if the map name already exists, if it does throw an error
            if not UserMap.objects.filter(name=n).exists():
                update_map_form.save()
                messages.success(request, f'Map name changed.')
            else: 
                #throw error if map already exists
                messages.error(request, f'Map name already exists.')

            #redirect to the new url
            return redirect('main-map', username=username, map_name=selected_map)
        else:
            update_map_form = UpdateMap(request.POST, instance=selected_map)

    #delete map
    elif request.method == 'POST' and 'deleteMap' in request.POST:
            #delete the map
            selected_map.delete()
            messages.error(request, f'Map Deleted.')
            return redirect('main-home')
    
    #create pin
    elif request.method == 'POST' and 'create_pin_btn' in request.POST:
        create_pin_form = CreatePin(request.POST)
        if create_pin_form.is_valid():
            #get pin name to check if it already exists
            pin_name = create_pin_form.cleaned_data['name']
            #if pin name already exists throw an error
            if Pin.objects.filter(usermap=selected_map, name=pin_name).exists():
                messages.error(request, 'A pin with this name already exists in this map.')

            else:
                # Linking the pin to the selected map
                new_pin = Pin(
                    usermap=selected_map,  
                    name= pin_name,
                    lat=create_pin_form.cleaned_data['lat'],
                    long=create_pin_form.cleaned_data['long'],
                    notes=create_pin_form.cleaned_data['notes']
                )
                new_pin.save()
                #make success message
                messages.success(request, f'New pin "{pin_name}" created successfully.')
                #redirect to the newly created view pin page
                return redirect('main-pin', username=username, map_name=selected_map, pin_name= pin_name)
        
        else:
            create_pin_form = CreatePin(request.POST)

    #function to toggle bookmark
    elif request.method == 'POST' and 'toggleBookmark' in request.POST:
        #write the variables to the database IF it is not already in the database
        #variables to be written are current user (request.user), creater of map (username), and map name (map_name)
        if not is_bookmarked:
            # If it does not exist then create new bookmark
            new_bookmark = Bookmarks(user=request.user, creator=general_user, map_name=map_name)
            new_bookmark.save()

            #generate success message
            messages.success(request, f'"{map_name}" has been saved')
        else:
            #get existing bookmark
            existing_bookmark = Bookmarks.objects.filter(user=request.user, creator=general_user, map_name=map_name).first()
            existing_bookmark.delete()
            # if the map already exists - throw an error
            messages.error(request, f'"{map_name}" has been removed from Saved Maps')

        #refresh page 
        return redirect('main-map', username=general_user, map_name=map_name)


    #function to like map
    elif request.method == 'POST' and 'likeBtn' in request.POST:
        #if current users name is not in the database for likes

        #if user has already liked the map, remove the like
        if request.user in selected_map.likes.all():
            #remove the like
            selected_map.likes.remove(request.user)
        else:
            #add the like
            selected_map.likes.add(request.user)

        #save data
        selected_map.save()
        #refresh page
        return redirect('main-map', username=general_user, map_name=map_name)


    #push current map data to view
    context = {
        'usermap': selected_map,
        'current_user': username,
        'general_user': general_user,
        'likes_count': likes_count,
        'pins': pins,
        'pins_all' : pins_all,
        'update_map_form': update_map_form,
        'create_pin_form': create_pin_form,
        'is_bookmarked': is_bookmarked
    }

    return render(request, 'map.html', context)


def pin(request, username, map_name, pin_name):

    #load general user
    general_user = User.objects.get(username=username)

    user = User.objects.get(username=request.user)
    username = user.username

    #get the map name for the route
    usermap = UserMap.objects.get(name=map_name, user=general_user)

    #get the respective pin
    pin = Pin.objects.get(usermap=usermap, name=pin_name)

    context = {
        'usermap': usermap,
        'pin': pin,
        'current_user': username,
        'general_user': general_user
    }

    return render(request, 'pin/view_pin.html', context)


#function to edit pin
def edit_pin(request, username, map_name, pin_name):

    #load general user
    general_user = User.objects.get(username=username)

    #get current user
    user = User.objects.get(username=request.user)
    username = user.username

    usermap = UserMap.objects.get(name=map_name, user=general_user) 
    #get the respective pin
    pin = Pin.objects.get(usermap=usermap, name=pin_name)

    initial_data = {
        'name': pin.name,
        'lat': pin.lat,
        'long': pin.long,
        'notes': pin.notes
    }

    #create form to update map 
    create_pin_form = CreatePin(initial = initial_data)

    #UPDATE PIN
    if request.method == 'POST' and 'update_pin_btn' in request.POST:
        create_pin_form = CreatePin(request.POST, initial = initial_data) 
        if create_pin_form.is_valid():
            #check if pin name already exists
            new_name = create_pin_form.cleaned_data['name']

            if Pin.objects.filter(usermap=usermap, name=new_name).exclude(id=pin.id).exists():
                messages.error(request, 'Another pin with this name already exists in this map.')
            else:
                # Save the form directly to update the existing pin
                pin.name = new_name
                pin.lat = create_pin_form.cleaned_data['lat']
                pin.long = create_pin_form.cleaned_data['long']
                pin.notes = create_pin_form.cleaned_data['notes']

                pin.save()        
                messages.success(request, f'Pin "{new_name}" updated successfully.')
                #redirect to respective pins view page
                return redirect('main-pin', username=general_user, map_name=usermap, pin_name= pin.name)
            
        else:

            create_pin_form = CreatePin(request.POST, initial = initial_data) 

    #DELETE PIN
    if request.method == 'POST' and 'delete_pin_btn' in request.POST:
        #delete respective point
        pin.delete()
        #message that pin was deleted
        messages.error(request, f'Pin was deleted.')

        #redirect to maps homepage
        return redirect('main-map', username=username, map_name=usermap)



    context = {
        'usermap': usermap,
        'form': create_pin_form,
        'pin': pin,
        'current_user': username,
        'general_user': general_user
    }

    return render(request, 'pin/edit_pin.html', context)



#settings page functionality
@login_required
def settings(request):
    return render(request, 'settings.html')

#user profile page
@login_required
def user_profile(request, username):

    #load general user
    general_user = User.objects.get(username=username)

    #get username
    user = User.objects.get(username=username)
    user_maps = UserMap.objects.filter(user=user)

    #calculate the number of pins that are public
    public_maps_count = UserMap.objects.filter(user=user, private=False).count()

    context = {
        'user':user,
        'user_maps': user_maps,
        'general_user': general_user,
        'public_maps_count': public_maps_count

    }

    return render(request, 'user_profile.html', context)
