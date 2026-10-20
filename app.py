from pathlib import Path
import dill
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
FEATURES = [
    "having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol",
    "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State",
    "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL",
    "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
    "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain",
    "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page",
    "Statistical_report",
]
LABELS = {
    "having_IP_Address": "IP address in URL", "URL_Length": "URL length", "Shortining_Service": "URL shortener",
    "having_At_Symbol": "@ symbol in URL", "double_slash_redirecting": "Double slash redirect",
    "Prefix_Suffix": "Hyphen in domain", "having_Sub_Domain": "Subdomains", "SSLfinal_State": "SSL certificate",
    "Domain_registeration_length": "Domain registration length", "Favicon": "External favicon",
    "port": "Nonstandard port", "HTTPS_token": "HTTPS token in domain", "Request_URL": "External resource requests",
    "URL_of_Anchor": "External links in anchors", "Links_in_tags": "External links in tags", "SFH": "Server form handler",
    "Submitting_to_email": "Form submits to email", "Abnormal_URL": "Abnormal URL", "Redirect": "Redirect count",
    "on_mouseover": "Mouseover behavior", "RightClick": "Right-click disabled", "popUpWidnow": "Popup window",
    "Iframe": "Iframe usage", "age_of_domain": "Domain age", "DNSRecord": "DNS record",
    "web_traffic": "Web traffic rank", "Page_Rank": "Page rank", "Google_Index": "Search engine indexed",
    "Links_pointing_to_page": "Links pointing to page", "Statistical_report": "Statistical report flag",
}
GROUPS = {
    "URL structure": FEATURES[:7], "Domain & connection": FEATURES[7:12],
    "Page behavior": FEATURES[12:23], "Reputation": FEATURES[23:],
}

