from django.db.models import F
from django.db.models.aggregates import Max
from django.db.models.expressions import Case, Value, When
from django.utils import timezone
from stopwatchr.models import alerts, stocks, users
from stopwatchr.serializers import AlertsSerializer, StocksSerializer, UsersSerializer

def alert_cron_job():
  print('run [alert_cron_job]')
  # stock_data = {
  #   'stockId': 'stock_manual_3',
  #   'user': 3,
  #   'type': 'Manual',
  #   'name': 'apple',
  #   'entry': 115,
  #   'stop': 12,
  #   'last_updated': timezone.now(),
  # }
  # stock_serializer = StocksSerializer(data=stock_data)
  # if stock_serializer.is_valid():
  #     stock_serializer.save()
  one_h_ago = timezone.now()-timezone.timedelta(hours=1)
  one_d_ago = timezone.now()-timezone.timedelta(days=1)
  print('timezone now = ', timezone.now())
  updated_price = 100
  stocks_list = stocks.objects.all()
  stocks_list = stocks_list.filter(last_updated__gte=one_h_ago, entry__gt=updated_price / (1 - (F('stop') / 100)))
  if stocks_list:
    stocks_serializer = StocksSerializer(stocks_list, many=True)
    print('stocks = ', stocks_serializer.data)

    users_list = users.objects.all().exclude(alert_options='None')
    users_serializer = UsersSerializer(users_list, many=True)
    print('users = ', users_serializer.data)
    for user in users_serializer.data:
      print('user = ', user.get('id'))
      user_id = user.get('id')
      user_alert_option = user.get('alert_options')
      alerts_list = alerts.objects.all()
      alerts_list = alerts_list.filter(
        user__id=Value(user_id), 
        user__alert_options=Value(user_alert_option), 
        created__gte=Case(
          When(user__alert_options='Daily', then=Value(one_d_ago)),
          default=Value(one_h_ago),
        ))
      if len(alerts_list) < 1:
        print('to do')
        user_stocks_list = stocks_list.filter(user_id=user_id)
        if len(user_stocks_list) > 0:
          stocks_serializer = StocksSerializer(user_stocks_list, many=True)
          print('user stocks = ', stocks_serializer.data)
          
          for stock in stocks_serializer.data:
            alerts.objects.create(
              stock=stocks.objects.get(id=stock.get('id')),
              user=users.objects.get(id=user_id),
              is_archived=False,
              created=timezone.now(),
            )
