import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analysis import generate_insights


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="📊",
    layout="wide"
)


# -------------------- PURPLE THEME --------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f8f5ff, #eee7ff);
}

[data-testid="stSidebar"] {
    background-color: #e9ddff;
}

h1, h2, h3 {
    color: #51247a;
}

.stMetric {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e0d2ff;
    box-shadow: 0 3px 10px rgba(80, 40, 120, 0.08);
}

.stButton > button {
    background-color: #7541a6;
    color: white;
    border-radius: 8px;
}

[data-testid="stExpander"] {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #e0d2ff;
}

</style>
""", unsafe_allow_html=True)


# -------------------- PAGE TITLE --------------------

st.markdown("""
<div style="
    background: linear-gradient(90deg, #51247a, #9564c5);
    padding: 25px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
">
    <h1 style="color:white; margin:0;">
        📊 EduPro Analytics Dashboard
    </h1>
    <p style="color:#f0e6ff; margin:8px 0 0 0;">
        Learner Demographics and Course Enrollment Behavior Analysis
    </p>
</div>
""", unsafe_allow_html=True)


# -------------------- READ CSV FILES --------------------

import os

base_path = os.path.dirname(os.path.abspath(__file__))

users = pd.read_csv(
    os.path.join(base_path, "Users.csv"),
    sep="\t"
)

courses = pd.read_csv(
    os.path.join(base_path, "Courses.csv"),
    sep="\t"
)

transactions = pd.read_csv(
    os.path.join(base_path, "Transaction.csv"),
    sep="\t"
)
# -------------------- MERGE DATASETS --------------------

data = transactions.merge(users, on="UserID")
data = data.merge(courses, on="CourseID")


# -------------------- DATA PREPROCESSING --------------------

data["TransactionDate"] = pd.to_datetime(
    data["TransactionDate"],
    errors="coerce"
)

bins = [0, 18, 25, 35, 45, 100]

labels = [
    "<18",
    "18-25",
    "26-35",
    "36-45",
    "45+"
]

data["AgeGroup"] = pd.cut(
    data["Age"],
    bins=bins,
    labels=labels
)


# -------------------- SIDEBAR --------------------

st.sidebar.markdown("""
<div style="text-align:center; padding:20px 5px;">
    <h2 style="color:#51247a;">📊 EduPro</h2>
    <p style="color:#7541a6; font-size:14px;">
        Learning Analytics Platform
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard Overview",
        "👥 Learner Analysis",
        "📚 Course Analysis",
        "✨ AI Insights",
        "📥 Download",
        "🎯 Conclusion"
    ]
)


# -------------------- SIDEBAR FILTERS --------------------

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Apply Filters")

filtered_data = data.copy()

# Age Filter

age_options = ["All"] + sorted(
    data["AgeGroup"].dropna().astype(str).unique().tolist()
)

age = st.sidebar.selectbox(
    "Select Age Group",
    age_options
)

# Gender Filter

gender_options = ["All"] + sorted(
    data["Gender"].dropna().unique().tolist()
)

gender = st.sidebar.selectbox(
    "Select Gender",
    gender_options
)

# Course Category Filter

category_options = ["All"] + sorted(
    data["CourseCategory"].dropna().unique().tolist()
)

category = st.sidebar.selectbox(
    "Select Course Category",
    category_options
)

# Course Level Filter

level_options = ["All"] + sorted(
    data["CourseLevel"].dropna().unique().tolist()
)

level = st.sidebar.selectbox(
    "Select Course Level",
    level_options
)

# Date Filter

valid_dates = data["TransactionDate"].dropna()

if not valid_dates.empty:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "Select Transaction Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:
    selected_dates = (None, None)


# -------------------- APPLY FILTERS --------------------

if age != "All":
    filtered_data = filtered_data[
        filtered_data["AgeGroup"].astype(str) == age
    ]

if gender != "All":
    filtered_data = filtered_data[
        filtered_data["Gender"] == gender
    ]

if category != "All":
    filtered_data = filtered_data[
        filtered_data["CourseCategory"] == category
    ]

if level != "All":
    filtered_data = filtered_data[
        filtered_data["CourseLevel"] == level
    ]