st.set_page_config(page_title="Signal | Phishing intelligence", page_icon="🔒", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#eaf0ff; --muted:#8995ad; --panel:#111a2b; --line:#26344b; --mint:#54e0bd; --red:#ff657a; }
.stApp { background: radial-gradient(ellipse at 80% -10%, #173750 0, transparent 34%), #0a101b; color:var(--ink); font-family:'Manrope',sans-serif; }
[data-testid="stSidebar"] { background:#0e1726; border-right:1px solid var(--line); }
.block-container { max-width:1240px; padding-top:2.2rem; padding-bottom:4rem; }
h1,h2,h3 { letter-spacing:-.04em; color:var(--ink); }
.hero { padding:2.2rem 2.5rem; border:1px solid #293b54; border-radius:22px; background:linear-gradient(120deg,rgba(20,37,57,.96),rgba(13,24,39,.84)); margin-bottom:1.4rem; }
.eyebrow { color:var(--mint); font:500 11px 'DM Mono',monospace; letter-spacing:.16em; text-transform:uppercase; }
.hero h1 { font-size:clamp(2.3rem,5vw,4rem); line-height:1.05; margin:.65rem 0; }
.hero p { color:#a8b5c9; max-width:610px; font-size:1rem; margin:0; }
.metric { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:1rem 1.2rem; min-height:88px; }
.metric-label { color:var(--muted); font-size:.75rem; text-transform:uppercase; letter-spacing:.09em; }
.metric-value { color:var(--ink); font-weight:800; font-size:1.25rem; margin-top:.3rem; }
div[data-testid="stTabs"] button { color:#9eacc2; }
.stButton button[kind="primary"],button[kind="primary"] { background:#54e0bd; color:#07151a; border:0; border-radius:10px; font-weight:800; min-height:2.8rem; }
.stButton button { border-radius:10px; }
div[data-testid="stFileUploader"] { background:#111a2b; border:1px dashed #354862; border-radius:14px; padding:1rem; }
[data-testid="stMetric"] { background:#111a2b; border:1px solid #26344b; padding:1rem; border-radius:14px; }
div[data-testid="stAlert"] { border-radius:14px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_bundle(path_text):
    with open(path_text, "rb") as stream:
        return dill.load(stream)

def latest_model():
    candidates = list((ROOT / "Artifacts").glob("*/model_trainer/model.pkl"))
    return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None

def predict(bundle, frame):
    missing = [column for column in bundle["feature_names"] if column not in frame.columns]
    if missing:
        raise ValueError("Missing required feature columns: " + ", ".join(missing))
    ordered = frame[bundle["feature_names"]].apply(pd.to_numeric, errors="raise")
    matrix = bundle["preprocessor"].transform(ordered)
    predictions = bundle["model"].predict(matrix)
    probability = None
    if hasattr(bundle["model"], "predict_proba"):
        probabilities = bundle["model"].predict_proba(matrix)
        classes = list(bundle["model"].classes_)
        probability = probabilities[:, classes.index(-1)] if -1 in classes else probabilities.max(axis=1)
    return predictions, probability

model_path = latest_model()
with st.sidebar:
    st.markdown("<div class='eyebrow'>SIGNAL / MODEL CONSOLE</div>", unsafe_allow_html=True)
    st.markdown("### Phishing intelligence")
    st.caption("Network security / supervised classification")
    st.divider()
    if model_path:
        st.markdown("**Model status**")
        st.success("Ready | Random Forest", icon=":material/check_circle:")
        st.caption(f"Latest artifact: `{model_path.parent.parent.name}`")
    else:
        st.warning("No trained model found")
        st.caption("Train one with `python main.py` first.")
    st.divider()
    st.caption("Input values use the dataset encoding: ?1 = safe signal, 0 = neutral, 1 = suspicious signal. Model scores support analyst review; they are not a guarantee of safety.")

st.markdown("""
<div class="hero"><div class="eyebrow">NETWORK SECURITY / THREAT ANALYSIS</div>
<h1>See the signal.<br>Stop the threat.</h1>
<p>Score phishing indicators with your trained network security model. Analyze one URL profile or inspect a full batch in seconds.</p></div>
""", unsafe_allow_html=True)

m1,m2,m3 = st.columns(3)
for col,label,value in [(m1,"Inference engine","Random Forest"),(m2,"Signals per analysis","30 features"),(m3,"Model artifact","Ready" if model_path else "Not trained")]:
    col.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)
st.write("")

if not model_path:
    st.info("Train the model first with `python main.py`. The frontend will detect the newest model artifact automatically.")
    st.stop()
bundle = load_bundle(str(model_path))

single_tab, batch_tab, guide_tab = st.tabs(["Single analysis", "Batch scan", "Feature guide"])
with single_tab:
    st.markdown("### Analyze a URL profile")
    st.caption("Enter the feature values produced by the phishing dataset feature extraction process.")
    with st.form("single_prediction"):
        values = {}
        group_cols = st.columns(2)
        for idx, (group, columns) in enumerate(GROUPS.items()):
            with group_cols[idx % 2]:
                st.markdown(f"**{group}**")
                for feature in columns:
                    values[feature] = st.select_slider(LABELS[feature], options=[-1, 0, 1], value=0, key=f"single_{feature}")
        submitted = st.form_submit_button("Analyze indicators", type="primary", use_container_width=True)
    if submitted:
        try:
            prediction, probability = predict(bundle, pd.DataFrame([values]))
            phishing = int(prediction[0]) == -1
            if phishing:
                st.error("Likely phishing - the model found a pattern associated with phishing websites.", icon=":material/warning:")
            else:
                st.success("Likely legitimate - the model found a pattern associated with legitimate websites.", icon=":material/check_circle:")
            result_cols = st.columns(2)
            result_cols[0].metric("Classification", "Phishing" if phishing else "Legitimate")
            if probability is not None:
                result_cols[1].metric("Phishing confidence", f"{probability[0]:.1%}")
            st.caption("Use this result as a risk signal alongside your normal security checks.")
        except Exception as error:
            st.error(f"Could not score this profile: {error}")

with batch_tab:
    st.markdown("### Scan a CSV batch")
    st.caption("Upload a CSV with the 30 model features. A `Result` target column is not required.")
    template = pd.DataFrame([{feature: 0 for feature in FEATURES}])
    st.download_button("Download CSV template", template.to_csv(index=False), "phishing_feature_template.csv", "text/csv")
    upload = st.file_uploader("Choose a feature CSV", type=["csv"], help="Each row should describe one website using the dataset numeric feature encoding.")
    if upload is not None:
        try:
            source = pd.read_csv(upload)
            predictions, probabilities = predict(bundle, source)
            results = source.copy()
            results["prediction"] = ["Phishing" if int(value) == -1 else "Legitimate" for value in predictions]
            if probabilities is not None:
                results["phishing_confidence"] = probabilities.round(4)
            phishing_count = int((predictions == -1).sum())
            a,b,c = st.columns(3)
            a.metric("Websites scanned", f"{len(results):,}")
            b.metric("Flagged as phishing", f"{phishing_count:,}")
            c.metric("Flag rate", f"{phishing_count / len(results):.1%}" if len(results) else "0.0%")
            st.dataframe(results, use_container_width=True, hide_index=True)
            st.download_button("Download scan results", results.to_csv(index=False), "phishing_scan_results.csv", "text/csv", type="primary")
        except Exception as error:
            st.error(f"Unable to process this file: {error}")

with guide_tab:
    st.markdown("### What the model reads")
    st.caption("These inputs are engineered signals from the training dataset, grouped by the part of a website they describe.")
    for group, columns in GROUPS.items():
        with st.expander(group, expanded=group == "URL structure"):
            st.markdown("\n".join(f"- **{LABELS[column]}** | `{column}`" for column in columns))
    st.info("The model does not fetch or crawl the URL itself. Supply features from your data pipeline; do not treat a classification as proof that a site is safe.")
