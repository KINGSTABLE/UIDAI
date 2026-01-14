import os
import sys
import subprocess
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from fpdf import FPDF
import networkx as nx
import json

# --- PROJECT CONFIGURATION ---
PROJECT_DIR = "UIDAI_AIGAP_ULTIMATE"
MODULES_DIR = os.path.join(PROJECT_DIR, "modules")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")

# --- ENHANCED FILE CONTENTS ---

# 1. requirements.txt
requirements_content = """streamlit
pandas>=2.0.0
numpy
scikit-learn
plotly
statsmodels
fpdf
openpyxl
xlsxwriter
networkx
streamlit-aggrid
streamlit-folium
folium
python-docx
pydeck
"""

# 2. data_generator.py (Enhanced with Governance Metrics)
data_generator_content = '''import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

def generate_ultimate_data(num_records=50000):
    """
    Generate comprehensive data with governance metrics
    """
    print("🚀 Generating Ultimate Dataset (50,000 records)...")
    
    # Enhanced Geo-Database with Tier Classification
    geo_db = {
        'Maharashtra': {
            'tier': 'Tier-1',
            'districts': {
                'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'zones': ['South', 'West', 'Central']},
                'Pune': {'lat': 18.5204, 'lon': 73.8567, 'zones': ['Central', 'West']},
                'Nagpur': {'lat': 21.1458, 'lon': 79.0882, 'zones': ['North']},
                'Thane': {'lat': 19.2183, 'lon': 72.9781, 'zones': ['West']}
            }
        },
        'Delhi': {
            'tier': 'Tier-1',
            'districts': {
                'New Delhi': {'lat': 28.6139, 'lon': 77.2090, 'zones': ['Central']},
                'South Delhi': {'lat': 28.5246, 'lon': 77.2196, 'zones': ['South']},
                'North Delhi': {'lat': 28.7041, 'lon': 77.1025, 'zones': ['North']}
            }
        },
        'Karnataka': {
            'tier': 'Tier-1',
            'districts': {
                'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'zones': ['East', 'West', 'North', 'South']},
                'Mysore': {'lat': 12.2958, 'lon': 76.6394, 'zones': ['Central']}
            }
        },
        'Tamil Nadu': {
            'tier': 'Tier-1',
            'districts': {
                'Chennai': {'lat': 13.0827, 'lon': 80.2707, 'zones': ['Central', 'South']},
                'Coimbatore': {'lat': 11.0168, 'lon': 76.9558, 'zones': ['Central']}
            }
        },
        'Uttar Pradesh': {
            'tier': 'Tier-2',
            'districts': {
                'Lucknow': {'lat': 26.8467, 'lon': 80.9462, 'zones': ['Central']},
                'Kanpur': {'lat': 26.4499, 'lon': 80.3319, 'zones': ['Central']},
                'Ghaziabad': {'lat': 28.6692, 'lon': 77.4538, 'zones': ['West']}
            }
        },
        'Gujarat': {
            'tier': 'Tier-2',
            'districts': {
                'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'zones': ['Central']},
                'Surat': {'lat': 21.1702, 'lon': 72.8311, 'zones': ['South']}
            }
        }
    }
    
    update_types = ['Biometric Update', 'Address Change', 'Mobile Link', 'DOB Correction', 'Name Change']
    statuses = ['Success', 'Rejected', 'Pending', 'Flagged for Fraud']
    rejection_reasons = [
        'Document Mismatch', 'Biometric Failure', 'Duplicate Request',
        'Data Inconsistency', 'Network Failure', 'Verification Pending'
    ]
    
    # Operator Performance Profiles
    operator_profiles = {
        'High': {'error_rate': 0.01, 'speed': 1.2, 'satisfaction_boost': 0.5},
        'Medium': {'error_rate': 0.05, 'speed': 1.0, 'satisfaction_boost': 0.0},
        'Low': {'error_rate': 0.15, 'speed': 0.8, 'satisfaction_boost': -0.5}
    }
    
    data = []
    start_date = datetime.now() - timedelta(days=730)  # 2 years of data
    
    for i in range(num_records):
        state = random.choice(list(geo_db.keys()))
        state_data = geo_db[state]
        district = random.choice(list(state_data['districts'].keys()))
        district_data = state_data['districts'][district]
        
        # Add jitter to coordinates
        lat = district_data['lat'] + random.uniform(-0.2, 0.2)
        lon = district_data['lon'] + random.uniform(-0.2, 0.2)
        zone = random.choice(district_data['zones'])
        
        # Temporal patterns
        date = start_date + timedelta(days=random.randint(0, 730))
        hour = random.randint(8, 20)
        weekday = date.weekday()  # 0=Monday, 6=Sunday
        
        # Update type with temporal variations
        if weekday == 0:  # Monday
            type_weights = [0.4, 0.3, 0.2, 0.05, 0.05]
        elif weekday >= 5:  # Weekend
            type_weights = [0.5, 0.25, 0.15, 0.05, 0.05]
        else:
            type_weights = [0.35, 0.35, 0.2, 0.05, 0.05]
        
        update_type = random.choices(update_types, weights=type_weights)[0]
        
        # Operator assignment
        operator_profile = random.choices(
            ['High', 'Medium', 'Low'], 
            weights=[0.2, 0.6, 0.2]
        )[0]
        op_profile = operator_profiles[operator_profile]
        
        # Status determination
        base_success_rate = 0.85
        success_rate = min(0.98, base_success_rate + (op_profile['speed'] - 1) * 0.1)
        
        if random.random() < success_rate:
            status = 'Success'
            proc_time = max(1, int(np.random.normal(3, 1) * op_profile['speed']))
            satisfaction = min(5, max(1, int(np.random.normal(4.5, 0.5) + op_profile['satisfaction_boost'])))
            issue = 'None'
            feedback = random.choice([
                "Smooth and efficient", "Staff was helpful", "Quick processing",
                "Good facility", "Digital process worked well"
            ])
        else:
            # Determine failure type
            if random.random() < 0.3:  # 30% of failures are fraud
                status = 'Flagged for Fraud'
                proc_time = random.randint(1, 3)
                satisfaction = 1
                issue = 'Suspicious Activity'
                feedback = "Transaction flagged for review"
            else:
                status = random.choice(['Rejected', 'Pending'])
                proc_time = random.randint(5, 15)
                satisfaction = random.randint(1, 2)
                issue = random.choice(rejection_reasons)
                feedback = random.choice([
                    "Process too slow", "Document requirements unclear",
                    "Technical issues", "Staff unhelpful"
                ])
        
        # Governance Metrics
        risk_score = random.uniform(0, 100)
        compliance_score = random.uniform(60, 100)
        
        data.append({
            'Transaction_ID': f"TXN-{1000000 + i:07d}",
            'Date': date,
            'Time': f"{hour:02d}:{random.randint(0, 59):02d}",
            'Weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday],
            'State': state,
            'State_Tier': state_data['tier'],
            'District': district,
            'Zone': zone,
            'Latitude': lat,
            'Longitude': lon,
            'Update_Type': update_type,
            'Status': status,
            'Processing_Time_Days': proc_time,
            'Satisfaction_Score': satisfaction,
            'Issue_Reason': issue,
            'Citizen_Feedback': feedback,
            'Operator_ID': f"OP-{random.randint(100, 999)}",
            'Operator_Profile': operator_profile,
            'Center_ID': f"CEN-{random.randint(1, 50)}",
            'Risk_Score': round(risk_score, 2),
            'Compliance_Score': round(compliance_score, 2),
            'Session_Duration_Minutes': random.randint(5, 45),
            'Digital_Channel': random.choice(['Mobile App', 'Web Portal', 'Kiosk', 'Center Visit']),
            'Device_Type': random.choice(['Smartphone', 'Tablet', 'Desktop', 'Biometric Device']),
            'Aadhaar_Linked_Service': random.choice([
                'Banking', 'PAN', 'Driving License', 'Passport', 
                'Ration Card', 'Pension', 'Health Insurance', 'None'
            ])
        })
        
        # Progress indicator
        if i % 5000 == 0:
            print(f"   Generated {i:,} records...")
    
    df = pd.DataFrame(data)
    
    # Save in multiple formats
    df.to_csv('aadhaar_ultimate_data.csv', index=False)
    df.to_parquet('aadhaar_ultimate_data.parquet', index=False)
    
    # Generate metadata
    metadata = {
        'generated_date': datetime.now().isoformat(),
        'total_records': len(df),
        'date_range': {
            'start': df['Date'].min().isoformat(),
            'end': df['Date'].max().isoformat()
        },
        'states_covered': df['State'].nunique(),
        'districts_covered': df['District'].nunique()
    }
    
    with open('data_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Ultimate Dataset Generated: {len(df):,} records")
    print(f"📊 States: {df['State'].nunique()}, Districts: {df['District'].nunique()}")
    print(f"📁 Files saved: CSV, Parquet, JSON metadata")
    
    return df

if __name__ == "__main__":
    generate_ultimate_data()
'''