if (
    isinstance(selected_dates, (tuple, list))
    and len(selected_dates) == 2
    and selected_dates[0] is not None
    and selected_dates[1] is not None
):

    start_date, end_date = selected_dates

    filtered_data = filtered_data[
        (filtered_data["TransactionDate"].dt.date >= start_date)
        & (filtered_data["TransactionDate"].dt.date <= end_date)
    ]


# -------------------- DASHBOARD OVERVIEW --------------------

if page == "📊 Dashboard Overview":

    st.subheader("📊 Dashboard Overview")

    st.subheader("📌 Dashboard Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👨‍🎓 Total Enrollments",
        len(filtered_data)
    )

    col2.metric(
        "📚 Total Learners",
        filtered_data["UserID"].nunique()
    )

    col3.metric(
        "📖 Total Courses",
        filtered_data["CourseID"].nunique()
    )

    if not filtered_data.empty:

        st.markdown("---")
        st.subheader("👥 Age Group Distribution")

        fig, ax = plt.subplots(figsize=(9, 5))

        age_counts = (
            filtered_data["AgeGroup"]
            .astype(str)
            .value_counts()
            .reindex(labels, fill_value=0)
        )

        age_counts.plot(
            kind="bar",
            ax=ax,
            color="#8054B8",
            edgecolor="#51247A",
            width=0.6
        )

        ax.set_xlabel("Age Group")
        ax.set_ylabel("Enrollments")
        ax.set_title("Learner Age Group Distribution")

        ax.set_facecolor("#FAF7FF")
        fig.patch.set_facecolor("#FAF7FF")

        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.xticks(rotation=0)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No data available for the selected filters.")


# -------------------- LEARNER ANALYSIS --------------------

