# Goal of this script is to take the data from Scott Z's system and dump it into
# the local SQL DB

import pypyodbc
import csv


connection = pypyodbc.connect('Driver={SQL Server};'
                             'Server=.\SQLEXPRESS;'
                             'Database=cmprod-speakersdb')
cursor = connection.cursor()
#
# SQLCommand = ("SELECT * FROM dbo.Sessions WHERE Sessions.Accepted = 1")
# cursor.execute(SQLCommand)
# results = cursor.fetchone()
# while results:
#     print results[0]
#     results = cursor.fetchone()
#
# connection.close()

# open the csv and start processing

def valid_id(id):
    valid = True
    if id is '0':
        valid = False
    elif id.isalpha():
        valid = False
    elif len(id) > 5:
        valid = False
    return valid


def update_session_record(stat_row):
    # build the SQL Command
    sql = "UPDATE Sessions SET AttendeeCount1 = {0}, AttendeeCount2 = {1}, Attendees = {2}, " \
          "ActualStartTime = '{3}', ActualEndTime = '{4}', ProctorComments = '{5}' WHERE Id = {6}".format(
            int(stat_row[10]),
            int(stat_row[11]),
            ((int(stat_row[10]) + int(stat_row[11])) / 2),
            stat_row[8],
            stat_row[9],
            stat_row[12].replace("'", "''"),
            int(stat_row[0]))

    cursor.execute(sql)
    connection.commit()
    print 'Updated session {0}'.format(int(stat_row[0]))


with open('c:/Users/robgi/Downloads/download.csv', 'rb') as csv_file:
    stat_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in stat_reader:
        if valid_id(row[0]):
            update_session_record(row)

# clean up
if connection is not None:
    connection.close()
