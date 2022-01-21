import jwt

from django.conf import settings
from django.db.models.expressions import Value
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from storekit.errors import AppValidationError
from storekit.receipt import subscribe_receipt

from stopwatchr.models import alerts, users, stocks
from stopwatchr.serializers import AlertsSerializer, UsersSerializer, StocksSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['GET', 'POST', 'DELETE'])
def users_list(request):
    if request.method == 'GET':
        stopwatchr = users.objects.all()
        
        username = request.GET.get('username', None)
        if username is not None:
            stopwatchr = stopwatchr.filter(username__icontains=username)
        
        users_serializer = UsersSerializer(stopwatchr, many=True)
        return JsonResponse(users_serializer.data, safe=False)
 
    elif request.method == 'POST':
        users_data = JSONParser().parse(request)
        # check if username is duplicated
        all_users = users.objects.all()
        matched_user = all_users.filter(username=users_data.get('username'))
        if not matched_user:
            # register
            users_serializer = UsersSerializer(data=users_data)
            if users_serializer.is_valid():
                users_serializer.save()

                # get the new registered user data from db
                new_user = users.objects.filter(username=users_data.get('username'))
                return JsonResponse(get_tokens_for_user(new_user.get()), status=status.HTTP_201_CREATED)
            return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({ "error": "Username already exists." }, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        count = users.objects.all().delete()
        return JsonResponse({'message': '{} stopwatchr were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    try: 
        user_data = users.objects.get(pk=pk) 
    except users.DoesNotExist: 
        return JsonResponse({'message': 'The users does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        users_serializer = UsersSerializer(user_data) 
        return JsonResponse(users_serializer.data) 
 
    elif request.method == 'PUT': 
        users_data = JSONParser().parse(request) 
        users_serializer = UsersSerializer(user_data, data=users_data) 
        if users_serializer.is_valid(): 
            users_serializer.save() 
            return JsonResponse(users_serializer.data) 
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        user_data.delete() 
        return JsonResponse({'message': 'users was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        stopwatchr = users.objects.all()

        login_data = JSONParser().parse(request)
        if login_data:
            nameMatchedUser = stopwatchr.filter(username=login_data.get('username'))
            if nameMatchedUser:
                pwdMatchedUser = nameMatchedUser.filter(password=login_data.get('password'))
                if pwdMatchedUser:
                    # matchedUser_serializer = UsersSerializer(pwdMatchedUser, many=True)
                    # return JsonResponse(matchedUser_serializer.data[0], status=status.HTTP_200_OK)
                    return JsonResponse(get_tokens_for_user(pwdMatchedUser.get()), status=status.HTTP_200_OK)
                return JsonResponse({ "error": "wrong password." }, status=status.HTTP_200_OK)
            return JsonResponse({ "error": "user doesn't exist." }, status=status.HTTP_200_OK)
        return JsonResponse({ "error": "params don't correct." }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def stocks_list(request):
    if request.method == 'GET':
        userId = request.GET.get('userId', None)
        if userId is not None:
            stocks_list = stocks.objects.all()
            stocks_list = stocks_list.filter(
                user=Value(userId)
            )

            stocks_serializer = StocksSerializer(stocks_list, many=True)
            return JsonResponse(stocks_serializer.data, safe=False)
        return JsonResponse({ 'error': 'Invalid params' }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        stock_data = JSONParser().parse(request)
        stock_serializer = StocksSerializer(data=stock_data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse(stock_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = stocks.objects.all().delete()
        return JsonResponse({'message': '{} stopwatchr were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def alerts_list(request):
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    if request.method == 'GET':
        alerts_list = alerts.objects.all()
        alerts_list = alerts_list.filter(
            user__id=Value(decoded_token.get('user_id'))
        )

        alerts_serializer = AlertsSerializer(alerts_list, many=True)
        return JsonResponse(alerts_serializer.data, safe=False)

    elif request.method == 'PUT':
        params = JSONParser().parse(request)
        alerts_list = alerts.objects.all()
        result = alerts_list.filter(
            user__id=decoded_token.get('user_id'),
            id__in=params.get('ids_list')
        ).update(is_archived=True)
        if result > 0:
            return JsonResponse({ 'success': True }, status=status.HTTP_200_OK)
        return JsonResponse({ 'success': False }, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     count = stocks.objects.all().delete()
    #     return JsonResponse({'message': '{} stopwatchr were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_subscribe_receipt(request):
    token = request.headers.get('Authorization')
    token = token.replace('Bearer ', '')
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id = decoded_token.get('user_id')

    if request.method == 'POST':
        try:
            body_data = JSONParser().parse(request)
            verify_result = subscribe_receipt(receipt=body_data.get('receipt-data'), sandbox=True)

            if verify_result:
                # todo: complete the user data with subscription info
                # users_list = users.objects.all()
                # result = users_list.filter(
                #     id=user_id,
                # ).update()
                # if result > 0:
                    return JsonResponse({ 'success': True }, status=status.HTTP_200_OK)
            return JsonResponse({ 'success': False }, safe=False)
                
        except AppValidationError or AttributeError:
            return JsonResponse({ 'success': False }, status=status.HTTP_400_BAD_REQUEST)
