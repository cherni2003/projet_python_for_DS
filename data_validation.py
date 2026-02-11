import pandas as pd
import numpy as np
from typing import Dict, List

class DataValidator:
    """Class to validate and inspect processed data"""
    
    def __init__(self, filepath: str='C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/processed/processed_data.csv'):
        """Initialize with processed data file"""
        self.df = pd.read_csv(filepath)
        print(f"✅ Loaded data: {filepath}")
        print(f"   Shape: {self.df.shape}")
    
    def check_missing_values(self) -> pd.DataFrame:
        """
        Analyze missing values in the dataset
        
        Returns:
            DataFrame with missing value statistics
        """
        print("\n" + "=" * 70)
        print("🔍 MISSING VALUES ANALYSIS")
        print("=" * 70)
        
        missing = self.df.isna().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing_Count': missing.values,
            'Missing_Percentage': missing_pct.values
        })
        
        # Filter only columns with missing values
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
            'Missing_Percentage', ascending=False
        )
        
        if len(missing_df) > 0:
            print(missing_df.to_string(index=False))
        else:
            print("✅ No missing values found!")
        
        return missing_df
    
    def check_duplicates(self) -> int:
        """
        Check for duplicate countries
        
        Returns:
            Number of duplicates
        """
        print("\n" + "=" * 70)
        print("🔍 DUPLICATE CHECK")
        print("=" * 70)
        
        duplicates = self.df.duplicated(subset=['Country']).sum()
        
        if duplicates > 0:
            print(f"⚠️  Found {duplicates} duplicate countries:")
            dupe_countries = self.df[self.df.duplicated(subset=['Country'], keep=False)]['Country']
            print(dupe_countries.to_string())
        else:
            print("✅ No duplicate countries found!")
        
        return duplicates
    
    def check_outliers(self, column: str, threshold: float = 3.0) -> List:
        """
        Detect outliers using Z-score method
        
        Args:
            column: Column name to check
            threshold: Z-score threshold (default 3.0)
            
        Returns:
            List of outlier indices
        """
        if column not in self.df.columns:
            print(f"⚠️  Column '{column}' not found")
            return []
        
        data = self.df[column].dropna()
        
        if len(data) == 0:
            return []
        
        mean = data.mean()
        std = data.std()
        
        if std == 0:
            return []
        
        z_scores = np.abs((data - mean) / std)
        outliers = data[z_scores > threshold]
        
        return outliers.index.tolist()
    
    def analyze_outliers(self) -> Dict:
        """
        Analyze outliers in key numerical columns
        
        Returns:
            Dictionary with outlier information
        """
        print("\n" + "=" * 70)
        print("🔍 OUTLIER ANALYSIS (Z-score > 3)")
        print("=" * 70)
        
        numerical_cols = [
            'Population', 'GDP_USD_billions', 'GDP_per_Capita',
            'Life_Expectancy', 'Life_Expectancy_Gender_Gap'
        ]
        
        outlier_report = {}
        
        for col in numerical_cols:
            if col in self.df.columns:
                outlier_indices = self.check_outliers(col)
                
                if len(outlier_indices) > 0:
                    outlier_countries = self.df.loc[outlier_indices, ['Country', col]]
                    outlier_report[col] = outlier_countries
                    
                    print(f"\n{col}: {len(outlier_indices)} outliers")
                    print(outlier_countries.to_string(index=False))
        
        if not outlier_report:
            print("✅ No significant outliers detected!")
        
        return outlier_report
    
    def check_data_ranges(self) -> Dict:
        """
        Check if data values are in reasonable ranges
        
        Returns:
            Dictionary with range validation results
        """
        print("\n" + "=" * 70)
        print("🔍 DATA RANGE VALIDATION")
        print("=" * 70)
        
        issues = []
        
        # Check Population (should be > 0)
        if 'Population' in self.df.columns:
            negative_pop = self.df[self.df['Population'] <= 0]
            if len(negative_pop) > 0:
                issues.append(f"⚠️  {len(negative_pop)} countries with Population <= 0")
        
        # Check Life Expectancy (should be 30-120)
        if 'Life_Expectancy' in self.df.columns:
            invalid_life = self.df[
                (self.df['Life_Expectancy'] < 30) | 
                (self.df['Life_Expectancy'] > 120)
            ]
            if len(invalid_life) > 0:
                issues.append(f"⚠️  {len(invalid_life)} countries with Life Expectancy outside 30-120 range")
                print(invalid_life[['Country', 'Life_Expectancy']].to_string(index=False))
        
        # Check GDP (should be > 0)
        if 'GDP_USD_billions' in self.df.columns:
            negative_gdp = self.df[self.df['GDP_USD_billions'] <= 0]
            if len(negative_gdp) > 0:
                issues.append(f"⚠️  {len(negative_gdp)} countries with GDP <= 0")
        
        # Check Gender Gap (should be 0-15 years)
        if 'Life_Expectancy_Gender_Gap' in self.df.columns:
            invalid_gap = self.df[
                (self.df['Life_Expectancy_Gender_Gap'] < 0) | 
                (self.df['Life_Expectancy_Gender_Gap'] > 15)
            ]
            if len(invalid_gap) > 0:
                issues.append(f"⚠️  {len(invalid_gap)} countries with Gender Gap outside 0-15 range")
                print(invalid_gap[['Country', 'Life_Expectancy_Gender_Gap']].to_string(index=False))
        
        if not issues:
            print("✅ All data values are in reasonable ranges!")
        else:
            for issue in issues:
                print(issue)
        
        return {'issues': issues}
    
    def get_top_bottom_countries(self, n: int = 10):
        """
        Display top and bottom countries by key metrics
        
        Args:
            n: Number of countries to show
        """
        print("\n" + "=" * 70)
        print(f"🏆 TOP & BOTTOM {n} COUNTRIES BY KEY METRICS")
        print("=" * 70)
        
        metrics = {
            'Population': 'Population',
            'GDP_USD_billions': 'GDP (billions)',
            'Life_Expectancy': 'Life Expectancy',
            'GDP_per_Capita': 'GDP per Capita'
        }
        
        for col, label in metrics.items():
            if col in self.df.columns and self.df[col].notna().sum() > 0:
                print(f"\n{'='*35}")
                print(f"📊 {label}")
                print('='*35)
                
                # Top N
                print(f"\nTop {n}:")
                top = self.df.nlargest(n, col)[['Country', col]]
                print(top.to_string(index=False))
                
                # Bottom N
                print(f"\nBottom {n}:")
                bottom = self.df.nsmallest(n, col)[['Country', col]]
                print(bottom.to_string(index=False))
    
    def correlation_analysis(self):
        """Analyze correlations between numerical variables"""
        print("\n" + "=" * 70)
        print("🔍 CORRELATION ANALYSIS")
        print("=" * 70)
        
        # Select numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Remove rank columns
        numerical_cols = [col for col in numerical_cols if 'Rank' not in col]
        
        # Calculate correlation matrix
        corr_matrix = self.df[numerical_cols].corr()
        
        # Find strong correlations (> 0.7 or < -0.7)
        print("\n📈 Strong Correlations (|r| > 0.7):")
        
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': round(corr_value, 3)
                    })
        
        if strong_corr:
            corr_df = pd.DataFrame(strong_corr)
            print(corr_df.to_string(index=False))
        else:
            print("No strong correlations found (|r| > 0.7)")
        
        # Correlation with Life Expectancy
        if 'Life_Expectancy' in numerical_cols:
            print("\n🎯 Correlation with Life Expectancy:")
            life_corr = corr_matrix['Life_Expectancy'].sort_values(ascending=False)
            print(life_corr.to_string())
    
    def data_completeness_report(self):
        """Report on data completeness by country"""
        print("\n" + "=" * 70)
        print("📊 DATA COMPLETENESS REPORT")
        print("=" * 70)
        
        # Calculate completeness for each row
        self.df['Completeness'] = self.df.notna().sum(axis=1) / len(self.df.columns) * 100
        
        # Categorize completeness
        complete = self.df[self.df['Completeness'] == 100.0]
        mostly_complete = self.df[(self.df['Completeness'] >= 80) & (self.df['Completeness'] < 100)]
        partial = self.df[(self.df['Completeness'] >= 50) & (self.df['Completeness'] < 80)]
        incomplete = self.df[self.df['Completeness'] < 50]
        
        print(f"✅ Complete (100%): {len(complete)} countries ({len(complete)/len(self.df)*100:.1f}%)")
        print(f"⚠️  Mostly Complete (80-99%): {len(mostly_complete)} countries ({len(mostly_complete)/len(self.df)*100:.1f}%)")
        print(f"⚠️  Partial (50-79%): {len(partial)} countries ({len(partial)/len(self.df)*100:.1f}%)")
        print(f"❌ Incomplete (<50%): {len(incomplete)} countries ({len(incomplete)/len(self.df)*100:.1f}%)")
        
        # Show incomplete countries
        if len(incomplete) > 0:
            print("\n❌ Countries with <50% data:")
            print(incomplete[['Country', 'Completeness']].sort_values('Completeness').to_string(index=False))
    
    def generate_full_report(self):
        """Generate a complete validation report"""
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE DATA VALIDATION REPORT")
        print("=" * 70)
        
        # 1. Basic info
        print(f"\n📊 Dataset Overview:")
        print(f"   Total Countries: {len(self.df)}")
        print(f"   Total Features: {len(self.df.columns)}")
        
        # 2. Missing values
        self.check_missing_values()
        
        # 3. Duplicates
        self.check_duplicates()
        
        # 4. Data ranges
        self.check_data_ranges()
        
        # 5. Outliers
        self.analyze_outliers()
        
        # 6. Completeness
        self.data_completeness_report()
        
        # 7. Top/Bottom countries
        self.get_top_bottom_countries(n=5)
        
        # 8. Correlations
        self.correlation_analysis()
        
        print("\n" + "=" * 70)
        print("✅ VALIDATION REPORT COMPLETE")
        print("=" * 70)


def main():
    """Run validation on processed data"""
    
    # Create validator
    validator = DataValidator(r'C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/processed/processed_data.csv')
    
    # Generate full report
    validator.generate_full_report()


if __name__ == "__main__":
    main()
