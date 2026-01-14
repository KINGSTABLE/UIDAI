import pandas as pd
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