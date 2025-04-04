def user_preferences(request):
    """
    Makes user preferences (unit system and currency) available to all templates.
    """
    context = {
        'unit_system': 'metric',  # Default
        'distance_unit': 'km',
        'volume_unit': 'liters',
        'currency': 'USD',
        'currency_symbol': '$'
    }
    
    if request.user.is_authenticated:
        # Set unit system
        unit_system = request.user.profile.unit_system
        context['unit_system'] = unit_system
        
        # Set distance and volume units based on unit system
        if unit_system == 'imperial':
            context['distance_unit'] = 'mi'
            context['volume_unit'] = 'gal'
        else:  # metric
            context['distance_unit'] = 'km'
            context['volume_unit'] = 'liters'
        
        # Set currency and symbol
        currency = request.user.profile.currency
        context['currency'] = currency
        
        # Set currency symbol
        if currency == 'USD':
            context['currency_symbol'] = '$'
        elif currency == 'EUR':
            context['currency_symbol'] = '€'
        elif currency == 'HUF':
            context['currency_symbol'] = 'Ft'
    
    return context 