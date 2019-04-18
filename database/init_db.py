import os

from dotenv import load_dotenv, find_dotenv
from pymysql import connect

load_dotenv(find_dotenv())

USER = os.getenv('USER')
PASSWORD = os.getenv('ROOT_PASSWORD')
SERVER_HOST = os.getenv('MYSQL_SERVER_HOST')
SERVER_HOST = 'localhost'


def create_database(csr):
    csr.execute('CREATE DATABASE demo; ')


def use_databse(csr):
    csr.execute('use demo;')


def create_table(csr):
    create_user = """
        CREATE TABLE user (
        ID INTEGER AUTO_INCREMENT PRIMARY KEY,
        Name TEXT NOT NULL);
    """

    create_account = """
        CREATE TABLE account (
        ID INTEGER AUTO_INCREMENT PRIMARY KEY,
        User_ID INT NOT NULL,
        Balance INT NOT NULL DEFAULT 0,
        FOREIGN KEY (User_ID) REFERENCES user (ID));
    """

    csr.execute(create_user)
    csr.execute(create_account)


if __name__ == "__main__":
    ctx = connect(user=USER, password=PASSWORD)
    cursor = ctx.cursor()

    create_database(cursor)
    use_databse(cursor)

    create_table(cursor)

    ctx.commit()
