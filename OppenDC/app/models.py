from django.db import models

# Create your models here.

class Source(models.Model):
    STATUS = (
        (0, 'PASSED'),
        (1, 'ERROR'),
    )
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    gitrepo = models.CharField(max_length=100)
    lastcontrol = models.DateTimeField()
    status = models.BooleanField(choices=STATUS)
    build_version = models.CharField(max_length=20)
    on_revision = models.BooleanField()

    def __str__(self):
        return self.name

class Client(models.Model):
    client_name = models.CharField(max_length=50)

class Server(models.Model):
    SERVER_TYPES = (
        ('CLIENT','CLIENT'),
        ('OWN','OWN'),
        ('OTHER','OTHER'),
    )
    server_code = models.CharField(max_length=20)
    server_type = models.CharField(max_length=10, choices=SERVER_TYPES)
    server_name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.server_name

class Target(models.Model):
    client_code = models.ForeignKey(Client, on_delete=models.CASCADE)
    server_code = models.ForeignKey(Server, on_delete=models.CASCADE)
    target_name = models.CharField(max_length=50)
    sources_group = models.ManyToManyField(Source, through='SourcesTargets')
    url_target = models.CharField(max_length=100)
    
    def __str__(self):
        return self.target_name

class SourcesTargets(models.Model):
    target_id = models.ForeignKey(Target, on_delete=models.CASCADE)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    source_build_version = models.CharField(max_length=20)
    
    def __str__(self):
        return self.target_id +':'+ self.source_id  +':'+ self.last_update  +':'+ self.source_build_version

class DeployHistory(models.Model):
    HISTORY_STATUS = (
        (0, 'SUCCESS'),
        (1, 'FAIL'),
        (2, 'UNKNOWN'),
    )
    date = models.DateField()
    time = models.TimeField()
    target_id = models.ForeignKey(Target, on_delete=models.CASCADE)
    status = models.IntegerField(choices=HISTORY_STATUS)

    def __str__(self):
        return self.date  +':'+ self.time  +':'+ self.target_id