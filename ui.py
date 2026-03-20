# """
# ui.py  (entry point: run with `streamlit run ui.py`)
# -----------------------------------------------------
# Main Streamlit interface for the AI SOP Training Generator.
# """

# import os
# import json
# import streamlit as st

# from pdf_parser import preprocess_input
# from llm_handler import call_groq_llm, AVAILABLE_MODELS


# # ── Page configuration ────────────────────────────────────────────────────────

# st.set_page_config(
#     page_title="SOP Training Generator",
#     page_icon="🎓",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ── Custom CSS ────────────────────────────────────────────────────────────────

# st.markdown(
#     """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'DM Sans', sans-serif;
#     }

#     /* App background */
#     .stApp {
#         background: #f7f8fc;
#     }

#     /* Sidebar */
#     section[data-testid="stSidebar"] {
#         background: #1a1a2e !important;
#     }
#     section[data-testid="stSidebar"] * {
#         color: #e0e4f0 !important;
#     }
#     section[data-testid="stSidebar"] .stSelectbox label,
#     section[data-testid="stSidebar"] .stTextInput label {
#         color: #a0b0cc !important;
#         font-size: 0.8rem !important;
#         text-transform: uppercase;
#         letter-spacing: 0.08em;
#     }

#     /* Main header */
#     .main-header {
#         background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
#         padding: 2.5rem 2rem 2rem;
#         border-radius: 16px;
#         margin-bottom: 2rem;
#         position: relative;
#         overflow: hidden;
#     }
#     .main-header::before {
#         content: '';
#         position: absolute;
#         top: -40px; right: -40px;
#         width: 200px; height: 200px;
#         background: rgba(255,255,255,0.03);
#         border-radius: 50%;
#     }
#     .main-header h1 {
#         font-family: 'DM Serif Display', serif;
#         color: #ffffff;
#         font-size: 2.4rem;
#         margin: 0 0 0.3rem;
#         letter-spacing: -0.02em;
#     }
#     .main-header p {
#         color: #8ba4c8;
#         font-size: 1rem;
#         margin: 0;
#         font-weight: 300;
#     }
#     .header-badge {
#         display: inline-block;
#         background: rgba(255,255,255,0.12);
#         color: #a0c4ff;
#         font-size: 0.72rem;
#         letter-spacing: 0.1em;
#         text-transform: uppercase;
#         padding: 4px 12px;
#         border-radius: 20px;
#         margin-bottom: 0.8rem;
#         font-weight: 500;
#     }

#     /* Section cards */
#     .section-card {
#         background: #ffffff;
#         border-radius: 12px;
#         padding: 1.5rem;
#         margin-bottom: 1.2rem;
#         box-shadow: 0 2px 12px rgba(0,0,0,0.06);
#         border: 1px solid #eef0f6;
#     }
#     .section-title {
#         font-family: 'DM Serif Display', serif;
#         font-size: 1.4rem;
#         color: #1a1a2e;
#         margin-bottom: 0.8rem;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }

#     /* Summary bullets */
#     .bullet-item {
#         background: #f0f5ff;
#         border-left: 3px solid #0f3460;
#         padding: 0.6rem 1rem;
#         border-radius: 0 8px 8px 0;
#         margin-bottom: 0.5rem;
#         font-size: 0.93rem;
#         color: #2c3e60;
#     }
#     .rule-item {
#         background: #fff8e6;
#         border-left: 3px solid #e9a800;
#         padding: 0.6rem 1rem;
#         border-radius: 0 8px 8px 0;
#         margin-bottom: 0.5rem;
#         font-size: 0.93rem;
#         color: #5a4000;
#     }

#     /* Step cards */
#     .step-header {
#         display: flex;
#         align-items: center;
#         gap: 0.8rem;
#         margin-bottom: 0.6rem;
#     }
#     .step-number {
#         background: #0f3460;
#         color: white;
#         width: 32px; height: 32px;
#         border-radius: 50%;
#         display: flex; align-items: center; justify-content: center;
#         font-size: 0.85rem;
#         font-weight: 600;
#         flex-shrink: 0;
#     }
#     .step-title-text {
#         font-size: 1.05rem;
#         font-weight: 600;
#         color: #1a1a2e;
#     }
#     .step-description {
#         color: #4a5568;
#         font-size: 0.93rem;
#         line-height: 1.6;
#         margin-bottom: 0.6rem;
#     }
#     .step-example {
#         background: #eef9f4;
#         border-left: 3px solid #22c55e;
#         padding: 0.6rem 1rem;
#         border-radius: 0 8px 8px 0;
#         font-size: 0.88rem;
#         color: #1a5c38;
#         margin-top: 0.5rem;
#     }
#     .step-tip {
#         font-size: 0.85rem;
#         color: #7c6f00;
#         background: #fffbe6;
#         padding: 4px 10px;
#         border-radius: 6px;
#         display: inline-block;
#         margin: 3px 3px 0 0;
#     }

