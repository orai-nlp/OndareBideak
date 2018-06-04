from django.conf import settings # import the settings file

def base_url(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'BASE_URL': settings.BASE_URL}


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_ANALYTICS': settings.GOOGLE_ANALYTICS,
	'MAPBOX_KEY': settings.MAPBOX_KEY
}
