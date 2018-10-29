from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    language  = models.CharField(max_length=30,blank=True)
    birthdate = models.DateField(default='2000-01-01',blank=True)
    profile_pic = models.ImageField(blank=True, upload_to='profile_pics', default='profile_pics/no-image.jpg')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.first_name


class Course(models.Model):
    teacher     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title       = models.CharField(max_length=50)
    description = models.TextField()
    level       = models.CharField(max_length=30)
    horario     = models.CharField(max_length=30,default = 'MATUTINO')
    precio      = models.IntegerField(default=0)
    

    def __str__(self):
        return self.title


class Take(models.Model):
    student     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_rating = models.IntegerField(blank=True,null=True)
    teacher_rating = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.course.title + " - " + self.student.user.first_name
