from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings as d_set


class Userinfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=40)
    user_email = models.CharField(max_length=40)
    user_rman = models.CharField(max_length=20, default='')
    user_address = models.CharField(max_length=100, default='')
    user_mnumber = models.CharField(max_length=6, default='')
    user_pnumber = models.CharField(max_length=11, default='')

    def generate_reset_token(self, expiration=3600):
        s = Serializer(d_set.SECRET_KEY, expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(d_set.SECRET_KEY)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = Userinfo.objects.filter(id=data.get('reset')).first()
        if not user:
            return False
        user.user_pwd = new_password
        user.save()
        return True
