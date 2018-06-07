from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Source(models.Model):
    STATUS = (
        (0, 'ERROR'),
        (1, 'PASSED'),
    )
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=50)
    gitrepo = models.CharField(max_length=100, null=True)
    lastcontrol = models.DateTimeField(null=True)
    status = models.BooleanField(choices=STATUS)
    build_version = models.CharField(max_length=20, null=True)
    internal_teamcity_build = models.IntegerField(null=True)
    on_revision = models.BooleanField()

    def __str__(self):
        return self.name

class Client(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)

class Server(models.Model):
    SERVER_TYPES = (
        ('CLIENT','CLIENT'),
        ('OWN','OWN'),
        ('OTHER','OTHER'),
    )
    server_code = models.CharField(max_length=20, unique=True, db_index=True)
    server_type = models.CharField(max_length=10, choices=SERVER_TYPES)
    server_name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, validators=[URLValidator()])

    def __str__(self):
        return self.server_name

class Target(models.Model):
    TARGET_TYPE = (
        (0, 'QA'),
        (1, 'Canary'),
        (2, 'Normal'),
    )
    client_code = models.ForeignKey(Client, on_delete=models.CASCADE)
    server_code = models.ForeignKey(Server, on_delete=models.CASCADE)
    target_name = models.CharField(max_length=50, db_index=True)
    sources_group = models.ManyToManyField(Source, through='SourcesTargets')
    url_target = models.CharField(max_length=100, validators=[URLValidator()])
    target_type = models.IntegerField(choices=TARGET_TYPE, default=2)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.target_name

class SourcesTargets(models.Model):
    target_id = models.ForeignKey(Target, on_delete=models.CASCADE)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    source_build_version = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return str(self.target_id) +':'+ str(self.source_id)  +':'+ str(self.last_update)  +':'+ str(self.source_build_version)

class Update(models.Model):
    UPDATE_STATUS = (
        (0, 'QA'),
        (1, 'Canary'),
        (2, 'Deploy'),
    )
    source_code = models.CharField(max_length=20, db_index=True)
    create_datetime = models.DateTimeField()
    source_build_version = models.CharField(max_length=20)
    source_build = models.FileField(upload_to='builds/%Y/')
    stage = models.IntegerField(choices=UPDATE_STATUS, default=0)
    closed = models.BooleanField()
    next_stage_datetime_set = models.DateTimeField()
    internal_teamcity_build = models.IntegerField(default=0)
    scriptdir_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.source_code +' : '+ self.source_build_version  +' : '+ str(self.create_datetime)  +' : '+ str(self.stage)


class DeployHistory(models.Model):
    HISTORY_STATUS = (
        (0, 'FAIL'),
        (1, 'SUCCESS'),
        (2, 'UNKNOWN'),
    )
    date = models.DateField()
    time = models.TimeField()
    target_id = models.ForeignKey(Target, on_delete=models.CASCADE)
    status = models.IntegerField(choices=HISTORY_STATUS)

    def __str__(self):
        return str(self.date)  +':'+ str(self.time)  +':'+ str(self.target_id)