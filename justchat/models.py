from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

class Chat(models.Model):
    name = models.CharField(max_length=64)
    origin = models.CharField(max_length=32, default='chat')
    dialoque = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    usergroup = models.ManyToManyField(Group, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # To get all chat objects
    @staticmethod
    def get_all_chats(user):
        # Fetch user's groups
        user_groups = user.groups.all()

        # Fetch chats that the user owns
        owned_chats = Chat.objects.filter(owner=user)

        # Fetch chats associated with the user's groups
        group_chats = Chat.objects.filter(usergroup__in=user_groups)

        # Combine both querysets, remove duplicates, and order by timestamp in descending order
        all_chats = (owned_chats | group_chats).distinct().order_by('-timestamp')

        return all_chats

    # To get a single chat object by name
    @staticmethod
    def get_chat_by_name(id):
        try:
            return Chat.objects.get(id=id)
        except Chat.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the Chat object is being updated
            original = Chat.objects.get(pk=self.pk)
            self.owner = original.owner  # Ensure the owner remains unchanged
        else:  # New object being created
            if 'owner' in kwargs:
                self.owner = kwargs.pop('owner')

        super().save(*args, **kwargs)  # Ensure the super call is correctly indented and placed

    @classmethod
    def delete_chat(cls, id):
        try:
            chat = cls.objects.get(id=id)
            chat.delete()
            # Return True as a confirmation of the operation success
            return True
        except cls.DoesNotExist:
            # Return False since there's no such chat object
            return False

class ChatImage(models.Model):
    name = models.CharField(max_length=128)
    chatrow = models.IntegerField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name