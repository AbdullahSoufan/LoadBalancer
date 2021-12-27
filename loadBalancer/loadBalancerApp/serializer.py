from rest_framework import serializers
class bookSerializer(serializers.ModelSerializer):

    fields = ('id', 'title')
class bookSerializer2(serializers.ModelSerializer):

    fields = ('title', 'quantity', 'price')