# 3. modules/governance_engine.py
governance_engine_content = '''import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import networkx as nx

class GovernanceAIDecisionEngine:
    """
    Advanced Governance AI Engine for UIDAI
    Converts analytics into actionable governance decisions
    """
    
    def __init__(self, df):
        self.df = df
        self.risk_thresholds = {
            'CRITICAL': 70,
            'HIGH': 45,
            'MODERATE': 25,
            'LOW': 0
        }
        
    # ======================================
    # RISK SCORING ENGINE
    # ======================================
    def compute_risk_scores(self, group_by=['State', 'District']):
        """
        Computes governance risk scores (0-100) at multiple levels
        """
        if isinstance(group_by, str):
            group_by = [group_by]
            
        grp = self.df.groupby(group_by)
        
        risk_table = grp.agg(
            total_txn=('Transaction_ID', 'count'),
            success_rate=('Status', lambda x: (x == 'Success').mean()),
            rejection_rate=('Status', lambda x: (x == 'Rejected').mean()),
            fraud_rate=('Status', lambda x: (x.str.contains('Fraud')).mean()),
            pending_rate=('Status', lambda x: (x == 'Pending').mean()),
            avg_processing=('Processing_Time_Days', 'mean'),
            std_processing=('Processing_Time_Days', 'std'),
            avg_satisfaction=('Satisfaction_Score', 'mean'),
            min_satisfaction=('Satisfaction_Score', 'min'),
            risk_score_avg=('Risk_Score', 'mean'),
            compliance_score_avg=('Compliance_Score', 'mean')
        ).reset_index()
        
        # Fill NaN values
        risk_table = risk_table.fillna(0)
        
        # Normalization function
        def normalize(series, reverse=False):
            if series.std() == 0:
                return pd.Series([0.5] * len(series), index=series.index)
            normalized = (series - series.min()) / (series.max() - series.min() + 1e-6)
            return 1 - normalized if reverse else normalized
        
        # Normalize metrics (higher = worse)
        risk_table['rej_n'] = normalize(risk_table['rejection_rate'])
        risk_table['fraud_n'] = normalize(risk_table['fraud_rate'])
        risk_table['pending_n'] = normalize(risk_table['pending_rate'])
        risk_table['proc_n'] = normalize(risk_table['avg_processing'])
        risk_table['proc_var_n'] = normalize(risk_table['std_processing'])
        risk_table['sat_n'] = 1 - normalize(risk_table['avg_satisfaction'])  # Lower satisfaction = higher risk
        
        # Dynamic weights based on severity
        weights = {
            'rej_n': 0.25,
            'fraud_n': 0.30,
            'pending_n': 0.15,
            'proc_n': 0.15,
            'proc_var_n': 0.05,
            'sat_n': 0.10
        }
        
        # Calculate weighted risk score
        risk_table['Risk_Score'] = (
            weights['rej_n'] * risk_table['rej_n'] +
            weights['fraud_n'] * risk_table['fraud_n'] +
            weights['pending_n'] * risk_table['pending_n'] +
            weights['proc_n'] * risk_table['proc_n'] +
            weights['proc_var_n'] * risk_table['proc_var_n'] +
            weights['sat_n'] * risk_table['sat_n']
        ) * 100
        
        # Risk classification
        risk_table['Risk_Level'] = risk_table['Risk_Score'].apply(self.classify_risk)
        
        return risk_table.sort_values('Risk_Score', ascending=False)
    
    # ======================================
    # RISK CLASSIFICATION
    # ======================================
    def classify_risk(self, score):
        if score >= self.risk_thresholds['CRITICAL']:
            return '🚨 CRITICAL'
        elif score >= self.risk_thresholds['HIGH']:
            return '🔴 HIGH'
        elif score >= self.risk_thresholds['MODERATE']:
            return '🟡 MODERATE'
        else:
            return '🟢 LOW'
    
    # ======================================
    # RECOMMENDATION ENGINE
    # ======================================
    def generate_recommendations(self, row):
        """
        Generate AI-powered recommendations based on risk profile
        """
        actions = []
        priorities = []
        
        # Priority 1: Fraud & Security
        if row['fraud_rate'] > 0.03:
            actions.append({
                'action': 'Immediate fraud investigation squad deployment',
                'priority': 'P1',
                'deadline': '24 hours',
                'department': 'Security & Audit'
            })
        elif row['fraud_rate'] > 0.01:
            actions.append({
                'action': 'Enhanced document verification protocol',
                'priority': 'P2',
                'deadline': '3 days',
                'department': 'Verification'
            })
        
        # Priority 2: High Rejections
        if row['rejection_rate'] > 0.15:
            actions.append({
                'action': 'Staff retraining on document requirements',
                'priority': 'P1',
                'deadline': '48 hours',
                'department': 'Training'
            })
        elif row['rejection_rate'] > 0.10:
            actions.append({
                'action': 'Process simplification review',
                'priority': 'P2',
                'deadline': '1 week',
                'department': 'Operations'
            })
        
        # Priority 3: Processing Delays
        if row['avg_processing'] > 10:
            actions.append({
                'action': 'Temporary staff augmentation',
                'priority': 'P1',
                'deadline': '72 hours',
                'department': 'HR'
            })
        elif row['avg_processing'] > 7:
            actions.append({
                'action': 'Process optimization team review',
                'priority': 'P2',
                'deadline': '2 weeks',
                'department': 'Efficiency'
            })
        
        # Priority 4: Citizen Satisfaction
        if row['avg_satisfaction'] < 3.0:
            actions.append({
                'action': 'Citizen experience redesign workshop',
                'priority': 'P2',
                'deadline': '2 weeks',
                'department': 'Customer Service'
            })
        elif row['avg_satisfaction'] < 3.5:
            actions.append({
                'action': 'Feedback implementation program',
                'priority': 'P3',
                'deadline': '1 month',
                'department': 'Quality'
            })
        
        # Priority 5: Pending Cases
        if row['pending_rate'] > 0.20:
            actions.append({
                'action': 'Pending case clearance drive',
                'priority': 'P1',
                'deadline': '1 week',
                'department': 'Backlog'
            })
        
        # Add operational improvements if no critical issues
        if not actions:
            actions.append({
                'action': 'Maintain current operational excellence',
                'priority': 'P4',
                'deadline': 'Ongoing',
                'department': 'All'
            })
        
        # Add capacity planning if high volume
        if row['total_txn'] > 1000:
            actions.append({
                'action': 'Capacity planning review for peak periods',
                'priority': 'P3',
                'deadline': '1 month',
                'department': 'Planning'
            })
        
        return actions
    
    # ======================================
    # TREND ANALYSIS
    # ======================================
    def analyze_trends(self, period='30D'):
        """
        Analyze risk trends over time
        """
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        recent_date = self.df['Date'].max()
        cutoff_date = recent_date - pd.Timedelta(days=int(period[:-1]))
        
        recent_data = self.df[self.df['Date'] > cutoff_date]
        historical_data = self.df[self.df['Date'] <= cutoff_date]
        
        recent_risk = self.compute_risk_scores()
        historical_risk = self.compute_risk_scores()
        
        # Compare trends
        trend_analysis = {
            'period': period,
            'recent_date_range': {
                'start': recent_data['Date'].min().strftime('%Y-%m-%d'),
                'end': recent_data['Date'].max().strftime('%Y-%m-%d')
            },
            'historical_date_range': {
                'start': historical_data['Date'].min().strftime('%Y-%m-%d'),
                'end': historical_data['Date'].max().strftime('%Y-%m-%d')
            },
            'risk_change': {
                'improved': [],
                'worsened': [],
                'stable': []
            }
        }
        
        return trend_analysis
    
    # ======================================
    # VISUALIZATION ENGINE
    # ======================================
    def create_risk_heatmap(self):
        """
        Create interactive heatmap of risk scores
        """
        risk_df = self.compute_risk_scores(['State', 'District'])
        
        fig = px.density_mapbox(
            risk_df,
            lat='Latitude',
            lon='Longitude',
            z='Risk_Score',
            radius=20,
            center=dict(lat=20.5937, lon=78.9629),
            zoom=3,
            mapbox_style="carto-positron",
            hover_data=['State', 'District', 'Risk_Level', 'total_txn'],
            color_continuous_scale="RdYlGn_r",  # Red (high risk) to Green (low risk)
            title="Geospatial Risk Heatmap"
        )
        
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        return fig
    
    def create_risk_radar(self, entity_name, entity_type='District'):
        """
        Create radar chart for risk dimensions
        """
        if entity_type == 'District':
            entity_data = self.df[self.df['District'] == entity_name]
        else:
            entity_data = self.df[self.df['State'] == entity_name]
        
        metrics = {
            'Rejection Rate': (entity_data['Status'] == 'Rejected').mean() * 100,
            'Fraud Rate': entity_data['Status'].str.contains('Fraud').mean() * 100,
            'Avg Processing Time': entity_data['Processing_Time_Days'].mean(),
            'Satisfaction Score': entity_data['Satisfaction_Score'].mean(),
            'Compliance Score': entity_data['Compliance_Score'].mean(),
            'Success Rate': (entity_data['Status'] == 'Success').mean() * 100
        }
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            line_color='blue'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(metrics.values()) * 1.1]
                )),
            showlegend=False,
            title=f"Risk Profile: {entity_name}"
        )
        
        return fig
    
    def create_trend_chart(self, entity_name, metric='Risk_Score'):
        """
        Create time series trend chart
        """
        if 'District' in self.df.columns and entity_name in self.df['District'].unique():
            entity_data = self.df[self.df['District'] == entity_name]
        elif entity_name in self.df['State'].unique():
            entity_data = self.df[self.df['State'] == entity_name]
        else:
            entity_data = self.df
        
        daily_metrics = entity_data.groupby('Date').agg({
            'Risk_Score': 'mean',
            'Processing_Time_Days': 'mean',
            'Satisfaction_Score': 'mean',
            'Transaction_ID': 'count'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_metrics['Date'],
            y=daily_metrics[metric],
            mode='lines+markers',
            name=metric,
            line=dict(color='red' if 'Risk' in metric else 'blue')
        ))
        
        fig.update_layout(
            title=f"{metric.replace('_', ' ').title()} Trend for {entity_name}",
            xaxis_title="Date",
            yaxis_title=metric.replace('_', ' ').title(),
            template="plotly_white"
        )
        
        return fig
    
    # ======================================
    # ANOMALY DETECTION
    # ======================================
    def detect_anomalies(self):
        """
        Detect statistical anomalies in operations
        """
        center_stats = self.df.groupby(['Center_ID', 'District']).agg({
            'Transaction_ID': 'count',
            'Processing_Time_Days': ['mean', 'std'],
            'Satisfaction_Score': 'mean',
            'Status': lambda x: (x == 'Rejected').mean()
        }).reset_index()
        
        center_stats.columns = ['Center_ID', 'District', 'Volume', 'Avg_Time', 'Time_Std', 'Avg_Satisfaction', 'Rejection_Rate']
        
        # Isolation Forest for anomaly detection
        features = center_stats[['Volume', 'Avg_Time', 'Time_Std', 'Avg_Satisfaction', 'Rejection_Rate']]
        iso = IsolationForest(contamination=0.1, random_state=42)
        center_stats['Anomaly_Score'] = iso.fit_predict(features)
        center_stats['Is_Anomaly'] = center_stats['Anomaly_Score'] == -1
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        center_stats['Cluster'] = kmeans.fit_predict(features)
        
        return center_stats
    
    # ======================================
    # GOVERNANCE BRIEF GENERATOR
    # ======================================
    def generate_governance_brief(self, top_n=10, level='District'):
        """
        Generate comprehensive governance briefs
        """
        risk_df = self.compute_risk_scores(['State', level] if level != 'All' else ['State'])
        
        briefs = []
        for idx, row in risk_df.head(top_n).iterrows():
            actions = self.generate_recommendations(row)
            
            brief = {
                'rank': idx + 1,
                'entity_type': level,
                'entity_name': row[level] if level != 'All' else row['State'],
                'state': row['State'],
                'risk_level': row['Risk_Level'],
                'risk_score': round(row['Risk_Score'], 1),
                'total_transactions': int(row['total_txn']),
                'key_metrics': {
                    'success_rate': f"{row['success_rate'] * 100:.1f}%",
                    'rejection_rate': f"{row['rejection_rate'] * 100:.1f}%",
                    'fraud_rate': f"{row['fraud_rate'] * 100:.2f}%",
                    'avg_processing_days': round(row['avg_processing'], 1),
                    'avg_satisfaction': round(row['avg_satisfaction'], 2),
                    'compliance_score': round(row.get('compliance_score_avg', 0), 1)
                },
                'recommended_actions': actions,
                'priority_summary': {
                    'P1': len([a for a in actions if a['priority'] == 'P1']),
                    'P2': len([a for a in actions if a['priority'] == 'P2']),
                    'P3': len([a for a in actions if a['priority'] == 'P3']),
                    'P4': len([a for a in actions if a['priority'] == 'P4'])
                },
                'generated_timestamp': datetime.now().isoformat()
            }
            briefs.append(brief)
        
        return briefs
    
    # ======================================
    # FORMATTING UTILITIES
    # ======================================
    @staticmethod
    def format_brief(brief):
        """
        Format brief for human-readable output
        """
        emoji = {
            '🚨 CRITICAL': '🚨',
            '🔴 HIGH': '🔴',
            '🟡 MODERATE': '🟡',
            '🟢 LOW': '🟢'
        }.get(brief['risk_level'], '⚪')
        
        text = f"""
{emoji} {brief['entity_type'].upper()} GOVERNANCE BRIEF #{brief['rank']}
{'=' * 50}

📌 Entity: {brief['entity_name']}, {brief['state']}
📊 Risk Level: {brief['risk_level']} (Score: {brief['risk_score']}/100)
📈 Total Transactions: {brief['total_transactions']:,}

📋 KEY PERFORMANCE INDICATORS:
   • Success Rate: {brief['key_metrics']['success_rate']}
   • Rejection Rate: {brief['key_metrics']['rejection_rate']}
   • Fraud Rate: {brief['key_metrics']['fraud_rate']}
   • Avg Processing Time: {brief['key_metrics']['avg_processing_days']} days
   • Citizen Satisfaction: {brief['key_metrics']['avg_satisfaction']}/5.0
   • Compliance Score: {brief['key_metrics']['compliance_score']}/100

🚀 RECOMMENDED ACTIONS ({len(brief['recommended_actions'])} total):
"""
        
        for i, action in enumerate(brief['recommended_actions'], 1):
            priority_emoji = {
                'P1': '🔴',
                'P2': '🟠',
                'P3': '🟡',
                'P4': '🟢'
            }.get(action['priority'], '⚪')
            
            text += f"   {priority_emoji} {i}. {action['action']}\n"
            text += f"      ⏰ Deadline: {action['deadline']} | 📋 Department: {action['department']}\n"
        
        text += f"""
📅 Generated: {brief['generated_timestamp'][:19]}
"""
        
        return text.strip()
    
    def generate_executive_summary(self):
        """
        Generate overall executive summary
        """
        total_txn = len(self.df)
        success_rate = (self.df['Status'] == 'Success').mean() * 100
        avg_satisfaction = self.df['Satisfaction_Score'].mean()
        
        risk_df = self.compute_risk_scores()
        critical_count = (risk_df['Risk_Level'] == '🚨 CRITICAL').sum()
        high_count = (risk_df['Risk_Level'] == '🔴 HIGH').sum()
        
        summary = f"""
🏛️ UIDAI GOVERNANCE EXECUTIVE SUMMARY
{'=' * 50}

📊 OVERVIEW:
   • Total Transactions Analyzed: {total_txn:,}
   • Success Rate: {success_rate:.1f}%
   • Average Citizen Satisfaction: {avg_satisfaction:.2f}/5.0

🚨 RISK ASSESSMENT:
   • Critical Risk Entities: {critical_count}
   • High Risk Entities: {high_count}
   • Total Entities Assessed: {len(risk_df)}

🎯 TOP PRIORITIES:
"""
        
        # Add top 3 critical items
        top_critical = risk_df[risk_df['Risk_Level'] == '🚨 CRITICAL'].head(3)
        for idx, row in top_critical.iterrows():
            summary += f"   • {row['District']}, {row['State']} (Score: {row['Risk_Score']:.1f})\n"
        
        summary += f"""
📈 RECOMMENDED FOCUS AREAS:
   1. Fraud Prevention Enhancement
   2. Citizen Experience Improvement
   3. Processing Time Optimization
   4. Compliance Standardization

⏰ NEXT REVIEW: {datetime.now() + timedelta(days=7):%Y-%m-%d}
"""
        
        return summary.strip()
'''