#     /* Quiz */
#     .quiz-question {
#         font-size: 1rem;
#         font-weight: 600;
#         color: #1a1a2e;
#         margin-bottom: 0.6rem;
#         line-height: 1.5;
#     }
#     .quiz-type-badge {
#         font-size: 0.7rem;
#         text-transform: uppercase;
#         letter-spacing: 0.1em;
#         padding: 2px 8px;
#         border-radius: 4px;
#         font-weight: 600;
#         margin-right: 6px;
#     }
#     .badge-mcq { background: #dbeafe; color: #1d4ed8; }
#     .badge-scenario { background: #fce7f3; color: #9d174d; }

#     .correct-answer {
#         background: #dcfce7;
#         border: 1px solid #86efac;
#         border-radius: 8px;
#         padding: 0.7rem 1rem;
#         font-size: 0.9rem;
#         color: #166534;
#         margin-top: 0.5rem;
#     }

#     /* Generate button */
#     .stButton > button {
#         background: linear-gradient(135deg, #0f3460, #1a1a2e) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 10px !important;
#         padding: 0.7rem 2rem !important;
#         font-size: 1rem !important;
#         font-weight: 600 !important;
#         letter-spacing: 0.02em;
#         transition: all 0.2s;
#         width: 100%;
#     }
#     .stButton > button:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 6px 20px rgba(15,52,96,0.35) !important;
#     }

#     /* Download buttons */
#     .stDownloadButton > button {
#         background: white !important;
#         color: #0f3460 !important;
#         border: 1.5px solid #0f3460 !important;
#         border-radius: 8px !important;
#         font-weight: 500 !important;
#     }

#     /* Input section */
#     .input-section {
#         background: white;
#         border-radius: 12px;
#         padding: 1.5rem;
#         box-shadow: 0 2px 12px rgba(0,0,0,0.06);
#         border: 1px solid #eef0f6;
#         margin-bottom: 1rem;
#     }

#     /* Tab styling */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 4px;
#         background: #f0f2f8;
#         padding: 4px;
#         border-radius: 10px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         border-radius: 8px;
#         padding: 6px 16px;
#         font-weight: 500;
#     }

#     /* Expanders */
#     .streamlit-expanderHeader {
#         background: #f8f9ff !important;
#         border-radius: 8px !important;
#         font-weight: 500 !important;
#     }

#     /* Overview tag */
#     .overview-box {
#         background: linear-gradient(135deg, #eef4ff, #f0f7ff);
#         border: 1px solid #c7d9f5;
#         border-radius: 10px;
#         padding: 1rem 1.2rem;
#         font-size: 0.95rem;
#         color: #2c4470;
#         line-height: 1.65;
#         margin-bottom: 1rem;
#     }

#     /* Progress bar override */
#     .stProgress .st-bo { background-color: #0f3460; }

#     /* Dividers */
#     hr { border-color: #eef0f6 !important; }

#     /* Hide streamlit branding */
#     #MainMenu, footer { visibility: hidden; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ── Sidebar ───────────────────────────────────────────────────────────────────

# with st.sidebar:
#     st.markdown(
#         """
#         <div style="text-align:center; padding: 1rem 0 0.5rem;">
#             <span style="font-size:2.5rem;">🎓</span>
#             <h3 style="color:#fff; font-family:'DM Serif Display',serif; margin:0.3rem 0 0.1rem;">
#                 SOP Trainer
#             </h3>
#             <p style="color:#6b7fa3; font-size:0.78rem; margin:0;">Powered by Groq + LLaMA 3</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("---")
#     st.markdown(
#         '<p style="font-size:0.7rem;text-transform:uppercase;letter-spacing:.1em;color:#6b7fa3;margin-bottom:.4rem;">Configuration</p>',
#         unsafe_allow_html=True,
#     )

#     # API Key
#     api_key_input = st.text_input(
#         "Groq API Key",
#         type="password",
#         value=os.environ.get("GROQ_API_KEY", ""),
#         placeholder="gsk_...",
#         help="Get your free API key at console.groq.com",
#     )

#     # Model selection
#     model_label = st.selectbox(
#         "LLM Model",
#         options=list(AVAILABLE_MODELS.keys()),
#         index=0,
#         help="LLaMA 3 70B gives the best results. 8B is faster.",
#     )
#     selected_model = AVAILABLE_MODELS[model_label]

#     st.markdown("---")
#     st.markdown(
#         """
#         <div style="font-size:0.78rem; color:#5a6a88; line-height:1.7;">
#         <b style="color:#8ba4c8;">How it works:</b><br>
#         1. Add your Groq API key<br>
#         2. Upload a PDF or paste SOP text<br>
#         3. Click <b>Generate</b><br>
#         4. Review & export the training module
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("---")
#     st.markdown(
#         '<p style="font-size:0.68rem; color:#3d4f6a; text-align:center;">Free tier · No OpenAI · Open source models</p>',
#         unsafe_allow_html=True,
#     )


# # ── Main header ───────────────────────────────────────────────────────────────

