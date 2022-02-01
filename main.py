import csv
import json

def json_tool(studentsFile, marksFile, testsFile, coursesFile, jsonFile):
     
    data = {
        "students": []
    }
    scores = []
    students_list = []
    courses_list = []
    courses = []
     
    with open(studentsFile, encoding='utf-8') as csvS:
        csvReader = csv.DictReader(csvS)
         
        for rows in csvReader:
            rows['totalAverage'] = 0
            rows['courses'] = []
            data['students'].append(rows)

    with open(coursesFile, encoding='utf-8') as csvC:
        csvReader = csv.DictReader(csvC)
         
        for rows in csvReader:
            courses_list.append(rows['id'])
            courses.append(rows)
            
    with open(marksFile, encoding='utf-8') as csvM:
        csvReaderM = csv.DictReader(csvM)
        
        for rows in csvReaderM:
            with open(testsFile, encoding='utf-8') as csvT:
                csvReaderT = csv.DictReader(csvT)
                for row in csvReaderT:
                    if rows['test_id'] == row['id']:
                        rows['course_id'] = row['course_id']
                        rows['mark'] = int(rows['mark']) * int(row['weight']) / 100
                        scores.append(rows)
            key = rows['student_id']
            students_list.append(key)

    student_set = set(students_list)
    summary = {}
     
    for i in student_set:
        result = {}
        for j in courses_list:
            tally = 0
            for d in scores:
                if i == d['student_id'] and j == d['course_id']:
                    tally += float(d['mark'])
            if tally > 0:
                result[j] = round(tally, 1)
            summary[i] = result        

    for i in data['students']:
        for x, y in summary.items():
            if i['id'] == x:
                total = 0
                for j in y:
                    total += y[j]
                    n = ''
                    t = ''
                    for k in courses:
                        if j == k['id']:
                            n += k['name']
                            t += k['teacher']
                    s = { 'id': j, 'name': n, 'teacher': t, 'courseAverage': y[j] }
                    i['courses'].append(s)
                i['totalAverage'] = round(total / len(y), 2)

    json_object = json.dumps(data, indent = 4)
    
    with open("results.json", "w") as jsonFile:
        jsonFile.write(json_object)

studentsFile = r'students.csv'
marksFile = r'marks.csv'
testsFile = r'tests.csv'
coursesFile = r'courses.csv'
jsonFile = r'results.json'

json_tool(studentsFile, marksFile, testsFile, coursesFile, jsonFile)