# 4. modules/reporting_engine.py
reporting_engine_content = '''from fpdf import FPDF
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
from modules.governance_engine import GovernanceAIDecisionEngine

class UltimatePDFReport(FPDF):
    """
    Enhanced PDF reporting engine with governance insights
    """
    
    def __init__(self, df, entity_name="National", entity_type="National"):
        super().__init__()
        self.df = df
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.governance_engine = GovernanceAIDecisionEngine(df)
        
        # Colors
        self.colors = {
            'primary': (0, 51, 102),     # Dark Blue
            'secondary': (0, 102, 204),   # Blue
            'success': (0, 153, 0),       # Green
            'warning': (255, 153, 0),     # Orange
            'danger': (204, 0, 0),        # Red
            'light': (240, 240, 240),     # Light Gray
            'dark': (51, 51, 51),         # Dark Gray
        }
        
    def header(self):
        # UIDAI Header
        self.set_font('Arial', 'B', 16)
        self.set_text_color(*self.colors['primary'])
        self.cell(0, 10, 'UNIQUE IDENTIFICATION AUTHORITY OF INDIA', 0, 1, 'C')
        
        # Subtitle
        self.set_font('Arial', 'I', 12)
        self.set_text_color(*self.colors['secondary'])
        self.cell(0, 10, 'AIGAP Ultimate - Governance Intelligence Report', 0, 1, 'C')
        
        # Entity Info
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*self.colors['dark'])
        self.cell(0, 8, f"Report For: {self.entity_type} - {self.entity_name}", 0, 1, 'C')
        
        # Date Line
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M IST')}", 0, 1, 'C')
        self.ln(5)
        
        # Add separator
        self.set_draw_color(*self.colors['primary'])
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} / {{nb}} - CONFIDENTIAL', 0, 0, 'C')
    
    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('Arial', 'B', 14)
            self.set_text_color(*self.colors['primary'])
            self.set_fill_color(*self.colors['light'])
            self.cell(0, 10, title, 0, 1, 'L', 1)
        else:
            self.set_font('Arial', 'B', 12)
            self.set_text_color(*self.colors['secondary'])
            self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def add_section(self, title, content, level=1):
        self.chapter_title(title, level)
        self.set_font('Arial', '', 11)
        self.set_text_color(*self.colors['dark'])
        self.multi_cell(0, 6, content)
        self.ln(5)
    
    def add_table(self, title, headers, data, col_widths=None):
        self.chapter_title(title, 2)
        
        if not col_widths:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Table Header
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(*self.colors['light'])
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, str(header), 1, 0, 'C', 1)
        self.ln()
        
        # Table Data
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 255, 255)
        
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'C')
            self.ln()
        
        self.ln(5)
    
    def add_metric_card(self, title, value, change=None, color='primary'):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(*self.colors[color])
        self.cell(60, 15, title, 1, 0, 'C', 1)
        
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*self.colors['dark'])
        self.cell(40, 15, str(value), 1, 0, 'C')
        
        if change:
            self.set_font('Arial', '', 9)
            color_code = self.colors['success'] if '+' in str(change) else self.colors['danger']
            self.set_text_color(*color_code)
            self.cell(30, 15, str(change), 1, 0, 'C')
        
        self.ln(8)
    
    def generate_full_report(self, report_type='comprehensive', level='District', top_n=20):
        """
        Generate comprehensive governance report
        """
        self.add_page()
        
        # 1. EXECUTIVE SUMMARY
        summary = self.governance_engine.generate_executive_summary()
        self.add_section('1. EXECUTIVE SUMMARY', summary, 1)
        
        # 2. KEY METRICS DASHBOARD
        self.chapter_title('2. KEY PERFORMANCE METRICS', 1)
        
        # Calculate metrics
        total_txn = len(self.df)
        success_rate = (self.df['Status'] == 'Success').mean() * 100
        avg_satisfaction = self.df['Satisfaction_Score'].mean()
        avg_processing = self.df['Processing_Time_Days'].mean()
        compliance_score = self.df['Compliance_Score'].mean()
        
        # Create metrics row
        self.add_metric_card('Total Transactions', f"{total_txn:,}")
        self.add_metric_card('Success Rate', f"{success_rate:.1f}%")
        self.add_metric_card('Avg Satisfaction', f"{avg_satisfaction:.2f}/5.0")
        self.ln(5)
        self.add_metric_card('Avg Processing Time', f"{avg_processing:.1f} days")
        self.add_metric_card('Compliance Score', f"{compliance_score:.1f}/100")
        self.add_metric_card('Digital Penetration', 
                           f"{(self.df['Digital_Channel'] != 'Center Visit').mean()*100:.1f}%")
        
        # 3. RISK ASSESSMENT
        risk_df = self.governance_engine.compute_risk_scores(['State', level])
        
        self.add_section('3. RISK ASSESSMENT & GOVERNANCE SCORING', 
                        f"The following {level.lower()}s have been identified as priority areas "
                        f"based on multi-dimensional risk scoring.", 1)
        
        # Top Risk Table
        headers = ['Rank', level, 'State', 'Risk Score', 'Risk Level', 'Total TXN', 'Success Rate']
        data = []
        
        for idx, row in risk_df.head(top_n).iterrows():
            data.append([
                idx + 1,
                row[level],
                row['State'],
                f"{row['Risk_Score']:.1f}",
                row['Risk_Level'],
                f"{int(row['total_txn']):,}",
                f"{row['success_rate']*100:.1f}%"
            ])
        
        self.add_table(f'Top {top_n} High-Risk {level}s', headers, data)
        
        # 4. DETAILED GOVERNANCE BRIEFS
        self.add_section('4. DETAILED GOVERNANCE BRIEFS', 
                        f"Detailed analysis and recommendations for top {min(5, top_n)} high-risk entities.", 1)
        
        briefs = self.governance_engine.generate_governance_brief(top_n=5, level=level)
        
        for brief in briefs:
            brief_text = self.governance_engine.format_brief(brief)
            self.add_section(f"{brief['rank']}. {brief['entity_name']} ({brief['state']})", 
                           brief_text, 2)
            self.ln(5)
        
        # 5. TREND ANALYSIS
        self.add_section('5. TREND ANALYSIS & FORECASTING', 
                        "Historical performance trends and forward-looking insights.", 1)
        
        # Add trend data
        self.set_font('Arial', '', 10)
        self.cell(0, 6, "📈 Monthly Transaction Volume Trend:", 0, 1)
        self.ln(2)
        
        # Monthly aggregation
        self.df['Month'] = pd.to_datetime(self.df['Date']).dt.to_period('M')
        monthly_stats = self.df.groupby('Month').agg({
            'Transaction_ID': 'count',
            'Satisfaction_Score': 'mean',
            'Processing_Time_Days': 'mean'
        }).tail(12)  # Last 12 months
        
        headers = ['Month', 'Transactions', 'Avg Satisfaction', 'Avg Processing (Days)']
        data = []
        
        for idx, row in monthly_stats.iterrows():
            data.append([
                str(idx),
                f"{row['Transaction_ID']:,}",
                f"{row['Satisfaction_Score']:.2f}",
                f"{row['Processing_Time_Days']:.1f}"
            ])
        
        self.add_table('Last 12 Months Performance', headers, data)
        
        # 6. ANOMALY DETECTION
        self.add_section('6. ANOMALY & FRAUD DETECTION', 
                        "Statistical anomalies and potential fraud indicators identified by AI engine.", 1)
        
        anomalies = self.governance_engine.detect_anomalies()
        critical_anomalies = anomalies[anomalies['Is_Anomaly']].head(10)
        
        if len(critical_anomalies) > 0:
            headers = ['Center ID', 'District', 'Volume', 'Avg Time', 'Rejection Rate', 'Status']
            data = []
            
            for _, row in critical_anomalies.iterrows():
                status = "🚨 INVESTIGATE" if row['Rejection_Rate'] > 0.15 else "⚠️ MONITOR"
                data.append([
                    row['Center_ID'],
                    row['District'],
                    f"{int(row['Volume']):,}",
                    f"{row['Avg_Time']:.1f}",
                    f"{row['Rejection_Rate']*100:.1f}%",
                    status
                ])
            
            self.add_table('Critical Anomalies Detected', headers, data)
        else:
            self.set_font('Arial', '', 11)
            self.set_text_color(*self.colors['success'])
            self.cell(0, 8, "✅ No critical anomalies detected in current analysis.", 0, 1)
            self.ln(5)
        
        # 7. RECOMMENDATIONS & ACTION PLAN
        self.add_section('7. STRATEGIC RECOMMENDATIONS & ACTION PLAN', 
                        "Prioritized actions for governance improvement.", 1)
        
        # Generate recommendations for top 3
        top_briefs = self.governance_engine.generate_governance_brief(top_n=3, level=level)
        
        for brief in top_briefs:
            self.set_font('Arial', 'B', 11)
            self.set_text_color(*self.colors['primary'])
            self.cell(0, 8, f"📍 {brief['entity_name']} ({brief['state']}):", 0, 1)
            
            self.set_font('Arial', '', 10)
            for action in brief['recommended_actions']:
                bullet = '•' if action['priority'] in ['P3', 'P4'] else '⚡'
                self.cell(10, 6, '', 0, 0)
                self.cell(0, 6, f"{bullet} {action['action']} ({action['priority']} - Due: {action['deadline']})", 0, 1)
            
            self.ln(3)
        
        # 8. APPENDICES
        self.add_page()
        self.add_section('APPENDIX A: METHODOLOGY & SCORING', 
                        """
SCORING METHODOLOGY:
• Risk Score (0-100): Weighted combination of rejection rate (25%), fraud rate (30%), 
  pending cases (15%), processing time (15%), processing variance (5%), and 
  citizen satisfaction (10%).
• Success Rate: Percentage of transactions marked as 'Success'.
• Compliance Score: Based on adherence to UIDAI operational standards.

DATA SOURCES:
• Aadhaar Update Transaction Database
• Citizen Feedback System
• Operator Performance Metrics
• Geographic Information System
                        """, 1)
        
        self.add_section('APPENDIX B: GLOSSARY', 
                        """
CRITICAL TERMS:
• Risk Level: Classification based on composite risk score (Critical ≥70, High ≥45, Moderate ≥25, Low <25)
• Governance Brief: Comprehensive analysis of entity performance with actionable recommendations
• Anomaly Detection: Statistical identification of unusual patterns requiring investigation
• Compliance Score: Measure of adherence to UIDAI standards and protocols
                        """, 1)
        
        # Save the report
        filename = f"UIDAI_Governance_Report_{self.entity_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        return filename, self.output(dest='S').encode('latin1')
    
    def generate_quick_report(self, entity_name, entity_type='District'):
        """
        Generate a quick snapshot report
        """
        self.add_page()
        
        # Filter data for entity
        if entity_type == 'District':
            entity_data = self.df[self.df['District'] == entity_name]
            state = entity_data['State'].iloc[0] if not entity_data.empty else 'Unknown'
        else:
            entity_data = self.df[self.df['State'] == entity_name]
            state = entity_name
        
        if entity_data.empty:
            self.add_section('NO DATA AVAILABLE', 
                           f"No data found for {entity_type}: {entity_name}", 1)
            filename = f"No_Data_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            return filename, self.output(dest='S').encode('latin1')
        
        # Calculate metrics
        total_txn = len(entity_data)
        success_rate = (entity_data['Status'] == 'Success').mean() * 100
        avg_satisfaction = entity_data['Satisfaction_Score'].mean()
        avg_processing = entity_data['Processing_Time_Days'].mean()
        
        self.add_section(f'QUICK SNAPSHOT: {entity_name}', 
                        f"{entity_type} Performance Overview", 1)
        
        # Metrics
        self.add_metric_card('Total Transactions', f"{total_txn:,}")
        self.add_metric_card('Success Rate', f"{success_rate:.1f}%")
        self.add_metric_card('Avg Satisfaction', f"{avg_satisfaction:.2f}/5.0")
        self.ln(10)
        self.add_metric_card('Avg Processing Time', f"{avg_processing:.1f} days")
        self.add_metric_card('Digital Adoption', 
                           f"{(entity_data['Digital_Channel'] != 'Center Visit').mean()*100:.1f}%")
        
        # Recent Activity
        self.add_section('RECENT ACTIVITY', "Last 30 days performance", 2)
        
        recent_date = pd.to_datetime(entity_data['Date']).max()
        cutoff_date = recent_date - pd.Timedelta(days=30)
        recent_data = entity_data[pd.to_datetime(entity_data['Date']) > cutoff_date]
        
        if len(recent_data) > 0:
            recent_success = (recent_data['Status'] == 'Success').mean() * 100
            recent_satisfaction = recent_data['Satisfaction_Score'].mean()
            
            self.set_font('Arial', '', 10)
            self.cell(0, 6, f"📊 Last 30 Days: {len(recent_data):,} transactions", 0, 1)
            self.cell(0, 6, f"✅ Success Rate: {recent_success:.1f}%", 0, 1)
            self.cell(0, 6, f"😊 Satisfaction: {recent_satisfaction:.2f}/5.0", 0, 1)
        else:
            self.cell(0, 6, "No recent activity data available.", 0, 1)
        
        filename = f"Quick_Report_{entity_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        return filename, self.output(dest='S').encode('latin1')
'''

