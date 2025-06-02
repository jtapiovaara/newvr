from django.db import models
from django.contrib.auth.models import User, Group


class ChatManager(models.Manager):
    def get_all_chats_for_user(self, user):
        user_groups = user.groups.all()
        owned_chats = self.filter(owner=user)
        group_chats = self.filter(usergroup__in=user_groups)
        return (owned_chats | group_chats).distinct().order_by('-timestamp')


class Chat(models.Model):
    name = models.CharField(max_length=64)
    origin = models.CharField(max_length=32, default='chat')
    dialoque = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    usergroup = models.ManyToManyField(Group, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ChatManager()

    def __str__(self):
        return self.name

    def append_dialogue(self, question, answer):
        self.dialoque += f"<{self.owner.username}> {question}" + answer
        self.save()

    @classmethod
    def get_chat_by_id(cls, id):
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            return None


class ChatImage(models.Model):
    name = models.CharField(max_length=128)
    chatrow = models.IntegerField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
