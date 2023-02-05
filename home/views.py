from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action



class LoginApi(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST) 

        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid credentials'
            }, status.HTTP_400_BAD_REQUEST)

        token,_ = Token.objects.get_or_create(user=user) 
        return Response({'status': True, 'message': 'User Logined', 'token':str(token)}, status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
                'status': True,
                'message': 'User Created'
            }, status.HTTP_201_CREATED
        )
        
        




#Function Based View with @api_view (decorators)
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def home(request):
    courses = {
        'course_name' : 'Python - Django',
        'learn': ['Python', 'Django', 'Flask', 'DRF'],
        'course_provider' : 'Mehfooz Ali'
        }

    if request.method=='GET':
        print('You hit a Get Method')
        return Response(courses)

    elif request.method=='POST':
        data = request.data
        print('------------')
        print(data)
        print('------------')
        print('You hit a POST Method')
        return Response(courses)

    elif request.method=='PUT':
        print('You hit a PUT Method')
        return Response(courses)
    
    else: 
        print('You hit a Invalid  Method')
        return Response(courses)



@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'Success'}) 

    return Response(serializer.errors)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        obj = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(obj, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Person record deleted'}) 




#Class based Views with APIView
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        obj = Person.objects.all()
        
        try:
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(obj, page_size)
            serializer = PeopleSerializer(paginator.page(page), many=True) 
        except Exception as e:
            return Response(
                {'status':False, 
                 'message' : 'Inavlid Page !'})

        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Person record deleted'}) 



class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ['post', 'get']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset =  queryset.filter(name__startswith = search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({'status':200, 'data' : serializer.data}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['post'])
    def send_mail_to_person(self, request, pk):
        return Response(
                {'status': True, 
                 'message' : 'Mail has been sent successfuly !' }
                 )