# 5. modules/visualization_engine.py
visualization_engine_content = '''import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from datetime import datetime
import networkx as nx

class UltimateVisualizationEngine:
    """
    Advanced visualization engine for governance intelligence
    """
    
    def __init__(self, df):
        self.df = df
        self.color_scales = {
            'risk': 'RdYlGn_r',  # Red (high risk) to Green (low risk)
            'performance': 'Viridis',
            'satisfaction': 'RdYlGn',
            'time': 'Plasma',
            'compliance': 'Blues'
        }
    
    def create_risk_heatmap(self, risk_df):
        """
        Create geospatial heatmap of risk scores
        """
        # Get unique coordinates for each district
        district_coords = self.df.groupby(['District', 'State']).agg({
            'Latitude': 'mean',
            'Longitude': 'mean'
        }).reset_index()
        
        # Merge with risk data
        heatmap_data = pd.merge(risk_df, district_coords, on=['District', 'State'])
        
        fig = px.density_mapbox(
            heatmap_data,
            lat='Latitude',
            lon='Longitude',
            z='Risk_Score',
            radius=25,
            center=dict(lat=22.0, lon=78.0),
            zoom=3.5,
            mapbox_style="carto-positron",
            hover_data=['District', 'State', 'Risk_Level', 'total_txn', 'success_rate'],
            color_continuous_scale=self.color_scales['risk'],
            range_color=[0, 100],
            title="📊 Geospatial Risk Distribution",
            height=600
        )
        
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title="Risk Score",
                thickness=20,
                len=0.75,
                yanchor="middle",
                y=0.5
            )
        )
        
        return fig
    
    def create_performance_radar(self, entity_data, entity_name):
        """
        Create radar chart for performance metrics
        """
        metrics = {
            'Success Rate': (entity_data['Status'] == 'Success').mean() * 100,
            'Citizen Satisfaction': entity_data['Satisfaction_Score'].mean() * 20,  # Scale to 100
            'Processing Speed': max(0, 100 - (entity_data['Processing_Time_Days'].mean() * 10)),
            'Digital Adoption': (entity_data['Digital_Channel'] != 'Center Visit').mean() * 100,
            'Compliance Score': entity_data['Compliance_Score'].mean(),
            'Fraud Prevention': 100 - (entity_data['Status'].str.contains('Fraud').mean() * 1000)
        }
        
        # Cap values at 100
        metrics = {k: min(100, max(0, v)) for k, v in metrics.items()}
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            fillcolor='rgba(0, 102, 204, 0.3)',
            line=dict(color='rgb(0, 102, 204)', width=2),
            hoverinfo='text',
            text=[f"{k}: {v:.1f}" for k, v in metrics.items()]
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    gridcolor='lightgray',
                    linecolor='gray'
                )
            ),
            showlegend=False,
            title=f"🎯 Performance Radar: {entity_name}",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(size=12)
        )
        
        return fig
    
    def create_temporal_trend(self, entity_name, entity_type='District', metric='Risk_Score'):
        """
        Create time series trend with confidence intervals
        """
        if entity_type == 'District':
            entity_data = self.df[self.df['District'] == entity_name]
        elif entity_type == 'State':
            entity_data = self.df[self.df['State'] == entity_name]
        else:
            entity_data = self.df
        
        # Daily aggregation
        daily_metrics = entity_data.groupby('Date').agg({
            'Risk_Score': 'mean',
            'Processing_Time_Days': 'mean',
            'Satisfaction_Score': 'mean',
            'Transaction_ID': 'count'
        }).reset_index()
        
        # Sort by date
        daily_metrics = daily_metrics.sort_values('Date')
        
        # Calculate rolling average and confidence intervals
        window = 7
        daily_metrics[f'{metric}_rolling'] = daily_metrics[metric].rolling(window=window, center=True).mean()
        daily_metrics[f'{metric}_std'] = daily_metrics[metric].rolling(window=window, center=True).std()
        
        fig = go.Figure()
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=daily_metrics['Date'],
            y=daily_metrics[f'{metric}_rolling'] + 1.96 * daily_metrics[f'{metric}_std'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            name='Upper Bound'
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_metrics['Date'],
            y=daily_metrics[f'{metric}_rolling'] - 1.96 * daily_metrics[f'{metric}_std'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(68, 68, 68, 0.1)',
            name='95% Confidence'
        ))
        
        # Add rolling average
        fig.add_trace(go.Scatter(
            x=daily_metrics['Date'],
            y=daily_metrics[f'{metric}_rolling'],
            mode='lines',
            line=dict(color='blue', width=3),
            name=f'{metric.replace("_", " ").title()} (7-day avg)'
        ))
        
        # Add actual points
        fig.add_trace(go.Scatter(
            x=daily_metrics['Date'],
            y=daily_metrics[metric],
            mode='markers',
            marker=dict(color='red', size=4, opacity=0.3),
            name='Daily Values',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f"📈 {metric.replace('_', ' ').title()} Trend: {entity_name}",
            xaxis_title="Date",
            yaxis_title=metric.replace('_', ' ').title(),
            template="plotly_white",
            hovermode="x unified",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
    
    def create_comparison_barchart(self, risk_df, top_n=15):
        """
        Create comparison bar chart for top entities
        """
        top_entities = risk_df.head(top_n).copy()
        top_entities['Label'] = top_entities['District'] + ', ' + top_entities['State']
        
        fig = px.bar(
            top_entities,
            x='Risk_Score',
            y='Label',
            orientation='h',
            color='Risk_Score',
            color_continuous_scale=self.color_scales['risk'],
            hover_data=['total_txn', 'success_rate', 'avg_processing', 'avg_satisfaction'],
            title=f"🏆 Top {top_n} Entities by Risk Score"
        )
        
        fig.update_layout(
            yaxis=dict(title=''),
            xaxis=dict(title='Risk Score (0-100)'),
            coloraxis_showscale=False,
            height=max(400, top_n * 25)
        )
        
        # Add success rate as text
        for i, row in enumerate(top_entities.itertuples()):
            fig.add_annotation(
                x=row.Risk_Score + 2,
                y=row.Index,
                text=f"{row.success_rate*100:.0f}% success",
                showarrow=False,
                font=dict(size=9, color='gray')
            )
        
        return fig
    
    def create_sunburst_hierarchy(self):
        """
        Create hierarchical sunburst chart
        """
        hierarchy_data = self.df.groupby(['State', 'District', 'Status']).size().reset_index(name='Count')
        
        fig = px.sunburst(
            hierarchy_data,
            path=['State', 'District', 'Status'],
            values='Count',
            color='Count',
            color_continuous_scale=self.color_scales['performance'],
            title="🌳 Hierarchical Transaction Distribution"
        )
        
        fig.update_layout(
            margin=dict(t=40, l=0, r=0, b=0),
            coloraxis_colorbar=dict(
                title="Transaction Count",
                thickness=20
            )
        )
        
        return fig
    
    def create_correlation_matrix(self, metrics_df):
        """
        Create correlation heatmap
        """
        corr_cols = ['Risk_Score', 'success_rate', 'rejection_rate', 'fraud_rate', 
                    'avg_processing', 'avg_satisfaction', 'compliance_score_avg']
        
        corr_matrix = metrics_df[corr_cols].corr()
        
        # Create annotated heatmap
        fig = ff.create_annotated_heatmap(
            z=corr_matrix.values,
            x=corr_cols,
            y=corr_cols,
            annotation_text=corr_matrix.round(2).values,
            colorscale='RdBu',
            showscale=True,
            zmin=-1,
            zmax=1
        )
        
        fig.update_layout(
            title="🔗 Metric Correlation Matrix",
            xaxis=dict(tickangle=45),
            height=500
        )
        
        return fig
    
    def create_network_graph(self, centers_df):
        """
        Create network graph of centers and their relationships
        """
        G = nx.Graph()
        
        # Add nodes (centers)
        for _, row in centers_df.iterrows():
            G.add_node(
                row['Center_ID'],
                size=row['Volume'] / 100,
                color=row['Risk_Score'] if 'Risk_Score' in row else 50,
                district=row['District']
            )
        
        # Add edges based on geographic proximity (simplified)
        # In reality, this would be based on actual relationships
        centers_list = centers_df['Center_ID'].tolist()
        for i in range(len(centers_list)):
            for j in range(i + 1, min(i + 3, len(centers_list))):  # Connect to next 2 centers
                G.add_edge(centers_list[i], centers_list[j], weight=0.5)
        
        # Convert to plotly
        pos = nx.spring_layout(G, seed=42)
        
        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=0.5, color='gray'),
                    hoverinfo='none'
                )
            )
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                size=[G.nodes[node]['size'] * 10 for node in G.nodes()],
                color=[G.nodes[node]['color'] for node in G.nodes()],
                colorbar=dict(
                    thickness=15,
                    title='Risk Score',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2
            )
        )
        
        # Add node labels
        node_text = []
        for node in G.nodes():
            node_text.append(f"Center: {node}<br>District: {G.nodes[node]['district']}")
        
        node_trace.text = node_text
        
        fig = go.Figure(data=edge_trace + [node_trace],
                       layout=go.Layout(
                           title='🕸️ Center Network Analysis',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    def create_gauge_chart(self, value, title, min_val=0, max_val=100):
        """
        Create gauge chart for single metric
        """
        # Determine color
        if value < max_val * 0.4:
            color = "green"
        elif value < max_val * 0.7:
            color = "orange"
        else:
            color = "red"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, max_val * 0.4], 'color': "lightgray"},
                    {'range': [max_val * 0.4, max_val * 0.7], 'color': "gray"},
                    {'range': [max_val * 0.7, max_val], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_val * 0.8
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig
'''