elif page == "👥 Learner Analysis":

    st.subheader("👥 Learner Analysis")

    if not filtered_data.empty:

        # Age Group Distribution

        st.markdown("---")
        st.subheader("Age Group Distribution")

        age_counts = (
            filtered_data["AgeGroup"]
            .astype(str)
            .value_counts()
            .reindex(labels, fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        age_counts.plot(
            kind="bar",
            ax=ax,
            color="#8054B8",
            edgecolor="#51247A"
        )

        ax.set_xlabel("Age Group")
        ax.set_ylabel("Enrollments")
        ax.set_title("Learner Age Group Distribution")

        ax.set_facecolor("#FAF7FF")
        fig.patch.set_facecolor("#FAF7FF")

        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        plt.xticks(rotation=0)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        # Gender Distribution

        st.markdown("---")
        st.subheader("⚧ Gender Distribution")

        gender_counts = filtered_data["Gender"].value_counts()

        if not gender_counts.empty:

            fig, ax = plt.subplots(figsize=(7, 5))

            gender_counts.plot(
                kind="pie",
                autopct="%1.1f%%",
                startangle=90,
                ax=ax,
                colors=["#8054B8", "#B99AE0", "#E0D2F5"],
                wedgeprops={
                    "edgecolor": "white",
                    "linewidth": 2
                }
            )

            ax.set_ylabel("")
            ax.set_title("Learner Gender Distribution")

            fig.patch.set_facecolor("#FAF7FF")
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

    else:
        st.info("No learner data available for the selected filters.")


# -------------------- COURSE ANALYSIS --------------------

elif page == "📚 Course Analysis":

    st.subheader("📚 Course Analysis")

    if not filtered_data.empty:

        # Course Category Distribution

        st.markdown("---")
        st.subheader("📚 Course Category Distribution")

        category_counts = filtered_data["CourseCategory"].value_counts()

        fig, ax = plt.subplots(figsize=(9, 5))

        category_counts.plot(
            kind="bar",
            ax=ax,
            color="#9564C5",
            edgecolor="#51247A"
        )

        ax.set_xlabel("Course Category")
        ax.set_ylabel("Enrollments")
        ax.set_title("Enrollment by Course Category")

        ax.set_facecolor("#FAF7FF")
        fig.patch.set_facecolor("#FAF7FF")

        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        # Course Level Distribution

        st.markdown("---")
        st.subheader("🎓 Course Level Distribution")

        level_counts = filtered_data["CourseLevel"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))

        level_counts.plot(
            kind="bar",
            ax=ax,
            color="#8054B8",
            edgecolor="#51247A"
        )

        ax.set_xlabel("Course Level")
        ax.set_ylabel("Enrollments")
        ax.set_title("Enrollment by Course Level")

        ax.set_facecolor("#FAF7FF")
        fig.patch.set_facecolor("#FAF7FF")

        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        plt.xticks(rotation=0)
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        # Top 10 Popular Courses

        st.markdown("---")
        st.subheader("🏆 Top 10 Popular Courses")

        top_courses = (
            filtered_data["CourseName"]
            .value_counts()
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(10, 6))

        top_courses.sort_values().plot(
            kind="barh",
            ax=ax,
            color="#9564C5",
            edgecolor="#51247A"
        )

        ax.set_xlabel("Number of Enrollments")
        ax.set_ylabel("Course Name")
        ax.set_title("Top 10 Most Popular Courses")

        ax.set_facecolor("#FAF7FF")
        fig.patch.set_facecolor("#FAF7FF")

        ax.grid(axis="x", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No course data available for the selected filters.")


# -------------------- AI INSIGHTS --------------------

elif page == "✨ AI Insights":

    st.markdown("---")

    st.header("✨ AI Insights")

    st.caption(
        "Data-driven insights and recommendations "
        "based on learner enrollment patterns."
    )

    if not filtered_data.empty:

        insights = generate_insights(filtered_data)

        with st.expander(
            "👥 Learner Demographic Insights",
            expanded=True
        ):

            if insights.get("Learner Demographic Insights"):
                for point in insights["Learner Demographic Insights"]:
                    st.write("•", point)
            else:
                st.info("No learner demographic insights available.")

        with st.expander("📚 Course Category Insights"):

            if insights.get("Course Category Insights"):
                for point in insights["Course Category Insights"]:
                    st.write("•", point)
            else:
                st.info("No course category insights available.")

        with st.expander("🏆 Popular Course Insights"):

            if insights.get("Popular Course Insights"):
                for point in insights["Popular Course Insights"]:
                    st.write("•", point)
            else:
                st.info("No popular course insights available.")

        with st.expander("💡 AI Recommendations"):

            if insights.get("AI Recommendations"):
                for point in insights["AI Recommendations"]:
                    st.write("•", point)
            else:
                st.info("No recommendations available.")

    else:
        st.info("No data available to generate AI Insights.")


# -------------------- DOWNLOAD --------------------

elif page == "📥 Download":

    st.markdown("---")

    st.header("📥 Download Filtered Data")

    st.write(
        "Download the dataset based on your selected sidebar filters."
    )

    st.metric(
        "Total Filtered Records",
        len(filtered_data)
    )

    if not filtered_data.empty:

        csv = filtered_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="edupro_filtered_data.csv",
            mime="text/csv"
        )

    else:
        st.info("No records available to download.")


# -------------------- CONCLUSION --------------------

elif page == "🎯 Conclusion":

    st.markdown("---")

    st.header("🎯 Conclusion")

    st.write("""
    This dashboard provides insights into learner demographics and
    course enrollment behavior on the EduPro platform.

    It helps identify popular course categories, learner age groups,
    gender participation, and enrollment patterns.

    The AI Insights section generates dataset-based recommendations
    to support better course planning and enrollment decisions.

    By using data analysis and visualization, EduPro helps transform
    enrollment records into meaningful information for better
    educational decision-making.
    """)


# -------------------- FOOTER --------------------

st.markdown("---")

st.markdown("""
<div style="
    text-align: center;
    padding: 20px;
    background: #eee7ff;
    border-radius: 12px;
">
    <h4 style="color: #51247a; margin-bottom: 5px;">
        📊 EduPro Analytics Dashboard
    </h4>
    <p style="color: #7541a6; margin: 0;">
        Developed by Sakthi Sree
    </p>
    <p style="color: #7541a6; font-size: 13px;">
        Unified Mentor Data Analytics Internship Project
    </p>
</div>

""", unsafe_allow_html=True)
