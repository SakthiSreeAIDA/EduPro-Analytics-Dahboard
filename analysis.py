def generate_insights(filtered_data):

    insights = {
        "Learner Demographic Insights": [],
        "Course Category Insights": [],
        "Popular Course Insights": [],
        "AI Recommendations": []
    }

    # 1. Learner Demographics
    insights["Learner Demographic Insights"].append(
        f"Total enrollment records: {len(filtered_data)}."
    )

    if "Gender" in filtered_data.columns:
        gender = filtered_data["Gender"].value_counts()

        if not gender.empty:
            insights["Learner Demographic Insights"].append(
                f"Most represented gender: {gender.index[0]}."
            )

    # 2. Course Category Insights
    if "CourseCategory" in filtered_data.columns:

        category_counts = (
            filtered_data["CourseCategory"]
            .dropna()
            .value_counts()
            .sort_values(ascending=False)
        )

        if not category_counts.empty:

            most_popular = category_counts.index[0]
            least_popular = category_counts.index[-1]

            insights["Course Category Insights"].append(
                f"Most popular category: {most_popular} "
                f"({category_counts.iloc[0]} enrollments)."
            )

            insights["Course Category Insights"].append(
                f"Least popular category: {least_popular} "
                f"({category_counts.iloc[-1]} enrollments)."
            )

            insights["AI Recommendations"].append(
                f"Promote {least_popular} courses "
                "to improve enrollment."
            )

            insights["AI Recommendations"].append(
                f"Consider introducing related advanced courses "
                f"in {most_popular}."
            )

    # 3. Popular Course Insights
    if "CourseName" in filtered_data.columns:

        courses = filtered_data["CourseName"].dropna().value_counts()

        if not courses.empty:
            insights["Popular Course Insights"].append(
                f"Most enrolled course: {courses.index[0]} "
                f"({courses.iloc[0]} enrollments)."
            )

    # 4. General Recommendations
    insights["AI Recommendations"].append(
        "Introduce courses based on learner enrollment trends."
    )

    return insights