# 6. app.py (Ultimate Dashboard)
app_content = '''import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import base64
from io import BytesIO

# Import custom modules
from modules.governance_engine import GovernanceAIDecisionEngine
from modules.reporting_engine import UltimatePDFReport
from modules.visualization_engine import UltimateVisualizationEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="UIDAI AIGAP Ultimate - Governance Command Center",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(90deg, #002d62, #0066cc);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #002d62;
        margin-bottom: 10px;
    }
    
    .metric-card-critical {
        border-left-color: #d32f2f;
        background: linear-gradient(135deg, #fff5f5, #ffebee);
    }
    
    .metric-card-high {
        border-left-color: #ff9800;
        background: linear-gradient(135deg, #fff3e0, #ffecb3);
    }
    
    .metric-card-moderate {
        border-left-color: #ffc107;
        background: linear-gradient(135deg, #fff8e1, #fff9c4);
    }
    
    .metric-card-low {
        border-left-color: #4caf50;
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #002d62, #0066cc);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002d62 0%, #004080 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Custom headers */
    h1, h2, h3 {
        color: #002d62 !important;
        font-weight: 700 !important;
    }
    
    /* Alert boxes */
    .alert-critical {
        background: linear-gradient(135deg, #ffcdd2, #ef9a9a);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #d32f2f;
        margin: 10px 0;
    }
    
    .alert-high {
        background: linear-gradient(135deg, #ffe0b2, #ffcc80);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'governance_engine' not in st.session_state:
    st.session_state.governance_engine = None
if 'viz_engine' not in st.session_state:
    st.session_state.viz_engine = None

# --- AUTHENTICATION ---
def authenticate():
    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='main-title'>", unsafe_allow_html=True)
            st.title("🔐 UIDAI SECURE ACCESS")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.info("""
            ### 🇮🇳 Unique Identification Authority of India
            **AIGAP Ultimate - Governance Intelligence Platform**
            
            *Authorized Personnel Only*
            """)
            
            tab1, tab2 = st.tabs(["🔑 Login", "👥 Guest Access"])
            
            with tab1:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                if st.button("Login", type="primary"):
                    if username == "admin" and password == "admin":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            with tab2:
                st.warning("Guest access provides limited functionality")
                if st.button("Continue as Guest"):
                    st.session_state.logged_in = True
                    st.session_state.guest_mode = True
                    st.rerun()
        
        st.stop()

authenticate()

# --- DATA LOADING ---
@st.cache_data(ttl=3600)
def load_data():
    """Load and cache data"""
    data_files = ['aadhaar_ultimate_data.csv', 'aadhaar_ultimate_data.parquet']
    
    for file in data_files:
        if os.path.exists(file):
            try:
                if file.endswith('.parquet'):
                    df = pd.read_parquet(file)
                else:
                    df = pd.read_csv(file, parse_dates=['Date'])
                
                print(f"✅ Loaded {len(df):,} records from {file}")
                return df
            except Exception as e:
                print(f"⚠️ Error loading {file}: {e}")
    
    # If no data file exists, show warning
    st.warning("No data file found. Please run data generator first.")
    return pd.DataFrame()

if st.session_state.df is None:
    with st.spinner("Loading governance data..."):
        st.session_state.df = load_data()
        
        if not st.session_state.df.empty:
            st.session_state.governance_engine = GovernanceAIDecisionEngine(st.session_state.df)
            st.session_state.viz_engine = UltimateVisualizationEngine(st.session_state.df)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg", width=150)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Governance Dashboard")
    
    # Navigation
    menu = st.radio(
        "Navigation",
        [
            "📊 National Overview",
            "🏛️ Governance Intelligence",
            "📍 Geospatial Analysis",
            "📈 Performance Analytics",
            "🚨 Risk Management",
            "📑 Reporting Center",
            "⚙️ System Configuration"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🔍 Filters")
    
    # Date Range
    if not st.session_state.df.empty:
        min_date = st.session_state.df['Date'].min().date()
        max_date = st.session_state.df['Date'].max().date()
        
        date_range = st.date_input(
            "Date Range",
            value=(max_date - timedelta(days=90), max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # State Filter
    states = ["All"] + sorted(st.session_state.df['State'].unique().tolist()) if not st.session_state.df.empty else ["All"]
    selected_state = st.selectbox("State", states)
    
    # District Filter
    if selected_state != "All" and not st.session_state.df.empty:
        districts = ["All"] + sorted(st.session_state.df[st.session_state.df['State'] == selected_state]['District'].unique().tolist())
        selected_district = st.selectbox("District", districts)
    else:
        selected_district = "All"
    
    # Analysis Level
    analysis_level = st.selectbox(
        "Analysis Level",
        ["National", "State", "District", "Center"],
        index=0
    )
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 🖥️ System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Records", f"{len(st.session_state.df):,}" if not st.session_state.df.empty else "0")
    with col2:
        st.metric("Last Update", datetime.now().strftime("%H:%M"))
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.session_state.df = load_data()
        if not st.session_state.df.empty:
            st.session_state.governance_engine = GovernanceAIDecisionEngine(st.session_state.df)
            st.session_state.viz_engine = UltimateVisualizationEngine(st.session_state.df)
        st.rerun()

# --- MAIN CONTENT ---
if st.session_state.df.empty:
    st.error("""
    ## No Data Available
    
    Please generate data first by running:
    ```bash
    python data_generator.py
    ```
    
    Or use the System Configuration panel to generate sample data.
    """)
    st.stop()

# Apply filters
filtered_df = st.session_state.df.copy()

if selected_state != "All":
    filtered_df = filtered_df[filtered_df['State'] == selected_state]
if selected_district != "All":
    filtered_df = filtered_df[filtered_df['District'] == selected_district]

# Update governance engine with filtered data
filtered_engine = GovernanceAIDecisionEngine(filtered_df)
filtered_viz = UltimateVisualizationEngine(filtered_df)

# --- PAGE ROUTING ---
if menu == "📊 National Overview":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🇮🇳 National Governance Dashboard")
        st.caption("Real-time Governance Intelligence for Aadhaar Operations")
    with col2:
        st.metric("Live Entities", f"{filtered_df['District'].nunique()}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Metrics Row
    st.subheader("🚀 Executive Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_txn = len(filtered_df)
        st.metric("Total Transactions", f"{total_txn:,}")
    
    with col2:
        success_rate = (filtered_df['Status'] == 'Success').mean() * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        avg_satisfaction = filtered_df['Satisfaction_Score'].mean()
        st.metric("Citizen Satisfaction", f"{avg_satisfaction:.2f}/5.0")
    
    with col4:
        avg_processing = filtered_df['Processing_Time_Days'].mean()
        st.metric("Avg Processing", f"{avg_processing:.1f} days")
    
    with col5:
        compliance_score = filtered_df['Compliance_Score'].mean()
        st.metric("Compliance", f"{compliance_score:.1f}/100")
    
    # Risk Overview
    st.subheader("🚨 Risk Overview")
    
    risk_df = filtered_engine.compute_risk_scores(['State', 'District'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Risk Distribution
        risk_dist = risk_df['Risk_Level'].value_counts()
        fig = px.pie(
            values=risk_dist.values,
            names=risk_dist.index,
            title="Risk Level Distribution",
            color_discrete_sequence=['#4CAF50', '#FFC107', '#FF9800', '#D32F2F'],
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top Critical Risks
        st.markdown("### 🚨 Critical Risks")
        critical_risks = risk_df[risk_df['Risk_Level'] == '🚨 CRITICAL'].head(5)
        
        for _, row in critical_risks.iterrows():
            st.markdown(f"""
            <div class='alert-critical'>
            **{row['District']}, {row['State']}**
            - Score: {row['Risk_Score']:.1f}/100
            - Transactions: {int(row['total_txn']):,}
            </div>
            """, unsafe_allow_html=True)
    
    # Recent Activity
    st.subheader("📈 Recent Activity Trend")
    
    # Last 30 days trend
    recent_date = filtered_df['Date'].max()
    cutoff_date = recent_date - timedelta(days=30)
    recent_df = filtered_df[filtered_df['Date'] > cutoff_date]
    
    if not recent_df.empty:
        daily_trend = recent_df.groupby('Date').agg({
            'Transaction_ID': 'count',
            'Satisfaction_Score': 'mean',
            'Processing_Time_Days': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_trend['Date'],
            y=daily_trend['Transaction_ID'],
            mode='lines+markers',
            name='Transaction Volume',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_trend['Date'],
            y=daily_trend['Satisfaction_Score'] * 100,  # Scale for visualization
            mode='lines',
            name='Satisfaction (scaled)',
            yaxis='y2',
            line=dict(color='green', width=2, dash='dot')
        ))
        
        fig.update_layout(
            title="30-Day Activity Trend",
            xaxis_title="Date",
            yaxis_title="Transaction Volume",
            yaxis2=dict(
                title="Satisfaction Score",
                overlaying='y',
                side='right',
                range=[0, 500]  # Since we scaled satisfaction
            ),
            template="plotly_white",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif menu == "🏛️ Governance Intelligence":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("🏛️ Governance Intelligence Engine")
    st.caption("AI-Powered Decision Support System")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate Governance Briefs
    with st.spinner("Generating governance intelligence..."):
        briefs = filtered_engine.generate_governance_brief(top_n=10, level='District')
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            critical_count = len([b for b in briefs if '🚨' in b['risk_level']])
            st.metric("Critical Risks", critical_count, delta=None)
        
        with col2:
            high_count = len([b for b in briefs if '🔴' in b['risk_level']])
            st.metric("High Risks", high_count)
        
        with col3:
            total_actions = sum(len(b['recommended_actions']) for b in briefs[:5])
            st.metric("Recommended Actions", total_actions)
        
        with col4:
            p1_actions = sum(
                len([a for a in b['recommended_actions'] if a['priority'] == 'P1']) 
                for b in briefs[:5]
            )
            st.metric("P1 Actions", p1_actions)
    
    # Detailed Briefs
    st.subheader("📋 Governance Briefs")
    
    for brief in briefs[:5]:  # Show top 5
        with st.expander(f"{brief['rank']}. {brief['entity_name']} ({brief['state']}) - {brief['risk_level']}", expanded=True):
            # Display formatted brief
            st.markdown(filtered_engine.format_brief(brief))
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📊 View Detailed Analytics", key=f"analytics_{brief['entity_name']}"):
                    st.session_state.selected_entity = brief['entity_name']
                    st.session_state.selected_entity_type = 'District'
                    st.rerun()
            
            with col2:
                if st.button(f"📄 Generate PDF Report", key=f"pdf_{brief['entity_name']}"):
                    # Generate PDF report
                    pdf_report = UltimatePDFReport(filtered_df, brief['entity_name'], 'District')
                    filename, pdf_bytes = pdf_report.generate_quick_report(brief['entity_name'], 'District')
                    
                    st.download_button(
                        label="Download Report",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )
            
            with col3:
                if st.button(f"🔄 Monitor Progress", key=f"monitor_{brief['entity_name']}"):
                    st.info(f"Setting up monitoring for {brief['entity_name']}...")
    
    # Executive Summary
    st.subheader("📝 Executive Summary")
    
    executive_summary = filtered_engine.generate_executive_summary()
    st.markdown(f"""
    <div style='background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #002d62;'>
    {executive_summary}
    </div>
    """, unsafe_allow_html=True)

elif menu == "📍 Geospatial Analysis":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("📍 Geospatial Intelligence")
    st.caption("Interactive Mapping and Spatial Analysis")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Map Type Selection
    map_type = st.selectbox(
        "Select Map Layer",
        [
            "Risk Heatmap",
            "Transaction Density",
            "Satisfaction Index",
            "Processing Time",
            "Fraud Hotspots",
            "Compliance Status"
        ]
    )
    
    # Generate appropriate map
    with st.spinner("Generating geospatial visualization..."):
        risk_df = filtered_engine.compute_risk_scores(['State', 'District'])
        
        if map_type == "Risk Heatmap":
            fig = filtered_viz.create_risk_heatmap(risk_df)
        elif map_type == "Transaction Density":
            # Create density map based on transaction volume
            district_volume = filtered_df.groupby(['District', 'State', 'Latitude', 'Longitude']).size().reset_index(name='Volume')
            fig = px.density_mapbox(
                district_volume,
                lat='Latitude',
                lon='Longitude',
                z='Volume',
                radius=20,
                center=dict(lat=22.0, lon=78.0),
                zoom=3.5,
                mapbox_style="carto-positron",
                hover_data=['District', 'State'],
                color_continuous_scale="Viridis",
                title="Transaction Density Map"
            )
        elif map_type == "Satisfaction Index":
            district_satisfaction = filtered_df.groupby(['District', 'State', 'Latitude', 'Longitude'])['Satisfaction_Score'].mean().reset_index()
            fig = px.scatter_mapbox(
                district_satisfaction,
                lat='Latitude',
                lon='Longitude',
                color='Satisfaction_Score',
                size=np.ones(len(district_satisfaction)) * 10,
                hover_data=['District', 'State'],
                color_continuous_scale="RdYlGn",
                range_color=[1, 5],
                title="Citizen Satisfaction Index"
            )
            fig.update_layout(mapbox_style="carto-positron")
        else:
            # Default to risk heatmap
            fig = filtered_viz.create_risk_heatmap(risk_df)
        
        st.plotly_chart(fig, use_container_width=True, height=600)
    
    # Map Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        highest_risk = risk_df.iloc[0] if not risk_df.empty else None
        if highest_risk is not None:
            st.metric(
                "Highest Risk Area",
                f"{highest_risk['District']}, {highest_risk['State']}",
                delta=f"{highest_risk['Risk_Score']:.1f}"
            )
    
    with col2:
        avg_risk = risk_df['Risk_Score'].mean() if not risk_df.empty else 0
        st.metric("Average Risk Score", f"{avg_risk:.1f}/100")
    
    with col3:
        critical_count = (risk_df['Risk_Level'] == '🚨 CRITICAL').sum()
        st.metric("Critical Zones", critical_count)
    
    # Detailed District List
    st.subheader("📊 District Performance Table")
    
    # Sortable dataframe
    display_cols = ['District', 'State', 'Risk_Score', 'Risk_Level', 'total_txn', 'success_rate', 'avg_processing', 'avg_satisfaction']
    display_df = risk_df[display_cols].copy()
    display_df['success_rate'] = (display_df['success_rate'] * 100).round(1)
    display_df['avg_satisfaction'] = display_df['avg_satisfaction'].round(2)
    display_df['avg_processing'] = display_df['avg_processing'].round(1)
    display_df['Risk_Score'] = display_df['Risk_Score'].round(1)
    
    # Rename columns for display
    display_df.columns = ['District', 'State', 'Risk Score', 'Risk Level', 'Total TXN', 'Success %', 'Avg Days', 'Satisfaction']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        column_config={
            "Risk Score": st.column_config.ProgressColumn(
                "Risk Score",
                help="Risk score (0-100)",
                format="%.1f",
                min_value=0,
                max_value=100,
            ),
            "Success %": st.column_config.NumberColumn(
                "Success %",
                format="%.1f%%"
            ),
            "Satisfaction": st.column_config.NumberColumn(
                "Satisfaction",
                format="%.2f"
            )
        }
    )

elif menu == "📈 Performance Analytics":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("📈 Performance Analytics")
    st.caption("Deep Dive into Operational Metrics")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Performance Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview Metrics",
        "📈 Trend Analysis",
        "🔍 Comparative Analysis",
        "🎯 Performance Radar"
    ])
    
    with tab1:
        st.subheader("Key Performance Indicators")
        
        # Create metric cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Success Rate Gauge
            success_rate = (filtered_df['Status'] == 'Success').mean() * 100
            fig = filtered_viz.create_gauge_chart(success_rate, "Success Rate", 0, 100)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Satisfaction Gauge
            avg_satisfaction = filtered_df['Satisfaction_Score'].mean() * 20  # Scale to 100
            fig = filtered_viz.create_gauge_chart(avg_satisfaction, "Citizen Satisfaction", 0, 100)
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_processing = filtered_df['Processing_Time_Days'].mean()
            processing_score = max(0, 100 - (avg_processing * 10))  # Inverse score
            fig = filtered_viz.create_gauge_chart(processing_score, "Processing Efficiency", 0, 100)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            digital_rate = (filtered_df['Digital_Channel'] != 'Center Visit').mean() * 100
            fig = filtered_viz.create_gauge_chart(digital_rate, "Digital Adoption", 0, 100)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            compliance_score = filtered_df['Compliance_Score'].mean()
            fig = filtered_viz.create_gauge_chart(compliance_score, "Compliance Score", 0, 100)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Temporal Trend Analysis")
        
        # Entity selection for trend analysis
        entities = ["Overall"] + sorted(filtered_df['District'].unique().tolist())
        selected_entity = st.selectbox("Select Entity for Trend Analysis", entities)
        
        # Metric selection
        trend_metric = st.selectbox(
            "Select Metric",
            ["Risk_Score", "Processing_Time_Days", "Satisfaction_Score", "Transaction_Volume"]
        )
        
        if selected_entity:
            with st.spinner("Generating trend analysis..."):
                if selected_entity == "Overall":
                    entity_name = "Overall"
                    entity_type = "Overall"
                else:
                    entity_name = selected_entity
                    entity_type = "District"
                
                fig = filtered_viz.create_temporal_trend(entity_name, entity_type, trend_metric)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Comparative Analysis")
        
        # Generate risk scores for comparison
        risk_df = filtered_engine.compute_risk_scores(['State', 'District'])
        
        # Comparison chart
        top_n = st.slider("Number of entities to compare", 5, 30, 15)
        fig = filtered_viz.create_comparison_barchart(risk_df, top_n)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Metric Correlation Analysis")
        fig = filtered_viz.create_correlation_matrix(risk_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Performance Radar Analysis")
        
        # Entity selection for radar chart
        radar_entity = st.selectbox("Select Entity for Radar Chart", 
                                  sorted(filtered_df['District'].unique().tolist()))
        
        if radar_entity:
            entity_data = filtered_df[filtered_df['District'] == radar_entity]
            fig = filtered_viz.create_performance_radar(entity_data, radar_entity)
            st.plotly_chart(fig, use_container_width=True)

elif menu == "🚨 Risk Management":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("🚨 Risk Management Center")
    st.caption("Proactive Risk Identification and Mitigation")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Anomaly Detection
    with st.spinner("Running anomaly detection..."):
        anomalies = filtered_engine.detect_anomalies()
        critical_anomalies = anomalies[anomalies['Is_Anomaly']]
        
        # Anomaly Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Centers", len(anomalies))
        
        with col2:
            st.metric("Anomalies Detected", len(critical_anomalies))
        
        with col3:
            high_risk_anomalies = len(critical_anomalies[critical_anomalies['Rejection_Rate'] > 0.15])
            st.metric("High Risk Anomalies", high_risk_anomalies)
    
    # Anomaly Details
    if not critical_anomalies.empty:
        st.subheader("🚨 Critical Anomalies Requiring Attention")
        
        # Display anomalies in expandable sections
        for idx, row in critical_anomalies.head(10).iterrows():
            risk_level = "🔴 HIGH" if row['Rejection_Rate'] > 0.15 else "🟡 MEDIUM"
            
            with st.expander(f"{risk_level} - {row['Center_ID']} ({row['District']})", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Volume", f"{int(row['Volume']):,}")
                
                with col2:
                    st.metric("Avg Processing", f"{row['Avg_Time']:.1f} days")
                
                with col3:
                    st.metric("Rejection Rate", f"{row['Rejection_Rate']*100:.1f}%")
                
                with col4:
                    st.metric("Satisfaction", f"{row['Avg_Satisfaction']:.2f}/5.0")
                
                # Recommendations
                st.markdown("### 🎯 Recommended Actions")
                
                if row['Rejection_Rate'] > 0.15:
                    st.error("""
                    **Immediate Action Required:**
                    1. Dispatch audit team within 24 hours
                    2. Review last 100 transactions
                    3. Temporary suspension recommended
                    """)
                elif row['Rejection_Rate'] > 0.10:
                    st.warning("""
                    **Priority Action Required:**
                    1. Supervisor review within 48 hours
                    2. Additional training required
                    3. Enhanced monitoring for 2 weeks
                    """)
                else:
                    st.info("""
                    **Monitoring Recommended:**
                    1. Weekly performance review
                    2. Compare with regional benchmarks
                    3. Share best practices
                    """)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📋 Create Audit Ticket", key=f"audit_{row['Center_ID']}"):
                        st.success(f"Audit ticket created for {row['Center_ID']}")
                
                with col2:
                    if st.button(f"📧 Notify Supervisor", key=f"notify_{row['Center_ID']}"):
                        st.info(f"Notification sent for {row['Center_ID']}")
                
                with col3:
                    if st.button(f"📊 View Details", key=f"details_{row['Center_ID']}"):
                        st.session_state.selected_center = row['Center_ID']
                        st.rerun()
    else:
        st.success("✅ No critical anomalies detected!")
    
    # Network Analysis
    st.subheader("🕸️ Center Network Analysis")
    
    with st.spinner("Generating network analysis..."):
        # Use a subset of centers for network visualization
        centers_sample = anomalies.head(20) if len(anomalies) > 20 else anomalies
        
        if not centers_sample.empty:
            fig = filtered_viz.create_network_graph(centers_sample)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough centers for network analysis")

elif menu == "📑 Reporting Center":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("📑 Reporting Center")
    st.caption("Generate Comprehensive Governance Reports")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Report Type Selection
    report_type = st.selectbox(
        "Select Report Type",
        [
            "📊 Comprehensive Governance Report",
            "🚨 Risk Assessment Report",
            "📈 Performance Analysis Report",
            "📍 Geospatial Intelligence Report",
            "⚡ Quick Snapshot Report"
        ]
    )
    
    # Report Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        report_level = st.selectbox(
            "Report Level",
            ["National", "State", "District", "Center"],
            index=0
        )
    
    with col2:
        if report_level == "State":
            entities = ["All"] + sorted(filtered_df['State'].unique().tolist())
            selected_entity = st.selectbox("Select State", entities)
        elif report_level == "District":
            entities = ["All"] + sorted(filtered_df['District'].unique().tolist())
            selected_entity = st.selectbox("Select District", entities)
        elif report_level == "Center":
            entities = ["All"] + sorted(filtered_df['Center_ID'].unique().tolist())
            selected_entity = st.selectbox("Select Center", entities)
        else:
            selected_entity = "National"
    
    # Additional Options
    with st.expander("⚙️ Report Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            include_charts = st.checkbox("Include Charts & Visualizations", value=True)
            include_anomalies = st.checkbox("Include Anomaly Detection", value=True)
        
        with col2:
            include_recommendations = st.checkbox("Include Action Recommendations", value=True)
            report_format = st.selectbox("Format", ["PDF", "HTML", "Excel"])
    
    # Generate Report
    if st.button("🔄 Generate Report", type="primary", use_container_width=True):
        with st.spinner(f"Generating {report_type}..."):
            try:
                # Initialize report generator
                report_generator = UltimatePDFReport(filtered_df, selected_entity, report_level)
                
                if "Comprehensive" in report_type:
                    filename, pdf_bytes = report_generator.generate_full_report(
                        report_type='comprehensive',
                        level='District' if report_level == 'National' else report_level,
                        top_n=20
                    )
                else:
                    filename, pdf_bytes = report_generator.generate_quick_report(selected_entity, report_level)
                
                # Display download button
                st.success(f"✅ Report generated successfully: {filename}")
                
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.download_button(
                        label="📥 Download Report",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                # Preview
                with st.expander("📄 Report Preview"):
                    st.info("""
                    **Report Contents:**
                    1. Executive Summary
                    2. Key Performance Metrics
                    3. Risk Assessment
                    4. Detailed Governance Briefs
                    5. Trend Analysis
                    6. Anomaly Detection
                    7. Strategic Recommendations
                    8. Appendices
                    """)
                    
                    # Show sample data
                    st.dataframe(
                        filtered_engine.compute_risk_scores(['State', 'District']).head(10),
                        use_container_width=True
                    )
            
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    
    # Report Templates
    st.subheader("📋 Report Templates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Daily Briefing", use_container_width=True):
            st.info("Daily briefing template loaded")
            st.session_state.report_template = "daily"
    
    with col2:
        if st.button("Weekly Review", use_container_width=True):
            st.info("Weekly review template loaded")
            st.session_state.report_template = "weekly"
    
    with col3:
        if st.button("Monthly Audit", use_container_width=True):
            st.info("Monthly audit template loaded")
            st.session_state.report_template = "monthly"
    
    # Scheduled Reports
    st.subheader("⏰ Scheduled Reports")
    
    if st.button("🔄 Configure Auto-Reports", use_container_width=True):
        st.info("Auto-report configuration coming soon!")

elif menu == "⚙️ System Configuration":
    st.markdown("<div class='main-title'>", unsafe_allow_html=True)
    st.title("⚙️ System Configuration")
    st.caption("System Settings and Data Management")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # System Info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Information")
        
        system_info = {
            "Platform": "UIDAI AIGAP Ultimate",
            "Version": "v3.0.0",
            "Data Records": f"{len(st.session_state.df):,}",
            "States Covered": f"{st.session_state.df['State'].nunique()}",
            "Districts Covered": f"{st.session_state.df['District'].nunique()}",
            "Date Range": f"{st.session_state.df['Date'].min().date()} to {st.session_state.df['Date'].max().date()}",
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in system_info.items():
            st.text(f"{key}: {value}")
    
    with col2:
        st.subheader("Data Management")
        
        # Data Generation
        if st.button("🔄 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating sample data..."):
                # Import data generator function
                import data_generator
                st.session_state.df = data_generator.generate_ultimate_data()
                st.session_state.governance_engine = GovernanceAIDecisionEngine(st.session_state.df)
                st.session_state.viz_engine = UltimateVisualizationEngine(st.session_state.df)
                st.success("✅ Sample data generated successfully!")
                st.rerun()
        
        # Data Export
        if st.button("📤 Export Data", use_container_width=True):
            # Create export options
            export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
            
            if export_format == "CSV":
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="aadhaar_governance_data.csv",
                    mime="text/csv"
                )
            elif export_format == "Excel":
                # For Excel export, we'd use pandas ExcelWriter
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Governance Data')
                
                st.download_button(
                    label="Download Excel",
                    data=buffer.getvalue(),
                    file_name="aadhaar_governance_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    # System Settings
    st.subheader("⚙️ System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk Thresholds
        st.markdown("### Risk Threshold Configuration")
        
        critical_threshold = st.slider("Critical Risk Threshold", 0, 100, 70)
        high_threshold = st.slider("High Risk Threshold", 0, 100, 45)
        moderate_threshold = st.slider("Moderate Risk Threshold", 0, 100, 25)
        
        if st.button("Update Thresholds", use_container_width=True):
            st.success("Risk thresholds updated!")
    
    with col2:
        # Notification Settings
        st.markdown("### Notification Settings")
        
        email_alerts = st.checkbox("Email Alerts", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
        dashboard_alerts = st.checkbox("Dashboard Alerts", value=True)
        
        alert_frequency = st.selectbox(
            "Alert Frequency",
            ["Real-time", "Hourly", "Daily", "Weekly"]
        )
    
    # Data Quality Check
    st.subheader("🔍 Data Quality Check")
    
    if st.button("Run Data Quality Check", use_container_width=True):
        with st.spinner("Checking data quality..."):
            # Perform data quality checks
            total_records = len(st.session_state.df)
            missing_values = st.session_state.df.isnull().sum().sum()
            duplicate_records = st.session_state.df.duplicated().sum()
            date_range = st.session_state.df['Date'].max() - st.session_state.df['Date'].min()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", f"{total_records:,}")
            
            with col2:
                st.metric("Missing Values", missing_values)
            
            with col3:
                st.metric("Duplicate Records", duplicate_records)
            
            with col4:
                st.metric("Date Range", f"{date_range.days} days")
            
            if missing_values == 0 and duplicate_records == 0:
                st.success("✅ Data quality check passed!")
            else:
                st.warning("⚠️ Data quality issues detected")

# --- FOOTER ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <small>
    🇮🇳 Unique Identification Authority of India<br>
    AIGAP Ultimate v3.0 | Governance Intelligence Platform<br>
    © 2024 UIDAI. All rights reserved. | For Official Use Only
    </small>
    </div>
    """, unsafe_allow_html=True)
'''

