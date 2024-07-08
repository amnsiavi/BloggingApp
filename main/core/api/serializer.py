from rest_framework.serializers import ModelSerializer

from core.models import BlogUsers



class BlogUsersSerializer(ModelSerializer):
    
    class Meta:
        model = BlogUsers
        fields = ['id','username','email','DOB','password','bio','profession','date_joined','is_superuser']