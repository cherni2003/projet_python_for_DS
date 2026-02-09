"""
Web Scraping Script for Wikipedia Country Data
Scrapes population, GDP, and life expectancy data from Wikipedia
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict

class WikipediaScraper:
    """Class to scrape country data from Wikipedia"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        # Remove references like [1], [2], etc.
        text = re.sub(r'\[.*?\]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def scrape_population(self) -> pd.DataFrame:
        """
        Scrape population data from Wikipedia
        Returns: DataFrame with Country and Population columns
        """
        url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
        
        print(f"📊 Scraping population data from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main table
            table = soup.find('table', {'class': 'wikitable'})
            
            if not table:
                print("❌ Table not found!")
                return pd.DataFrame()
            
            data = []
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 3:
                    try:
                        # Extract rank, country, and population
                        rank = self.clean_text(cols[0].get_text())
                        country = self.clean_text(cols[1].get_text())
                        population = self.clean_text(cols[2].get_text())
                        
                        data.append({
                            'Rank': rank,
                            'Country': country,
                            'Population': population
                        })
                    except Exception as e:
                        continue
            
            df = pd.DataFrame(data)
            print(f"✅ Successfully scraped {len(df)} countries")
            return df
            
        except Exception as e:
            print(f"❌ Error scraping population data: {e}")
            return pd.DataFrame()
    
    def scrape_gdp(self) -> pd.DataFrame:
        """
        Scrape GDP data from Wikipedia
        Returns: DataFrame with Country and GDP columns
        """
        url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
        
        print(f"\n💰 Scraping GDP data from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find tables - usually IMF, World Bank, and UN tables
            tables = soup.find_all('table', {'class': 'wikitable'})
            
            data = []
            
            # Try to find the IMF table (usually the first one)
            for table in tables[:1]:
                rows = table.find_all('tr')[2:]  # Skip header rows
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 3:
                        try:
                            rank = self.clean_text(cols[0].get_text())
                            country = self.clean_text(cols[1].get_text())
                            gdp = self.clean_text(cols[2].get_text())
                            
                            data.append({
                                'Rank': rank,
                                'Country': country,
                                'GDP (USD millions)': gdp
                            })
                        except Exception as e:
                            continue
            
            df = pd.DataFrame(data)
            print(f"✅ Successfully scraped {len(df)} countries")
            return df
            
        except Exception as e:
            print(f"❌ Error scraping GDP data: {e}")
            return pd.DataFrame()
    
    def scrape_life_expectancy(self) -> pd.DataFrame:
        """
        Scrape life expectancy data from Wikipedia
        Returns: DataFrame with Country and Life Expectancy columns
        """
        url = "https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy"
        
        print(f"\n🏥 Scraping life expectancy data from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main table
            tables = soup.find_all('table', {'class': 'wikitable'})
            
            data = []
            
            for table in tables[:1]:  # First table usually has the most recent data
                rows = table.find_all('tr')[1:]
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2:
                        try:
                            country = self.clean_text(cols[0].get_text())
                            
                            # Try to get overall life expectancy (usually second column)
                            life_exp = self.clean_text(cols[1].get_text())
                            
                            # Get male and female if available
                            male = self.clean_text(cols[2].get_text()) if len(cols) > 2 else ''
                            female = self.clean_text(cols[3].get_text()) if len(cols) > 3 else ''
                            
                            data.append({
                                'Country': country,
                                'Life Expectancy (Overall)': life_exp,
                                'Life Expectancy (Male)': male,
                                'Life Expectancy (Female)': female
                            })
                        except Exception as e:
                            continue
            
            df = pd.DataFrame(data)
            print(f"✅ Successfully scraped {len(df)} countries")
            return df
            
        except Exception as e:
            print(f"❌ Error scraping life expectancy data: {e}")
            return pd.DataFrame()
    
    def scrape_all(self, save_to_csv=True, save_to_excel=True) -> Dict[str, pd.DataFrame]:
        """
        Scrape all three datasets
        
        Args:
            save_to_csv: Save each dataset to separate CSV files
            save_to_excel: Save all datasets to one Excel file with multiple sheets
            
        Returns: Dictionary containing all three DataFrames
        """
        print("="*70)
        print("🚀 STARTING WIKIPEDIA WEB SCRAPING")
        print("="*70)
        
        # Scrape all data
        df_population = self.scrape_population()
        df_gdp = self.scrape_gdp()
        df_life_exp = self.scrape_life_expectancy()
        
        results = {
            'population': df_population,
            'gdp': df_gdp,
            'life_expectancy': df_life_exp
        }
        
        # Save to CSV
        if save_to_csv:
            print("\n" + "="*70)
            print("💾 SAVING TO CSV FILES")
            print("="*70)
            
            if not df_population.empty:
                df_population.to_csv('population_data.csv', index=False, encoding='utf-8')
                print("✅ Saved: population_data.csv")
            
            if not df_gdp.empty:
                df_gdp.to_csv('gdp_data.csv', index=False, encoding='utf-8')
                print("✅ Saved: gdp_data.csv")
            
            if not df_life_exp.empty:
                df_life_exp.to_csv('life_expectancy_data.csv', index=False, encoding='utf-8')
                print("✅ Saved: life_expectancy_data.csv")
        
        # Save to Excel
        if save_to_excel:
            print("\n" + "="*70)
            print("📊 SAVING TO EXCEL FILE")
            print("="*70)
            
            try:
                with pd.ExcelWriter('countries_data.xlsx', engine='openpyxl') as writer:
                    if not df_population.empty:
                        df_population.to_excel(writer, sheet_name='Population', index=False)
                    if not df_gdp.empty:
                        df_gdp.to_excel(writer, sheet_name='GDP', index=False)
                    if not df_life_exp.empty:
                        df_life_exp.to_excel(writer, sheet_name='Life Expectancy', index=False)
                
                print("✅ Saved: countries_data.xlsx (with multiple sheets)")
            except Exception as e:
                print(f"❌ Error saving Excel file: {e}")
        
        # Display summary
        print("\n" + "="*70)
        print("📈 DATA SUMMARY")
        print("="*70)
        print(f"Population data: {len(df_population)} rows")
        print(f"GDP data: {len(df_gdp)} rows")
        print(f"Life Expectancy data: {len(df_life_exp)} rows")
        
        # Display previews
        if not df_population.empty:
            print("\n" + "="*70)
            print("👥 POPULATION DATA (Top 10)")
            print("="*70)
            print(df_population.head(10).to_string(index=False))
        
        if not df_gdp.empty:
            print("\n" + "="*70)
            print("💰 GDP DATA (Top 10)")
            print("="*70)
            print(df_gdp.head(10).to_string(index=False))
        
        if not df_life_exp.empty:
            print("\n" + "="*70)
            print("🏥 LIFE EXPECTANCY DATA (Top 10)")
            print("="*70)
            print(df_life_exp.head(10).to_string(index=False))
        
        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETED!")
        print("="*70)
        
        return results


# Example usage
if __name__ == "__main__":
    # Create scraper instance
    scraper = WikipediaScraper()
    
    # Scrape all data and save to files
    data = scraper.scrape_all(save_to_csv=True, save_to_excel=True)
    
    # You can also scrape individual datasets:
    # df_pop = scraper.scrape_population()
    # df_gdp = scraper.scrape_gdp()
    # df_life = scraper.scrape_life_expectancy()
    
    # Access the data
    # population_df = data['population']
    # gdp_df = data['gdp']
    # life_expectancy_df = data['life_expectancy']