# st.markdown(
#     """
#     <div class="main-header">
#         <div class="header-badge">AI-Powered Training Generator</div>
#         <h1>SOP Training System</h1>
#         <p>Transform any Standard Operating Procedure into a complete training module — with summaries, step-by-step guides, and quizzes — in seconds.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# # ── Input section ─────────────────────────────────────────────────────────────

# st.markdown("### 📥 Input Your SOP")

# tab_pdf, tab_text = st.tabs(["📄 Upload PDF", "✏️ Paste Text"])

# with tab_pdf:
#     st.markdown('<div class="input-section">', unsafe_allow_html=True)
#     uploaded_file = st.file_uploader(
#         "Upload your SOP document (PDF)",
#         type=["pdf"],
#         help="Upload any PDF-format SOP document",
#         label_visibility="visible",
#     )
#     if uploaded_file:
#         st.success(f"✅ Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
#     st.markdown("</div>", unsafe_allow_html=True)

# with tab_text:
#     st.markdown('<div class="input-section">', unsafe_allow_html=True)
#     pasted_text = st.text_area(
#         "Paste your SOP text here",
#         height=260,
#         placeholder="Paste the full text of your Standard Operating Procedure here...\n\nFor example:\n\n1. Purpose\nThis SOP describes the process for...\n\n2. Scope\nThis procedure applies to...",
#     )
#     if pasted_text:
#         word_count = len(pasted_text.split())
#         st.caption(f"📊 {word_count:,} words · {len(pasted_text):,} characters")
#     st.markdown("</div>", unsafe_allow_html=True)


# # ── Generate button ───────────────────────────────────────────────────────────

# st.markdown("")
# col_btn, col_info = st.columns([1, 2])

# with col_btn:
#     generate_clicked = st.button("🚀 Generate Training Module", use_container_width=True)

# with col_info:
#     st.markdown(
#         """
#         <div style="padding: 0.7rem 0; color: #6b7fa3; font-size: 0.85rem;">
#         ⚡ Typically takes 10–30 seconds &nbsp;·&nbsp; 
#         🔒 Your data is not stored &nbsp;·&nbsp; 
#         🆓 Uses free Groq API
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# # ── State management ──────────────────────────────────────────────────────────

# if "training_data" not in st.session_state:
#     st.session_state.training_data = None
# if "quiz_revealed" not in st.session_state:
#     st.session_state.quiz_revealed = {}


# # ── Generation logic ──────────────────────────────────────────────────────────

# if generate_clicked:
#     # Resolve API key
#     resolved_api_key = api_key_input.strip() or os.environ.get("GROQ_API_KEY", "").strip()

#     if not resolved_api_key:
#         st.error("⚠️ Please enter your Groq API key in the sidebar.")
#         st.stop()

#     # Determine input source
#     has_pdf = uploaded_file is not None
#     has_text = bool(pasted_text and pasted_text.strip())

#     if not has_pdf and not has_text:
#         st.error("⚠️ Please upload a PDF or paste SOP text before generating.")
#         st.stop()

#     with st.spinner("Processing your SOP document..."):
#         progress_bar = st.progress(0)
#         status_text = st.empty()

#         try:
#             # Step 1: Parse input
#             status_text.text("📄 Extracting and cleaning text...")
#             progress_bar.progress(20)

#             # Re-seek uploaded file if needed
#             if has_pdf:
#                 uploaded_file.seek(0)

#             sop_text = preprocess_input(
#                 uploaded_file=uploaded_file if has_pdf else None,
#                 raw_text=pasted_text if has_text else "",
#             )

#             if len(sop_text.strip()) < 50:
#                 st.error("⚠️ The extracted text is too short. Please provide a more detailed SOP.")
#                 st.stop()

#             # Step 2: Call LLM
#             status_text.text("🧠 Sending to LLM (this may take 15–30s)...")
#             progress_bar.progress(50)

#             training_data = call_groq_llm(
#                 sop_text=sop_text,
#                 api_key=resolved_api_key,
#                 model=selected_model,
#             )

#             progress_bar.progress(90)
#             status_text.text("✅ Finalizing output...")

#             st.session_state.training_data = training_data
#             st.session_state.quiz_revealed = {}

#             progress_bar.progress(100)
#             status_text.empty()
#             progress_bar.empty()

#             st.success("✅ Training module generated successfully!")

#         except ValueError as e:
#             progress_bar.empty()
#             status_text.empty()
#             st.error(f"⚠️ Input Error: {e}")
#         except RuntimeError as e:
#             progress_bar.empty()
#             status_text.empty()
#             st.error(f"🔌 API Error: {e}")
#         except Exception as e:
#             progress_bar.empty()
#             status_text.empty()
#             st.error(f"❌ Unexpected error: {e}")
#             st.info("Try again, or simplify your SOP document.")


# # ── Output display ────────────────────────────────────────────────────────────

# if st.session_state.training_data:
#     data = st.session_state.training_data

