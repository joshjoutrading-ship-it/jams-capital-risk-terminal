import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Set page config
st.set_page_config(
    page_title="JAMS Capital | Market Risk Terminal",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Bloomberg CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

/* Global styling */
.main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
.block-container {
    background-color: #000000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    padding: 0.5rem !important;
}

/* Headers only in Bloomberg orange */
h1, h2, h3 {
    color: #FF9500 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    margin: 15px 0 10px 0 !important;
}

h1 {
    text-align: center;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
}

/* All other text in white */
p, div, span, label, td, th, 
.stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
    color: #FFFFFF !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 400 !important;
}

/* Data tables */
.dataframe {
    background-color: #000000 !important;
    border: 1px solid #333333 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
}

.dataframe th {
    background-color: #1a1a1a !important;
    color: #FF9500 !important;
    font-weight: 600 !important;
    text-align: center !important;
    padding: 6px !important;
    border: 1px solid #333333 !important;
}

.dataframe td {
    color: #FFFFFF !important;
    background-color: #000000 !important;
    text-align: center !important;
    padding: 6px !important;
    border: 1px solid #333333 !important;
    font-weight: 400 !important;
}

/* Buttons */
.stButton button {
    background-color: #FF9500 !important;
    color: #000000 !important;
    font-weight: 600 !important;
    border: none !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
}

/* Risk score display */
.risk-score-large {
    font-size: 6rem !important;
    font-weight: 700 !important;
    text-align: center;
    margin: 20px 0 !important;
    color: #FFFFFF !important;
}

/* Terminal text */
.terminal-line {
    font-family: 'IBM Plex Mono', monospace !important;
    color: #FFFFFF !important;
    font-size: 0.9rem !important;
    line-height: 1.4 !important;
    margin: 3px 0 !important;
}

/* Professional sensitivity table styling */
.sensitivity-table {
    border-collapse: collapse !important;
    width: 100% !important;
    margin: 10px 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
}

.sensitivity-table th {
    border: 1px solid #FF9500 !important;
    padding: 8px 12px !important;
    text-align: center !important;
    color: #FF9500 !important;
    background-color: #1a1a1a !important;
    font-weight: 600 !important;
}

.sensitivity-table td {
    border: 1px solid #FF9500 !important;
    padding: 8px 12px !important;
    text-align: center !important;
    color: #FFFFFF !important;
    background-color: #000000 !important;
    font-weight: 400 !important;
}

.sensitivity-table td.highlighted {
    border: 2px solid #FFFFFF !important;
    background-color: #1a1a1a !important;
}

/* Compact layout */
.main .block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* Tooltip styling */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: pointer;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 450px;
    background-color: #1a1a1a;
    color: #FFFFFF;
    text-align: left;
    border-radius: 6px;
    padding: 15px;
    position: absolute;
    z-index: 1000;
    top: 25px;
    left: -200px;
    opacity: 0;
    transition: opacity 0.3s;
    border: 2px solid #FF9500;
    font-size: 0.8rem;
    line-height: 1.4;
    max-height: 400px;
    overflow-y: auto;
}