# 7. readme content (reconstructed and completed)
readme_content = """# UIDAI AIGAP Ultimate - Governance Intelligence Platform

## Overview
The Ultimate Governance Intelligence Platform for UIDAI Aadhaar operations, combining:
- Advanced AI-driven governance decision making
- Comprehensive risk assessment and scoring
- Interactive geospatial visualization
- Automated reporting and briefing generation
- Real-time anomaly detection

## Features

### 🏛️ Governance Intelligence Engine
- Multi-dimensional risk scoring (0-100)
- AI-powered recommendation generation
- Priority-based action planning
- Trend analysis and forecasting

### 📊 Advanced Analytics
- Interactive dashboards with Plotly
- Geospatial heatmaps and network analysis
- Performance radar charts and gauges
- Temporal trend analysis with confidence intervals

### 📑 Smart Reporting
- Comprehensive PDF report generation
- Executive summaries and governance briefs
- Automated anomaly detection reports
- Customizable report templates

### 🚨 Risk Management
- Real-time anomaly detection using Isolation Forest
- Center clustering with K-Means
- Network analysis for relationship mapping
- Proactive alerting system

## Installation

1. **Setup Project**
   ```bash
   # Run the setup script to create project structure
   python uidai_project_setup.py
   cd UIDAI_AIGAP_ULTIMATE
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Data**
   ```bash
   python data_generator.py
   ```

4. **Run Application**
   ```bash
   streamlit run app.py
   ```

## Usage
- Login using default credentials (admin/admin) or continue as Guest.
- Navigate through the sidebar to access different modules.
- Generate reports from the Reporting Center.
- Monitor real-time risks and anomalies on the dashboard.
"""

