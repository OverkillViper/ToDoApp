from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, ProfileForm
from .models import User, Profile
from .helpers import send_password_reset_mail
from .serializers import UserSerializer
import uuid

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id'        : request.user.id,
        'name'      : request.user.name,
        'email'     : request.user.email,
        'avatar'    : request.user.get_avatar()
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email'     : data.get('email'),
        'name'      : data.get('name'),
        'password1' : data.get('password1'),
        'password2' : data.get('password2'),
    })

    if form.is_valid():
        form.save()
        user = User.objects.get(email=request.data.get('email'))
        profile = Profile(user=user)
        profile.save()
        # Send verification email later!
    else:
        print(form.errors)
        message = 'error'

    return JsonResponse({'message': message, 'errors': form.errors})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def password_recover(request):
    data = request.data
    
    if not User.objects.filter(email=data.get('email')).exists():
        return JsonResponse({'status' : 'No user found with the provided email'})
    else:
        user = User.objects.get(email=data.get('email'))
        token = str(uuid.uuid4())
        profile = Profile.objects.get(user=user)
        profile.forget_password_token = token
        profile.save()
        profile.forget_password_token
        send_password_reset_mail(user.email, token)
        return JsonResponse({'status' : 'success'})
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def reset_password(request):
    token = request.data.get('token')
    password = request.data.get('password')
    
    if Profile.objects.filter(forget_password_token=token).exists():
        profile = Profile.objects.get(forget_password_token=token)
        user = User.objects.get(id=profile.user.id)
        try:
            user.set_password(password)
            user.save()
            
            profile.forget_password_token = ""
            profile.save()
            
            return JsonResponse({'status' : 'success'})
        except Exception as e:
            return JsonResponse({'error' : e})
        
    else:
        return JsonResponse({'error': 'Invalid token. The token may be expired or it has already been used once.'})
    
@api_view(['POST'])
def check_user_password(request):
    password = request.data.get('password')
    user = request.user
    match = user.check_password(password)
    
    if(match):
        return JsonResponse({'status' : 'match'})
    else:
        return JsonResponse({'status' : 'failed'})
    
@api_view(['POST'])
def change_password(request):
    try:
        user = request.user
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        
        return JsonResponse({'status' : 'success'})
    except Exception as e:
        return JsonResponse({'error' : e})
    
@api_view(['DELETE'])
def delete_user(request):
    try:
        user = request.user
        user.avatar.delete()
        user.delete()
        
        return JsonResponse({'status' : 'User deleted successfully'})
    except Exception as e:
        return JsonResponse({'error' : e})
    
@api_view(['POST'])
def upload_avatar(request):
    try:
        user = request.user
        
        user.avatar.delete()
        
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            
        serializer = UserSerializer(user)

        return JsonResponse({'status': 'success', 'user': serializer.data})
        # return JsonResponse({'message': 'success'})
    except Exception as e:
        return JsonResponse({'error' : e})
    
@api_view(['POST'])
def change_username(request):
    try:
        user = request.user
        print(request.data.get('name'))
        user.name = request.data.get('name')
        user.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error' : e})
    