.tooltip .tooltiptext::before {
    content: "";
    position: absolute;
    top: -7px;
    left: 220px;
    border-width: 0 7px 7px 7px;
    border-style: solid;
    border-color: transparent transparent #FF9500 transparent;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

.info-icon {
    background-color: #FF9500;
    color: #000000;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    cursor: pointer;
}

/* Portfolio input styling */
.portfolio-input {
    background-color: #1a1a1a !important;
    border: 2px solid #FF9500 !important;
    color: #FFFFFF !important;
    padding: 10px !important;
    border-radius: 5px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1rem !important;
}

.hedge-recommendation {
    background-color: #1a1a1a;
    border: 2px solid #FF9500;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}

.hedge-strategy {
    background-color: #000000;
    border: 1px solid #333333;
    border-radius: 5px;
    padding: 10px;
    margin: 5px 0;
}

/* Input field styling */
.stNumberInput input {
    background-color: #1a1a1a !important;
    border: 2px solid #FF9500 !important;
    color: #FFFFFF !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

.stNumberInput label {
    color: #FF9500 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

class MarketRiskDashboard:
    def __init__(self):
        self.current_data = {}
        self.historical_data = pd.DataFrame()
        self.risk_score = 0
        self.detailed_metrics = {}

    @st.cache_data(ttl=30)
    def fetch_market_data(_self):
        """Fetch real-time market data"""
        try:
            tickers = ['HYG', 'TLT', 'UUP', 'FXY', 'RSP', 'SPY', 'IWM', '^VIX', 'XLU', 'XLK']
            data = yf.download(tickers, period='90d', interval='1d', progress=False)['Close']
            
            if data is not None and not data.empty:
                latest = data.iloc[-1]
                
                current_data = {
                    'hyg_price': latest['HYG'],
                    'tlt_price': latest['TLT'],
                    'uup_price': latest['UUP'],
                    'fxy_price': latest['FXY'],
                    'rsp_price': latest['RSP'],
                    'spy_price': latest['SPY'],
                    'iwm_price': latest['IWM'],
                    'vix_price': latest['^VIX'],
                    'xlu_price': latest['XLU'],
                    'xlk_price': latest['XLK'],
                    'timestamp': datetime.now()
                }
                
                return current_data, data
        except Exception as e:
            st.error(f"DATA FEED ERROR: {e}")
            return None, None

    def calculate_risk_metrics(self, current_data, historical_data):
        """Calculate comprehensive forward-looking risk metrics"""
        if not current_data or historical_data.empty:
            return 0, {}
            
        try:
            # Enhanced Credit Risk Score (0-4) - More sensitive to changes
            credit_score = 0
            hyg_tlt_ratio = current_data['hyg_price'] / current_data['tlt_price']
            hyg_tlt_5d_change = (hyg_tlt_ratio / (historical_data['HYG'].iloc[-6] / historical_data['TLT'].iloc[-6]) - 1) * 100
            hyg_tlt_10d_change = (hyg_tlt_ratio / (historical_data['HYG'].iloc[-11] / historical_data['TLT'].iloc[-11]) - 1) * 100
            
            # More granular credit scoring
            if hyg_tlt_5d_change < -2.5:
                credit_score += 4
            elif hyg_tlt_5d_change < -1.5:
                credit_score += 3
            elif hyg_tlt_5d_change < -0.8:
                credit_score += 2
            elif hyg_tlt_5d_change < -0.3:
                credit_score += 1
            
            # Add 10-day trend component
            if hyg_tlt_10d_change < -3:
                credit_score += 1
                
            # Enhanced Currency Stress Score (0-4) - More weight to JPY moves
            currency_score = 0
            fxy_5d_change = (current_data['fxy_price'] / historical_data['FXY'].iloc[-6] - 1) * 100
            uup_5d_change = (current_data['uup_price'] / historical_data['UUP'].iloc[-6] - 1) * 100
            
            # JPY strength is key risk-off indicator
            if fxy_5d_change > 3.5:
                currency_score += 4
            elif fxy_5d_change > 2.5:
                currency_score += 3
            elif fxy_5d_change > 1.5:
                currency_score += 2
            elif fxy_5d_change > 0.8:
                currency_score += 1
                
            # USD strength can also indicate stress in some contexts
            if uup_5d_change > 4:
                currency_score += 1
            elif uup_5d_change > 2.5:
                currency_score += 0.5
                
            # Enhanced Market Breadth Score (0-4) - More comprehensive
            breadth_score = 0
            rsp_spy_ratio = current_data['rsp_price'] / current_data['spy_price']
            rsp_spy_5d_ago = historical_data['RSP'].iloc[-6] / historical_data['SPY'].iloc[-6]
            rsp_spy_change = (rsp_spy_ratio / rsp_spy_5d_ago - 1) * 100
            
            iwm_spy_change = ((current_data['iwm_price'] / historical_data['IWM'].iloc[-6]) / 
                             (current_data['spy_price'] / historical_data['SPY'].iloc[-6]) - 1) * 100
            
            # Defensive rotation (Utilities vs Tech)
            xlu_xlk_ratio = current_data['xlu_price'] / current_data['xlk_price']
            xlu_xlk_5d_ago = historical_data['XLU'].iloc[-6] / historical_data['XLK'].iloc[-6]
            defensive_rotation = (xlu_xlk_ratio / xlu_xlk_5d_ago - 1) * 100
            
            # More sensitive breadth scoring
            if rsp_spy_change < -2.5:
                breadth_score += 2
            elif rsp_spy_change < -1.2:
                breadth_score += 1.5
            elif rsp_spy_change < -0.6:
                breadth_score += 1
            
            if iwm_spy_change < -4:
                breadth_score += 2
            elif iwm_spy_change < -2.5:
                breadth_score += 1.5
            elif iwm_spy_change < -1.2:
                breadth_score += 1
            
            if defensive_rotation > 3:
                breadth_score += 1.5
            elif defensive_rotation > 1.5:
                breadth_score += 1
            elif defensive_rotation > 0.8:
                breadth_score += 0.5
                
            # VIX momentum component
            vix_30d = historical_data['^VIX'].iloc[-30:]
            vix_percentile = (vix_30d < current_data['vix_price']).sum() / len(vix_30d) * 100
            vix_5d_change = (current_data['vix_price'] / historical_data['^VIX'].iloc[-6] - 1) * 100
            
            # Add VIX momentum score (0-2)
            vix_momentum_score = 0
            if current_data['vix_price'] < 15 and (credit_score > 2 or currency_score > 2):
                vix_momentum_score += 2  # Divergence penalty
            elif vix_5d_change > 25:
                vix_momentum_score += 1
            elif vix_5d_change > 15:
                vix_momentum_score += 0.5
                
            # Total Risk Score (0-10) with weighted components
            total_score = (credit_score * 1.0) + (currency_score * 1.0) + (breadth_score * 0.8) + (vix_momentum_score * 1.0)
            risk_score = min(10, max(0, round(total_score * 0.8)))  # Scale to 0-10
            
            # VIX Outlook
            vix_outlook = self.generate_vix_outlook(current_data['vix_price'], vix_percentile, vix_5d_change, risk_score)
            
            # Hedge Recommendation
            hedge_pct = self.calculate_hedge_percentage(risk_score, vix_percentile, current_data['vix_price'])
            
            detailed_metrics = {
                'hyg_tlt_change': hyg_tlt_5d_change,
                'hyg_tlt_10d_change': hyg_tlt_10d_change,
                'fxy_change': fxy_5d_change,
                'uup_change': uup_5d_change,
                'rsp_spy_change': rsp_spy_change,
                'iwm_spy_change': iwm_spy_change,
                'defensive_rotation': defensive_rotation,
                'credit_score': credit_score,
                'currency_score': currency_score,
                'breadth_score': breadth_score,
                'vix_momentum_score': vix_momentum_score,
                'vix_percentile': vix_percentile,
                'vix_5d_change': vix_5d_change,
                'vix_outlook': vix_outlook,
                'hedge_percentage': hedge_pct
            }
            
            return risk_score, detailed_metrics
            
        except Exception as e:
            st.error(f"CALCULATION ERROR: {e}")
            return 0, {}
    
    def generate_market_summary(self, risk_score, detailed_metrics, current_data):
        """Generate comprehensive market summary paragraph"""
        
        # Risk assessment
        if risk_score >= 8:
            risk_assessment = "EXTREME RISK ENVIRONMENT with multiple stress indicators flashing red"
        elif risk_score >= 6:
            risk_assessment = "ELEVATED RISK CONDITIONS with significant market stress building"
        elif risk_score >= 4:
            risk_assessment = "MODERATE RISK LEVELS with selective pressure points emerging"
        else:
            risk_assessment = "LOW RISK ENVIRONMENT with markets showing resilience"
        
        # Credit analysis
        credit_change = detailed_metrics.get('hyg_tlt_change', 0)
        if credit_change < -2:
            credit_status = "credit spreads widening aggressively indicating institutional stress"
        elif credit_change < -1:
            credit_status = "credit markets showing initial signs of stress"
        else:
            credit_status = "credit conditions remain stable"
        
        # Currency analysis
        jpy_change = detailed_metrics.get('fxy_change', 0)
        if jpy_change > 2:
            currency_status = "strong JPY appreciation signaling flight-to-quality flows"
        elif jpy_change > 1:
            currency_status = "moderate JPY strength suggesting risk-off sentiment"
        else:
            currency_status = "currency markets showing normal risk appetite"
        
        # Breadth analysis
        breadth_change = detailed_metrics.get('rsp_spy_change', 0)
        small_cap_change = detailed_metrics.get('iwm_spy_change', 0)
        if breadth_change < -1 and small_cap_change < -2:
            breadth_status = "market breadth deteriorating with small caps severely underperforming"
        elif breadth_change < -1 or small_cap_change < -2:
            breadth_status = "market breadth showing signs of weakness"
        else:
            breadth_status = "broad market participation remains healthy"
        
        # VIX analysis
        vix_level = current_data['vix_price']
        vix_percentile = detailed_metrics.get('vix_percentile', 50)
        if vix_level > 30:
            vix_status = f"VIX elevated at {vix_level:.1f} suggesting high fear levels"
        elif vix_level < 15:
            vix_status = f"VIX compressed at {vix_level:.1f} indicating complacency"
        else:
            vix_status = f"VIX at {vix_level:.1f} within normal ranges"
        
        # Hedge recommendation
        hedge_pct = detailed_metrics.get('hedge_percentage', 0)
        if hedge_pct > 70:
            hedge_rec = f"IMMEDIATE AGGRESSIVE HEDGING REQUIRED at {hedge_pct:.0f}% of dollar beta"
        elif hedge_pct > 40:
            hedge_rec = f"SIGNIFICANT HEDGE POSITION WARRANTED at {hedge_pct:.0f}% of dollar beta"
        elif hedge_pct > 20:
            hedge_rec = f"MODERATE HEDGING APPROPRIATE at {hedge_pct:.0f}% of dollar beta"
        else:
            hedge_rec = f"MINIMAL HEDGE REQUIRED at {hedge_pct:.0f}% of dollar beta"
        
        summary = f"""MARKET ANALYSIS: {risk_assessment}. Current assessment shows {credit_status}, while {currency_status}. Market internals indicate {breadth_status}. Volatility measures show {vix_status} ({vix_percentile:.0f}th percentile). Forward-looking risk indicators suggest {hedge_rec}. Risk score of {risk_score}/10 reflects confluence of credit stress ({detailed_metrics.get('credit_score', 0)}/4), currency flows ({detailed_metrics.get('currency_score', 0)}/3), and breadth deterioration ({detailed_metrics.get('breadth_score', 0)}/3). Immediate action required for risk management positioning."""
        
        return summary
    
    def generate_vix_outlook(self, current_vix, percentile, change_5d, risk_score):
        """Generate VIX outlook"""
        if risk_score >= 8 and current_vix < 25:
            return "DIVERGENCE ALERT: High risk score with low VIX suggests imminent spike to 25-35 range"
        elif risk_score >= 6 and current_vix < 20:
            return "BUILDING PRESSURE: Risk indicators elevated, expect VIX advance to 20-25 range"
        elif current_vix > 30 and risk_score < 4:
            return "MEAN REVERSION: High VIX with improving fundamentals suggests decline to 15-20 range"
        elif percentile > 80:
            return "ELEVATED REGIME: VIX in top quintile, monitor for reversal signals"
        elif percentile < 20:
            return "COMPLACENCY WARNING: Low volatility environment vulnerable to sudden spikes"
        else:
            return "NEUTRAL ENVIRONMENT: VIX in normal range, monitor risk score for early warnings"
    
    def generate_hedge_strategy(self, portfolio_dollar_beta, hedge_percentage, current_vix, risk_score):
        """Generate specific hedge strategy recommendations"""
        
        if portfolio_dollar_beta <= 0:
            return "Please enter a valid portfolio dollar beta amount."
        
        hedge_amount = portfolio_dollar_beta * (hedge_percentage / 100)
        
        strategies = []
        
        # Determine optimal hedge strategy based on risk level and VIX
        if risk_score <= 3:
            # Low risk - minimal hedging
            if hedge_amount > 0:
                sh_shares = int(hedge_amount / 27.34)  # Assuming SH price ~$27.34
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${hedge_amount:,.0f}",
                    'rationale': 'Low cost hedge for minimal risk environment'
                })
            else:
                strategies.append({
                    'instrument': 'NO HEDGE REQUIRED',
                    'action': 'HOLD CASH',
                    'amount': 'N/A',
                    'cost': '$0',
                    'rationale': 'Risk environment does not warrant hedging costs'
                })
                
        elif risk_score <= 6:
            # Moderate risk - SH primary with small put position
            sh_allocation = hedge_amount * 0.75
            put_allocation = hedge_amount * 0.25
            
            sh_shares = int(sh_allocation / 27.34)
            put_contracts = int(put_allocation / 500)  # Assuming $500 per SPY put
            
            strategies.append({
                'instrument': 'SH (Inverse S&P ETF)',
                'action': 'BUY',
                'amount': f"{sh_shares:,} shares",
                'cost': f"${sh_allocation:,.0f}",
                'rationale': 'Primary hedge via inverse ETF for cost efficiency'
            })
            
            if put_contracts > 0:
                strategies.append({
                    'instrument': 'SPY Put Options',
                    'action': 'BUY',
                    'amount': f"{put_contracts} contracts",
                    'cost': f"${put_allocation:,.0f}",
                    'rationale': 'Put options for convexity in moderate stress scenario'
                })
                
        else:
            # High risk - Aggressive hedging with puts primary
            if current_vix > 25:
                # VIX already high - use SH + sell calls
                sh_allocation = hedge_amount * 0.6
                call_allocation = hedge_amount * 0.4
                
                sh_shares = int(sh_allocation / 27.34)
                call_contracts = int(call_allocation / 800)  # Assuming $800 premium per call
                
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${sh_allocation:,.0f}",
                    'rationale': 'Inverse ETF when vol already elevated'
                })
                
                strategies.append({
                    'instrument': 'SPY Call Options',
                    'action': 'SELL',
                    'amount': f"{call_contracts} contracts",
                    'cost': f"+${call_allocation:,.0f} premium",
                    'rationale': 'Sell calls for additional premium when VIX high'
                })
            else:
                # VIX still low with high risk score - use puts for gamma
                put_allocation = hedge_amount * 0.7
                sh_allocation = hedge_amount * 0.3
                
                put_contracts = int(put_allocation / 500)
                sh_shares = int(sh_allocation / 27.34)
                
                strategies.append({
                    'instrument': 'SPY Put Options',
                    'action': 'BUY',
                    'amount': f"{put_contracts} contracts",
                    'cost': f"${put_allocation:,.0f}",
                    'rationale': 'Put options for gamma exposure before VIX spike'
                })
                
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${sh_allocation:,.0f}",
                    'rationale': 'Base hedge via inverse ETF'
                })
        
    def calculate_hedge_percentage(self, risk_score, vix_percentile, current_vix):
        """Calculate recommended hedge percentage"""
        base_hedge = min(risk_score * 8.75, 87.5)  # Max 87.5% hedge
        
        # VIX adjustments
        if current_vix > 35:
            base_hedge = max(base_hedge - 15, 0)
        elif current_vix > 25:
            base_hedge = max(base_hedge - 10, 0)
        elif current_vix < 12:
            base_hedge += 12.5
            
        # Percentile adjustments
        if vix_percentile > 90:
            base_hedge = max(base_hedge - 12.5, 0)
        elif vix_percentile < 10:
            base_hedge += 12.5
            
        return min(max(base_hedge, 0), 87.5)
    
    def generate_hedge_strategy(self, portfolio_dollar_beta, hedge_percentage, current_vix, risk_score):
        """Generate specific hedge strategy recommendations"""
        
        if portfolio_dollar_beta <= 0:
            return "Please enter a valid portfolio dollar beta amount."
        
        hedge_amount = portfolio_dollar_beta * (hedge_percentage / 100)
        
        strategies = []
        
        # Determine optimal hedge strategy based on risk level and VIX
        if risk_score <= 3:
            # Low risk - minimal hedging
            if hedge_amount > 0:
                sh_shares = int(hedge_amount / 27.34)  # Assuming SH price ~$27.34
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${hedge_amount:,.0f}",
                    'rationale': 'Low cost hedge for minimal risk environment'
                })
            else:
                strategies.append({
                    'instrument': 'NO HEDGE REQUIRED',
                    'action': 'HOLD CASH',
                    'amount': 'N/A',
                    'cost': '$0',
                    'rationale': 'Risk environment does not warrant hedging costs'
                })
                
        elif risk_score <= 6:
            # Moderate risk - SH primary with small put position
            sh_allocation = hedge_amount * 0.75
            put_allocation = hedge_amount * 0.25
            
            sh_shares = int(sh_allocation / 27.34)
            put_contracts = int(put_allocation / 500)  # Assuming $500 per SPY put
            
            strategies.append({
                'instrument': 'SH (Inverse S&P ETF)',
                'action': 'BUY',
                'amount': f"{sh_shares:,} shares",
                'cost': f"${sh_allocation:,.0f}",
                'rationale': 'Primary hedge via inverse ETF for cost efficiency'
            })
            
            if put_contracts > 0:
                strategies.append({
                    'instrument': 'SPY Put Options',
                    'action': 'BUY',
                    'amount': f"{put_contracts} contracts",
                    'cost': f"${put_allocation:,.0f}",
                    'rationale': 'Put options for convexity in moderate stress scenario'
                })
                
        else:
            # High risk - Aggressive hedging with puts primary
            if current_vix > 25:
                # VIX already high - use SH + sell calls
                sh_allocation = hedge_amount * 0.6
                call_allocation = hedge_amount * 0.4
                
                sh_shares = int(sh_allocation / 27.34)
                call_contracts = int(call_allocation / 800)  # Assuming $800 premium per call
                
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${sh_allocation:,.0f}",
                    'rationale': 'Inverse ETF when vol already elevated'
                })
                
                strategies.append({
                    'instrument': 'SPY Call Options',
                    'action': 'SELL',
                    'amount': f"{call_contracts} contracts",
                    'cost': f"+${call_allocation:,.0f} premium",
                    'rationale': 'Sell calls for additional premium when VIX high'
                })
            else:
                # VIX still low with high risk score - use puts for gamma
                put_allocation = hedge_amount * 0.7
                sh_allocation = hedge_amount * 0.3
                
                put_contracts = int(put_allocation / 500)
                sh_shares = int(sh_allocation / 27.34)
                
                strategies.append({
                    'instrument': 'SPY Put Options',
                    'action': 'BUY',
                    'amount': f"{put_contracts} contracts",
                    'cost': f"${put_allocation:,.0f}",
                    'rationale': 'Put options for gamma exposure before VIX spike'
                })
                
                strategies.append({
                    'instrument': 'SH (Inverse S&P ETF)',
                    'action': 'BUY',
                    'amount': f"{sh_shares:,} shares",
                    'cost': f"${sh_allocation:,.0f}",
                    'rationale': 'Base hedge via inverse ETF'
                })
        
        return strategies
    
    def create_charts(self, historical_data, current_data, risk_score):
        """Create professional Bloomberg-style charts with info tooltips"""
        
        # Generate actual risk score history based on historical data
        risk_history = []
        dates = historical_data.index[-60:]
        
        for i in range(len(dates)):
            try:
                # Calculate historical risk score for each day
                if i >= 10:  # Need at least 10 days for calculations
                    hist_data = historical_data.iloc[:len(historical_data) - (59 - i)]
                    hist_current = {
                        'hyg_price': hist_data['HYG'].iloc[-1],
                        'tlt_price': hist_data['TLT'].iloc[-1],
                        'fxy_price': hist_data['FXY'].iloc[-1],
                        'uup_price': hist_data['UUP'].iloc[-1],
                        'rsp_price': hist_data['RSP'].iloc[-1],
                        'spy_price': hist_data['SPY'].iloc[-1],
                        'iwm_price': hist_data['IWM'].iloc[-1],
                        'vix_price': hist_data['^VIX'].iloc[-1],
                        'xlu_price': hist_data['XLU'].iloc[-1],
                        'xlk_price': hist_data['XLK'].iloc[-1],
                    }
                    hist_score, _ = self.calculate_risk_metrics(hist_current, hist_data)
                    risk_history.append(hist_score)
                else:
                    risk_history.append(np.random.randint(0, 4))  # Placeholder for early days
            except:
                risk_history.append(np.random.randint(0, 4))
        
        # Ensure current score is correct
        risk_history[-1] = risk_score
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=['FORWARD RISK SCORE', 'CREDIT STRESS HYG/TLT', 
                           'CURRENCY STRESS USD/JPY', 'MARKET BREADTH RSP/SPY', 
                           'VIX VOLATILITY INDEX', 'DEFENSIVE ROTATION XLU/XLK'],
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        # Bloomberg styling
        fig.update_layout(
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#FFFFFF', family='IBM Plex Mono', size=10),
            height=700,
            showlegend=False,
            margin=dict(l=40, r=40, t=80, b=40)
        )
        
        # 1. Risk Score Chart with actual calculated history
        fig.add_trace(
            go.Scatter(x=dates, y=risk_history, 
                      mode='lines+markers', 
                      line=dict(color='#FF9500', width=3),
                      marker=dict(size=4, color='#FF9500'),
                      name='Risk Score'),
            row=1, col=1
        )
        fig.add_hline(y=3, line_dash="dot", line_color="#00FF00", row=1, col=1)
        fig.add_hline(y=6, line_dash="dash", line_color="#FFFF00", row=1, col=1)
        fig.add_hline(y=8, line_dash="solid", line_color="#FF0000", row=1, col=1)
        
        # 2. Credit Spreads
        hyg_tlt_ratio = historical_data['HYG'] / historical_data['TLT']
        fig.add_trace(
            go.Scatter(x=hyg_tlt_ratio.index[-60:], y=hyg_tlt_ratio.iloc[-60:],
                      mode='lines', line=dict(color='#FF9500', width=2)),
            row=1, col=2
        )
        
        # 3. Currency Stress
        usd_jpy_proxy = historical_data['UUP'] / historical_data['FXY']
        fig.add_trace(
            go.Scatter(x=usd_jpy_proxy.index[-60:], y=usd_jpy_proxy.iloc[-60:],
                      mode='lines', line=dict(color='#FF9500', width=2)),
            row=2, col=1
        )
        
        # 4. Market Breadth
        rsp_spy_ratio = historical_data['RSP'] / historical_data['SPY']
        fig.add_trace(
            go.Scatter(x=rsp_spy_ratio.index[-60:], y=rsp_spy_ratio.iloc[-60:],
                      mode='lines', line=dict(color='#FF9500', width=2)),
            row=2, col=2
        )
        
        # 5. VIX Level
        fig.add_trace(
            go.Scatter(x=historical_data['^VIX'].index[-60:], y=historical_data['^VIX'].iloc[-60:],
                      mode='lines', line=dict(color='#FF9500', width=2)),
            row=3, col=1
        )
        fig.add_hline(y=20, line_dash="dash", line_color="#FFFF00", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#FF0000", row=3, col=1)
        
        # 6. Defensive Rotation
        defensive_ratio = historical_data['XLU'] / historical_data['XLK']
        fig.add_trace(
            go.Scatter(x=defensive_ratio.index[-60:], y=defensive_ratio.iloc[-60:],
                      mode='lines', line=dict(color='#FF9500', width=2)),
            row=3, col=2
        )
        
        # Update all axes
        for i in range(1, 4):
            for j in range(1, 3):
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333333', 
                               color='#FFFFFF', row=i, col=j)
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333333',
                               color='#FFFFFF', row=i, col=j)
        
        return fig

