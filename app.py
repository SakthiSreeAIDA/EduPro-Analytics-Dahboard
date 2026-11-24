import pandas as pd
import matplotlib.pyplot as plt

# Read CSV files
users = pd.read_csv("data/Users.csv", sep="\t")
courses = pd.read_csv("data/Courses.csv", sep="\t")
transactions = pd.read_csv("data/Transaction.csv", sep="\t")
teachers = pd.read_csv("data/Teachers.csv", sep="\t")

# Remove duplicates
users = users.drop_duplicates()
courses = courses.drop_duplicates()
transactions = transactions.drop_duplicates()
teachers = teachers.drop_duplicates()

# Merge datasets
merged_data = transactions.merge(users, on="UserID")
merged_data = merged_data.merge(courses, on="CourseID")
bins = [0, 18, 25, 35, 45, 100]
labels = ['<18', '18-25', '26-35', '36-45', '45+']

merged_data['AgeGroup'] = pd.cut(
    merged_data['Age'],
    bins=bins,
    labels=labels
)

print(merged_data['AgeGroup'].value_counts())

# Create Age Groups  ← ADD THIS HERE
bins = [0, 18, 25, 35, 45, 100]
labels = ['<18', '18-25', '26-35', '36-45', '45+']

merged_data['AgeGroup'] = pd.cut(
    merged_data['Age'],
    bins=bins,
    labels=labels
)

# Now analyze Age Groups
print(merged_data['AgeGroup'].value_counts())
print("\nGender Distribution")
print(merged_data['Gender'].value_counts())
print("\nCourse Category Distribution")
print(merged_data['CourseCategory'].value_counts())
print("\nCourse Level Distribution")
print(merged_data['CourseLevel'].value_counts())
print("\nAverage Courses Per Learner")
print(merged_data.groupby('UserID').size().mean())
print("\nAge Group vs Course Category")
print(pd.crosstab(merged_data['AgeGroup'], merged_data['CourseCategory']))
print("\nGender vs Course Level")
print(pd.crosstab(merged_data['Gender'], merged_data['CourseLevel']))

merged_data['AgeGroup'].value_counts().plot(kind='bar')
plt.title("Age Group Distribution")
plt.xlabel("Age Group")
plt.ylabel("Number of Enrollments")
plt.show()
plt.figure()
plt.figure()

merged_data['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title("Gender Distribution")
plt.ylabel("")
plt.show()
plt.figure()

merged_data['CourseCategory'].value_counts().plot(kind='bar')
plt.title("Course Category Distribution")
plt.xlabel("Course Category")
plt.ylabel("Number of Enrollments")
plt.show()
plt.figure()

merged_data['CourseLevel'].value_counts().plot(kind='bar')
plt.title("Course Level Distribution")
plt.xlabel("Course Level")
plt.ylabel("Number of Enrollments")
plt.show()
plt.figure()

pd.crosstab(
    merged_data['AgeGroup'],
    merged_data['CourseCategory']
).plot(kind='bar')

plt.title("Age Group vs Course Category")
plt.xlabel("Age Group")
plt.ylabel("Enrollments")
plt.show()
avg_courses = merged_data.groupby('UserID')['CourseID'].count().mean()

print("Average Courses per Learner:", avg_courses)
plt.figure()

merged_data['CourseName'].value_counts().head(10).plot(kind='bar')

plt.title("Top 10 Most Popular Courses")
plt.xlabel("Course Name")
plt.ylabel("Enrollments")
plt.xticks(rotation=45)
plt.show()

plt.figure()
pd.crosstab(
    merged_data['Gender'],
    merged_data['CourseLevel']
).plot(kind='bar')

plt.title("Gender vs Course Level")
plt.xlabel("")
plt.figure()

merged_data['CourseCategory'].value_counts().plot(kind='bar')

plt.title("Course Category Distribution")
plt.xlabel("Course Category")
plt.ylabel("Number of Enrollments")
plt.show()
plt.figure()

merged_data['CourseLevel'].value_counts().plot(kind='bar')

plt.title("Course Level Distribution")
plt.xlabel("Course Level")
plt.ylabel("Number of Enrollments")
plt.show()
average_courses = merged_data.groupby('UserID')['CourseID'].count().mean()

print("Average Courses per Learner:", average_courses)
plt.figure()

merged_data['CourseName'].value_counts().head(10).plot(kind='bar')

plt.title("Top 10 Most Popular Courses")
plt.xlabel("Course Name")
plt.ylabel("Number of Enrollments")
plt.xticks(rotation=45)

plt.show()