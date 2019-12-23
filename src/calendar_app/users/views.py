from .forms import (
    EventForm,
    ThemeForm,
    UserRegisterForm
)
from .models import (
    Calendar,
    Event
)
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
import ast
import calendar
import datetime as dt
import re
import requests  # Requires pip install requests


# profile() is used to process the all of data that is used as context on the profile page.
def profile(request, month, day, year):
    theme_form = ThemeForm(request.POST or None)
    event_form = EventForm(request.POST or None)

    current_user = request.user

    # calendar_data starts as empty dictionary and will be filled with keys equal the index of a returned image and
    # values equal to dictionaries containing all data associated with the corresponding image retrieved by
    # Unsplash's API such as; image URL, author, etc...
    calendar_data = {}

    if theme_form.is_valid():

        # The first thing I want is to delete any previous calendar object that belongs to the user
        # in order to avoid multiple calendars which will end up being a waste of memory
        Calendar.objects.filter(user=current_user).delete()

        theme = theme_form.cleaned_data

        # UNSPLASH_API_KEY is stored in an environment variable and passed through the settings
        api_key = settings.UNSPLASH_API_KEY

        # Data passed through the theme_form is in a dictionary I need to isolate what the user actually typed in
        # and pass it as a string into the url in order to retrieve what it is that the user is looking for
        for i in theme:
            theme = str(theme[i])

        api = requests.get(
            f'https://api.unsplash.com/search/photos?page=1&per_page=12&query={theme}&client_id={api_key}',
            stream=True
        )

        api_dict = api.json()['results']

        # Now I need to iterate through each result in order to separate all dictionaries that don't pertain to
        # each other and save the dictionaries to the Calendar model
        for idx, i in enumerate(api_dict):
            calendar_data[idx] = (api_dict[idx])

        model = Calendar(user=current_user, January=calendar_data[0], February=calendar_data[1],
                         March=calendar_data[2], April=calendar_data[3], May=calendar_data[4],
                         June=calendar_data[5], July=calendar_data[6], August=calendar_data[7],
                         September=calendar_data[8], October=calendar_data[9], November=calendar_data[10],
                         December=calendar_data[11])
        model.save()

        # This just resets the form to be blank when the page is loaded
        # in order to avoid having the form filled out again.
        theme_form = ThemeForm()

    # This form a bit more straight forward. I didn't have hoops to jump through so it just takes the form,
    # associates it with the user who created the event and then saves it and clears the inputs.
    if event_form.is_valid():
        event_form = event_form.save(commit=False)
        event_form.author = request.user
        event_form.save()
        event_form = EventForm()

    # I wanted to make the calendar in a way that I could customize each individual piece of it so I used a combination
    # of the DateTime and Calendar libraries and then created variables to isolate each part.

    # I changed the first day of the week from Monday to Sunday.
    calendar.setfirstweekday(6)

    # current_month_num i.e. 10 for October or 12 for December.
    # This, however, will change when navigating to the next or previous month
    current_month_num = month
    current_day = day
    current_yr = year

    # Because I have it so that the 'current month' will change, I need a fixed variable that does not change
    # from page to page.
    actual_current_month = dt.date.today().month

    # Using the calendar library, I used the previously created current year and month variables in order to get
    # string version of sunday through saturday instead of hard coding them into the html.
    calendar_month = calendar.month(current_yr, current_month_num)
    calendar_month_items = re.split('\n', str(calendar_month))
    days_of_week = re.split(' ', calendar_month_items[1])
    days_of_week = [day for day in days_of_week]

    current_month_string = calendar.month_name[month]

    # I needed an accurate count of days regardless of which month was being viewed so I used the calendar.monthrange
    # function and iterated through a range up to the number provided by that and made it into a list.
    days_in_month = int(calendar.monthrange(current_yr, current_month_num)[1])
    days_in_month = [day for day in range(1, days_in_month + 1)]

    # The following code is used to make sure the numbers line up with the proper day of week.
    first_weekday_of_month = range(calendar.weekday(current_yr, current_month_num, 1) + 1)
    spacer = len(range(calendar.weekday(current_yr, current_month_num, 1) + 1))

    event_items = Event.objects.all

    # This if statement checks to see if the authenticated user has a saved calendar. If so,
    # it goes to the user's model object that matches the current_month_string, grabs the url, author name,
    # link to authors page and the alt text provided by the author. If not it used a default image that I selected.
    if Calendar.objects.filter(user=current_user).exists():
        obj = Calendar.objects.get(user=current_user)
        obj = getattr(obj, current_month_string)
        obj = ast.literal_eval(obj)
        calendar_image = obj['urls']['regular']
        image_author = obj['user']['name']
        author_link = obj['links']['html']
        alt_text = obj['alt_description']
    else:
        calendar_image = static("images/zachary-shakked-ur_UgxTS5cU-unsplash.jpg")
        image_author = 'Zachary Shakked'
        author_link = "https://unsplash.com/@zacharyshakked"
        alt_text = "yeah, ok"

    calendar_context = {
        'current_month_string': current_month_string,
        'image_author': image_author,
        'author_link': author_link,
        'alt_text': alt_text,
        'theme_form': theme_form,
        'calendar_image': calendar_image,
        'event_form': event_form,
        'event_items': event_items,
        'spacer': spacer,
        'current_month_number': current_month_num,
        'actual_current_month': actual_current_month,
        'current_day': current_day,
        'current_year': current_yr,
        'calendar month': calendar_month,
        'calendar month items': calendar_month_items,
        'days_in_month': days_in_month,
        'days_in_week': days_of_week,
        'first_weekday_of_month': first_weekday_of_month,
    }
    return calendar_context

# next_ month() and previous_month() take the month number and year number, which are passed through the url as
# keyword arguments. These are used to make sure that the month number will fall between 1 and 12 when it is passed
# on to the profile() function. They also make it so that the year will change when going from December to January
# and visa versa.
@login_required
def previous_month(request, month_num, year_num):
    if month_num.isdigit() and year_num.isdigit():
        if int(month_num) > 12 or int(year_num) > 9999 or int(year_num) < 1000:
            return redirect('profile_home')
    else:
        return redirect('profile_home')
    if int(month_num) < 0:
        month_num = abs(int(month_num)) % 12
    if int(month_num) == 1 or int(month_num) == 0:
        month_num = 13
        context = profile(request, int(month_num) - 1, dt.date.today().day, abs(int(year_num)) - 1)
    else:
        context = profile(request, int(month_num) - 1, dt.date.today().day, abs(int(year_num)))
    return render(request, 'users/profile.html', {'context': context})


@login_required
def next_month(request, month_num, year_num):
    if month_num.isdigit() and year_num.isdigit():
        if int(month_num) > 12 or int(year_num) > 9999 or int(year_num) < 1000:
            return redirect('profile_home')
    else:
        return redirect('profile_home')
    if int(month_num) >= 12:
        month_num = abs(int(month_num)) % 12
        context = profile(request, int(month_num) + 1, dt.date.today().day, abs(int(year_num)) + 1)
    else:
        context = profile(request, int(month_num) + 1, dt.date.today().day, abs(int(year_num)))
    return render(request, 'users/profile.html', {'context': context})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_home(request):
    context = profile(request, dt.date.today().month, dt.date.today().day, dt.date.today().year)
    return render(request, 'users/profile.html', {'context': context})


def event_delete_view(request, object_id):
    obj = get_object_or_404(Event, id=object_id)
    obj.delete()
    return redirect('profile_home')
