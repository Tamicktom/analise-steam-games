"""
Módulo de configuração do banco de dados e modelos SQLAlchemy.

Este módulo contém:
- Configuração de conexão com o banco de dados PostgreSQL
- Definição de tabelas de associação (many-to-many)
- Definição de modelos ORM (Object-Relational Mapping)
- Sessão de banco de dados
"""

import os
import sqlalchemy
import sqlalchemy.orm as orm
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv()
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Verificar se todas as variáveis foram carregadas
required_vars = {
    "POSTGRES_HOST": POSTGRES_HOST,
    "POSTGRES_PORT": POSTGRES_PORT,
    "POSTGRES_USER": POSTGRES_USER,
    "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
    "POSTGRES_DB": POSTGRES_DB,
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

# URL de conexão com o banco de dados
DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Criar o motor de conexão com o banco de dados
engine = sqlalchemy.create_engine(DATABASE_URL)

# Base declarativa para os modelos
Base = orm.declarative_base()


# Tabelas de associação (many-to-many)
game_developer = sqlalchemy.Table(
    "game_developer",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("developer_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("developers.id"), primary_key=True)
)

game_publisher = sqlalchemy.Table(
    "game_publisher",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("publisher_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), primary_key=True)
)

game_category = sqlalchemy.Table(
    "game_category",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"), primary_key=True)
)

game_genre = sqlalchemy.Table(
    "game_genre",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("genre_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"), primary_key=True)
)

game_tag = sqlalchemy.Table(
    "game_tag",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("tag_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tags.id"), primary_key=True)
)

game_language = sqlalchemy.Table(
    "game_language",
    Base.metadata,
    sqlalchemy.Column("game_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), primary_key=True),
    sqlalchemy.Column("language_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("languages.id"), primary_key=True)
)


# Definição dos modelos
class Developer(Base):
    __tablename__ = "developers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    games = orm.relationship("Game", secondary=game_developer, back_populates="developers")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Publisher(Base):
    __tablename__ = "publishers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    games = orm.relationship("Game", secondary=game_publisher, back_populates="publishers")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Category(Base):
    __tablename__ = "categories"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    games = orm.relationship("Game", secondary=game_category, back_populates="categories")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Genre(Base):
    __tablename__ = "genres"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    games = orm.relationship("Game", secondary=game_genre, back_populates="genres")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Tag(Base):
    __tablename__ = "tags"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    games = orm.relationship("Game", secondary=game_tag, back_populates="tags")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Language(Base):
    __tablename__ = "languages"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    games = orm.relationship("Game", secondary=game_language, back_populates="languages")

    @classmethod
    def get_or_create(cls, name, session):
        parsed = name.strip().lower()
        obj = session.query(cls).filter_by(name=parsed).first()
        if obj:
            return obj
        obj = cls(name=parsed)
        session.add(obj)
        session.commit()
        return obj


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), nullable=False)
    screenshot_url = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)


class Movie(Base):
    __tablename__ = "movies"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id"), nullable=False)
    movie_url = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)


class Game(Base):
    __tablename__ = "games"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    app_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    release_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    estimated_owners_lower = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    estimated_owners_upper = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    peak_ccu = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    required_age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.0)
    discount = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0.0)
    dlc_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    about_the_game = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    header_image = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    website = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    support_url = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    support_email = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    windows = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    mac = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    linux = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    metacritic_score = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    metacritic_url = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    user_score = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    positive = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    negative = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    score_rank = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    achievements = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    recommendations = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    average_playtime_forever = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    average_playtime_2weeks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    median_playtime_forever = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    median_playtime_2weeks = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    # RELACIONAMENTOS M:N
    developers = orm.relationship("Developer", secondary=game_developer, back_populates="games")
    publishers = orm.relationship("Publisher", secondary=game_publisher, back_populates="games")
    categories = orm.relationship("Category", secondary=game_category, back_populates="games")
    genres = orm.relationship("Genre", secondary=game_genre, back_populates="games")
    tags = orm.relationship("Tag", secondary=game_tag, back_populates="games")
    languages = orm.relationship("Language", secondary=game_language, back_populates="games")


# Sessão para comunicação com banco
session = sqlalchemy.orm.Session(engine)


def test_connection():
    """Testa a conexão com o banco de dados."""
    try:
        with engine.connect() as connection:
            print("✅ Conexão com o banco de dados estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False
