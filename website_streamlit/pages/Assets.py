import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def linear_regression_next(y: np.ndarray) -> float:
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    return float(intercept + slope * len(y))


def ema_next(y: np.ndarray, span: int = 10) -> float:
    return float(pd.Series(y).ewm(span=span, adjust=False).mean().iloc[-1])


def knn_next(close: pd.Series, window: int = 5, k: int = 5) -> float:
    values = close.values
    if len(values) < window + 6:
        return float(values[-1])

    patterns = []
    for i in range(window, len(values) - 1):
        seq = values[i - window:i]
        base = seq[0]
        if base == 0:
            continue
        norm_seq = (seq / base) - 1
        next_return = (values[i + 1] / values[i]) - 1
        patterns.append((norm_seq, next_return))

    current = values[-window:]
    current_base = current[0]
    current_norm = (current / current_base) - 1

    distances = []
    for seq, next_return in patterns:
        dist = np.linalg.norm(seq - current_norm)
        distances.append((dist, next_return))

    nearest = sorted(distances, key=lambda x: x[0])[:k]
    avg_return = np.mean([x[1] for x in nearest]) if nearest else 0
    return float(values[-1] * (1 + avg_return))


def prepare_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    df["Return"] = df["Close"].pct_change()
    df["MA_5"] = df["Close"].rolling(5).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["Volatility_20"] = df["Return"].rolling(20).std() * np.sqrt(252)
    df["RSI_14"] = compute_rsi(df["Close"], 14)

    return df.dropna().copy()


