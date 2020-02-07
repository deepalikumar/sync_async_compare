from flask.cli import AppGroup
from faker import Faker

from app import db
from blog.models import User, Post, Comment, Category, PostCategory


data_cli = AppGroup("data")
fake = Faker()
Faker.seed(4321234)


@data_cli.command("seed")
def seed():
    """Seeds test data"""
    PostCategory.query.delete()
    Category.query.delete()
    Comment.query.delete()
    Post.query.delete()
    User.query.delete()

    programming = Category(name="programming")
    finance = Category(name="finance")
    travel = Category(name="travel")
    general = Category(name="general")
    categories = [programming, finance, travel, general]

    comments = []
    for _ in range(1000):
        comments.append(
            Comment(
                commenter=fake.user_name(),
                comment=fake.sentence(nb_words=30, variable_nb_words=True),
            )
        )

    for _ in range(100):
        user = User(username=fake.user_name(), email=fake.email())
        for _ in range(100):
            post = Post(
                title=fake.bs(),
                body=fake.paragraph(nb_sentences=30, variable_nb_sentences=True),
            )
            post.comments = fake.random_elements(
                comments, length=fake.random_int(0, 100), unique=True
            )
            post.categories = fake.random_elements(
                categories, length=fake.random_int(1, 4), unique=True
            )
            user.posts.append(post)
        db.session.add(user)

    db.session.commit()
    db.session.close_all()
