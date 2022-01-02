from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from events.constants import EVENT_TYPES
from events.models import Events, ApiKey


def IncomeExpensesView(request, wallet_hash):
    valid_key = ApiKey.objects.filter(key=request.headers['x-api-key']).first()
    if not valid_key:
        raise PermissionDenied()
    event_filter = Q(Q(to_wallet=wallet_hash) | Q(from_wallet=wallet_hash))
    if date_lte := request.GET.get('date_lte'):
        event_filter &= Q(epoch_timestamp__lte=date_lte)
    if date_gte := request.GET.get('date_gte'):
        event_filter &= Q(epoch_timestamp__gte=date_gte)

    all_income_events, all_expenses_events = [], []
    total_income, total_expenses = 0.0, 0.0
    all_events = Events.objects.filter(event_filter).exclude(contract_hash__in="0x0000000000000000000000000000000000000000").order_by('-epoch_timestamp')  
    events_per_type = {v: [e for e in all_events if e.event_type == k] for k, v in EVENT_TYPES.items()}

    for event_type, relevant_events in events_per_type.items():
        if event_type == EVENT_TYPES.get(1):
            income_events = [e for e in relevant_events if e.to_wallet == wallet_hash]
            expenses_events = []
        else:
            income_events = [e for e in relevant_events if e.from_wallet == wallet_hash]
            expenses_events = [e for e in relevant_events if e.to_wallet == wallet_hash]
        
        income_sum= sum([e.total_price_event() for e in income_events])
        total_income += income_sum
        expenses_sum= sum([e.total_price_event() for e in expenses_events])
        total_expenses += expenses_sum

        if income_events:
            all_income_events.append({'events': [e.dict_record() for e in income_events], 'event_type': event_type, 'total_sum': income_sum})
        if expenses_events:
            all_expenses_events.append({'events': [e.dict_record() for e in expenses_events], 'event_type': event_type, 'total_sum': expenses_sum})


    data = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "income": all_income_events,
        "expenses": all_expenses_events
    }
    response = JsonResponse(data)

    return response