def metric_card(title: str, value: str, delta: str | None = None):
    delta_html = f"<p class='metric-delta'>{delta}</p>" if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <p class="metric-label">{title}</p>
            <h3 class="metric-value">{value}</h3>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def prediction_card(title: str, price: float, delta_pct: float, subtitle: str):
    color = "#10b981" if delta_pct >= 0 else "#f43f5e"
    st.markdown(
        f"""
        <div class="feature-card prediction-card">
            <div class="prediction-top">
                <h3>{title}</h3>
                <span class="prediction-badge">model</span>
            </div>
            <div class="prediction-price">${price:,.2f}</div>
            <p class="prediction-delta" style="color:{color};">{delta_pct:+.2f}% vs latest close</p>
            <p class="prediction-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def app():
    st.markdown("""
    <style>
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
        text-align: center;
    }

    .feature-card, .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
        height: 100%;
    }
    .feature-card:hover, .metric-card:hover {
        transform: translateY(-5px);
        border-color: #8B5CF6;
        background: rgba(139, 92, 246, 0.05);
    }

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

    .section-label {
        text-align: center;
        color: #52525b;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin: 2rem 0 0.8rem 0;
    }

    .metric-label {
        color: #a1a1aa;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        color: white;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .metric-delta {
        color: #71717a;
        font-size: 0.88rem;
        margin-top: 0.6rem;
        margin-bottom: 0;
    }

    .prediction-card h3 {
        color: white;
        margin: 0;
        font-size: 1.05rem;
    }
    .prediction-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.8rem;
    }
    .prediction-badge {
        color: #B3A369;
        border: 1px solid rgba(179, 163, 105, 0.35);
        background: rgba(179, 163, 105, 0.08);
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .prediction-price {
        color: white;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }
    .prediction-delta, .prediction-subtitle {
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    .prediction-subtitle {
        color: #a1a1aa;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-container">
            <div class="gt-badge">GEORGIA TECH • DSGT EXECUTIVE PROJECT</div>
            <h1 class="hero-title">Investment Assets</h1>
            <p class="hero-subtitle">
                Monitor live market behavior, inspect technical signals, and compare lightweight next-day forecasting models.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("Asset Controls")
        ticker = st.text_input("Enter Ticker Symbol", value="AAPL").upper().strip()
        period = st.selectbox("Data Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)
        interval = st.selectbox("Interval", ["1d", "1wk"], index=0)
        show_volume = st.checkbox("Show Volume", value=True)

    try:
        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
        return

    if data.empty:
        st.error(f"No data returned for {ticker}. Try another symbol or a longer period.")
        return

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [c[0] if isinstance(c, tuple) else c for c in data.columns]

    data = data.dropna().copy()
    features = prepare_features(data)

    if features.empty or len(features) < 25:
        st.warning("Not enough history to compute indicators and forecasts reliably.")
        st.dataframe(data.tail(10), use_container_width=True)
        return

    close = features["Close"]
    last_close = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    day_change_pct = ((last_close - prev_close) / prev_close) * 100
    period_return_pct = ((last_close - float(close.iloc[0])) / float(close.iloc[0])) * 100
    volatility = float(features["Volatility_20"].iloc[-1] * 100)
    rsi = float(features["RSI_14"].iloc[-1])

    window = min(30, len(close))
    knn_pred = knn_next(close, window=5, k=5)
    ema_pred = ema_next(close.tail(window).values, span=10)
    lr_pred = linear_regression_next(close.tail(window).values)
    ensemble_pred = float(np.mean([knn_pred, ema_pred, lr_pred]))

    st.markdown("<p class='section-label'>MARKET SNAPSHOT</p>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Last Close", f"${last_close:,.2f}", f"{day_change_pct:+.2f}% vs previous close")
    with m2:
        metric_card("Period Return", f"{period_return_pct:+.2f}%")
    with m3:
        metric_card("Annualized Volatility", f"{volatility:.2f}%")
    with m4:
        metric_card("RSI (14)", f"{rsi:.1f}", "Momentum indicator")

    st.markdown("<p class='section-label'>PRICE HISTORY</p>", unsafe_allow_html=True)
    chart_df = pd.DataFrame({
        "Close": features["Close"],
        "MA 5": features["MA_5"],
        "MA 20": features["MA_20"],
    })
    st.line_chart(chart_df, use_container_width=True)

    if show_volume and "Volume" in data.columns:
        st.markdown("<p class='section-label'>TRADING VOLUME</p>", unsafe_allow_html=True)
        st.bar_chart(data[["Volume"]].tail(60), use_container_width=True)

    st.markdown("<p class='section-label'>NEXT-DAY MODELS</p>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        prediction_card("kNN Prediction", knn_pred, ((knn_pred - last_close) / last_close) * 100, "Nearest historical patterns")
    with p2:
        prediction_card("EMA Trend", ema_pred, ((ema_pred - last_close) / last_close) * 100, "Exponential smoothing signal")
    with p3:
        prediction_card("Linear Trend", lr_pred, ((lr_pred - last_close) / last_close) * 100, "Short-window regression fit")
    with p4:
        prediction_card("Ensemble Forecast", ensemble_pred, ((ensemble_pred - last_close) / last_close) * 100, "Average of the model stack")

    st.markdown("<br><p style='text-align:center; color:#52525b; font-size:0.8rem; font-weight:700;'>MODEL DIAGNOSTICS</p>", unsafe_allow_html=True)
    diagnostics = pd.DataFrame({
        "Metric": [
            "Latest Close",
            "5-Day Moving Average",
            "20-Day Moving Average",
            "Annualized Volatility",
            "RSI (14)",
            "Period Return"
        ],
        "Value": [
            f"${last_close:,.2f}",
            f"${features['MA_5'].iloc[-1]:,.2f}",
            f"${features['MA_20'].iloc[-1]:,.2f}",
            f"{volatility:.2f}%",
            f"{rsi:.1f}",
            f"{period_return_pct:+.2f}%"
        ],
        "Interpretation": [
            "Most recent adjusted close used as the anchor for all forecasts.",
            "Short-term momentum baseline.",
            "Medium-term direction baseline.",
            "Higher values generally mean noisier one-step predictions.",
            "Above 70 may be overbought; below 30 may be oversold.",
            "Net move across the chosen analysis window."
        ]
    })
    st.dataframe(diagnostics, use_container_width=True, hide_index=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; padding: 2rem 0; color: #71717a; font-size: 0.85rem;">
            <p>Developed in the <b>RoboInvesting</b> project style</p>
            <p style="max-width: 700px; margin: 0 auto; color: #52525b;">
                <b>Disclaimer:</b> This page is for educational and exploratory analysis only. 
                Predictions shown here are lightweight models and should not be used as financial advice.
            </p>
        </div>
    """, unsafe_allow_html=True)
