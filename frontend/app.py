import os
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://hack-fte-54z9.onrender.com"
)

st.set_page_config(
    page_title="Prospect Research Agent",
    layout="wide"
)

# =====================================
# HEADER
# =====================================

st.title("🏆 Prospect Research Agent")

st.write(
    "Add one or more companies and enrich them using AI."
)

st.divider()

# =====================================
# ENRICH SECTION
# =====================================

st.subheader("🚀 Enrich Companies")

if "company_count" not in st.session_state:
    st.session_state.company_count = 1

for i in range(st.session_state.company_count):

    st.markdown(f"### Company {i + 1}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.text_input(
            "Website Name",
            key=f"name_{i}",
            placeholder="OpenAI"
        )

    with col2:
        st.text_input(
            "Company URL",
            key=f"url_{i}",
            placeholder="https://openai.com"
        )

st.write("")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "➕ Add Company",
        use_container_width=True
    ):
        st.session_state.company_count += 1
        st.rerun()

with col2:

    if st.session_state.company_count > 1:

        if st.button(
            "➖ Remove Company",
            use_container_width=True
        ):
            st.session_state.company_count -= 1
            st.rerun()

st.write("")

enrich_button = st.button(
    "🚀 Enrich All Companies",
    use_container_width=True
)

# =====================================
# ENRICH LOGIC
# =====================================

if enrich_button:

    companies = []

    for i in range(st.session_state.company_count):

        website_name = st.session_state.get(
            f"name_{i}",
            ""
        ).strip()

        company_url = st.session_state.get(
            f"url_{i}",
            ""
        ).strip()

        if website_name and company_url:

            companies.append({
                "website_name": website_name,
                "url": company_url
            })

    if not companies:

        st.error(
            "Please add at least one company."
        )

    else:

        results = []

        with st.spinner(
            "Processing companies..."
        ):

            for company in companies:

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/enrich",
                        json=company,
                        timeout=120
                    )

                    response.raise_for_status()

                    results.append(
                        response.json()
                    )

                except Exception as e:

                    results.append({
                        "website_name":
                            company["website_name"],
                        "error": str(e)
                    })

        st.success(
            f"Successfully processed {len(results)} companies"
        )

        st.subheader(
            "Enrichment Results"
        )

        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True
        )

st.divider()

# =====================================
# RESULTS SECTION
# =====================================

st.subheader("📊 Results")

show_results = st.button(
    "Show All Results",
    use_container_width=True
)

if show_results:

    try:

        with st.spinner(
            "Loading results..."
        ):

            response = requests.get(
                f"{API_BASE_URL}/results",
                timeout=60
            )

            response.raise_for_status()

            results = response.json()

        if not results:

            st.info(
                "No company profiles found."
            )

        else:

            df = pd.DataFrame(results)

            st.dataframe(
                df,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            "Failed to load results."
        )

        st.write(e)