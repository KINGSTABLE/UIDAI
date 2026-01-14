from fpdf import FPDF
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
        self.entity_name = self.clean_text(entity_name)
        self.entity_type = self.clean_text(entity_type)
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
    
    def clean_text(self, text):
        """
        Remove unsupported characters (emojis, etc.) that cause UnicodeEncodeError in FPDF.
        Retains only Latin-1 characters.
        """
        if not isinstance(text, str):
            return str(text)
        # Encode to latin-1 and ignore errors (drops chars), then decode back
        return text.encode('latin-1', 'ignore').decode('latin-1')

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
        self.cell(0, 8, self.clean_text(f"Report For: {self.entity_type} - {self.entity_name}"), 0, 1, 'C')
        
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
        title = self.clean_text(title)
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
        self.multi_cell(0, 6, self.clean_text(content))
        self.ln(5)
    
    def add_table(self, title, headers, data, col_widths=None):
        self.chapter_title(title, 2)
        
        if not col_widths:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Table Header
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(*self.colors['light'])
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, self.clean_text(str(header)), 1, 0, 'C', 1)
        self.ln()
        
        # Table Data
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 255, 255)
        
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, self.clean_text(str(cell)), 1, 0, 'C')
            self.ln()
        
        self.ln(5)
    
    def add_metric_card(self, title, value, change=None, color='primary'):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(*self.colors[color])
        self.cell(60, 15, self.clean_text(title), 1, 0, 'C', 1)
        
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*self.colors['dark'])
        self.cell(40, 15, self.clean_text(str(value)), 1, 0, 'C')
        
        if change:
            self.set_font('Arial', '', 9)
            color_code = self.colors['success'] if '+' in str(change) else self.colors['danger']
            self.set_text_color(*color_code)
            self.cell(30, 15, self.clean_text(str(change)), 1, 0, 'C')
        
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
        self.cell(0, 6, self.clean_text("Monthly Transaction Volume Trend:"), 0, 1)
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
                status = "INVESTIGATE" if row['Rejection_Rate'] > 0.15 else "MONITOR"
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
            self.cell(0, 8, self.clean_text("No critical anomalies detected in current analysis."), 0, 1)
            self.ln(5)
        
        # 7. RECOMMENDATIONS & ACTION PLAN
        self.add_section('7. STRATEGIC RECOMMENDATIONS & ACTION PLAN', 
                        "Prioritized actions for governance improvement.", 1)
        
        # Generate recommendations for top 3
        top_briefs = self.governance_engine.generate_governance_brief(top_n=3, level=level)
        
        for brief in top_briefs:
            self.set_font('Arial', 'B', 11)
            self.set_text_color(*self.colors['primary'])
            self.cell(0, 8, self.clean_text(f"{brief['entity_name']} ({brief['state']}):"), 0, 1)
            
            self.set_font('Arial', '', 10)
            for action in brief['recommended_actions']:
                self.cell(10, 6, '', 0, 0)
                self.cell(0, 6, self.clean_text(f"- {action['action']} ({action['priority']} - Due: {action['deadline']})"), 0, 1)
            
            self.ln(3)
        
        # 8. APPENDICES
        self.add_page()
        self.add_section('APPENDIX A: METHODOLOGY & SCORING', 
                        """
SCORING METHODOLOGY:
- Risk Score (0-100): Weighted combination of rejection rate (25%), fraud rate (30%), 
  pending cases (15%), processing time (15%), processing variance (5%), and 
  citizen satisfaction (10%).
- Success Rate: Percentage of transactions marked as 'Success'.
- Compliance Score: Based on adherence to UIDAI operational standards.

DATA SOURCES:
- Aadhaar Update Transaction Database
- Citizen Feedback System
- Operator Performance Metrics
- Geographic Information System
                        """, 1)
        
        self.add_section('APPENDIX B: GLOSSARY', 
                        """
CRITICAL TERMS:
- Risk Level: Classification based on composite risk score (Critical >=70, High >=45, Moderate >=25, Low <25)
- Governance Brief: Comprehensive analysis of entity performance with actionable recommendations
- Anomaly Detection: Statistical identification of unusual patterns requiring investigation
- Compliance Score: Measure of adherence to UIDAI standards and protocols
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
            self.cell(0, 6, self.clean_text(f"Last 30 Days: {len(recent_data):,} transactions"), 0, 1)
            self.cell(0, 6, self.clean_text(f"Success Rate: {recent_success:.1f}%"), 0, 1)
            self.cell(0, 6, self.clean_text(f"Satisfaction: {recent_satisfaction:.2f}/5.0"), 0, 1)
        else:
            self.cell(0, 6, self.clean_text("No recent activity data available."), 0, 1)
        
        filename = f"Quick_Report_{entity_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        return filename, self.output(dest='S').encode('latin1')