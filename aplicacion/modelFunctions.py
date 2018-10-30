import os, time, datetime
def upload_profile_pic_to(instance,filename):
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    ext = filename.split('.')[-1]
    filename = '{}/{}.{}'.format(instance.pk, ts, ext)
    return os.path.join('profile_pics', filename)