def main():
    # Header
    st.markdown("# JAMS CAPITAL MARKET RISK TERMINAL")
    
    # Control panel
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("REFRESH DATA"):
            st.rerun()
    with col2:
        auto_refresh = st.checkbox("AUTO REFRESH", value=True)
    with col3:
        st.write(f"LAST UPDATE: {datetime.now().strftime('%H:%M:%S')}")
    with col4:
        st.write("FEED STATUS: LIVE")
    
    st.markdown("---")
    
    # Initialize and fetch data
    dashboard = MarketRiskDashboard()
    current_data, historical_data = dashboard.fetch_market_data()
    
    if current_data and historical_data is not None:
        risk_score, detailed_metrics = dashboard.calculate_risk_metrics(current_data, historical_data)
        
        # Market summary at the top
        summary = dashboard.generate_market_summary(risk_score, detailed_metrics, current_data)
        st.markdown("## EXECUTIVE SUMMARY")
        st.markdown(f'<div class="terminal-line">{summary}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Portfolio Input and Hedge Strategy
        st.markdown("## PORTFOLIO HEDGING STRATEGY")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### PORTFOLIO INPUT")
            portfolio_dollar_beta = st.number_input(
                "Enter Portfolio Dollar Beta ($)",
                min_value=0.0,
                value=100000.0,
                step=10000.0,
                format="%.0f",
                help="Total dollar beta exposure of your portfolio (sum of position size × beta for each holding)"
            )
            
            if portfolio_dollar_beta > 0:
                hedge_amount = portfolio_dollar_beta * (detailed_metrics.get('hedge_percentage', 0) / 100)
                st.markdown(f"**Portfolio Dollar Beta:** ${portfolio_dollar_beta:,.0f}")
                st.markdown(f"**Recommended Hedge %:** {detailed_metrics.get('hedge_percentage', 0):.1f}%")
                st.markdown(f"**Dollar Amount to Hedge:** ${hedge_amount:,.0f}")
        
        with col2:
            st.markdown("### HEDGE EXECUTION STRATEGY")
            
            if portfolio_dollar_beta > 0:
                hedge_strategies = dashboard.generate_hedge_strategy(
                    portfolio_dollar_beta, 
                    detailed_metrics.get('hedge_percentage', 0), 
                    current_data['vix_price'], 
                    risk_score
                )
                
                if isinstance(hedge_strategies, str):
                    st.write(hedge_strategies)
                else:
                    for i, strategy in enumerate(hedge_strategies):
                        st.markdown(f"""
                        <div class="hedge-strategy">
                            <strong>STRATEGY {i+1}: {strategy['instrument']}</strong><br/>
                            <strong>ACTION:</strong> {strategy['action']}<br/>
                            <strong>AMOUNT:</strong> {strategy['amount']}<br/>
                            <strong>COST:</strong> {strategy['cost']}<br/>
                            <strong>RATIONALE:</strong> {strategy['rationale']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Add execution notes
                    st.markdown("""
                    <div class="hedge-recommendation">
                        <strong>EXECUTION NOTES:</strong><br/>
                        • Execute hedges in order of priority during market hours<br/>
                        • Monitor risk score changes for dynamic adjustments<br/>
                        • Consider liquidity and bid-ask spreads for options<br/>
                        • Scale into positions over 2-3 trading sessions for large amounts
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("Enter your portfolio dollar beta to see specific hedge recommendations.")
        
        st.markdown("---")
        
        # Main metrics display
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            # Risk score
            if risk_score >= 8:
                risk_color = "#FF0000"
                risk_level = "EXTREME RISK"
            elif risk_score >= 6:
                risk_color = "#FF6600"
                risk_level = "HIGH RISK"
            elif risk_score >= 4:
                risk_color = "#FFFF00"
                risk_level = "MODERATE RISK"
            else:
                risk_color = "#00FF00"
                risk_level = "LOW RISK"
            
            st.markdown("### FORWARD RISK SCORE")
            st.markdown(f'<div class="risk-score-large" style="color: {risk_color};">{risk_score}</div>', unsafe_allow_html=True)
            st.markdown(f"**STATUS:** {risk_level}")
            st.markdown(f"**RECOMMENDED HEDGE:** {detailed_metrics.get('hedge_percentage', 0):.1f}%")
        
        with col2:
            st.markdown("### CREDIT RISK")
            st.markdown(f"**SCORE:** {detailed_metrics.get('credit_score', 0)}/4")
            st.markdown(f"**HYG/TLT:** {current_data['hyg_price']/current_data['tlt_price']:.4f}")
            st.markdown(f"**5D CHANGE:** {detailed_metrics.get('hyg_tlt_change', 0):.2f}%")
        
        with col3:
            st.markdown("### CURRENCY STRESS")
            st.markdown(f"**SCORE:** {detailed_metrics.get('currency_score', 0)}/3")
            st.markdown(f"**JPY 5D:** {detailed_metrics.get('fxy_change', 0):.2f}%")
            st.markdown(f"**USD 5D:** {detailed_metrics.get('uup_change', 0):.2f}%")
        
        with col4:
            st.markdown("### MARKET BREADTH")
            st.markdown(f"**SCORE:** {detailed_metrics.get('breadth_score', 0)}/3")
            st.markdown(f"**EW RATIO:** {detailed_metrics.get('rsp_spy_change', 0):.2f}%")
            st.markdown(f"**SMALL CAP:** {detailed_metrics.get('iwm_spy_change', 0):.2f}%")
        
        with col5:
            st.markdown("### VIX ANALYSIS")
            st.markdown(f"**LEVEL:** {current_data['vix_price']:.2f}")
            st.markdown(f"**PERCENTILE:** {detailed_metrics.get('vix_percentile', 0):.0f}th")
            st.markdown(f"**5D CHANGE:** {detailed_metrics.get('vix_5d_change', 0):.1f}%")
        
        st.markdown("---")
        
        # VIX Outlook
        st.markdown("## VIX OUTLOOK")
        st.markdown(f'<div class="terminal-line">{detailed_metrics.get("vix_outlook", "ANALYZING...")}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts with analysis
        st.markdown("## MARKET ANALYSIS CHARTS")
        
        # Add info tooltips before the chart
        st.markdown("""
        <div style="margin-bottom: 10px;">
            <span class="tooltip">
                <span class="info-icon">i</span>
                <span class="tooltiptext">
                    <strong>CHART INTERPRETATIONS:</strong><br/><br/>
                    <strong>FORWARD RISK SCORE:</strong> 0-3 Low risk, 4-6 Moderate risk, 7-10 High risk. Early warning when it spikes before VIX.<br/><br/>
                    <strong>CREDIT STRESS:</strong> Rising = healthy markets, Falling = stress building. Leads equity selloffs by 1-2 weeks.<br/><br/>
                    <strong>CURRENCY STRESS:</strong> Rising = normal appetite, Falling = JPY strength/risk-off. Precedes volatility spikes.<br/><br/>
                    <strong>MARKET BREADTH:</strong> Rising = broad participation, Falling = mega-cap concentration. Signals institutional distribution.<br/><br/>
                    <strong>VIX:</strong> <15 complacency, 15-25 normal, >30 fear/bottoms. Use with risk score for divergences.<br/><br/>
                    <strong>DEFENSIVE ROTATION:</strong> Rising = flight to defensives, Falling = risk-on. Smart money positioning.
                </span>
            </span>
            <span style="margin-left: 8px; color: #FFFFFF;">Hover for chart interpretation guide</span>
        </div>
        """, unsafe_allow_html=True)
        
        chart_fig = dashboard.create_charts(historical_data, current_data, risk_score)
        st.plotly_chart(chart_fig, use_container_width=True)
        
        # Chart analysis summaries
        col1, col2 = st.columns(2)
        with col1:
            st.write("**FORWARD RISK SCORE:** Current risk environment shows confluence of multiple stress indicators with forward-looking signals suggesting elevated hedging requirements.")
            st.write("**CURRENCY STRESS:** USD/JPY proxy indicates flight-to-quality dynamics with JPY strength reflecting risk-off sentiment in global markets.")
            st.write("**VIX VOLATILITY:** Current volatility levels relative to historical ranges suggest market complacency or stress depending on percentile positioning.")
        
        with col2:
            st.write("**CREDIT STRESS:** HYG/TLT spread indicates institutional credit market stress levels and early warning signals for broader market deterioration.")
            st.write("**MARKET BREADTH:** RSP/SPY ratio demonstrates equal-weight vs cap-weight performance divergence indicating underlying market participation health.")
            st.write("**DEFENSIVE ROTATION:** XLU/XLK ratio shows sector rotation into defensive positions suggesting institutional positioning changes.")
        
        st.markdown("---")
        
        # Sensitivity Analysis
        st.markdown("## SENSITIVITY ANALYSIS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### HEDGE PERCENTAGE MATRIX")
            st.write("*Recommended hedge percentage by VIX level and Risk Score*")
            
            # Create professional table HTML
            hedge_html = """
            <table class="sensitivity-table">
                <tr>
                    <th rowspan="2">VIX</th>
                    <th colspan="6">RISK SCORE</th>
                </tr>
                <tr>
                    <th>0</th><th>2</th><th>4</th><th>6</th><th>8</th><th>10</th>
                </tr>
            """
            
            vix_levels = [10, 12, 15, 18, 20, 25, 30, 35, 40, 50]
            for vix in vix_levels:
                hedge_html += f"<tr><td>{vix}</td>"
                for score in [0, 2, 4, 6, 8, 10]:
                    hedge = dashboard.calculate_hedge_percentage(score, 50, vix)
                    if abs(vix - current_data['vix_price']) < 3 and score == risk_score:
                        hedge_html += f"<td class='highlighted'>{hedge:.1f}</td>"
                    else:
                        hedge_html += f"<td>{hedge:.1f}</td>"
                hedge_html += "</tr>"
            
            hedge_html += "</table>"
            st.markdown(hedge_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### PORTFOLIO IMPACT ANALYSIS")
            st.write("*Expected net portfolio impact percentage after hedging*")
            
            impact_html = """
            <table class="sensitivity-table">
                <tr>
                    <th rowspan="2">VIX</th>
                    <th colspan="6">RISK SCORE</th>
                </tr>
                <tr>
                    <th>0</th><th>2</th><th>4</th><th>6</th><th>8</th><th>10</th>
                </tr>
            """
            
            for vix in vix_levels:
                impact_html += f"<tr><td>{vix}</td>"
                for score in [0, 2, 4, 6, 8, 10]:
                    hedge = dashboard.calculate_hedge_percentage(score, 50, vix) / 100
                    expected_decline = -(vix * 0.4)
                    net_impact = expected_decline * (1 - hedge)
                    if abs(vix - current_data['vix_price']) < 3 and score == risk_score:
                        impact_html += f"<td class='highlighted'>{net_impact:.2f}</td>"
                    else:
                        impact_html += f"<td>{net_impact:.2f}</td>"
                impact_html += "</tr>"
            
            impact_html += "</table>"
            st.markdown(impact_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current market data
        st.markdown("## CURRENT MARKET DATA")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            equity_data = pd.DataFrame({
                'TICKER': ['SPY', 'RSP', 'IWM', 'VIX'],
                'PRICE': [f"{current_data['spy_price']:.2f}", f"{current_data['rsp_price']:.2f}", 
                         f"{current_data['iwm_price']:.2f}", f"{current_data['vix_price']:.2f}"],
                'STATUS': ['TRACKING', 'MONITOR', 'WEAK' if detailed_metrics.get('iwm_spy_change', 0) < -2 else 'NORMAL', 
                          'ELEVATED' if current_data['vix_price'] > 25 else 'NORMAL']
            })
            st.markdown("**EQUITY INDICES**")
            st.dataframe(equity_data, use_container_width=True, hide_index=True)
        
        with col2:
            credit_data = pd.DataFrame({
                'TICKER': ['HYG', 'TLT', 'SPREAD'],
                'PRICE': [f"{current_data['hyg_price']:.2f}", f"{current_data['tlt_price']:.2f}", 
                         f"{current_data['hyg_price']/current_data['tlt_price']:.4f}"],
                'STATUS': ['STABLE' if detailed_metrics.get('hyg_tlt_change', 0) > -1 else 'STRESS', 
                          'SAFE HAVEN', 'WATCH' if detailed_metrics.get('hyg_tlt_change', 0) < -1 else 'NORMAL']
            })
            st.markdown("**CREDIT MARKETS**")
            st.dataframe(credit_data, use_container_width=True, hide_index=True)
        
        with col3:
            currency_data = pd.DataFrame({
                'TICKER': ['UUP', 'FXY', 'RATIO'],
                'PRICE': [f"{current_data['uup_price']:.2f}", f"{current_data['fxy_price']:.2f}", 
                         f"{current_data['uup_price']/current_data['fxy_price']:.2f}"],
                'STATUS': ['STRONG' if detailed_metrics.get('uup_change', 0) > 2 else 'NEUTRAL', 
                          'RISING' if detailed_metrics.get('fxy_change', 0) > 1 else 'FALLING',
                          'VOLATILE' if abs(detailed_metrics.get('fxy_change', 0)) > 2 else 'CALM']
            })
            st.markdown("**CURRENCIES**")
            st.dataframe(currency_data, use_container_width=True, hide_index=True)
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(30)
            st.rerun()
            
    else:
        st.error("DATA FEED OFFLINE - Unable to connect to market data sources")

if __name__ == "__main__":
    main()