def create_ultimate_project():
    """
    Create the ultimate AIGAP project structure
    """
    print("\n" + "="*60)
    print("🚀 UIDAI AIGAP ULTIMATE - PROJECT SETUP")
    print("="*60)
    
    # Create directories
    directories = [PROJECT_DIR, MODULES_DIR, ASSETS_DIR, REPORTS_DIR]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # --- MODIFICATION START ---
    # logic to read local files if they exist in the same folder as c.py
    try:
        with open("governance_engine.py", "r", encoding="utf-8") as f:
            print("📄 Found local governance_engine.py, using its content...")
            governance_engine_content = f.read()
    except FileNotFoundError:
        print("⚠️ Local governance_engine.py not found, using default embedded content.")

    try:
        with open("reporting_engine.py", "r", encoding="utf-8") as f:
            print("📄 Found local reporting_engine.py, using its content...")
            reporting_engine_content = f.read()
    except FileNotFoundError:
        print("⚠️ Local reporting_engine.py not found, using default embedded content.")
    # --- MODIFICATION END ---

    # Create files
    files = {
        os.path.join(PROJECT_DIR, "requirements.txt"): requirements_content,
        os.path.join(PROJECT_DIR, "data_generator.py"): data_generator_content,
        os.path.join(PROJECT_DIR, "app.py"): app_content,
        os.path.join(PROJECT_DIR, "README.md"): readme_content,
        os.path.join(MODULES_DIR, "__init__.py"): "# Governance AI Modules",
        os.path.join(MODULES_DIR, "governance_engine.py"): governance_engine_content,
        os.path.join(MODULES_DIR, "reporting_engine.py"): reporting_engine_content,
        os.path.join(MODULES_DIR, "visualization_engine.py"): visualization_engine_content,
    }
    
    # Attempt to copy this script itself if running from file
    if os.path.exists(__file__):
         files[os.path.join(PROJECT_DIR, "setup_project.py")] = open(__file__, 'r', encoding='utf-8').read()

    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    print("\n🎉 Project Setup Complete!")
    print(f"👉 Run: cd {PROJECT_DIR} && pip install -r requirements.txt")
    print("👉 Then: python data_generator.py")
    print("👉 Finally: streamlit run app.py")

if __name__ == "__main__":

    create_ultimate_project()
