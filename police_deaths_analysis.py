import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_demographic_pipeline():
    print("🔄 Initializing US Socio-Economic & Incident Analytics Pipeline...")
    
    # 1. Load dataframes with your EXACT file explorer names
    try:
        df_fatalities = pd.read_csv("Deaths_by_Police_US.csv", encoding="windows-1252")  
        df_poverty = pd.read_csv("Pct_People_Below_Poverty_Level.csv", encoding="windows-1252")
        df_income = pd.read_csv("Median_Household_Income_2015.csv", encoding="windows-1252")
        df_education = pd.read_csv("Pct_Over_25_Completed_High_School.csv", encoding="windows-1252")
    except FileNotFoundError as e:
        print(f"❌ Core File Missing Error: {e}")
        print("💡 Check your sidebar filenames and match spelling exactly.")
        return

    print("✅ Raw CSV dataframes loaded safely into workspace memory.")

    # 2. Extract and Clean Columns
    # Identify the correct state column inside your fatalities tracker 
    state_col = [col for col in df_fatalities.columns if 'state' in col.lower()][0]
    
    df_poverty['poverty_rate'] = pd.to_numeric(df_poverty['poverty_rate'], errors='coerce')
    df_education['percent_completed_hs'] = pd.to_numeric(df_education['percent_completed_hs'], errors='coerce')
    
    # 3. Compute Aggregations
    state_poverty = df_poverty.groupby('Geographic Area')['poverty_rate'].mean().reset_index()
    state_education = df_education.groupby('Geographic Area')['percent_completed_hs'].mean().reset_index()
    
    # 4. Perform Joins
    state_summary = pd.merge(state_poverty, state_education, on='Geographic Area')
    state_summary.columns = ['State', 'Mean_Poverty_Rate', 'Mean_HS_Graduation_Rate']
    
    incident_counts = df_fatalities[state_col].value_counts().reset_index()
    incident_counts.columns = ['State', 'Total_Incidents']
    
    master_df = pd.merge(state_summary, incident_counts, on='State', how='inner')
    
    print("\n正式 Master Socio-Economic Summary View Matrix (Top 10 Rows):")
    print(master_df.sort_values(by='Total_Incidents', ascending=False).head(10))
   
   # 5. Generate a Two-Panel Comparative Subplot Grid
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#0B0C10')
    sns.set_theme(style="darkgrid")

    # Plot 1: Poverty Rate vs Incidents
    sns.regplot(ax=axes[0], data=master_df, x='Mean_Poverty_Rate', y='Total_Incidents', 
                scatter_kws={'s':70, 'color':'#66FCF1'}, line_kws={'color':'#FF5A5F', 'linewidth':2.5})
    axes[0].set_title("Poverty Index vs Fatal Incidents", fontsize=12, fontweight='bold', color='#FFF')
    axes[0].set_xlabel("State Mean Poverty Rate (%)", color='#C5C6C7')
    axes[0].set_ylabel("Total Quantifiable Incidents Count", color='#C5C6C7')
    axes[0].set_facecolor('#1F2833')
    axes[0].tick_params(colors='#C5C6C7')

    # Plot 2: Graduation Rate vs Incidents
    sns.regplot(ax=axes[1], data=master_df, x='Mean_HS_Graduation_Rate', y='Total_Incidents', 
                scatter_kws={'s':70, 'color':'#45A29E'}, line_kws={'color':'#FF5A5F', 'linewidth':2.5})
    axes[1].set_title("High School Graduation Rate vs Fatal Incidents", fontsize=12, fontweight='bold', color='#FFF')
    axes[1].set_xlabel("State Mean Graduation Rate (%)", color='#C5C6C7')
    axes[1].set_ylabel("", color='#C5C6C7') # Share Y-axis contextually
    axes[1].set_facecolor('#1F2833')
    axes[1].tick_params(colors='#C5C6C7')

    output_plot = "demographic_comparative_insights.png"
    plt.savefig(output_plot, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print(f"\n🏆 Advanced comparative grid generated cleanly at: '{output_plot}'")