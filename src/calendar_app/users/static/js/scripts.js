
var viewEvents = document.getElementById('view_events');
var addEvent = document.getElementById('add_event');

var eventWrapper = document.getElementById('event_wrapper');
var eventForm = document.getElementById('event_form');

var closeEvents = document.getElementById('close_events');
var closeEventForm = document.getElementById('close_event_form');

var themeSearchLabel = document.getElementById('div_id_theme')

$(themeSearchLabel).click(function() {
    $('label:first-child').hide();
})

$(viewEvents).click(function() {
    $(eventWrapper).stop(true, false, true).slideToggle('fast');
});

$(closeEvents).click(function() {
    $(eventWrapper).stop(true, false, true).slideToggle('fast');
});

$(addEvent).click(function() {
    $(eventForm).stop(true, false, true).slideToggle('fast');
});

$(closeEventForm).click(function() {
    $(eventForm).stop(true, false, true).slideToggle('fast');
});


// The following code was used on lines 41-50 of profile.html
//in order to take advantage of django tags

//    <script type="text/javascript">
//    $( document ).ready(function() {
//        var eventName = document.getElementsByClassName('event_{{ event.id }}');
//        var eventDetails = document.getElementsByClassName('event_details');
//
//        $(eventName).click(function() {
//            $(this).next().stop(true, false, true).slideToggle('slow');
//        });
//    });
//    </script>