import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel


def createConnection(log):
    """
    Создает подключение к users.sqlite базе
    """
    # Create the connection
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("users.sqlite")

    # Try to open the connection and handle possible errors
    if not con.open():
        log.appendPlainText("Database Error: %s" % con.lastError().databaseText())
        return con

    # Create the application's window
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
    createTableQuery = QSqlQuery()
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


def insertBLOB(con, name, averagePulse, bytesFrame):
    """

    :param con:
    :param name:
    :param photo:
    :return:
    """
    if not con:
        return QLabel("Database Error: %s" % con.lastError().databaseText())
    cursor = con.cursor()
    # insert query
    sqlite_insert_blob_query = """ INSERT INTO Users
                              (name, averagePulse, image) VALUES (?, ?, ?)"""

    data_tuple = (name, averagePulse, bytesFrame)

    # using cursor object executing our query
    cursor.execute(sqlite_insert_blob_query, data_tuple)
    con.commit()
    cursor.close()
    return QLabel("Image and file inserted successfully as a BLOB into a table")
