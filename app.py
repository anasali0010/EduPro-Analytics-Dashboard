
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EduPro Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------

excel_file = "EduPro Online Platform.xlsx"

users = pd.read_excel(excel_file, sheet_name="Users")
courses = pd.read_excel(excel_file, sheet_name="Courses")
transactions = pd.read_excel(excel_file, sheet_name="Transactions")

# Merge Data
merged = transactions.merge(users, on="UserID")
merged = merged.merge(courses, on="CourseID")

# Age Groups
merged["AgeGroup"] = pd.cut(
    merged["Age"],
    bins=[0,18,25,35,45,100],
    labels=["<18","18-25","26-35","36-45","45+"]
)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    merged["Gender"].unique(),
    default=merged["Gender"].unique()
)

selected_level = st.sidebar.multiselect(
    "Select Course Level",
    merged["CourseLevel"].unique(),
    default=merged["CourseLevel"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Course Category",
    merged["CourseCategory"].unique(),
    default=merged["CourseCategory"].unique()
)

filtered = merged[
    (merged["Gender"].isin(selected_gender)) &
    (merged["CourseLevel"].isin(selected_level)) &
    (merged["CourseCategory"].isin(selected_category))
]

# -------------------------
# TITLE
# -------------------------

st.title("🎓 EduPro Analytics Dashboard")
st.markdown("Learner Demographics and Course Enrollment Behavior Analysis")

# -------------------------
# KPI SECTION
# -------------------------

total_enrollments = len(filtered)

total_learners = filtered["UserID"].nunique()

if total_learners == 0:
    avg_courses = 0
else:
    avg_courses = round(total_enrollments / total_learners, 2)

if filtered.empty:
    popular_category = "-"
else:
    popular_category = (
        filtered["CourseCategory"]
        .value_counts()
        .idxmax()
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Enrollments", total_enrollments)
col2.metric("Total Learners", total_learners)
col3.metric("Avg Courses / Learner", avg_courses)
col4.metric("Top Category", popular_category)

st.divider()

st.subheader("📌 Key Insights")


st.markdown("""

- Most learners belong to the **26–35** age group.

- **Data Science** is the most popular course category.

- Learners enroll in approximately **3.33 courses** on average.

- Beginner and Advanced courses have similar enrollment counts.

""")

st.write(f"Showing **{len(filtered)}** records after applying filters.")

st.subheader("Filtered Dataset Preview")

st.dataframe(
    filtered[
        [
            "Age",
            "Gender",
            "CourseCategory",
            "CourseLevel",
            "CourseName"
        ]
    ],
    use_container_width=True,
    height=350
    
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)
st.header("📊 Visual Analytics")

# ---------------- FIRST ROW ----------------

col1, col2 = st.columns(2)

# Gender
with col1:

    st.subheader("Gender Distribution")

    gender_count = filtered["Gender"].value_counts()

    fig, ax = plt.subplots(figsize=(5,4))

    gender_count.plot(kind="bar", ax=ax)

    for container in ax.containers:
     ax.bar_label(container)

    plt.xticks(rotation=0)

    ax.set_xlabel("Gender")
    ax.set_ylabel("Enrollments")
    
    st.pyplot(fig)
    plt.tight_layout()


# Age Group
with col2:

    st.subheader("Age Group Distribution")

    age_count = filtered["AgeGroup"].value_counts()

    fig, ax = plt.subplots(figsize=(5,4))

    age_count.plot(kind="bar", ax=ax)

    for container in ax.containers:
     ax.bar_label(container)

    plt.xticks(rotation=45)

    ax.set_xlabel("Age Group")
    ax.set_ylabel("Enrollments")

    st.pyplot(fig)
    plt.tight_layout()


# ---------------- SECOND ROW ----------------

col3, col4 = st.columns(2)

# Course Category
with col3:

    st.subheader("Top 10 Course Categories")

    category_count = (
        filtered["CourseCategory"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(7,5))

    category_count.plot(kind="barh", ax=ax)

    for container in ax.containers:
     ax.bar_label(container)
    
    ax.set_xlabel("Enrollments")
    ax.set_ylabel("Category")
    st.pyplot(fig)
    plt.tight_layout()

# Course Level
with col4:

    st.subheader("Course Level Popularity")

    level_count = filtered["CourseLevel"].value_counts()

    fig, ax = plt.subplots(figsize=(5,4))

    level_count.plot(kind="bar", ax=ax)

    for container in ax.containers:
     ax.bar_label(container)
    
    plt.xticks(rotation=0)

    ax.set_xlabel("Course Level")
    ax.set_ylabel("Enrollments")
    st.pyplot(fig)
    plt.tight_layout()
    
st.divider()

st.caption(
    "EduPro Analytics Dashboard | Developed using Python, Pandas, Matplotlib and Streamlit"
)