from django.db import models
from django.utils import timezone



class Post(models.Model):
    """docstring for Post: Project"""
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {"pk": str(self.pk)})

class Item(models.Model):
    """docstring for Item: Each item of a project"""
    post = models.ForeignKey(Post)
    author = models.ForeignKey('auth.User')
    abstract = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    #note = models.TextField(blank=True, null=True)
    #status=False=todo; status=True=done
    status = models.BooleanField(default=False)
    added_date = models.DateTimeField(
            default=timezone.now)
    done_date = models.DateTimeField(
            blank=True, null=True)
    def done(self):
        self.done_date = timezone.now()
        self.save()
    def __unicode__(self):
        return self.abstract + " (" + str(self.post) + ")"


    
        