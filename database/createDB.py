import os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QByteArray


def createConnection(log):
    """
    Создает подключение к users.sqlite базе
    """
    # Create the connection
    con = QSqlDatabase.addDatabase("QSQLITE")
    pathToTemp = "../database/"
    if not os.path.exists(pathToTemp):
        os.makedirs(pathToTemp)
    con.setDatabaseName(pathToTemp + "users.sqlite")

    # Try to open the connection and handle possible errors
    if not con.open():
        log.appendPlainText("Database Error: %s" % con.lastError().databaseText())
        return con

    log.appendPlainText("Connection Successfuly Opened!")
    return con


def createTable(con, log):
    """
    Создает таблицу по подключению
    :param con: текущие подключение к нашей базе
    :return: QLabel оповещение пользователя
    """
    if not con:
        log.appendPlainText("Database Error: %s" % con.lastError().databaseText())
        return
    createTableQuery = QSqlQuery(con)
    createTableQuery.exec(
    """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            averagePulse VARCHAR(50),
            image BLOB NOT NULL
        )
        """
    )
    log.appendPlainText("Table Successfully Created!")
    return


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def getAllInfo(con):
    """
    Возвращает список содержащий все изображения из бд в бинарном виде.
    """
    if not con and not con.open:
        return QLabel("Database Error: %s" % con.lastError().databaseText())
    query = QSqlQuery(con)
    query.prepare("""SELECT Users.name, Users.image FROM Users""")
    query.exec()
    info = {}
    while query.next():
        info[query.value(0)] = query.value(1)
    return info


def insertBLOB(con, name, averagePulse, bytesFrame):
    """

    :param con:
    :param name:
    :param photo:
    :return:
    """
    if not con and not con.open:
        return QLabel("Database Error: %s" % con.lastError().databaseText())
    query = QSqlQuery(con)
    image = QByteArray(bytesFrame)
    query.prepare(""" INSERT INTO Users
                              (name, averagePulse, image) VALUES (:name, :averagePulse, :image)"""
                  )

    query.bindValue(":name", name)
    query.bindValue(":averagePulse", averagePulse)
    query.bindValue(":image", image)
    query.exec()
    return QLabel("Image and file inserted successfully as a BLOB into a table")