#     st.markdown("---")

#     # Document title
#     doc_title = data.get("document_title", "Untitled SOP")
#     st.markdown(
#         f"""
#         <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;">
#             <div style="background:#0f3460;color:white;padding:8px 16px;border-radius:8px;font-weight:600;">
#                 📁 {doc_title}
#             </div>
#             <span style="color:#6b7fa3;font-size:0.85rem;">
#                 {len(data.get('training_steps',[]))} steps · 
#                 {len(data.get('quiz',[]))} quiz questions
#             </span>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # ── Section 1: Summary ────────────────────────────────────────────────────
#     summary = data.get("summary", {})

#     st.markdown(
#         '<div class="section-card"><div class="section-title">📋 Summary</div>',
#         unsafe_allow_html=True,
#     )

#     if summary.get("overview"):
#         st.markdown(
#             f'<div class="overview-box">{summary["overview"]}</div>',
#             unsafe_allow_html=True,
#         )

#     col_obj, col_rules = st.columns(2)

#     with col_obj:
#         st.markdown("**🎯 Key Objectives**")
#         for obj in summary.get("key_objectives", []):
#             st.markdown(f'<div class="bullet-item">• {obj}</div>', unsafe_allow_html=True)

#     with col_rules:
#         st.markdown("**⚠️ Important Rules**")
#         for rule in summary.get("important_rules", []):
#             st.markdown(f'<div class="rule-item">⚡ {rule}</div>', unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)  # end section-card

#     # ── Section 2: Training Steps ─────────────────────────────────────────────
#     st.markdown(
#         '<div class="section-card"><div class="section-title">🎓 Step-by-Step Training Module</div>',
#         unsafe_allow_html=True,
#     )

#     training_steps = data.get("training_steps", [])
#     for step in training_steps:
#         num = step.get("step_number", "")
#         title = step.get("title", "")
#         description = step.get("description", "")
#         example = step.get("example", "")
#         tips = step.get("tips", [])

#         with st.expander(f"Step {num}: {title}", expanded=(num == 1)):
#             st.markdown(
#                 f"""
#                 <div class="step-header">
#                     <div class="step-number">{num}</div>
#                     <div class="step-title-text">{title}</div>
#                 </div>
#                 <div class="step-description">{description}</div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             if example:
#                 st.markdown(
#                     f'<div class="step-example">💡 <b>Example:</b> {example}</div>',
#                     unsafe_allow_html=True,
#                 )

#             if tips:
#                 st.markdown("")
#                 tip_html = " ".join(f'<span class="step-tip">💡 {t}</span>' for t in tips)
#                 st.markdown(tip_html, unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)

#     # ── Section 3: Quiz ───────────────────────────────────────────────────────
#     st.markdown(
#         '<div class="section-card"><div class="section-title">📝 Quiz & Evaluation</div>',
#         unsafe_allow_html=True,
#     )

#     st.markdown(
#         '<p style="color:#6b7fa3;font-size:0.88rem;margin-bottom:1rem;">Test your understanding of the SOP. Click "Reveal Answer" after selecting your answer.</p>',
#         unsafe_allow_html=True,
#     )

#     quiz_items = data.get("quiz", [])
#     for q in quiz_items:
#         qnum = q.get("question_number", "")
#         qtype = q.get("type", "mcq")
#         question = q.get("question", "")
#         options = q.get("options", [])
#         answer = q.get("answer", "")
#         explanation = q.get("explanation", "")

#         badge_class = "badge-mcq" if qtype == "mcq" else "badge-scenario"
#         badge_label = "MCQ" if qtype == "mcq" else "Scenario"

#         with st.expander(f"Question {qnum}: {question[:70]}{'...' if len(question) > 70 else ''}", expanded=False):
#             st.markdown(
#                 f"""
#                 <span class="quiz-type-badge {badge_class}">{badge_label}</span>
#                 <div class="quiz-question">{question}</div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#             # Radio for options
#             radio_key = f"q_{qnum}"
#             if options:
#                 selected = st.radio(
#                     "Select your answer:",
#                     options=options,
#                     key=radio_key,
#                     label_visibility="collapsed",
#                 )

#             # Reveal button
#             reveal_key = f"reveal_{qnum}"
#             if st.button(f"🔍 Reveal Answer", key=f"btn_{qnum}"):
#                 st.session_state.quiz_revealed[reveal_key] = True

#             if st.session_state.quiz_revealed.get(reveal_key):
#                 st.markdown(
#                     f"""
#                     <div class="correct-answer">
#                         ✅ <b>Correct Answer: {answer}</b><br>
#                         <span style="font-size:0.88rem;color:#1a5c38;">{explanation}</span>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )

#     st.markdown("</div>", unsafe_allow_html=True)

#     # ── Export section ────────────────────────────────────────────────────────
#     st.markdown("### 💾 Export Training Module")

#     col_pdf, col_pptx, col_json = st.columns(3)

