import streamlit as st

def app():
    st.markdown("""
    <style>
    /* Hero Section with Modern Gradient */
    .hero-container {
        padding: 3rem 1rem;
        text-align: center;
    }
    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
        font-weight: 850 !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #8B5CF6 50%, #B3A369 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        color: #a1a1aa !important;
        font-size: 1.25rem;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    /* GitHub-style Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #8B5CF6;
        background: rgba(139, 92, 246, 0.05);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    /* GT Badge */
    .gt-badge {
        display: inline-block;
        background: rgba(179, 163, 105, 0.15);
        color: #B3A369;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(179, 163, 105, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-container">
            <div class="gt-badge">GEORGIA TECH • DSGT EXECUTIVE PROJECT</div>
            <h1 class="hero-title">RoboInvesting</h1>
            <p class="hero-subtitle">
                Engineering an autonomous agentic system to navigate complex market dynamics. 
                Integrating deep learning with real-time financial sentiment analysis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 style="color:white; margin-bottom:10px;">Agentic Chat</h3>
                <p style="color:#a1a1aa; font-size:0.9rem;">Advanced LLM wrappers providing contextual insights and natural language portfolio queries.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h3 style="color:white; margin-bottom:10px;">Market Analysis</h3>
                <p style="color:#a1a1aa; font-size:0.9rem;">Automated technical analysis including RSI, MACD, and real-time sentiment scoring.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <h3 style="color:white; margin-bottom:10px;">Risk Engine</h3>
                <p style="color:#a1a1aa; font-size:0.9rem;">Quantitative models designed to minimize drawdown through intelligent asset allocation.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><p style='text-align:center; color:#52525b; font-size:0.8rem; font-weight:700;'>TECH STACK</p>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; justify-content:center; gap:30px; opacity:0.6; filter:grayscale(1); padding: 10px;">
            <span style="color:white; font-size:1.1rem; font-weight:600;">Python</span>
            <span style="color:white; font-size:1.1rem; font-weight:600;">PyTorch</span>
            <span style="color:white; font-size:1.1rem; font-weight:600;">Streamlit</span>
            <span style="color:white; font-size:1.1rem; font-weight:600;">LangChain</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; padding: 2rem 0; color: #71717a; font-size: 0.85rem;">
            <p>Developed by the <b>Data Science Club at Georgia Tech (DSGT)</b></p>
            <p style="max-width: 700px; margin: 0 auto; color: #52525b;">
                <b>Disclaimer:</b> This project is for educational purposes only. Financial decisions 
                should not be made based on this software. We are not liable for any financial losses 
                incurred.
            </p>
        </div>
    """, unsafe_allow_html=True)