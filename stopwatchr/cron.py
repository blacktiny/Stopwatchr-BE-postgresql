from django.db.models import F
from django.db.models.expressions import Case, Value, When
from django.utils import timezone
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from stopwatchr.models import alerts, stocks, users
from stopwatchr.serializers import StocksSerializer, UsersSerializer

def alert_cron_job():
  print('run [alert_cron_job]')
  one_h_ago = timezone.now()-timezone.timedelta(hours=1)
  one_d_ago = timezone.now()-timezone.timedelta(days=1)
  # todo: get the updated stocks and prices through other third-party APIs
  updated_price = 100

  stocks_list = stocks.objects.all()
  stocks_list = stocks_list.filter(last_updated__gte=one_h_ago, entry__gt=updated_price / (1 - (F('stop') / 100)))

  if stocks_list:
    users_list = users.objects.all().exclude(alert_options='None')
    users_serializer = UsersSerializer(users_list, many=True)

    for user in users_serializer.data:
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
        user_stocks_list = stocks_list.filter(user_id=user_id)

        if len(user_stocks_list) > 0:
          stocks_serializer = StocksSerializer(user_stocks_list, many=True)

          device = FCMDevice.objects.filter(user_id=3)
          
          for stock in stocks_serializer.data:
            # add the new alerts to db
            alerts.objects.create(
              stock=stocks.objects.get(id=stock.get('id')),
              user=users.objects.get(id=user_id),
              is_archived=False,
              created=timezone.now(),
            )

            # send push notification to user device
            if device:
              result = device.send_message(
                Message(data={"title": "stopwatchr"}, notification=Notification(title="title", body="body", image="image_url"))
              )
              print(result)