#     with col_pdf:
#         try:
#             from export_utils import export_to_pdf
#             pdf_bytes = export_to_pdf(data)
#             st.download_button(
#                 label="📄 Download as PDF",
#                 data=pdf_bytes,
#                 file_name=f"{doc_title.replace(' ', '_')}_training.pdf",
#                 mime="application/pdf",
#                 use_container_width=True,
#             )
#         except ImportError:
#             st.info("Install `reportlab` to enable PDF export:\n`pip install reportlab`")
#         except Exception as e:
#             st.error(f"PDF export failed: {e}")

#     with col_pptx:
#         try:
#             from export_utils import export_to_pptx
#             pptx_bytes = export_to_pptx(data)
#             st.download_button(
#                 label="📊 Download as PowerPoint",
#                 data=pptx_bytes,
#                 file_name=f"{doc_title.replace(' ', '_')}_training.pptx",
#                 mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
#                 use_container_width=True,
#             )
#         except ImportError:
#             st.info("Install `python-pptx` to enable PPTX export:\n`pip install python-pptx`")
#         except Exception as e:
#             st.error(f"PPTX export failed: {e}")

#     with col_json:
#         json_str = json.dumps(data, indent=2)
#         st.download_button(
#             label="🗂️ Download as JSON",
#             data=json_str,
#             file_name=f"{doc_title.replace(' ', '_')}_training.json",
#             mime="application/json",
#             use_container_width=True,
#         )

# # ── Empty state ───────────────────────────────────────────────────────────────
# elif not generate_clicked:
#     st.markdown(
#         """
#         <div style="text-align:center; padding: 3rem 1rem; color: #9aa5b8;">
#             <div style="font-size:3.5rem; margin-bottom:1rem;">📋</div>
#             <h3 style="color:#4a5568; font-family:'DM Serif Display',serif; font-size:1.4rem;">
#                 Your training module will appear here
#             </h3>
#             <p style="font-size:0.9rem; max-width:400px; margin:0 auto; line-height:1.7;">
#                 Upload a PDF or paste your SOP text above, then click 
#                 <b style="color:#0f3460;">Generate Training Module</b> to get started.
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
"""
ui.py  (entry point: run with `streamlit run ui.py`)
-----------------------------------------------------
Main Streamlit interface for the AI SOP Training Generator.
"""

import os
import json
import streamlit as st

from pdf_parser import preprocess_input
from llm_handler import call_groq_llm, AVAILABLE_MODELS


