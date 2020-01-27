from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Group
from .serializers import UserSerializer, GroupSerializer
from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime


class UserViewset(viewsets.ModelViewSet):
    """Show all existing users for test purposes."""
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class GroupViewset(viewsets.ModelViewSet):
    """Show all existing groups for test purposes."""
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()


class UserFriendship(APIView):
    """Add or remove friend"""

    def post(self, request, friend):
        sender = request.user
        receiver = User.objects.get(id=friend)
        sender.friends.add(receiver)
        sender.save()
        receiver.friends.add(sender)
        receiver.save()
        return Response(
            'Friend added.'
        )

    def delete(self, request, friend):
        sender = request.user
        receiver = User.objects.get(id=friend)
        sender.friends.remove(receiver)
        sender.save()
        receiver.friends.remove(sender)
        receiver.save()
        return Response(
            'Friend removed.'
        )


class GroupMembership(APIView):
    """Join or leave group"""

    def post(self, request, group_id, user_id):
        member = request.user
        group = Group.objects.get(id=group_id)
        member.groups.add(group)
        member.save()
        return Response(
            'Member joined the group'
        )

    def delete(self, request, group_id, user_id):
        member = request.user
        group = Group.objects.get(id=group_id)
        member.groups.remove(group)
        member.save()
        if member == group.administrator:
            group.delete()
        return Response(
            'Member left the group.'
        )


class GroupManagement(APIView):
    """Create, edit or delete group"""
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request, group_id=None):
        data = request.data
        group = Group(
            name = data['name'],
            description = data['description'],
            administrator = request.user,
            avatar=request.data.get('avatar')
        )
        group.save()
        request.user.groups.add(group)
        request.user.save()
        # Return OK
        return Response(
            'Group created.'
        )

    def patch(self, request, group_id):
        group = Group.objects.get(id=group_id)
        if request.user == group.administrator:
            # TODO There should be a better way
            for key, value in request.data.items():
                if key == 'name':
                    group.name = value
                elif key == 'description':
                    group.description = value
                elif key == 'administrator':
                    group.administrator = value
            group.avatar = request.data.get('avatar') or group.avatar
            group.save()
            return Response(
                'Group data edited.'
            )
        else:
            return Response(
                'Only group administrator can edit the group.',
                status=status.HTTP_403_FORBIDDEN
            )


    def delete(self, request, group_id):
        group = Group.objects.get(id=group_id)
        if request.user == group.administrator:
            group.delete()
            return Response(
                'Group deleted.'
            )
        else:
            return Response(
                'Only group administrator can delete the group.',
                status=status.HTTP_403_FORBIDDEN
            )


class UserProfile(APIView):
    """Show or edit user profile"""
    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                'There is no user with this ID.',
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        if request.user == user:
            # TODO There should be a better way
            for key, value in request.data.items():
                if key == 'email':
                    user.email = value
                elif key == 'password':
                    user.password = value
                elif key == 'first_name':
                    user.first_name = value
                elif key == 'second_name':
                    user.second_name = value
                elif key == 'nickname':
                    user.nickname = value
                elif key == 'birth_date':
                    user.birth_date = value
                elif key == 'info':
                    user.info = value
            user.avatar = request.data.get('avatar') or user.avatar
            user.save()
            return Response(
                'User data edited.'
            )
        else:
            return Response(
                'You cannot edit profiles of other members.',
                status=status.HTTP_403_FORBIDDEN
            )