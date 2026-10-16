import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
      migrations.CreateModel(name="Profile", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("bio",models.CharField(blank=True,max_length=160)),("avatar",models.ImageField(blank=True,null=True,upload_to="avatars/")),("user",models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name="profile",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Post", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("image",models.ImageField(upload_to="posts/")),("caption",models.CharField(blank=True,max_length=2200)),("created_at",models.DateTimeField(auto_now_add=True)),("author",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="posts",to=settings.AUTH_USER_MODEL))], options={"ordering":["-created_at"]}),
      migrations.CreateModel(name="Follow", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),("followed",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="follower_links",to=settings.AUTH_USER_MODEL)),("follower",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="following_links",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Like", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("post",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="likes",to="social.post")),("user",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="likes",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Comment", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("text",models.CharField(max_length=500)),("created_at",models.DateTimeField(auto_now_add=True)),("post",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="comments",to="social.post")),("user",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="comments",to=settings.AUTH_USER_MODEL))], options={"ordering":["created_at"]}),
      migrations.AddConstraint(model_name="follow", constraint=models.UniqueConstraint(fields=("follower","followed"),name="unique_follow")),
      migrations.AddConstraint(model_name="like", constraint=models.UniqueConstraint(fields=("user","post"),name="unique_like")),
    ]