# ── Page configuration ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SOP Training Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* App background */
    .stApp {
        background: #f7f8fc;
    }

    /* Force readable defaults (prevents text blending when Streamlit base theme differs). */
    html, body {
        background: #f7f8fc !important;
        color: #0f172a !important;
        font-size: 16px !important;
    }
    div[data-testid="stAppViewContainer"] {
        background: #f7f8fc !important;
        color: #0f172a !important;
    }
    /* Ensure main content blocks inherit readable color. */
    div[data-testid="stVerticalBlock"],
    div[data-testid="stMainBlockContainer"],
    section[data-testid="stMain"] {
        color: #0f172a !important;
    }

    /* ── TARGETED TEXT COLOR FIX (quiz + expanders only) ── */
    /* Expander header text */
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary { color: #1a1a2e !important; }
    /* Radio labels inside expanders */
    div[data-testid="stExpander"] label p,
    div[data-testid="stExpander"] label span,
    div[data-testid="stExpander"] label { color: #1a1a2e !important; }
    /* All text inside expander body */
    div[data-testid="stExpanderDetails"] p,
    div[data-testid="stExpanderDetails"] span,
    div[data-testid="stExpanderDetails"] label,
    div[data-testid="stExpanderDetails"] div { color: #1a1a2e !important; }
    /* Expander panels: ensure light backgrounds to keep dark text readable. */
    div[data-testid="stExpander"] {
        background: #ffffff !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpanderDetails"] {
        background: #ffffff !important;
    }
    div[data-testid="stExpander"] summary {
        background: #f8f9ff !important;
        border-radius: 10px !important;
    }
    /* Text area */
    .stTextArea textarea {
        color: #0f172a !important;
        background: #ffffff !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
    .stTextArea textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
        font-size: 15px !important;
    }
    /* File uploader */
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] div { color: #0f172a !important; }
    /* File uploader dropzone area can default to a dark background; force readable contrast. */
    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploader"] div[role="button"] {
        background: #f3f4f6 !important;
        color: #0f172a !important;
    }
    div[data-testid="stFileUploader"] * {
        font-size: 14px !important;
        opacity: 1 !important;
        visibility: visible !important;
        color: #0f172a !important;
    }
    /* Force browse/upload button to always have visible contrast. */
    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] [role="button"] {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }
    div[data-testid="stFileUploader"] button *,
    div[data-testid="stFileUploader"] [role="button"] * {
        color: #0f172a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* Sidebar inputs should stay readable on the dark sidebar background. */
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] textarea {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    /* Radio/option labels sometimes bypass the expander selectors. */
    [data-testid="stRadio"] label,
    [role="radiogroup"] label,
    div[data-testid="stExpanderDetails"] [data-baseweb="radio"] label,
    div[data-testid="stExpanderDetails"] label {
        color: #0f172a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* Ensure nested text nodes (span/p) are also forced visible. */
    [data-testid="stRadio"] label *,
    [role="radiogroup"] label *,
    div[data-testid="stExpanderDetails"] [data-baseweb="radio"] label * {
        color: #0f172a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    [data-testid="stRadio"] label {
        background: transparent !important;
    }
    /* Quiz option font sizing. */
    [data-testid="stRadio"] label,
    [role="radiogroup"] label {
        font-size: 16px !important;
        line-height: 1.4 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e0e4f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label {
        color: #a0b0cc !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem 2rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.03);
        border-radius: 50%;
    }
    .main-header h1 {
        font-family: 'DM Serif Display', serif;
        color: #ffffff;
        font-size: 2.4rem;
        margin: 0 0 0.3rem;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #8ba4c8;
        font-size: 1rem;
        margin: 0;
        font-weight: 300;
    }
    .header-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        color: #a0c4ff;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }

    /* Section cards */
    .section-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #eef0f6;
    }
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: #1a1a2e;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Summary bullets */
    .bullet-item {
        background: #f0f5ff;
        border-left: 3px solid #0f3460;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.93rem;
        color: #2c3e60;
    }
    .rule-item {
        background: #fff8e6;
        border-left: 3px solid #e9a800;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
        font-size: 0.93rem;
        color: #5a4000;
    }

    /* Step cards */
    .step-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.6rem;
    }
    .step-number {
        background: #0f3460;
        color: white;
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.85rem;
        font-weight: 600;
        flex-shrink: 0;
    }
    .step-title-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1a1a2e;
    }
    .step-description {
        color: #4a5568;
        font-size: 0.93rem;
        line-height: 1.6;
        margin-bottom: 0.6rem;
    }
    .step-example {
        background: #eef9f4;
        border-left: 3px solid #22c55e;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #1a5c38;
        margin-top: 0.5rem;
    }
    .step-tip {
        font-size: 0.85rem;
        color: #7c6f00;
        background: #fffbe6;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
        margin: 3px 3px 0 0;
    }

    /* Quiz */
    .quiz-question {
        font-size: 1rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0.6rem;
        line-height: 1.5;
    }
    .quiz-type-badge {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-mcq { background: #dbeafe; color: #1d4ed8; }
    .badge-scenario { background: #fce7f3; color: #9d174d; }

    .correct-answer {
        background: #dcfce7;
        border: 1px solid #86efac;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        color: #166534;
        margin-top: 0.5rem;
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #1a1a2e) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(15,52,96,0.35) !important;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: white !important;
        color: #0f3460 !important;
        border: 1.5px solid #0f3460 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* Input section */
    .input-section {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #eef0f6;
        margin-bottom: 1rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f0f2f8;
        padding: 4px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 16px;
        font-weight: 500;
        color: #0f172a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] p {
        color: #0f172a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #0f3460 !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #f8f9ff !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* Overview tag */
    .overview-box {
        background: linear-gradient(135deg, #eef4ff, #f0f7ff);
        border: 1px solid #c7d9f5;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        font-size: 0.95rem;
        color: #2c4470;
        line-height: 1.65;
        margin-bottom: 1rem;
    }

    /* Progress bar override */
    .stProgress .st-bo { background-color: #0f3460; }

    /* Dividers */
    hr { border-color: #eef0f6 !important; }

    /* Hide streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 1rem 0 0.5rem;">
            <span style="font-size:2.5rem;">🎓</span>
            <h3 style="color:#fff; font-family:'DM Serif Display',serif; margin:0.3rem 0 0.1rem;">
                SOP Trainer
            </h3>
            <p style="color:#6b7fa3; font-size:0.78rem; margin:0;">Powered by Groq + LLaMA 3</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.7rem;text-transform:uppercase;letter-spacing:.1em;color:#6b7fa3;margin-bottom:.4rem;">Configuration</p>',
        unsafe_allow_html=True,
    )

    # API Key
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        placeholder="gsk_...",
        help="Get your free API key at console.groq.com",
    )

    # Model selection
    model_label = st.selectbox(
        "LLM Model",
        options=list(AVAILABLE_MODELS.keys()),
        index=0,
        help="LLaMA 3 70B gives the best results. 8B is faster.",
    )
    selected_model = AVAILABLE_MODELS[model_label]

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.78rem; color:#5a6a88; line-height:1.7;">
        <b style="color:#8ba4c8;">How it works:</b><br>
        1. Add your Groq API key<br>
        2. Upload a PDF or paste SOP text<br>
        3. Click <b>Generate</b><br>
        4. Review & export the training module
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.68rem; color:#3d4f6a; text-align:center;">Free tier · No OpenAI · Open source models</p>',
        unsafe_allow_html=True,
    )


# ── Main header ───────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="main-header">
        <div class="header-badge">AI-Powered Training Generator</div>
        <h1>SOP Training System</h1>
        <p>Transform any Standard Operating Procedure into a complete training module — with summaries, step-by-step guides, and quizzes — in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── Input section ─────────────────────────────────────────────────────────────

st.markdown("### 📥 Input Your SOP")

tab_pdf, tab_text = st.tabs(["📄 Upload PDF", "✏️ Paste Text"])

with tab_pdf:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your SOP document (PDF)",
        type=["pdf"],
        help="Upload any PDF-format SOP document",
        label_visibility="visible",
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_text:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    pasted_text = st.text_area(
        "Paste your SOP text here",
        height=260,
        placeholder="Paste the full text of your Standard Operating Procedure here...\n\nFor example:\n\n1. Purpose\nThis SOP describes the process for...\n\n2. Scope\nThis procedure applies to...",
    )
    if pasted_text:
        word_count = len(pasted_text.split())
        st.caption(f"📊 {word_count:,} words · {len(pasted_text):,} characters")
    st.markdown("</div>", unsafe_allow_html=True)


# ── Generate button ───────────────────────────────────────────────────────────

st.markdown("")
col_btn, col_info = st.columns([1, 2])

with col_btn:
    generate_clicked = st.button("🚀 Generate Training Module", use_container_width=True)

with col_info:
    st.markdown(
        """
        <div style="padding: 0.7rem 0; color: #6b7fa3; font-size: 0.85rem;">
        ⚡ Typically takes 10–30 seconds &nbsp;·&nbsp; 
        🔒 Your data is not stored &nbsp;·&nbsp; 
        🆓 Uses free Groq API
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── State management ──────────────────────────────────────────────────────────

if "training_data" not in st.session_state:
    st.session_state.training_data = None
if "quiz_revealed" not in st.session_state:
    st.session_state.quiz_revealed = {}


# ── Generation logic ──────────────────────────────────────────────────────────

if generate_clicked:
    # Resolve API key
    resolved_api_key = api_key_input.strip() or os.environ.get("GROQ_API_KEY", "").strip()

    if not resolved_api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()

    # Determine input source
    has_pdf = uploaded_file is not None
    has_text = bool(pasted_text and pasted_text.strip())

    if not has_pdf and not has_text:
        st.error("⚠️ Please upload a PDF or paste SOP text before generating.")
        st.stop()

    with st.spinner("Processing your SOP document..."):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Parse input
            status_text.text("📄 Extracting and cleaning text...")
            progress_bar.progress(20)

            # Re-seek uploaded file if needed
            if has_pdf:
                uploaded_file.seek(0)

            sop_text = preprocess_input(
                uploaded_file=uploaded_file if has_pdf else None,
                raw_text=pasted_text if has_text else "",
            )

            if len(sop_text.strip()) < 50:
                st.error("⚠️ The extracted text is too short. Please provide a more detailed SOP.")
                st.stop()

            # Step 2: Call LLM
            status_text.text("🧠 Sending to LLM (this may take 15–30s)...")
            progress_bar.progress(50)

            training_data = call_groq_llm(
                sop_text=sop_text,
                api_key=resolved_api_key,
                model=selected_model,
            )

            progress_bar.progress(90)
            status_text.text("✅ Finalizing output...")

            st.session_state.training_data = training_data
            st.session_state.quiz_revealed = {}

            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            st.success("✅ Training module generated successfully!")

        except ValueError as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"⚠️ Input Error: {e}")
        except RuntimeError as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"🔌 API Error: {e}")
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Unexpected error: {e}")
            st.info("Try again, or simplify your SOP document.")


# ── Output display ────────────────────────────────────────────────────────────

if st.session_state.training_data:
    data = st.session_state.training_data

    st.markdown("---")

    # Document title
    doc_title = data.get("document_title", "Untitled SOP")
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:#0f3460;color:white;padding:8px 16px;border-radius:8px;font-weight:600;">
                📁 {doc_title}
            </div>
            <span style="color:#6b7fa3;font-size:0.85rem;">
                {len(data.get('training_steps',[]))} steps · 
                {len(data.get('quiz',[]))} quiz questions
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Section 1: Summary ────────────────────────────────────────────────────
    summary = data.get("summary", {})

    st.markdown(
        '<div class="section-card"><div class="section-title">📋 Summary</div>',
        unsafe_allow_html=True,
    )

    if summary.get("overview"):
        st.markdown(
            f'<div class="overview-box">{summary["overview"]}</div>',
            unsafe_allow_html=True,
        )

    col_obj, col_rules = st.columns(2)

    with col_obj:
        st.markdown("**🎯 Key Objectives**")
        for obj in summary.get("key_objectives", []):
            st.markdown(f'<div class="bullet-item">• {obj}</div>', unsafe_allow_html=True)

    with col_rules:
        st.markdown("**⚠️ Important Rules**")
        for rule in summary.get("important_rules", []):
            st.markdown(f'<div class="rule-item">⚡ {rule}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end section-card

    # ── Section 2: Training Steps ─────────────────────────────────────────────
    st.markdown(
        '<div class="section-card"><div class="section-title">🎓 Step-by-Step Training Module</div>',
        unsafe_allow_html=True,
    )

    training_steps = data.get("training_steps", [])
    for step in training_steps:
        num = step.get("step_number", "")
        title = step.get("title", "")
        description = step.get("description", "")
        example = step.get("example", "")
        tips = step.get("tips", [])

        with st.expander(f"Step {num}: {title}", expanded=(num == 1)):
            st.markdown(
                f"""
                <div class="step-header">
                    <div class="step-number">{num}</div>
                    <div class="step-title-text">{title}</div>
                </div>
                <div class="step-description">{description}</div>
                """,
                unsafe_allow_html=True,
            )

            if example:
                st.markdown(
                    f'<div class="step-example">💡 <b>Example:</b> {example}</div>',
                    unsafe_allow_html=True,
                )

            if tips:
                st.markdown("")
                tip_html = " ".join(f'<span class="step-tip">💡 {t}</span>' for t in tips)
                st.markdown(tip_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Quiz ───────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-card"><div class="section-title">📝 Quiz & Evaluation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#6b7fa3;font-size:0.88rem;margin-bottom:1rem;">Test your understanding of the SOP. Click "Reveal Answer" after selecting your answer.</p>',
        unsafe_allow_html=True,
    )

    quiz_items = data.get("quiz", [])
    for q in quiz_items:
        qnum = q.get("question_number", "")
        qtype = q.get("type", "mcq")
        question = q.get("question", "")
        options = q.get("options", [])
        answer = q.get("answer", "")
        explanation = q.get("explanation", "")

        badge_class = "badge-mcq" if qtype == "mcq" else "badge-scenario"
        badge_label = "MCQ" if qtype == "mcq" else "Scenario"

        with st.expander(f"Question {qnum}: {question[:70]}{'...' if len(question) > 70 else ''}", expanded=False):
            st.markdown(
                f"""
                <span class="quiz-type-badge {badge_class}">{badge_label}</span>
                <div class="quiz-question">{question}</div>
                """,
                unsafe_allow_html=True,
            )

            # Radio for options
            radio_key = f"q_{qnum}"
            if options:
                selected = st.radio(
                    "Select your answer:",
                    options=options,
                    key=radio_key,
                    label_visibility="collapsed",
                )

            # Reveal button
            reveal_key = f"reveal_{qnum}"
            if st.button(f"🔍 Reveal Answer", key=f"btn_{qnum}"):
                st.session_state.quiz_revealed[reveal_key] = True

            if st.session_state.quiz_revealed.get(reveal_key):
                st.markdown(
                    f"""
                    <div class="correct-answer">
                        ✅ <b>Correct Answer: {answer}</b><br>
                        <span style="font-size:0.88rem;color:#1a5c38;">{explanation}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Export section ────────────────────────────────────────────────────────
    st.markdown("### 💾 Export Training Module")

    col_pdf, col_pptx, col_json = st.columns(3)

    with col_pdf:
        try:
            from export_utils import export_to_pdf
            pdf_bytes = export_to_pdf(data)
            st.download_button(
                label="📄 Download as PDF",
                data=pdf_bytes,
                file_name=f"{doc_title.replace(' ', '_')}_training.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except ImportError:
            st.info("Install `reportlab` to enable PDF export:\n`pip install reportlab`")
        except Exception as e:
            st.error(f"PDF export failed: {e}")

    with col_pptx:
        try:
            from export_utils import export_to_pptx
            pptx_bytes = export_to_pptx(data)
            st.download_button(
                label="📊 Download as PowerPoint",
                data=pptx_bytes,
                file_name=f"{doc_title.replace(' ', '_')}_training.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
            )
        except ImportError:
            st.info("Install `python-pptx` to enable PPTX export:\n`pip install python-pptx`")
        except Exception as e:
            st.error(f"PPTX export failed: {e}")

    with col_json:
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="🗂️ Download as JSON",
            data=json_str,
            file_name=f"{doc_title.replace(' ', '_')}_training.json",
            mime="application/json",
            use_container_width=True,
        )

# ── Empty state ───────────────────────────────────────────────────────────────
elif not generate_clicked:
    st.markdown(
        """
        <div style="text-align:center; padding: 3rem 1rem; color: #9aa5b8;">
            <div style="font-size:3.5rem; margin-bottom:1rem;">📋</div>
            <h3 style="color:#4a5568; font-family:'DM Serif Display',serif; font-size:1.4rem;">
                Your training module will appear here
            </h3>
            <p style="font-size:0.9rem; max-width:400px; margin:0 auto; line-height:1.7;">
                Upload a PDF or paste your SOP text above, then click 
                <b style="color:#0f3460;">Generate Training Module</b> to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )