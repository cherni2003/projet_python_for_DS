"""
Script d'Analyse Exploratoire des Données (EDA)
Analyse complète des données de population, PIB et espérance de vie
Sans nettoyage - Données brutes uniquement
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class CountryDataEDA:
    """Classe pour l'analyse exploratoire des données pays"""
    
    def __init__(self):
        self.df_population = None
        self.df_gdp = None
        self.df_life_exp = None
        self.output_dir = Path('eda_outputs')
        self.output_dir.mkdir(exist_ok=True)
        
    def load_data(self, from_excel=True):
        """
        Charger les données depuis Excel ou CSV
        
        Args:
            from_excel: Si True, charge depuis Excel, sinon depuis CSV
        """
        print("="*80)
        print("📁 CHARGEMENT DES DONNÉES BRUTES")
        print("="*80)
        
        try:
            if from_excel:
                print("📊 Chargement depuis countries_data.xlsx...")
                
                # Vérifier les feuilles disponibles
                excel_file = pd.ExcelFile('countries_data.xlsx')
                print(f"\n🔍 Feuilles disponibles: {excel_file.sheet_names}")
                
                # Mapper les noms de feuilles avec flexibilité
                sheet_mapping = {
                    'population': None,
                    'gdp': None,
                    'life_expectancy': None
                }
                
                for sheet in excel_file.sheet_names:
                    sheet_lower = sheet.lower().replace(' ', '').replace('_', '')
                    if 'population' in sheet_lower:
                        sheet_mapping['population'] = sheet
                    elif 'gdp' in sheet_lower or 'pib' in sheet_lower:
                        sheet_mapping['gdp'] = sheet
                    elif 'life' in sheet_lower or 'expectancy' in sheet_lower or 'esperance' in sheet_lower:
                        sheet_mapping['life_expectancy'] = sheet
                
                # Charger les données
                if sheet_mapping['population']:
                    self.df_population = pd.read_excel('countries_data.xlsx', sheet_name=sheet_mapping['population'])
                    print(f"✅ Population chargée depuis: '{sheet_mapping['population']}'")
                else:
                    print("⚠️ Feuille Population non trouvée dans Excel, chargement depuis CSV...")
                    self.df_population = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/population_data.csv')
                
                if sheet_mapping['gdp']:
                    self.df_gdp = pd.read_excel('countries_data.xlsx', sheet_name=sheet_mapping['gdp'])
                    print(f"✅ GDP chargé depuis: '{sheet_mapping['gdp']}'")
                else:
                    print("⚠️ Feuille GDP non trouvée dans Excel, chargement depuis CSV...")
                    self.df_gdp = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/gdp_data.csv')
                
                if sheet_mapping['life_expectancy']:
                    self.df_life_exp = pd.read_excel('countries_data.xlsx', sheet_name=sheet_mapping['life_expectancy'])
                    print(f"✅ Life Expectancy chargée depuis: '{sheet_mapping['life_expectancy']}'")
                else:
                    print("⚠️ Feuille Life Expectancy non trouvée dans Excel, chargement depuis CSV...")
                    try:
                        self.df_life_exp = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/life_expectancy.csv')
                    except FileNotFoundError:
                        print("⚠️ Fichier life_expectancy_data.csv non trouvé, création d'un DataFrame vide")
                        self.df_life_exp = pd.DataFrame()
                    
            else:
                print("📄 Chargement depuis fichiers CSV...")
                self.df_population = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/population_data.csv')
                print("✅ population_data.csv chargé")
                
                self.df_gdp = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/gdp_data.csv')
                print("✅ gdp_data.csv chargé")
                
                try:
                    self.df_life_exp = pd.read_csv('C:/Users/Cherni Oumaima/Desktop/projets python/projet_python_for_DS/data/raw/life_expectancy.csv')
                    print("✅ life_expectancy_data.csv chargé")
                except FileNotFoundError:
                    print("⚠️ life_expectancy_data.csv non trouvé, création d'un DataFrame vide")
                    self.df_life_exp = pd.DataFrame()
            
            print(f"\n📊 Résumé du chargement:")
            print(f"   Population: {len(self.df_population)} lignes")
            print(f"   GDP: {len(self.df_gdp)} lignes")
            print(f"   Life Expectancy: {len(self.df_life_exp)} lignes")
            print()
            
        except FileNotFoundError as e:
            print(f"❌ Erreur: Fichier non trouvé - {e}")
            print("💡 Assurez-vous d'avoir exécuté le script de scraping d'abord!")
            raise
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            print("\n💡 Essayez de charger depuis les fichiers CSV:")
            print("   analyzer.run_complete_eda(from_excel=False)")
            raise
    
    def basic_statistics(self):
        """Afficher les statistiques de base des données brutes"""
        print("="*80)
        print("📊 STATISTIQUES DE BASE - DONNÉES BRUTES")
        print("="*80)
        
        datasets = {
            'POPULATION': self.df_population,
            'GDP': self.df_gdp,
            'LIFE EXPECTANCY': self.df_life_exp
        }
        
        for name, df in datasets.items():
            if df.empty:
                print(f"\n⚠️ {name}: Dataset vide, ignoré")
                continue
                
            print(f"\n{'='*80}")
            print(f"📌 {name}")
            print(f"{'='*80}")
            
            print(f"\n🔢 Dimensions: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            
            print(f"\n📋 Colonnes:")
            for i, col in enumerate(df.columns, 1):
                print(f"   {i}. {col} ({df[col].dtype})")
            
            print(f"\n📊 Aperçu des données:")
            print(df.head(10).to_string(index=False))
            
            print(f"\n❓ Valeurs manquantes:")
            missing = df.isnull().sum()
            if missing.sum() > 0:
                for col, count in missing.items():
                    if count > 0:
                        pct = (count / len(df)) * 100
                        print(f"   {col}: {count} ({pct:.2f}%)")
            else:
                print("   ✅ Aucune valeur manquante détectée")
            
            print(f"\n🔢 Types de données:")
            print(df.dtypes.to_string())
            
            print(f"\n📈 Statistiques descriptives:")
            print(df.describe(include='all').to_string())
            
            print("\n")
    
    def data_quality_report(self):
        """Rapport sur la qualité des données brutes"""
        print("="*80)
        print("🔍 RAPPORT DE QUALITÉ DES DONNÉES BRUTES")
        print("="*80)
        
        datasets = {
            'Population': self.df_population,
            'GDP': self.df_gdp,
            'Life Expectancy': self.df_life_exp
        }
        
        quality_report = []
        
        for name, df in datasets.items():
            if df.empty:
                print(f"\n⚠️ {name}: Dataset vide, ignoré")
                continue
                
            print(f"\n{'='*80}")
            print(f"📊 {name.upper()}")
            print(f"{'='*80}")
            
            # Taille du dataset
            rows, cols = df.shape
            print(f"\n📏 Taille: {rows} lignes × {cols} colonnes")
            
            # Valeurs manquantes
            missing_total = df.isnull().sum().sum()
            missing_pct = (missing_total / (rows * cols)) * 100 if rows * cols > 0 else 0
            print(f"\n❓ Valeurs manquantes: {missing_total} ({missing_pct:.2f}%)")
            
            # Doublons
            duplicates = df.duplicated().sum()
            duplicates_pct = (duplicates / rows) * 100 if rows > 0 else 0
            print(f"\n🔄 Doublons: {duplicates} ({duplicates_pct:.2f}%)")
            
            # Types de données
            print(f"\n📊 Types de données:")
            for dtype, count in df.dtypes.value_counts().items():
                print(f"   {dtype}: {count} colonnes")
            
            # Valeurs uniques par colonne
            print(f"\n🔢 Valeurs uniques par colonne:")
            for col in df.columns:
                unique_count = df[col].nunique()
                unique_pct = (unique_count / rows) * 100 if rows > 0 else 0
                print(f"   {col}: {unique_count} ({unique_pct:.2f}%)")
            
            # Échantillons de données
            print(f"\n📋 Échantillon aléatoire (5 lignes):")
            print(df.sample(min(5, len(df))).to_string(index=False))
            
            quality_report.append({
                'Dataset': name,
                'Lignes': rows,
                'Colonnes': cols,
                'Valeurs manquantes': missing_total,
                '% Manquantes': f"{missing_pct:.2f}%",
                'Doublons': duplicates,
                '% Doublons': f"{duplicates_pct:.2f}%"
            })
        
        # Résumé global
        print(f"\n{'='*80}")
        print("📈 RÉSUMÉ GLOBAL DE LA QUALITÉ")
        print(f"{'='*80}\n")
        summary_df = pd.DataFrame(quality_report)
        print(summary_df.to_string(index=False))
        
        # Sauvegarder le rapport
        summary_df.to_csv(self.output_dir / 'quality_report.csv', index=False)
        print(f"\n💾 Rapport sauvegardé: {self.output_dir / 'quality_report.csv'}")
    
    def visualize_distributions(self):
        """Visualiser les distributions des données brutes"""
        print("\n" + "="*80)
        print("📊 VISUALISATION DES DISTRIBUTIONS")
        print("="*80)
        
        # Distribution de la longueur des valeurs textuelles
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Distribution de la Longueur des Valeurs Textuelles (Données Brutes)', 
                     fontsize=16, fontweight='bold')
        
        # Population - Country names length
        if not self.df_population.empty and 'Country' in self.df_population.columns:
            lengths = self.df_population['Country'].astype(str).str.len()
            axes[0, 0].hist(lengths, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            axes[0, 0].set_title('Longueur des Noms de Pays (Population)')
            axes[0, 0].set_xlabel('Nombre de caractères')
            axes[0, 0].set_ylabel('Fréquence')
            axes[0, 0].grid(True, alpha=0.3)
        else:
            axes[0, 0].text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
            axes[0, 0].set_title('Longueur des Noms de Pays (Population)')
        
        # Population values length
        if not self.df_population.empty and 'Population' in self.df_population.columns:
            lengths = self.df_population['Population'].astype(str).str.len()
            axes[0, 1].hist(lengths, bins=30, color='lightgreen', edgecolor='black', alpha=0.7)
            axes[0, 1].set_title('Longueur des Valeurs de Population')
            axes[0, 1].set_xlabel('Nombre de caractères')
            axes[0, 1].set_ylabel('Fréquence')
            axes[0, 1].grid(True, alpha=0.3)
        else:
            axes[0, 1].text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
            axes[0, 1].set_title('Longueur des Valeurs de Population')
        
        # GDP values length
        if not self.df_gdp.empty and 'GDP (USD millions)' in self.df_gdp.columns:
            lengths = self.df_gdp['GDP (USD millions)'].astype(str).str.len()
            axes[1, 0].hist(lengths, bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[1, 0].set_title('Longueur des Valeurs de PIB')
            axes[1, 0].set_xlabel('Nombre de caractères')
            axes[1, 0].set_ylabel('Fréquence')
            axes[1, 0].grid(True, alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
            axes[1, 0].set_title('Longueur des Valeurs de PIB')
        
        # Life expectancy values length
        if not self.df_life_exp.empty and 'Life Expectancy (Overall)' in self.df_life_exp.columns:
            lengths = self.df_life_exp['Life Expectancy (Overall)'].astype(str).str.len()
            axes[1, 1].hist(lengths, bins=30, color='plum', edgecolor='black', alpha=0.7)
            axes[1, 1].set_title('Longueur des Valeurs d\'Espérance de Vie')
            axes[1, 1].set_xlabel('Nombre de caractères')
            axes[1, 1].set_ylabel('Fréquence')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
            axes[1, 1].set_title('Longueur des Valeurs d\'Espérance de Vie')
        
        plt.tight_layout()
        output_file = self.output_dir / 'distributions_raw_data.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {output_file}")
        plt.close()
    
    def analyze_text_patterns(self):
        """Analyser les patterns dans les données textuelles brutes"""
        print("\n" + "="*80)
        print("🔤 ANALYSE DES PATTERNS TEXTUELS")
        print("="*80)
        
        # Population data
        if not self.df_population.empty and 'Population' in self.df_population.columns:
            pop_values = self.df_population['Population'].astype(str)
            
            print("\n📊 PATTERNS DANS LES DONNÉES DE POPULATION:")
            print(f"   Valeurs contenant des virgules: {pop_values.str.contains(',', na=False).sum()}")
            print(f"   Valeurs contenant des points: {pop_values.str.contains(r'\.', na=False).sum()}")
            print(f"   Valeurs contenant des espaces: {pop_values.str.contains(' ', na=False).sum()}")
            print(f"   Valeurs numériques pures: {pop_values.str.match(r'^\d+$', na=False).sum()}")
            
            print(f"\n   Exemples de valeurs:")
            for val in pop_values.head(10):
                print(f"      '{val}'")
        
        # GDP data
        if not self.df_gdp.empty and 'GDP (USD millions)' in self.df_gdp.columns:
            gdp_values = self.df_gdp['GDP (USD millions)'].astype(str)
            
            print("\n💰 PATTERNS DANS LES DONNÉES DE PIB:")
            print(f"   Valeurs contenant des virgules: {gdp_values.str.contains(',', na=False).sum()}")
            print(f"   Valeurs contenant des points: {gdp_values.str.contains(r'\.', na=False).sum()}")
            print(f"   Valeurs contenant des espaces: {gdp_values.str.contains(' ', na=False).sum()}")
            print(f"   Valeurs numériques pures: {gdp_values.str.match(r'^\d+$', na=False).sum()}")
            
            print(f"\n   Exemples de valeurs:")
            for val in gdp_values.head(10):
                print(f"      '{val}'")
        
        # Life expectancy data
        if not self.df_life_exp.empty and 'Life Expectancy (Overall)' in self.df_life_exp.columns:
            life_values = self.df_life_exp['Life Expectancy (Overall)'].astype(str)
            
            print("\n🏥 PATTERNS DANS LES DONNÉES D'ESPÉRANCE DE VIE:")
            print(f"   Valeurs contenant des virgules: {life_values.str.contains(',', na=False).sum()}")
            print(f"   Valeurs contenant des points: {life_values.str.contains(r'\.', na=False).sum()}")
            print(f"   Valeurs contenant des espaces: {life_values.str.contains(' ', na=False).sum()}")
            print(f"   Valeurs numériques avec décimales: {life_values.str.match(r'^\d+\.\d+$', na=False).sum()}")
            
            print(f"\n   Exemples de valeurs:")
            for val in life_values.head(10):
                print(f"      '{val}'")
    
    def create_data_overview_charts(self):
        """Créer des graphiques d'aperçu des données brutes"""
        print("\n" + "="*80)
        print("📈 CRÉATION DES GRAPHIQUES D'APERÇU")
        print("="*80)
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        fig.suptitle('Analyse de la Complexité des Données Brutes', 
                     fontsize=16, fontweight='bold')
        
        # Top pays avec les noms les plus longs
        if not self.df_population.empty and 'Country' in self.df_population.columns:
            country_lengths = self.df_population.copy()
            country_lengths['Name_Length'] = country_lengths['Country'].astype(str).str.len()
            top_20 = country_lengths.nlargest(20, 'Name_Length')
            
            axes[0, 0].barh(range(len(top_20)), top_20['Name_Length'], color='steelblue')
            axes[0, 0].set_yticks(range(len(top_20)))
            axes[0, 0].set_yticklabels(top_20['Country'], fontsize=8)
            axes[0, 0].set_xlabel('Longueur du nom (caractères)')
            axes[0, 0].set_title('Top 20 - Noms de Pays les Plus Longs')
            axes[0, 0].invert_yaxis()
            axes[0, 0].grid(True, alpha=0.3, axis='x')
        else:
            axes[0, 0].text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
        
        # Distribution du nombre de colonnes par dataset
        dataset_info = {
            'Population': len(self.df_population.columns) if not self.df_population.empty else 0,
            'GDP': len(self.df_gdp.columns) if not self.df_gdp.empty else 0,
            'Life Expectancy': len(self.df_life_exp.columns) if not self.df_life_exp.empty else 0
        }
        
        axes[0, 1].bar(dataset_info.keys(), dataset_info.values(), 
                       color=['skyblue', 'lightgreen', 'lightcoral'])
        axes[0, 1].set_ylabel('Nombre de colonnes')
        axes[0, 1].set_title('Nombre de Colonnes par Dataset')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Distribution du nombre de lignes par dataset
        dataset_rows = {
            'Population': len(self.df_population) if not self.df_population.empty else 0,
            'GDP': len(self.df_gdp) if not self.df_gdp.empty else 0,
            'Life Expectancy': len(self.df_life_exp) if not self.df_life_exp.empty else 0
        }
        
        axes[1, 0].bar(dataset_rows.keys(), dataset_rows.values(), 
                       color=['steelblue', 'seagreen', 'coral'])
        axes[1, 0].set_ylabel('Nombre de lignes')
        axes[1, 0].set_title('Nombre de Lignes par Dataset')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Valeurs manquantes par dataset
        missing_data = {
            'Population': self.df_population.isnull().sum().sum() if not self.df_population.empty else 0,
            'GDP': self.df_gdp.isnull().sum().sum() if not self.df_gdp.empty else 0,
            'Life Expectancy': self.df_life_exp.isnull().sum().sum() if not self.df_life_exp.empty else 0
        }
        
        axes[1, 1].bar(missing_data.keys(), missing_data.values(), 
                       color=['lightblue', 'lightgreen', 'lightcoral'])
        axes[1, 1].set_ylabel('Nombre de valeurs manquantes')
        axes[1, 1].set_title('Valeurs Manquantes par Dataset')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'data_overview_charts.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: {output_file}")
        plt.close()
    
    def generate_comprehensive_report(self):
        """Générer un rapport complet en format texte"""
        print("\n" + "="*80)
        print("📝 GÉNÉRATION DU RAPPORT COMPLET")
        print("="*80)
        
        report_file = self.output_dir / 'eda_comprehensive_report.txt'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT D'ANALYSE EXPLORATOIRE DES DONNÉES (EDA)\n")
            f.write("Données Brutes - Sans Nettoyage\n")
            f.write("="*80 + "\n\n")
            
            # Informations générales
            f.write("1. INFORMATIONS GÉNÉRALES\n")
            f.write("-" * 80 + "\n\n")
            
            datasets = {
                'Population': self.df_population,
                'GDP': self.df_gdp,
                'Life Expectancy': self.df_life_exp
            }
            
            for name, df in datasets.items():
                if df.empty:
                    f.write(f"\n{name.upper()}: Dataset vide\n")
                    continue
                    
                f.write(f"\n{name.upper()}:\n")
                f.write(f"  - Nombre de lignes: {len(df)}\n")
                f.write(f"  - Nombre de colonnes: {len(df.columns)}\n")
                f.write(f"  - Colonnes: {', '.join(df.columns)}\n")
                f.write(f"  - Mémoire utilisée: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
            
            # Qualité des données
            f.write("\n\n2. QUALITÉ DES DONNÉES\n")
            f.write("-" * 80 + "\n\n")
            
            for name, df in datasets.items():
                if df.empty:
                    continue
                    
                f.write(f"\n{name.upper()}:\n")
                
                # Valeurs manquantes
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    f.write(f"\n  Valeurs manquantes:\n")
                    for col, count in missing.items():
                        if count > 0:
                            pct = (count / len(df)) * 100
                            f.write(f"    - {col}: {count} ({pct:.2f}%)\n")
                else:
                    f.write(f"  ✅ Aucune valeur manquante\n")
                
                # Doublons
                duplicates = df.duplicated().sum()
                f.write(f"\n  Doublons: {duplicates}\n")
                
                # Types de données
                f.write(f"\n  Types de données:\n")
                for col in df.columns:
                    f.write(f"    - {col}: {df[col].dtype}\n")
            
            # Statistiques descriptives
            f.write("\n\n3. STATISTIQUES DESCRIPTIVES\n")
            f.write("-" * 80 + "\n\n")
            
            for name, df in datasets.items():
                if df.empty:
                    continue
                f.write(f"\n{name.upper()}:\n")
                f.write(f"\n{df.describe(include='all').to_string()}\n")
            
            # Échantillons de données
            f.write("\n\n4. ÉCHANTILLONS DE DONNÉES (Premières 10 lignes)\n")
            f.write("-" * 80 + "\n\n")
            
            for name, df in datasets.items():
                if df.empty:
                    continue
                f.write(f"\n{name.upper()}:\n")
                f.write(f"\n{df.head(10).to_string(index=False)}\n\n")
        
        print(f"✅ Rapport complet sauvegardé: {report_file}")
    
    def run_complete_eda(self, from_excel=True):
        """Exécuter l'analyse exploratoire complète"""
        print("\n" + "="*80)
        print("🚀 DÉMARRAGE DE L'ANALYSE EXPLORATOIRE COMPLÈTE (EDA)")
        print("="*80)
        
        # Charger les données
        self.load_data(from_excel=from_excel)
        
        # Statistiques de base
        self.basic_statistics()
        
        # Rapport de qualité
        self.data_quality_report()
        
        # Visualisations
        self.visualize_distributions()
        
        # Analyse des patterns textuels
        self.analyze_text_patterns()
        
        # Graphiques d'aperçu
        self.create_data_overview_charts()
        
        # Rapport complet
        self.generate_comprehensive_report()
        
        print("\n" + "="*80)
        print("✅ ANALYSE EXPLORATOIRE TERMINÉE!")
        print("="*80)
        print(f"\n📁 Tous les résultats sont sauvegardés dans: {self.output_dir}")
        print(f"\n📊 Fichiers générés:")
        print(f"   - quality_report.csv")
        print(f"   - distributions_raw_data.png")
        print(f"   - data_overview_charts.png")
        print(f"   - eda_comprehensive_report.txt")


# Point d'entrée principal
if __name__ == "__main__":
    # Créer une instance de l'analyseur
    analyzer = CountryDataEDA()
    
    # Exécuter l'analyse complète
    # Essai avec Excel d'abord, sinon basculer vers CSV
    try:
        analyzer.run_complete_eda(from_excel=True)
    except Exception as e:
        print("\n⚠️ Erreur avec Excel, tentative avec fichiers CSV...")
        analyzer.run_complete_eda(from_excel=False)
