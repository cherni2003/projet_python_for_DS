"""
Data Preprocessing and Feature Engineering Script
Week 2 - Wikipedia ML Pipeline Project

This script performs:
1. Data Cleaning
2. Country Name Standardization
3. Dataset Merging
4. Feature Engineering
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """Class to handle all data preprocessing and feature engineering"""
    
    def __init__(self):
        """Initialize the preprocessor with country name mappings"""
        # Dictionary for standardizing country names
        self.country_mappings = {
            'United States': ['United States', 'USA', 'US', 'United States of America'],
            'United Kingdom': ['United Kingdom', 'UK', 'Great Britain', 'Britain'],
            'Russia': ['Russia', 'Russian Federation'],
            'South Korea': ['South Korea', 'Korea, South', 'Republic of Korea'],
            'North Korea': ['North Korea', 'Korea, North', 'Democratic People\'s Republic of Korea'],
            'Democratic Republic of the Congo': ['Democratic Republic of the Congo', 'DR Congo', 'Congo (Kinshasa)', 'Congo, Democratic Republic of the'],
            'Republic of the Congo': ['Republic of the Congo', 'Congo', 'Congo (Brazzaville)', 'Congo, Republic of the'],
            'Czech Republic': ['Czech Republic', 'Czechia'],
            'Myanmar': ['Myanmar', 'Burma'],
            'Turkey': ['Turkey', 'Türkiye'],
            'Ivory Coast': ['Ivory Coast', 'Côte d\'Ivoire'],
            'East Timor': ['East Timor', 'Timor-Leste'],
            'Vatican City': ['Vatican City', 'Holy See'],
            'Cape Verde': ['Cape Verde', 'Cabo Verde'],
            'Eswatini': ['Eswatini', 'Swaziland'],
        }
        
        # Create reverse mapping for quick lookup
        self.name_to_standard = {}
        for standard_name, variants in self.country_mappings.items():
            for variant in variants:
                self.name_to_standard[variant.lower()] = standard_name
    
    def clean_numeric_value(self, value: str) -> float:
        """
        Clean and convert numeric values to float
        
        Args:
            value: String containing numeric value with possible commas, percentages, etc.
            
        Returns:
            Float value or NaN if conversion fails
        """
        if pd.isna(value):
            return np.nan
        
        # Convert to string and clean
        value_str = str(value)
        
        # Remove percentage signs
        value_str = value_str.replace('%', '')
        
        # Remove commas
        value_str = value_str.replace(',', '')
        
        # Remove any non-numeric characters except dots and minus
        value_str = re.sub(r'[^\d.-]', '', value_str)
        
        # Try to convert to float
        try:
            return float(value_str)
        except (ValueError, TypeError):
            return np.nan
    
    def standardize_country_name(self, country: str) -> str:
        """
        Standardize country names to a common format
        
        Args:
            country: Country name to standardize
            
        Returns:
            Standardized country name
        """
        if pd.isna(country):
            return country
        
        # Clean the country name
        country_clean = country.strip()
        
        # Remove reference numbers like [1], [2]
        country_clean = re.sub(r'\[.*?\]', '', country_clean).strip()
        
        # Remove parenthetical information
        country_clean = re.sub(r'\(.*?\)', '', country_clean).strip()
        
        # Check if we have a mapping
        country_lower = country_clean.lower()
        if country_lower in self.name_to_standard:
            return self.name_to_standard[country_lower]
        
        return country_clean
    
    def load_and_clean_population(self, filepath: Optional[str] = None) -> pd.DataFrame:
        """
        Load and clean population data
        
        Args:
            filepath: Path to population CSV file
            
        Returns:
            Cleaned DataFrame
        """
        if filepath is None:
            filepath = r'C:\Users\Cherni Oumaima\Desktop\projets python\projet_python_for_DS\data\raw\population_data.csv'
        print("=" * 70)
        print("📊 LOADING AND CLEANING POPULATION DATA")
        print("=" * 70)
        
        df = pd.read_csv(filepath)
        
        # Check the actual data structure - sometimes columns are shifted
        # If the first data row has a country name in 'Rank' column, the structure is shifted
        if df.iloc[0]['Rank'] in ['World', 'India', 'China']:
            # Columns are: Country (in Rank), Population (in Country), Percentage (in Population)
            df = df.rename(columns={
                'Rank': 'Country',
                'Country': 'Population',
                'Population': 'Percentage'
            })
            # Add a numeric rank
            df['Rank'] = range(1, len(df) + 1)
        
        # Remove 'World' row if present
        df = df[df['Country'] != 'World'].copy()
        
        # Standardize country names
        df['Country'] = df['Country'].apply(self.standardize_country_name)
        
        # Clean population values
        df['Population'] = df['Population'].apply(self.clean_numeric_value)
        
        # Clean rank
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Country'], keep='first')
        
        # Remove rows with missing country or population
        df = df.dropna(subset=['Country', 'Population'])
        
        # Keep only necessary columns
        df = df[['Rank', 'Country', 'Population']].copy()
        
        print(f"✅ Cleaned population data: {len(df)} countries")
        if df['Population'].max() > 0:
            print(f"   Population range: {df['Population'].min():,.0f} - {df['Population'].max():,.0f}")
        
        return df
    
    def load_and_clean_gdp(self, filepath: str='C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/gdp_data.csv') -> pd.DataFrame:
        """
        Load and clean GDP data
        
        Args:
            filepath: Path to GDP CSV file
            
        Returns:
            Cleaned DataFrame
        """
        print("\n" + "=" * 70)
        print("💰 LOADING AND CLEANING GDP DATA")
        print("=" * 70)
        
        df = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/gdp_data.csv')
        
        # Check if columns are shifted (country name in Rank column)
        if df.iloc[0]['Rank'] in ['United States', 'China', 'Germany', 'Japan']:
            # Columns are shifted: Country (in Rank), GDP1 (in Country), GDP2 (in GDP column)
            df = df.rename(columns={
                'Rank': 'Country',
                'Country': 'GDP_USD_millions',
                'GDP (USD millions)': 'GDP_USD_millions_alt'
            })
            # Add rank based on order
            df['Rank'] = range(1, len(df) + 1)
        
        # Standardize country names
        df['Country'] = df['Country'].apply(self.standardize_country_name)
        
        # Clean GDP values - use the main GDP column
        df['GDP_USD_millions'] = df['GDP_USD_millions'].apply(self.clean_numeric_value)
        
        # Convert to billions for readability
        df['GDP_USD_billions'] = df['GDP_USD_millions'] / 1000
        
        # Use Rank as GDP_Rank
        df['GDP_Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        
        # Keep only necessary columns
        df = df[['Country', 'GDP_Rank', 'GDP_USD_millions', 'GDP_USD_billions']].copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Country'], keep='first')
        
        # Remove rows with missing data
        df = df.dropna(subset=['Country', 'GDP_USD_millions'])
        
        print(f"✅ Cleaned GDP data: {len(df)} countries")
        if df['GDP_USD_billions'].max() > 0:
            print(f"   GDP range: ${df['GDP_USD_billions'].min():,.1f}B - ${df['GDP_USD_billions'].max():,.1f}B")
        
        return df
    
    def load_and_clean_life_expectancy(self, filepath: str ='C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/life_expectancy.csv') -> pd.DataFrame:
        """
        Load and clean life expectancy data
        Note: This is a placeholder - you need to scrape this data first
        
        Args:
            filepath: Path to life expectancy CSV file
            excel_path: Path to Excel file with life expectancy sheet
            
        Returns:
            Cleaned DataFrame
        """
        print("\n" + "=" * 70)
        print("🏥 LOADING AND CLEANING LIFE EXPECTANCY DATA")
        print("=" * 70)
        
        # Check if we need to scrape the data
        if filepath is None and excel_path is None:
            print("⚠️  Life expectancy data not found!")
            print("   You need to scrape this data first using the wikipedia_scraper.py")
            print("   Creating placeholder for demonstration...")
            
            # Create placeholder data
            df = pd.DataFrame({
                'Country': ['United States', 'China', 'India'],
                'Life_Expectancy': [78.5, 77.0, 70.0]
            })
            return df
        
        # Load from CSV if provided
        if filepath:
            df = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/life_expectancy.csv')
        elif excel_path:
            df = pd.read_excel(excel_path, sheet_name='Life Expectancy')
        
        # Standardize country names
        df['Country'] = df['Country'].apply(self.standardize_country_name)
        
        # Clean life expectancy value (usually the overall/both sexes column)
        life_exp_col = [col for col in df.columns if 'Overall' in col or 'Both' in col]
        if life_exp_col:
            df['Life_Expectancy'] = df[life_exp_col[0]].apply(self.clean_numeric_value)
        else:
            # Try the second column if no specific column found
            df['Life_Expectancy'] = df.iloc[:, 1].apply(self.clean_numeric_value)
        
        # Clean male and female if available
        if 'Life Expectancy (Male)' in df.columns:
            df['Life_Expectancy_Male'] = df['Life Expectancy (Male)'].apply(self.clean_numeric_value)
        
        if 'Life Expectancy (Female)' in df.columns:
            df['Life_Expectancy_Female'] = df['Life Expectancy (Female)'].apply(self.clean_numeric_value)
        
        # Keep only relevant columns
        cols_to_keep = ['Country', 'Life_Expectancy']
        if 'Life_Expectancy_Male' in df.columns:
            cols_to_keep.append('Life_Expectancy_Male')
        if 'Life_Expectancy_Female' in df.columns:
            cols_to_keep.append('Life_Expectancy_Female')
        
        df = df[cols_to_keep].copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Country'], keep='first')
        
        # Remove rows with missing data
        df = df.dropna(subset=['Country', 'Life_Expectancy'])
        
        print(f"✅ Cleaned life expectancy data: {len(df)} countries")
        print(f"   Life expectancy range: {df['Life_Expectancy'].min():.1f} - {df['Life_Expectancy'].max():.1f} years")
        
        return df
    
    def merge_datasets(self, df_population: pd.DataFrame, 
                       df_gdp: pd.DataFrame,
                       df_life_exp: pd.DataFrame) -> pd.DataFrame:
        """
        Merge all datasets on country name
        
        Args:
            df_population: Cleaned population DataFrame
            df_gdp: Cleaned GDP DataFrame
            df_life_exp: Cleaned life expectancy DataFrame
            
        Returns:
            Merged DataFrame
        """
        print("\n" + "=" * 70)
        print("🔗 MERGING DATASETS")
        print("=" * 70)
        
        # Start with population data
        df_merged = df_population.copy()
        
        # Merge with GDP data
        df_merged = df_merged.merge(
            df_gdp,
            on='Country',
            how='left',
            suffixes=('', '_gdp')
        )
        
        # Merge with life expectancy data
        df_merged = df_merged.merge(
            df_life_exp,
            on='Country',
            how='left',
            suffixes=('', '_life')
        )
        
        print(f"✅ Merged dataset: {len(df_merged)} countries")
        print(f"   Columns: {list(df_merged.columns)}")
        
        # Report merge statistics
        print("\n📊 Merge Statistics:")
        print(f"   - Countries with all data: {df_merged.dropna().shape[0]}")
        print(f"   - Countries missing GDP: {df_merged['GDP_USD_millions'].isna().sum()}")
        print(f"   - Countries missing Life Expectancy: {df_merged['Life_Expectancy'].isna().sum()}")
        
        return df_merged
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create new features from existing data
        
        Args:
            df: Merged DataFrame
            
        Returns:
            DataFrame with new features
        """
        print("\n" + "=" * 70)
        print("🔧 CREATING NEW FEATURES")
        print("=" * 70)
        
        df_featured = df.copy()
        
        # 1. GDP per Capita
        df_featured['GDP_per_Capita'] = (
            df_featured['GDP_USD_millions'] * 1_000_000 / df_featured['Population']
        )
        print("✅ Created: GDP_per_Capita")
        
        # 2. Log transformations (for skewed distributions)
        df_featured['Log_Population'] = np.log1p(df_featured['Population'])
        df_featured['Log_GDP'] = np.log1p(df_featured['GDP_USD_millions'])
        df_featured['Log_GDP_per_Capita'] = np.log1p(df_featured['GDP_per_Capita'])
        print("✅ Created: Log transformations (Population, GDP, GDP_per_Capita)")
        
        # 3. Population categories
        population_quartiles = df_featured['Population'].quantile([0.25, 0.5, 0.75])
        df_featured['Population_Category'] = pd.cut(
            df_featured['Population'],
            bins=[0, population_quartiles[0.25], population_quartiles[0.5], 
                  population_quartiles[0.75], float('inf')],
            labels=['Small', 'Medium', 'Large', 'Very Large']
        )
        print("✅ Created: Population_Category")
        
        # 4. GDP categories
        if df_featured['GDP_USD_billions'].notna().sum() > 3:
            gdp_quartiles = df_featured['GDP_USD_billions'].quantile([0.25, 0.5, 0.75])
            df_featured['GDP_Category'] = pd.cut(
                df_featured['GDP_USD_billions'],
                bins=[0, gdp_quartiles[0.25], gdp_quartiles[0.5], 
                      gdp_quartiles[0.75], float('inf')],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
            print("✅ Created: GDP_Category")
        else:
            print("⚠️  Skipped: GDP_Category (insufficient data)")
        
        # 5. Economic development indicator (GDP per capita categories)
        if df_featured['GDP_per_Capita'].notna().sum() > 3:
            gdp_pc_quartiles = df_featured['GDP_per_Capita'].quantile([0.33, 0.67])
            df_featured['Development_Level'] = pd.cut(
                df_featured['GDP_per_Capita'],
                bins=[0, gdp_pc_quartiles[0.33], gdp_pc_quartiles[0.67], float('inf')],
                labels=['Developing', 'Emerging', 'Developed']
            )
            print("✅ Created: Development_Level")
        else:
            print("⚠️  Skipped: Development_Level (insufficient data)")
        
        # 6. Gender gap in life expectancy (if available)
        if 'Life_Expectancy_Female' in df_featured.columns and 'Life_Expectancy_Male' in df_featured.columns:
            df_featured['Life_Expectancy_Gender_Gap'] = (
                df_featured['Life_Expectancy_Female'] - df_featured['Life_Expectancy_Male']
            )
            print("✅ Created: Life_Expectancy_Gender_Gap")
        
        # 7. Wealth score (normalized combination of GDP and GDP per capita)
        if df_featured['GDP_USD_billions'].notna().sum() > 3 and df_featured['GDP_per_Capita'].notna().sum() > 3:
            # Normalize values to 0-1 range
            gdp_min = df_featured['GDP_USD_billions'].min()
            gdp_max = df_featured['GDP_USD_billions'].max()
            
            if gdp_max > gdp_min:
                gdp_normalized = (
                    (df_featured['GDP_USD_billions'] - gdp_min) /
                    (gdp_max - gdp_min)
                )
            else:
                gdp_normalized = pd.Series(0, index=df_featured.index)
            
            gdp_pc_min = df_featured['GDP_per_Capita'].min()
            gdp_pc_max = df_featured['GDP_per_Capita'].max()
            
            if gdp_pc_max > gdp_pc_min:
                gdp_pc_normalized = (
                    (df_featured['GDP_per_Capita'] - gdp_pc_min) /
                    (gdp_pc_max - gdp_pc_min)
                )
            else:
                gdp_pc_normalized = pd.Series(0, index=df_featured.index)
            
            # Combined wealth score (average of both normalized values)
            df_featured['Wealth_Score'] = (gdp_normalized + gdp_pc_normalized) / 2
            print("✅ Created: Wealth_Score")
        else:
            print("⚠️  Skipped: Wealth_Score (insufficient data)")
        
        # 8. Population density proxy (requires area data - placeholder)
        # Note: You can add area data later and calculate real population density
        
        print(f"\n✅ Total features created: {len(df_featured.columns) - len(df.columns)}")
        
        return df_featured
    
    def get_data_quality_report(self, df: pd.DataFrame) -> Dict:
        """
        Generate a data quality report
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        print("\n" + "=" * 70)
        print("📋 DATA QUALITY REPORT")
        print("=" * 70)
        
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isna().sum().to_dict(),
            'missing_percentage': (df.isna().sum() / len(df) * 100).to_dict(),
            'duplicates': df.duplicated(subset=['Country']).sum(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist()
        }
        
        print(f"Total Rows: {report['total_rows']}")
        print(f"Total Columns: {report['total_columns']}")
        print(f"Duplicate Countries: {report['duplicates']}")
        
        print("\n📊 Missing Values:")
        for col, count in report['missing_values'].items():
            if count > 0:
                pct = report['missing_percentage'][col]
                print(f"   - {col}: {count} ({pct:.1f}%)")
        
        return report
    
    def save_processed_data(self, df: pd.DataFrame, 
                           csv_path: str = 'processed_data.csv',
                           excel_path: str = 'processed_data.xlsx'):
        """
        Save processed data to files
        
        Args:
            df: Processed DataFrame
            csv_path: Path to save CSV file
            excel_path: Path to save Excel file
        """
        print("\n" + "=" * 70)
        print("💾 SAVING PROCESSED DATA")
        print("=" * 70)
        
        # Save to CSV
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✅ Saved CSV: {csv_path}")
        
        # Save to Excel
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"✅ Saved Excel: {excel_path}")
        
        print(f"\n📦 Dataset shape: {df.shape}")
        print(f"   Rows: {df.shape[0]} countries")
        print(f"   Columns: {df.shape[1]} features")


def main():
    """Main preprocessing pipeline"""
    
    print("\n" + "=" * 70)
    print("🚀 STARTING DATA PREPROCESSING PIPELINE")
    print("=" * 70)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Step 1: Load and clean individual datasets
    df_population = preprocessor.load_and_clean_population('population_data.csv')
    df_gdp = preprocessor.load_and_clean_gdp('gdp_data.csv')
    
    # For life expectancy, try to load or create placeholder
    try:
        df_life_exp = preprocessor.load_and_clean_life_expectancy(
            filepath='life_expectancy_data.csv'
        )
    except FileNotFoundError:
        print("\n⚠️  Note: Run wikipedia_scraper.py to get life expectancy data")
        print("   Using placeholder data for demonstration...")
        df_life_exp = preprocessor.load_and_clean_life_expectancy()
    
    # Step 2: Merge datasets
    df_merged = preprocessor.merge_datasets(df_population, df_gdp, df_life_exp)
    
    # Step 3: Create new features
    df_final = preprocessor.create_features(df_merged)
    
    # Step 4: Generate data quality report
    quality_report = preprocessor.get_data_quality_report(df_final)
    
    # Step 5: Save processed data
    preprocessor.save_processed_data(
        df_final,
        csv_path='processed_data.csv',
        excel_path='processed_data.xlsx'
    )
    
    # Display sample of final dataset
    print("\n" + "=" * 70)
    print("📊 FINAL DATASET PREVIEW (Top 10 countries)")
    print("=" * 70)
    
    # Select key columns for display
    display_cols = ['Country', 'Population', 'GDP_USD_billions', 
                   'GDP_per_Capita', 'Life_Expectancy', 'Development_Level']
    
    # Filter columns that exist
    display_cols = [col for col in display_cols if col in df_final.columns]
    
    print(df_final[display_cols].head(10).to_string(index=False))
    
    print("\n" + "=" * 70)
    print("✅ PREPROCESSING COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    print("\n📁 Output Files:")
    print("   - processed_data.csv")
    print("   - processed_data.xlsx")
    
    print("\n🎯 Next Steps (Week 3):")
    print("   - Feature selection for modeling")
    print("   - Train/test split")
    print("   - Model training (Boosting algorithms)")
    print("   - Model evaluation with MLflow")
    
    return df_final


if __name__ == "__main__":
    # Run the preprocessing pipeline
    df_processed = main()
    
    # Optional: Display summary statistics
    print("\n" + "=" * 70)
    print("📈 SUMMARY STATISTICS")
    print("=" * 70)
    print(df_processed.describe().to_string())
