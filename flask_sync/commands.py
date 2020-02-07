import click
from flask.cli import AppGroup
from faker import Faker

from .app import db
from .blog import User, Post, Comment, Category


data_cli = AppGroup("data")
fake = Faker()
Faker.seed(4321234)


@data_cli.command("seed")
def seed():
    """Seeds test data"""
    Category.query.delete()
    programming = Category(name="programming")
    finance = Category(name="finance")
    travel = Category(name="travel")
    general = Category(name="general")
    categories = [programming, finance, travel, general]

    Comment.query.delete()
    comments = []
    for _ in range(1000):
        comments.append(
            Comment(
                commenter=fake.user_name(),
                comment=fake.sentence(nb_words=30, variable_nb_words=True),
            )
        )

    User.query.delete()
    for _ in range(10):
        user = User(username=fake.user_name(), email=fake.email())
        for _ in range(10):
            post = Post(
                title=fake.bs(),
                body=fake.paragraph(nb_sentences=30, variable_nb_sentences=True),
            )
            post.comments = fake.random_choices(
                comments, length=fake.random_int(min=0, max=100)
            )
            post.categories = fake.random_choices(
                categories, length=fake.random_int(1, 4)
            )
            user.posts.append(post)
        db.session.add(user)

    db.session.commit()
