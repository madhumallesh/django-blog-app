from time import sleep
from django.core.management.base import BaseCommand
from faker import Faker, providers

from django.contrib.auth.models import User
from blog.models import Posts, Comments, Tags

TAGS = Tags.objects.all()

IMAGES = [
    "01.jpg",
    "02.jpg",
    "03.jpg",
    "04.jpg",
    "05.jpg",
    "06.jpg",
    "07.jpg",
    "08.jpg",
    "09.jpg",
    "10.jpg",
    "11.jpg",
    "12.jpg",
    "13.jpg",
]

STATUS = ["Publish", "Private", "Draft"]

USERS = User.objects.all()

BLOGS = Posts.objects.filter(Status="Publish").order_by("-created_date").all()


class Provider(providers.BaseProvider):
    def blog_tags(self):
        return self.random_element(TAGS)

    def blog_image(self):
        return f"blogs/{self.random_element(IMAGES)}"

    def blog_user(self):
        return self.random_element(USERS)

    def ran_blog(self):
        return self.random_element(BLOGS)

    def blog_status(self):
        return self.random_element(STATUS)


class Command(BaseCommand):
    help: str = "create data to the models"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--n", type=int, help="no of data", default=1)
        parser.add_argument("--comment", action="store_true", help="create Comments")
        parser.add_argument("--post", action="store_true", help="create Posts")
        parser.add_argument("--user", action="store_true", help="create Users")
        parser.add_argument("--tags", action="store_true", help="create tags")


    def handle(self, *args, **options):
        fake = Faker("en_US")
        fake.add_provider(Provider)

        # create Users
        if options["user"]:
            for _ in range(0, options["n"]):
                User.objects.create_user(
                    username=fake.unique.name(),
                    email=fake.unique.email(),
                    password=fake.password(),
                )

        # create blog tags
        if options["tags"]:
            for i in ["Travel", "Comedy", "Business", "Entertainment", "Technology", "News", "Social"]:
                Tags.objects.create(tagname = i)

        # create Comments latest 10 blogs
        if options["comment"]:
            for _ in range(0, options["n"]):
                Comments.objects.create(
                    name=fake.name(),
                    email=fake.email(),
                    comment=fake.sentence(),
                    blog=fake.ran_blog(),
                )

        # create posts
        if options["post"]:
            for _ in range(0, options["n"]):
                # sleep(3)
                Posts.objects.create(
                    author=fake.blog_user(),
                    title=fake.unique.sentence(nb_words=5),
                    post_image=fake.blog_image(),
                    content=f"""<p>{fake.text(max_nb_chars=160)} </p> 
                    <p>{fake.text(max_nb_chars=160)} </p> 
                    <p>{fake.text(max_nb_chars=160)} </p>
                    <p><u><em><strong> {fake.word()} </strong></em></u></p>
                    <p>{fake.text(max_nb_chars=160)} </p>
                    <a href="{fake.url()}">{fake.unique.sentence(nb_words=5)}</a>
                    <p>{fake.text(max_nb_chars=160)} </p>
                    <p>{fake.text(max_nb_chars=160)} </p>
                    <p>{fake.text(max_nb_chars=160)} </p>
                    <p style="text-align:center"><span style="font-family:Georgia,serif"><strong><span style="font-size:18px">THANK YOU...</span></strong></span></p>
                    """,
                    tag=fake.blog_tags().tagname,
                    Status=fake.blog_status(),
                    created_date=fake.date(),
                )

        print("Totol Users : ", User.objects.count())
        print("Totol Posts : ", Posts.objects.count())
        print("Total Comments : ", Comments.objects.count())
