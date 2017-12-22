from django.shortcuts import render, redirect
from .models import * 
from django.contrib import messages 
import datetime

def index(request):
    return render(request, "bBelt_app/index.html")

def register(request): 

    response = User.objects.register(
        request.POST["name"],
        request.POST["alias"],
        request.POST["email"],
        request.POST["dob"],
        request.POST["password"], 
        request.POST["confirm"]
    )
 
    if response["valid"]: 
        request.session["user_id"] = response["user"].id 
        return redirect("/home")
    else: 
        for error_message in response["errors"]: 
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def login(request): 
    response = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )
    if response["valid"]: 
        request.session["user_id"] = response["user"].id 
        return redirect("/home")
    else: 
        for error_message in response["errors"]: 
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def home(request): #### Back to Home Page

    if "user_id" not in request.session:
        return redirect('/')
    available_trips = [] 

    me = User.objects.get(id=request.session["user_id"])
    available_trips = Trip.objects.order_by("start_date")








    allTrips = Trip.objects.all().exclude(user = me)
    arrTrips = []
    for trip in allTrips:
        arrTrips.append(trip.id)

    
    myTrips = Trip_Join.objects.filter(attendee = me )
    arrMyTrips = []
    for myTrip in myTrips:
        arrMyTrips.append(myTrip.trip_id)

    notMyTrips = set(arrTrips) - set(arrMyTrips)

    context = {
        "user" : me,
        "trips" : Trip.objects.filter(user = me),
        "attending" : Trip_Join.objects.filter(attendee = me),
        "otherTrips": available_trips,
        "notMyTrips": notMyTrips
    }


    print "___________________________________", arrTrips, arrMyTrips, notMyTrips


    return render(request, "bBelt_app/home.html", context)















def add(request): #### To Add a trip page
    return render(request, "bBelt_app/add.html")

def add_travel(request): ### Adds Travel Plans
    for field in request.POST:
        if len(request.POST[field]) < 1:
            messages.add_message(request, messages.INFO, 'All fields are required!')
            return redirect("/add")
            break
    try:
        startDate = datetime.datetime.strptime(request.POST['start_date'],'%m/%d/%Y')
        endDate = datetime.datetime.strptime(request.POST['end_date'],'%m/%d/%Y')

        if startDate < datetime.datetime.now():
            messages.add_message(request, messages.INFO, 'Start Date must be in the future. Also, it must be in MM/DD/YYYY format.')
            return redirect("/add")
        elif startDate > endDate:
            messages.add_message(request, messages.INFO, 'End Date must be after Start Date. It also needs to be in MM/DD/YYYY format.')
            return redirect("/add")
    except Exception,e:
        messages.add_message(request, messages.INFO, 'The dates entered are invalid. Must be in MM/DD/YYYY format.')
        return redirect("/add")

    user = User.objects.get(id = request.session['user_id'])
    Trip.objects.create(user = user, destination = request.POST['destination'], start_date = startDate, end_date = endDate, plan = request.POST['description'])

    print "___________________________________", user


    return redirect("/home")

def join(request, other_id):
    user = User.objects.get(id = request.session['user_id'])
    trip = Trip.objects.get(id = other_id)
    Trip_Join.objects.create(trip = trip, attendee = user)

    return redirect("/home")

def trip(request, id):
    attendees = Trip_Join.objects.filter(trip = id)

    context = {
        "trip": Trip.objects.get(id = id),
        "attendees" : attendees
    }

    return render(request, "bBelt_app/tripinfo.html", context)


def remove(request, id):
    trip = Trip.objects.get(id = id)
    myTrips = Trip_Join.objects.filter(trip = id)
    myTrips.delete()

    return redirect("/home")


def logout(request): 
    request.session.clear()
    return redirect("/")