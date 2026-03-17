import streamlit as st
import pandas as pd
from database import logs_collection


def admin_panel():

    st.title("⚙ Admin Control Panel")

    st.subheader("📜 Activity Logs")

    try:

        logs_data = list(logs_collection.find())
        logs = pd.DataFrame(logs_data)

        if "_id" in logs.columns:
            logs = logs.drop("_id", axis=1)

        # ------------------------------
        # SEARCH FILTER
        # ------------------------------
        st.subheader("🔍 Filter Logs")

        user_filter = st.selectbox(
            "Filter by User",
            ["All"] + list(logs["user"].unique())
        )

        if user_filter != "All":
            logs = logs[logs["user"] == user_filter]

        # ------------------------------
        # SHOW TABLE
        # ------------------------------
        st.subheader("📄 Log Records")

        st.dataframe(logs, use_container_width=True)

        # ------------------------------
        # SYSTEM METRICS
        # ------------------------------
        st.subheader("📊 System Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Actions", len(logs))
        c2.metric("Unique Users", logs["user"].nunique())
        c3.metric("Total Log Records", len(logs))

        # ------------------------------
        # USER ACTIVITY CHART
        # ------------------------------
        st.subheader("📊 User Activity Summary")

        user_counts = logs["user"].value_counts()

        st.bar_chart(user_counts)

        # ------------------------------
        # ACTION CHART
        # ------------------------------
        st.subheader("📈 System Actions")

        action_counts = logs["action"].value_counts()

        st.bar_chart(action_counts)

        # ------------------------------
        # RECENT ACTIVITY
        # ------------------------------
        st.subheader("🕒 Recent Activity")

        recent = logs.tail(5)

        st.table(recent)

        # ------------------------------
        # DOWNLOAD LOGS
        # ------------------------------
        st.subheader("⬇ Export Logs")

        st.download_button(
            "Download Logs CSV",
            logs.to_csv(index=False),
            "activity_logs.csv",
            "text/csv"
        )

        if st.button("🔄 Refresh Logs"):
            st.rerun()

    except:
        st.warning("⚠ No activity logs found yet.")